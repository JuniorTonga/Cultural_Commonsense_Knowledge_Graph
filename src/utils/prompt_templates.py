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

#xNext_extended_prompt={"extend_xNext_relation":[
 #           {
  #              "role": "system",
   #             "content": "You are a cultural commonsense knowledge extraction assistant."
    #        },
     #       {
      #          "role": "user",
       #         "content": '''Generate all possible  knowledge of  if-then cultural commonsense knowledge statements  for {location} related to {sub_topic} given an action {action}. Each statement should follow this structure: "If [action], then [knowledge]." The knowledge should describe what action is likely to follow or precede the initial action, reflecting cultural habits and practices associated with {sub_topic} in {location}. 
        #    Let's think step by step to generate the chain of action between the action and the knowledge. The knowledge must be classified into one of the following relation types: 
         #               - xNext: What would x likely want to do after the action? 
          #              - oNext: What would others likely want to do after the action? 
         #   In the relation types above, 'x' represents the agent or primary person performing the action, while 'o' refers to others who interact with or are affected by the action of 'x'. 
        #    Format your response strictly as a JSON array of objects, following this precise format without any additional text or explanation:

       # [
        #    {{
         #       "action": {action},
          #      "knowledge": "knowledge",
           #     "relation_type": "relation type",
            #    "result": "Complete sentence in {language}, using If and Then"
          #  }},
           # ...
       # ]

      #  Ensure that the "action," "knowledge," and "result" are generated in {language}, while the "relation_type" should be one of the specified options above.'''
       #     }
#]}


xNext_extended_prompt={"extend_xNext_relation": [{ "role": "system", "content": "You are a cultural commonsense knowledge extraction assistant."
}, { "role": "user", 
    "content":''' 
    You are tasked with generating as many as possible culturally sensitive commonsense knowledge events for {location} related to {sub_topic} based on an initial event which consists of an action and a knowledge. 
Each event should follow this structure: "If [action], then [knowledge]". Each event must reflect cultural habits, practices, traditions, and customs associated with {sub_topic} in {location}.

Initial event: {initial_event}

initial action: {init_action}

initial knowledge: {init_knwoledge}

Instructions:
    1. Next steps generation
        - Start from the entire initial event 
        - use the initial knowledge as the starting point to generate all new knowledges
        - Ensure that each new knowledge logically follows from the initial event as a whole, considering both the initial action and initial knowledge. 
        Each new knowledge must logically align with the initial action and initial knowledge, showing their natural progression. Specifically, focus on the relationship types listed below.
        - Format the new knowledge as conditional statements, starting with: “if {init_knwoledge}, then…”
        -  Each new knowledge must be classified into one of these relation types: 
              - xNext: What would x likely want to do after the action? 
              - oNext: What would others likely want to do after the action? 
            In the relation types above, 'x' represents the agent or primary person performing the action, while 'o' refers to others who interact with or are affected by the action of 'x'. 
    2. Intermediate steps generation
        - Start from the initial action from the initial event.
        - Create a chain of new knowledge leading to the initial knowledge.
        - Use a stepwise approach:
            - Start with: if {init_action}, then X
            - then: “if X, then Y”
            - generate new knowledge (X,Y, etc.) that logically and culturally connects to the previous step. Continue iterating until you arrive at the final step, where the generated knowledge aligns with the initial knowledge.
            - Please respect the stepwise approach
        - Each step must be classified into one of the relation types listed above.
        - The chain should logically explain how someone would arrive at the initial knowledge in a culturally sensitive way.
    3. Cultural relevance 
        Ensure all steps (new knowledge) are deeply rooted in and reflective of the culture in {location}, while being closely associated with the sub-topic {sub_topic} in {location}.
    4. Output format and output language
        Entire event sentence, action, knowlege in both next steps and intermediate steps must be written in {language} language.
        Your response must be formatted strictly as a JSON array of objects without any additional text or explanation and organized into two categories: next steps  and intermediate steps: 

        [{{"intermediate_steps": [
        {{
            "action": " action",
            "knowledge": "knowledge",
            "relation_type": "relation",
            "event": "If action, then knowledge"
        }}
    ],
    "next_steps": [
        {{
            "action": " action",
            "knowledge": "knowledge",
            "relation_type": "relation",
            "event": "If action, then knowledge"
        }}
    ]
}}]
'''
}]


                       
                       
                       
                       
                       
                       
                    
                       
                       
                       
                       
                       
                       
                       
                       
                       
                       
                       
                       
                       
                       
                       
                       
                       
                       
                       
                       
                       
                       
                       
                       }