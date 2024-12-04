# CCKG : Cultural Commonsense Knowledge Graph

Built a Cultural Commonsense Knowledge Graph( CCKG) that have geographical context.

### 1. Generating Initial Commonsense Data (Cultural Commonsense)

To run generation of initial commonsense data(cultural commonsense) data with GPT-4o :
```bash
python main.py --record_file_name <file_name> \
               --number_location <number_of_locations> \
               --generate_initial_ckg \
               --prompt_template generate_english_ckg \
               --number_subtopic <number_of_subtopics>
```
###  2. Extending oNext/xNext Relations

To extend the commonsense relationships (oNext/xNext), use the following command:
```bash
python main.py --record_file_name <file_name> \
               --initial_data_path <your_initial_commonsense_data_path> \
               --prompt_template extend_xNext_relation \
               --number_location <number_of_locations> \
               --number_extension <number_of_extensions>
```

Notes:
- --record_file_name: Specify the name of the file where the extended data will be saved.
- --initial_data_path: Provide the path to the initial commonsense data file.
- --number_location: (Optional) Specify the number of locations to process.
- --number_extension: Specify the number of iterations for extending the relations.
- ----number_subtopic: (Optional) Specify the number of subtopics to process. If omitted, the script will process all subtopics.
- --generate_initial_ckg: Action: store_true, description: Triggers the generation of initial cultural commonsense data.
