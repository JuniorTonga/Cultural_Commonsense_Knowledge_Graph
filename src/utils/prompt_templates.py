ckg_english_prompt={"generate_english_ckg":[
            {
                "role": "system",
                "content": "You are a cultural commonsense knowledge extraction assistant."
            },
            {
                "role": "user",
                "content": '''Generate as many if-then cultural commonsense knowledge statements as possible for {location} related to {sub_topic}. Each statement should follow this structure: "If [action], then [knowledge]." The knowledge should describe what action is likely to follow or precede the initial action, reflecting cultural habits and practices associated with {sub_topic} in {location}. 

        Let's think step by step to generate the chain of action between the action and the knowledge. The knowledge must be classified into one of the following relation types: 
            - xEffect: What effects does the action have on x? 
            - xNext: What would x likely want to do after the action? 
            - xNeed: What does x need to do before the action? 
            - oNext: What would others likely want to do after the action? 
            - oEffect: What effects does the action have on others?

        In the relation types above, 'x' represents the agent or primary person performing the action, while 'o' refers to others who interact with or are affected by the action of 'x'. 

        Format your response strictly as a JSON array of objects, following this precise format without any additional text or explanation:

        [
            {{
                "action": "action",
                "knowledge": "knowledge",
                "relation_type": "relation type",
                "result": "Complete sentence in {language}, using If and Then"
            }},
            ...
        ]

        Ensure that the "action," "knowledge," and "result" are generated in {language}, while the "relation_type" should be one of the specified options above.'''
            }
        ]}

xNext_extended_prompt={"extend_xNext_relation":[
            {
                "role": "system",
                "content": "You are a cultural commonsense knowledge extraction assistant."
            },
            {
                "role": "user",
                "content": '''Generate all possible  knowledge of  if-then cultural commonsense knowledge statements  for {location} related to {sub_topic} given an action {action}. Each statement should follow this structure: "If [action], then [knowledge]." The knowledge should describe what action is likely to follow or precede the initial action, reflecting cultural habits and practices associated with {sub_topic} in {location}. 
            Let's think step by step to generate the chain of action between the action and the knowledge. The knowledge must be classified into one of the following relation types: 
                        - xNext: What would x likely want to do after the action? 
                        - oNext: What would others likely want to do after the action? 
            In the relation types above, 'x' represents the agent or primary person performing the action, while 'o' refers to others who interact with or are affected by the action of 'x'. 
            Format your response strictly as a JSON array of objects, following this precise format without any additional text or explanation:

        [
            {{
                "action": {action},
                "knowledge": "knowledge",
                "relation_type": "relation type",
                "result": "Complete sentence in {language}, using If and Then"
            }},
            ...
        ]

        Ensure that the "action," "knowledge," and "result" are generated in {language}, while the "relation_type" should be one of the specified options above.'''
            }
]}