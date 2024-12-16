import json
import argparse
import pandas as pd 

def clean_output(response_text):
    start_index=response_text.find('[')
    if start_index !=-1:
        end_index=response_text.rfind(']',start_index)+1
        if end_index != -1:
            clean_json_string = response_text[start_index:end_index]
            try:
                return clean_json_string
            except json.JSONDecodeError as e:
                print(f"Invalid JSON format: {e}")
                return None
        else:
            print("No closing bracket found for JSON.")
            return None
    else:
        print("No valid JSON found.")
        return None


def parse_llm_response(args,response_text):
    commonsense_data=[]    
    try:
        clean_response_text=clean_output(response_text)
        commonsenses=json.loads(clean_response_text)
    except json.JSONDecodeError:
        return commonsense_data
    
    if args.prompt_template =="generate_english_ckg":
        for commonsense in commonsenses:
            if isinstance(commonsense,dict):
                event = commonsense.get("action", "").strip()
                knowledge = commonsense.get("knowledge", "").strip()
                relation_type = commonsense.get("relation_type", "").strip()
                if_then_event = commonsense.get("result", "").strip()

                commonsense_data.append({
                    "event":event,
                    "knowledge":knowledge,
                    "relation":relation_type,
                    "llm_result":if_then_event
            })
    elif args.prompt_template =='extend_xNext_relation':
        for key in commonsenses[0].keys(): 
            items_list = commonsenses[0].get(key, [])
            if not isinstance(items_list, list): 
                continue
            for items in items_list:
                event = items.get("action", "").strip()
                knowledge = items.get("knowledge", "").strip()
                relation_type = items.get("relation_type", "").strip()
                if_then_event = items.get("event", "").strip()

                commonsense_data.append({
                    "event":event,
                    "knowledge":knowledge,
                    "relation":relation_type,
                    "llm_result":if_then_event
            })

    return commonsense_data


def sample_subtopics(dataframe, total_samples, subtopic_column='sub_topic', random_state=42):
    """
    Samples rows from a DataFrame based on subtopics, ensuring a minimum per subtopic 
    and filling up to the desired total number of samples.

    Args:
    - dataframe (pd.DataFrame): The input DataFrame.
    - total_samples (int): Desired total number of samples.
    - subtopic_column (str): Column indicating subtopics.
    - random_state (int, optional): Seed for reproducibility. Default is 42.

    Returns:
    - pd.DataFrame: The sampled DataFrame.
    """
    min_per_subtopic = max(1, total_samples // dataframe[subtopic_column].nunique())
    grouped = dataframe.groupby(subtopic_column, group_keys=False)
    samples = grouped.apply(lambda x: x.sample(n=min(len(x), min_per_subtopic), random_state=random_state))
    remaining = total_samples - len(samples)
    if remaining > 0:
        additional_samples = dataframe.drop(samples.index).sample(n=remaining, random_state=random_state)
        samples = pd.concat([samples, additional_samples])
    return samples

#samples=sample_subtopics(x_next_df.head(55),20)


