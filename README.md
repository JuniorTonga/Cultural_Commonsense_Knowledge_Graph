# CCKG : Cultural Commonsense Knowledge Graph

Built a Cultural Commonsense Knowledge Graph( CCKG) that have geographical context.

### 1. Generating Initial Commonsense Data (Cultural Commonsense)

To run generation of initial commonsense data(cultural commonsense) data with GPT-4o :
 1. Monolingual setting (language of the prompt=english)
```bash
python main.py --record_file_name <file_name> \
               --action initial_generation \
               --model gpt-4o \
               --mode monolingual_setting
```
 2. Multilingual setting (language of the prompt=language of the location)
 ```bash
python main.py --record_file_name <file_name> \
               --action initial_generation \
               --model gpt-4o \
               --mode multilingual_setting
```

###  2. Extending oNext/xNext Relations

To extend the commonsense relationships (oNext/xNext) with GPT-4o, use the following command :
1. Monolingual setting (language of the prompt=english)
```bash
python main.py --record_file_name <file_name> \
               --initial_data_path <your_initial_commonsense_data_path> \
               --number_extension <number_of_extensions> \
               --model gpt-4o \
               --mode monolingual_setting \
               --action relation_extension
```
2. Multilingual setting (language of the prompt=language of the location)
```bash
python main.py --record_file_name <file_name> \
               --initial_data_path <your_initial_commonsense_data_path> \
               --number_extension <number_of_extensions> \
               --model gpt-4o \
               --mode mutilingual_setting \
               --action relation_extension
```

To generate with Llama 3.x model, just change --mode to  --model meta-llama/Llama-3.3-70B-Instruct 

Notes:
- --record_file_name: specify the name of the file where the extended data will be saved.
- --initial_data_path: provide the path to the initial commonsense data file.
- --number_location:  specify the number of locations to process. If omitted, the script will process all location. 
- --number_extension: specify the number of iterations for extending the relations.
- --number_subtopic: (optional) Specify the number of subtopics to process. If omitted, the script will process all subtopics.
- --action: choose action to perform between intiatial extraction or relation extensions. Choices=['initial_generation', 'relation_extension']
- --sub_sample: action: store_true, run a sub sample of data in the extension phase
- --mode : run monolingual(english for all location) or multilingual(each location with his local language). choices=['monolingual_setting', 'multilingual_setting']
