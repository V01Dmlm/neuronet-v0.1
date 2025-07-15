import json
import torch
from torch.utils.data import Dataset, DataLoader
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import get_peft_model, LoraConfig, TaskType
from tqdm import tqdm

# ========== CONFIG ==========
DATA_PATH = "neuronet_data.jsonl"
MODEL_NAME = "EleutherAI/gpt-neo-125M"
EPOCHS = 1
BATCH_SIZE = 2
MAX_LENGTH = 512
LEARNING_RATE = 3e-5
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# ========== DATA ==========
class JSONLDataset(Dataset):
    def __init__(self, data_path, tokenizer, max_length=512):
        self.samples = []
        with open(data_path, "r", encoding="utf-8") as f:
            for line in f:
                obj = json.loads(line)
                prompt = obj.get("prompt", "")
                completion = obj.get("completion", "")
                full_text = prompt + completion
                tokenized = tokenizer(
                    full_text,
                    truncation=True,
                    padding="max_length",
                    max_length=max_length,
                    return_tensors="pt"
                )
                input_ids = tokenized["input_ids"].squeeze(0)
                attention_mask = tokenized["attention_mask"].squeeze(0)
                self.samples.append((input_ids, attention_mask))

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        return self.samples[idx]

# ========== MAIN ==========
def main():
    print("📦 Loading tokenizer and model...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)

    print("🔧 Applying LoRA config...")
    lora_config = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        inference_mode=False,
        r=8,
        lora_alpha=32,
        lora_dropout=0.05,
    )
    model = get_peft_model(model, lora_config)
    model.to(DEVICE)
    model.train()

    print("🧠 Preparing dataset...")
    dataset = JSONLDataset(DATA_PATH, tokenizer, MAX_LENGTH)
    dataloader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)

    optimizer = torch.optim.AdamW(model.parameters(), lr=LEARNING_RATE)

    print(f"🚀 Starting training for {EPOCHS} epochs...")
    for epoch in range(EPOCHS):
        total_loss = 0.0
        loop = tqdm(dataloader, desc=f"Epoch {epoch+1}")
        for step, (input_ids, attention_mask) in enumerate(loop):
            input_ids = input_ids.to(DEVICE)
            attention_mask = attention_mask.to(DEVICE)

            outputs = model(
                input_ids=input_ids,
                attention_mask=attention_mask,
                labels=input_ids
            )
            loss = outputs.loss
            loss.backward()

            optimizer.step()
            optimizer.zero_grad()

            total_loss += loss.item()
            loop.set_postfix(loss=loss.item())

        avg_loss = total_loss / len(dataloader)
        print(f"✅ Epoch {epoch+1} completed. Average loss: {avg_loss:.4f}")

    print("💾 Saving fine-tuned model...")
    model.save_pretrained("./gptneo_lora_finetuned")
    tokenizer.save_pretrained("./gptneo_lora_finetuned")
    print("🎉 Training complete and model saved!")

if __name__ == "__main__":
    torch.manual_seed(42)
    main()
