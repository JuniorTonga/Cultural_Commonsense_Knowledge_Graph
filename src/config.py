import os 

key='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'
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', key)
# Get a free API key from https://console.groq.com/keys
groq_key="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"
GROQ_API_KEY=os.getenv('GROQ_API_KEY',groq_key)

#locations=['Indonesia', 'UK','Japan','Egypt','Germany']
#locations=['Indonesia']
locations=['China']
sub_topics=['breakfast', 'lunch', 'dinner', 'traditional foods and beverages', 'cutlery','cooking ware', 'fruit', 'food souvenirs', 'snacks',
                'wedding location', 'wedding food', 'wedding dowry', 'traditions before marriage', 'traditions when getting married', 'traditions after marriage', 
                'men’s wedding clothes', 'women’s wedding clothes', 'songs and activities during the wedding', 'invited guests at a wedding', 'gift brought to weddings', 'food at a wedding',
                 'eating habit', 'greetings habits', 'financial habits (saving, debit/credit)', 'punctuality habits', 'cleanliness habits', 'shower time habits', 'transportation habits', 
                 'popular sports','musical instruments', 'folks songs', 'traditional dances', 'use of art at certain events', 'poetry or similar literature',
                 'morning activities', 'afternoon activities', 'evening activities', 'Leisure and relaxation activities', 'Household activities (cleaning, home management)',
                  'relationships within the main family', 'relationships in the extended family', 'relations with society/neighbors', 'clan/descendant system',
                  'traditions during pregnancy', 'traditions after birth', 'how to care for a newborn baby', 'how to care for toddlers', 'how to care for teenagers', 'parents and children interactions as adults',
                 'when death occurs', 'the process of dealing with a corpse', 'traditions after the body is buried', 'the clothes of the mourners','inheritance matters',
                  'traditions before religious holidays', 'traditions leading up to religious holidays', 'traditions during religious holidays', 'traditions after holidays',
                  'Game types','regular religious activities', 'mystical things', 'traditional ceremonies', 'lifestyle', 'self care', 'traditional medicine', 'traditional sayings']