from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch
import textwrap

def chunk_text(text, max_tokens=800):
    return textwrap.wrap(text, max_tokens, break_long_words=False, replace_whitespace=False)

def spin_chapter(content):
    model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        device_map="auto",
        torch_dtype=torch.float16,
        load_in_4bit=False
    )
    pipe = pipeline("text-generation", model=model, tokenizer=tokenizer)

    chunks = chunk_text(content)
    spun_output = []

    for chunk in chunks:
        prompt = f"""
You are a professional writer. Rewrite the passage in your own words, keeping the meaning, tone, and events unchanged.
ORIGINAL:
{chunk}
PARAPHRASED:
"""
        result = pipe(prompt, max_new_tokens=512, temperature=0.7, do_sample=True)[0]['generated_text']
        rewritten = result.split("PARAPHRASED:")[-1].strip()
        spun_output.append("\n".join(dict.fromkeys(rewritten.splitlines())))

    return "\n\n".join(spun_output)
