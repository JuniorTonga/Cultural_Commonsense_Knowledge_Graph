#!/bin/bash

#SBATCH --job-name=CCKG # Job name
#SBATCH --error=logs/%j%x.err # error file
#SBATCH --output=logs/%j%x.out # output log file
#SBATCH --nodes=1                   # Run all processes on a single node    
#SBATCH --ntasks=1                  # Run on a single CPU
#SBATCH --mem=196G                   # Total RAM to be used
#SBATCH --cpus-per-task=8          # Number of CPU cores
#SBATCH --gres=gpu:4                # Number of GPUs (per node)
#SBATCH -p cscc-gpu-p
#SBATCH -q cscc-gpu-qos                   
#SBATCH --time=12:00:00             # Specify the time needed for your experiment

echo "starting test......................."

# Uncomment the following line and change to your HuggingFace Token to get access to models otherwise it will use my token
#export HF_TOKEN="..."

# please change this path to the path where the project is store
PROJECT_ROOT="/home/junior.tonga/Cultural_Commonsense_Knowledge_Graph"


if [ ! -d "$PROJECT_ROOT/results" ]; then
    echo "Results folder not found. Creating it..."
    mkdir -p "$PROJECT_ROOT/results"
fi


if [ ! -d "results" ]; then
    echo "Results folder not found. Creating it..."
    mkdir -p results
fi


python "$PROJECT_ROOT/src/main.py" \
    --record_file_name "$PROJECT_ROOT/results/multilingual_generation" \
    --model meta-llama/Llama-3.1-8B-Instruct \
    --action initial_generation \
    --mode multilingual_setting \
    --number_location 1
