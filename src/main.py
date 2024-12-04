from utils.llm_query import *
from utils.response_parser import *
import pandas as pd
import numpy as np
import os 
from openpyxl import load_workbook
from config import locations, sub_topics
from utils.prompt_templates import ckg_english_prompt, xNext_extended_prompt
import argparse
from sentence_transformers import SentenceTransformer





def prepare_prompt(prompt_type, **kwargs):
    if prompt_type in xNext_extended_prompt:
        template=xNext_extended_prompt[prompt_type]
    elif prompt_type in ckg_english_prompt:
        template=ckg_english_prompt[prompt_type]
    else:
        raise ValueError("Invalid prompt type")
    formatted_prompts = [
        { "role": message["role"], "content": message["content"].format(**kwargs) }
        for message in template ]
    return formatted_prompts


def generate_cultural_commonsense(args,location, sub_topic,action=None):
    if args.prompt_template =="generate_english_ckg":
        prompt=prepare_prompt('generate_english_ckg',location=location,sub_topic=sub_topic,language='english')
    elif args.prompt_template =='extend_xNext_relation':
        prompt=prepare_prompt('extend_xNext_relation',location=location,sub_topic=sub_topic,action=action,language='english')
    else:
        raise ValueError(f"Unknown prompt template: {args.prompt_template}")
    response_text=query_llm(prompt)
    structure_data=parse_gpt_llm_response(response_text)

    for entry in structure_data:
        entry['location']=location
        entry['sub_topic']=sub_topic

    return structure_data

def save_to_excel(data_sheets, file_name,extend=False):
    columns = ['event', 'knowledge', 'relation', 'llm_result', 'location', 'sub_topic']
    if os.path.exists(file_name):
        existing_workbook=load_workbook(file_name)

        if extend==True:
            if_sheet_exist='replace'
        else:
            if_sheet_exist='overlay'
        with pd.ExcelWriter(file_name,engine='openpyxl',mode='a',if_sheet_exists=if_sheet_exist) as writer:
            writer._book=existing_workbook
            writer._sheets ={ws.title:ws for ws in existing_workbook.worksheets}
        
            for sheet_name,data in data_sheets.items():
                if sheet_name in writer._sheets:
                    print(f"udpating sheet:{sheet_name}")
                else:
                    print(f"adding new sheet : {sheet_name}")
                df=pd.DataFrame(data,columns=columns)
                df.to_excel(writer,sheet_name=sheet_name,index=False)
    else:
        with pd.ExcelWriter(file_name,engine='openpyxl') as writer:
            for sheet_name, data in data_sheets.items():
                df=pd.DataFrame(data,columns=columns)
                df.to_excel(writer,sheet_name=sheet_name,index=False)

def process_first_expand_iteration(data,args):
    all_row_new_knowledges=[]
    for row in data:
        relation=row[2]
        loc=row[4]
        subTopic=row[5]
        # First extension : we extend just relation xNext and oNext
        if relation=='xNext' or relation=='oNext':
            action=row[1]
            commonsenses=generate_cultural_commonsense(args,location=loc,sub_topic=subTopic,action=action)
            if commonsenses: 
                filtered_commonsense = [item for item in commonsenses if all(key in item and item[key] 
                                                                                     for key in ['event', 'knowledge', 
                                                                                                 'relation', 'llm_result',
                                                                                                   'location', 'sub_topic'])]
                if filtered_commonsense:
                    row_new_knowledges=np.array([[item['event'],item['knowledge'],item['relation'],item['llm_result'],
                                                    item['location'],item['sub_topic']]for item in filtered_commonsense])
                    all_row_new_knowledges.append(row_new_knowledges)
                else:
                    print("Filtered commonsense data has missing or empty values, skipping this entry.")
            else:
                print("Commonsenses is empty, skipping this entry.")
    return all_row_new_knowledges
    
def expand_knowledge(list_of_knowledge_to_expand,args):
    all_row_new_knowledges=[]
    for kg_set in list_of_knowledge_to_expand:
        for row in kg_set:
            action=row[1]
            loc=row[4]
            subTopic=row[5]
            print('-----++++++++-sub-topic: {}-++++++++++---'.format(subTopic))
            print('-----action: {}----'.format(action))
            commonsenses=generate_cultural_commonsense(args,location=loc,sub_topic=subTopic,action=action)
            if commonsenses: 
                filtered_commonsense = [item for item in commonsenses if all(key in item and item[key] 
                                                                                     for key in ['event', 'knowledge', 'relation', 'llm_result', 'location', 'sub_topic'])]
                if filtered_commonsense:
                    row_new_knowledges=np.array([[item['event'],item['knowledge'],item['relation'],item['llm_result'],
                                                    item['location'],item['sub_topic']]for item in filtered_commonsense])
                    all_row_new_knowledges.append(row_new_knowledges)
                else:
                    print("Filtered commonsense data has missing or empty values, skipping this entry.")
            else:
                print("Commonsenses is empty, skipping this entry.")
    return all_row_new_knowledges


