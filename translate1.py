from transformers import AutoModelForCausalLM, AutoTokenizer
# Loading checkpoint shards:  40%|████      | 2/5 [00:25<00:39, 13.11s/it]
# Process finished with exit code 137 (interrupted by signal 9:SIGKILL)

model_id = "ModelSpace/GemmaX2-28-9B-v0.1"
tokenizer = AutoTokenizer.from_pretrained(model_id)

model = AutoModelForCausalLM.from_pretrained(model_id)

text = "Translate this from Chinese to English:\nChinese: 我爱机器翻译\nEnglish:"
inputs = tokenizer(text, return_tensors="pt")

outputs = model.generate(**inputs, max_new_tokens=512)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))