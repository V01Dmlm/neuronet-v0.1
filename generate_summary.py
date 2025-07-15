import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

def load_model(model_dir="./gptneo_lora_finetuned"):
    base_model_name = "EleutherAI/gpt-neo-125M"
    tokenizer = AutoTokenizer.from_pretrained(model_dir)
    base_model = AutoModelForCausalLM.from_pretrained(base_model_name)
    model = PeftModel.from_pretrained(base_model, model_dir)
    model.eval()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    return model, tokenizer, device

def generate_summary(model, tokenizer, device, abstract_text, max_length=150):
    prompt = f"Summarize the following abstract:\n{abstract_text}\nSummary:"
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
    input_ids = inputs.input_ids.to(device)
    attention_mask = inputs.attention_mask.to(device)
    with torch.no_grad():
        outputs = model.generate(
            input_ids,
            attention_mask=attention_mask,
            max_length=max_length + input_ids.shape[1],
            do_sample=True,
            temperature=0.7,
            top_p=0.9,
            eos_token_id=tokenizer.eos_token_id,
            pad_token_id=tokenizer.eos_token_id,
            num_return_sequences=1
        )
    summary = tokenizer.decode(outputs[0][input_ids.shape[1]:], skip_special_tokens=True)
    return summary.strip()

if __name__ == "__main__":
    model, tokenizer, device = load_model()
    sample_abstract = ("Alzheimer's disease is a neurodegenerative disorder "
                    "characterized by progressive memory loss and cognitive decline...")
    print("Generating summary...")
    summary = generate_summary(model, tokenizer, device, sample_abstract)
    print("Summary:\n", summary)
