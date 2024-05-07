from transformers import AutoTokenizer

def format_prompt(entry):   
    return f"This is a diary entry by Anne Frank dated {entry['Date']}: {''.join(entry['Lines'])}"

def get_tokenizer():
    base_model_id = "mistralai/Mistral-7B-v0.1"
    tokenizer = AutoTokenizer.from_pretrained(
        base_model_id,
        padding_side="left",
        add_eos_token=True,
        add_bos_token=True,
    )
    tokenizer.pad_token = tokenizer.eos_token
    return tokenizer

def tokenize_prompt(prompt):
    tokenizer = get_tokenizer()
    result = tokenizer(format_prompt(prompt), truncation=True, max_length=1024, padding="max_length")
    result["labels"] = result["input_ids"].copy()
    return result