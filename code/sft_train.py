from trl import SFTTrainer, SFTConfig
from datasets import load_dataset
from transformers import AutoModelForCausalLM

trainer = SFTTrainer(
    model=AutoModelForCausalLM.from_pretrained("Qwen/Qwen3-0.6B", device_map='auto'),
    train_dataset=load_dataset("trl-lib/Capybara", split="train"),
)
trainer.train()