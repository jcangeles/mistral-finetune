
# Personalized Writing Style Adaptation using QLoRA Fine-tuning on Mistral 7B

Application of QLoRA (Quantization and Low-Rank Adaptation) tech- niques on local large language models, more specifically Mistral-7B. Leveraging the revolutionary advancements of fine-tuning, the goal is to democratize the use of local LLMs by fine-tuning massive models and personalizing them by understanding users through their journal entries. By fine-tuning the Mistral, we adapt it to individual writing style, patterns and word choices.

## Installing
```
$ git clone https://github.com/jcangeles/mistral-finetune
```
And copy its contents to your Google Colab instance or local Jupyter Notebook.

## Requirements
Requirements are listed on the first cell of the main jupyter notebook. Additionally, you need to set your Hugging Face API token as a global variable HF_TOKEN, and you need a Weights & Biases API token if you want to evaluate its metric. Lastly, if dragged and dropped, folders aren't always created, make sure to have a "data" folder.

## Table of contents

* main.ipynb: main entrypoint
    * contains cells to pip install required libraries on Google Colab. Additional libraries might be required if done locally.
    * downloads diary text into data folder
    * calls other python files to parse text, load and tokenize dataset, load and train model, and apply optimizations.

* data_parser.py
    * fixes spelling, splits text into lines by date, and outputs a structured json file.

* data_loader.py
    * loads data, concatenates diary lines into paragraphs, splits dataset into training and evaluation, converts to Dataset structure.

* lora.py
    * prints trainable parameters and loads configufation to apply LoRA optimization. Inputs are model and the rank size (default 8)

* model_trainer.py
    * Fine-tunes Mistral model.
    * Inputs: model, train_dataset, validation_dataset, tokenizer
    * Reports to WandB
    * Outputs trainer
* model.py
    * loads and outputs 4-bit quantized model of Mistral 7B v0.1
    * Uses BitsAndBytesConfig
* tokenizer.py
    * formats diary entry to prompt for training "This is a diary entry from ..."
    * Tokenizes prompt, padding, adds eos and bos tokens, applies truncation


## Usage
Once cloned and loaded onto Google Colab, you can run every cell to
* install Requirements
* download diary
* parse and load text
* dowload the base mistral model (quantized)
* tokenize the train and val datasets
* Test the performance of the base model
* Apply LoRA to Mistral
* Fine-tune QLoRA Mistral
* Test the performance of optimized model