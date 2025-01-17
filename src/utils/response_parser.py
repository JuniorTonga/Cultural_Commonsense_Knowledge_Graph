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


def parse_llm_response(args, response_text):
    commonsense_data = []
    intermediaire_events = []
    next_events = []

    try:
        clean_response_text = clean_output(response_text)
        commonsenses = json.loads(clean_response_text)
    except json.JSONDecodeError:
        return commonsense_data

    if args.action == 'initial_generation':
        for commonsense in commonsenses:
            if isinstance(commonsense, dict):
                event = commonsense.get("action", "")
                knowledge = commonsense.get("knowledge", "")
                relation_type = commonsense.get("relation_type", "")
                if_then_event = commonsense.get("result", "")

                if not all([event, knowledge, relation_type, if_then_event]):
                    continue

                commonsense_data.append({
                    "event": event.strip(),
                    "knowledge": knowledge.strip(),
                    "relation": relation_type.strip(),
                    "llm_result": if_then_event.strip()
                })
        return commonsense_data

    elif args.action == 'relation_extension':
        for key in commonsenses[0].keys():
            items_list = commonsenses[0].get(key, [])
            if not isinstance(items_list, list):
                continue
            for items in items_list:
                event = items.get("action", "")
                knowledge = items.get("knowledge", "")
                relation_type = items.get("relation_type", "")
                if_then_event = items.get("event", "")

                if not all([event, knowledge, relation_type, if_then_event]):
                    continue

                if key == 'intermediate_steps':
                    intermediaire_events.append({
                        "event": event.strip(),
                        "knowledge": knowledge.strip(),
                        "relation": relation_type.strip(),
                        "llm_result": if_then_event.strip()
                    })
                elif key == 'next_steps':
                    next_events.append({
                        "event": event.strip(),
                        "knowledge": knowledge.strip(),
                        "relation": relation_type.strip(),
                        "llm_result": if_then_event.strip()
                    })
        return intermediaire_events, next_events



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


