# LLMs as Cultural Archives: Cultural Commonsense Knowledge Graph Extraction

[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

Official implementation of **"LLMs as Cultural Archives: Cultural Commonsense Knowledge Graph Extraction"**.

**Authors:** Junior Cedric Tonga, Chen Cecilia Liu, Iryna Gurevych, Fajri Koto

**Affiliations:** Mohamed bin Zayed University of Artificial Intelligence, Ubiquitous Knowledge Processing Lab (Technical University of Darmstadt)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Repository Structure](#repository-structure)
- [Installation](#installation)
- [Usage](#usage)
  - [1. Initial Generation](#1-initial-generation)
  - [2. Iterative Expansion](#2-relation-extension)
  - [3. Path Building](#3-path-building)
- [Quick Start Examples](#quick-start-examples)
- [Data Availability](#data-availability)
- [Citation](#citation)
- [License](#license)
- [Contact](#contact)

---

## 🔍 Overview

This repository contains the implementation of **LLMs as Cultural Archives: Cultural Commonsense Knowledge Graph Extraction**, a framework for extracting structured, culturally-grounded commonsense knowledge from Large Language Models. Our approach treats LLMs as cultural archives and systematically elicits culture-specific entities, relations, and practices to construct multi-step inferential chains.

### Key Contributions

- **Iterative Prompt-Based Framework**: Constructs multilingual cultural commonsense knowledge graphs with if-then inferential chains
- **Cross-Cultural Coverage**: Supports 5 countries (China, Indonesia, Japan, England, Egypt) in both English and native languages
- **Extensive Human Evaluation**: Assessed on cultural relevance, correctness, and logical path coherence
- **Downstream Applications**: Improves cultural reasoning and story generation tasks

### Example

<p align="center">
  <img src="Figure/Cultural_Assertions_Paths-Graph.drawio_big.jpg" alt="Cultural Commonsense Knowledge Graph Example" width="600"/>
</p>

*Figure 1: Example English if-then assertions from the Cultural Commonsense Knowledge Graph (CCKG) illustrating culturally grounded reasoning about breakfast in Indonesia.*

---

## ✨ Key Features

- 🌍 **Multi-country support**: China, Indonesia, Japan, England, Egypt
- 🗣️ **Multilingual**: English, Chinese, Indonesian, Japanese, Arabic
- 🔗 **5 Relation Types**: xNext, xEffect, xNeed, oNext, oEffect
- 📊 **37K+ English assertions**, 16K+ native-language assertions
- 🎯 **Proven improvements** on IndoCulture, ArabCulture benchmarks and Story generation.

---

## 📁 Repository Structure
```
Cultural_Commonsense_Knowledge_Graph/
├── Notebooks/
│   └── ProcessData_BuildPaths.ipynb    # Post-processing and path building
├── src/
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── llm_query.py               # LLM API interface
│   │   ├── prompt_templates.py        # Prompt templates
│   │   └── response_parser.py         # Response parsing utilities
│   ├── config.py                      # Configuration settings
│   └── main.py                        # Main execution script
├── Figure/                              # Figure displays
├── .gitignore
├── README.md
├── requirements.txt
└── LICENSE
```

---

## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/your-username/Cultural_Commonsense_Knowledge_Graph.git
cd Cultural_Commonsense_Knowledge_Graph
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure GPT-4o API key and HF TOKEN**

```bash
Paste them in the config.py file
```
---

## 📖 Usage

### 1. Initial Generation

Generate initial cultural commonsense assertions for your target countries and topics.

#### Monolingual Setting (English prompts for all locations)
```bash
python src/main.py \
    --record_file_name <output_file_name> \
    --action initial_generation \
    --model gpt-4o \
    --mode monolingual_setting \
    --number_location 5  # Optional: process specific number of locations
```

#### Multilingual Setting (Native language prompts)
```bash
python src/main.py \
    --record_file_name <output_file_name> \
    --action initial_generation \
    --model gpt-4o \
    --mode multilingual_setting \
    --number_location 5  # Optional: process specific number of locations
```

**Using Llama Models:**

Replace `--model gpt-4o` with:
```bash
--model meta-llama/Llama-3.3-70B-Instruct
```

---

### 2. Iterative Expansion

Iteratively expand oNext/xNext relations to build multi-step knowledge chains.

#### Monolingual Setting
```bash
python src/main.py \
    --record_file_name <output_file_name> \
    --initial_data_path <path_to_initial_data.xlsx> \
    --number_extension 3 \
    --model gpt-4o \
    --mode monolingual_setting \
    --action relation_extension 
```

#### Multilingual Setting
```bash
python src/main.py \
    --record_file_name <output_file_name> \
    --initial_data_path <path_to_initial_data.xlsx> \
    --number_extension 3 \
    --model gpt-4o \
    --mode multilingual_setting \
    --action relation_extension
```

#### Command-Line Arguments

| Argument | Description | Required | Default |
|----------|-------------|----------|---------|
| `--record_file_name` | Output file name for generated data | Yes | - |
| `--initial_data_path` | Path to initial assertions file | Yes (for extension) | - |
| `--number_extension` | Number of extension iterations | Yes (for extension) | - |
| `--model` | LLM model to use | No | `gpt-4o` |
| `--mode` | Language setting | No | `monolingual_setting` |
| `--action` | Action to perform | Yes | `initial_generation` |
| `--number_location` | Number of locations to process | No | All |
| `--number_subtopic` | Number of subtopics to process | No | All |
| `--sub_sample` | Run on data subsample | No | False |

---

### 3. Path Building

After generating and extending assertions, use the provided notebook to:

1. Remove duplicates
2. Filter malformed assertions
3. Construct inferential paths
4. Generate final CCKG statistics
```bash
jupyter notebook Notebooks/ProcessData_BuildPaths.ipynb
```

Follow the notebook instructions to complete the post-processing pipeline.

---

## 🚀 Quick Start Demo

### Example : Generating CCKG for Chinese Culture (in English)
```bash
# Step 1: Generate initial assertions for China
python src/main.py \
    --record_file_name china_initial \
    --action initial_generation \
    --model gpt-4o \
    --mode monolingual_setting
    ----number_location 1  # assuming that locations list in config.py have just China as location

# Step 2: Extend relations (3 iterations)
python src/main.py \
    --record_file_name china_extended \
    --initial_data_path data/china_initial.json \
    --number_extension 3 \
    --model gpt-4o \
    --mode monolingual_setting \
    --action relation_extension

# Step 3: Build paths using the notebook
jupyter notebook Notebooks/ProcessData_BuildPaths.ipynb
```
---

## 💾 Data Availability

The complete generated Cultural Commonsense Knowledge Graphs (CCKG) including:
- 37,363 English assertions across 5 countries
- 16,709 native-language assertions
- 27,649 English knowledge paths
- 6,571 native-language knowledge paths

**Access**: Due to the size and nature of the generated data, the complete CCKG datasets are available upon request. Please contact the authors (see [Contact](#contact) section) to obtain access to the data.

---

## 📄 Citation

If you use this code or data in your research, please cite our paper:
```
Available soon
```

---

## 📝 License

This project is licensed under the MIT License.

---

## 🤝 Contact

For questions, data requests, or collaborations, please contact:

- **Junior Cedric Tonga**: junior.tonga@mbzuai.ac.ae
- **Chen Cecilia Liu**: chen.liu@tu-darmstadt.de
- **Fajri Koto**: fajri.koto@mbzuai.ac.ae

---

## 🙏 Acknowledgments

This work was conducted at:
- Mohamed bin Zayed University of Artificial Intelligence
- Ubiquitous Knowledge Processing Lab, Technical University of Darmstadt

We thank all the human annotators who participated in the evaluation of our cultural knowledge graphs.

---
