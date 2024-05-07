import transformers
from datetime import datetime

def train_model(model, train_dataset, val_dataset, tokenizer):
    trainer = transformers.Trainer(
        model=model,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        args=transformers.TrainingArguments(
            output_dir="./mistral-hpml-finetune",
            warmup_steps=1,
            per_device_train_batch_size=2,
            gradient_accumulation_steps=1,
            gradient_checkpointing=True,
            max_steps=500,
            learning_rate=2.5e-5,
            bf16=True,
            optim="paged_adamw_8bit",
            logging_steps=25,
            logging_dir="./logs",
            save_strategy="steps",
            save_steps=25,
            evaluation_strategy="steps",
            eval_steps=25,
            do_eval=True,
            report_to="wandb",
            run_name=f"mistral-hpml-finetune-{datetime.now().strftime('%Y-%m-%d-%H-%M')}"
        ),
        data_collator=transformers.DataCollatorForLanguageModeling(tokenizer, mlm=False),
    )

    model.config.use_cache = False  # silence the warnings. Please re-enable for inference!
    return trainer