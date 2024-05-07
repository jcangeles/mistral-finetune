from peft import LoraConfig, get_peft_model, PeftModel, prepare_model_for_kbit_training

# util function from
# https://github.com/YiVal/YiVal/blob/22a1fa0e3ed27b8e2639a8340d6c3662e64c4e2f/src/yival/finetune/utils.py
def print_trainable_parameters(model):
    """
    Prints the number of trainable parameters in the model.
    """
    trainable_params = 0
    all_param = 0
    for _, param in model.named_parameters():
        all_param += param.numel()
        if param.requires_grad:
            trainable_params += param.numel()
    print(
        f"trainable params: {trainable_params} || all params: {all_param} || trainable%: {100 * trainable_params / all_param}"
    )


def lora_model(model, r=8):
    model = prepare_model_for_kbit_training(model)
    config = LoraConfig(
    r=r,
    lora_alpha=64,
    target_modules=[
        "q_proj",
        "k_proj",
        "v_proj",
        "o_proj",
        "gate_proj",
        "up_proj",
        "down_proj",
        "lm_head",
    ],
    bias="none",
    lora_dropout=0.05,  # Conventional
    task_type="CAUSAL_LM",
    )

    model = get_peft_model(model, config)
    return model