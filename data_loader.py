from datasets import load_dataset

def load_data():
    ds = load_dataset('json', data_files='data/parsed_diary.json', split="train")
    ds = ds.train_test_split(test_size=0.2, shuffle=True)
    train_dataset = ds['train']
    eval_dataset = ds['test']

    return train_dataset, eval_dataset