def extend_relation(model,initial_commonsense_data,args):
    data=initial_commonsense_data.values
    iter_all_new_knowledges=[]
    steps=args.number_extension
    data_sheets={}
    threshold=0.8
    for iter in range(steps):
         # First extension : we extend just relation xNext and oNext
        if iter==0:
            iter_all_new_knowledges=process_first_expand_iteration(data,args)
        else:
            # Filtering to see if the new knowledge is already present or not in the previous iteration and select new knowleges to expand
            pairs_to_add=[]
            list_of_knowledge_to_expand=[]
            events=data[:, 0]
            knowledges=data[:, 1]
            union_unique_values = np.unique(np.concatenate((events, knowledges)))
            union_unique_values_embed=model.encode(union_unique_values)

            for row_knowledges in iter_all_new_knowledges:
                knowledge_to_expand=[]
                row_new_knowledges_embedding=model.encode(row_knowledges[:,1])
                similarities_btw_union_new_knwolge = model.similarity(row_new_knowledges_embedding, union_unique_values_embed)
                for k_idx,knowledge in enumerate(row_knowledges[:,1]):
                    matched=False
                    for e_idx, union in enumerate(union_unique_values):
                        similarity=similarities_btw_union_new_knwolge[k_idx][e_idx]
                        if similarity > threshold :
                            pairs_to_add.append([row_knowledges[k_idx,0], union_unique_values[e_idx], 
                                                  row_knowledges[k_idx,2],row_knowledges[k_idx,3],
                                                  row_knowledges[k_idx,4],row_knowledges[k_idx,5]])
                            matched=True
                            break
                    if not matched:
                        pairs_to_add.append(row_knowledges[k_idx])
                        if k_idx<=5:
                            print('{} element added'.format(k_idx))
                            knowledge_to_expand.append(row_knowledges[k_idx])

                list_of_knowledge_to_expand.append(np.array(knowledge_to_expand))
            # update data with new knowledges
            new_rows=np.array(pairs_to_add)
            data=np.vstack((data,new_rows))
            # temporary save
            location=data[0, 4]
            data_sheets[location]=data
            record_file_name= args.record_file_name +'_temp'
            save_to_excel(data_sheets,record_file_name+'.xlsx',extend=True)
            # expand the new Knowlege 
            if iter < steps-1:
                iter_all_new_knowledges=expand_knowledge(list_of_knowledge_to_expand,args)
    return data


      

def add_params():
    parser= argparse.ArgumentParser()
    parser.add_argument("--record_file_name",type=str, help='name on which you want to save your file')
    parser.add_argument("--initial_data_path",type=str,help='path of the intial commonsense data file')
    parser.add_argument('--temp', type=float, default=1, help='temperature for generation (higher=more diverse)')
    parser.add_argument("--prompt_template", type=str, choices=['generate_english_ckg', 'extend_xNext_relation'],default='generate_english_ckg', help="key (s) of the prompt template you want to run" )
    parser.add_argument("--generate_initial_ckg",action='store_true',help='extract initial cultural commonsense')
    parser.add_argument("--number_location",type=int, default=1, help="number of location to process in the extension of relation")
    parser.add_argument("--number_extension",type=int, help="number of time to extend the relation")
    parser.add_argument("--number_subtopic",type=int, default=None,help="number of topic to process")

    params=parser.parse_args()

    return params


if __name__ =='__main__':

    args=add_params()
    data_sheets={}
    # Extract the initial if then cultural commonsense knowledges
    if args.generate_initial_ckg:
        if args.number_subtopic is not None:
            sub_topics=sub_topics[:args.number_subtopic]
        for loc in locations:
            all_data = []
            for subTopic in sub_topics:
                print(subTopic)
                for _ in range(0,1):
                    commonsense=generate_cultural_commonsense(args,loc,subTopic)
                    all_data.extend(commonsense)
            data_sheets[loc]=all_data
        record_file_name= args.record_file_name
        save_to_excel(data_sheets,record_file_name+'.xlsx',extend=True)

    else:
        # Extend the xNext/oNext relations
        model=SentenceTransformer("all-MiniLM-L6-v2")
        for index in range(args.number_location):
            location=locations[index]
            print('location', location)
            initial_commonsense_data=pd.read_excel(args.initial_data_path,sheet_name=location)
            # uncomment the following line if you want to do a test with just 14 lines of the initial dataset
            #initial_commonsense_data=initial_commonsense_data.head(14)
            expanded_data=extend_relation(model,initial_commonsense_data,args)
            data_sheets[location]=expanded_data
            record_file_name= args.record_file_name
            save_to_excel(data_sheets,record_file_name+'.xlsx')
    
    print('done')

