import json

def clean_output(response_text):
    start_index=response_text.find('[')
    if start_index !=-1:
        end_index=response_text.find(']',start_index)+1
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


def parse_gpt_llm_response(response_text):
    commonsense_data=[]    
    try:
        clean_response_text=clean_output(response_text)
        commonsenses=json.loads(clean_response_text)
    except json.JSONDecodeError:
        return commonsense_data
    
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
    return commonsense_data


