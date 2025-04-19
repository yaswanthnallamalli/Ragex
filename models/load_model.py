# models/load_model.py
import os
import sys
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline, BitsAndBytesConfig
from config.config import HUGGINGFACE_TOKEN, MISTRAL_LOCAL_PATH

# Add parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Cached pipeline
model_pipeline = None

def load_mistral_pipeline():
    """
    Loads and caches the Mistral text-generation pipeline (4-bit quant).
    """
    global model_pipeline
    if model_pipeline is None:
        quant_config = BitsAndBytesConfig(load_in_4bit=True)

        tokenizer = AutoTokenizer.from_pretrained(
            MISTRAL_LOCAL_PATH,
            token=HUGGINGFACE_TOKEN,
            cache_dir=MISTRAL_LOCAL_PATH,
            local_files_only=True
        )

        model = AutoModelForCausalLM.from_pretrained(
            MISTRAL_LOCAL_PATH,
            device_map="auto",
            token=HUGGINGFACE_TOKEN,
            trust_remote_code=True,
            quantization_config=quant_config,
            cache_dir=MISTRAL_LOCAL_PATH,
            local_files_only=True
        )

        model_pipeline = pipeline("text-generation", model=model, tokenizer=tokenizer)
        print("✅ Mistral model pipeline loaded and cached.")
    else:
        print("♻️ Reusing cached Mistral model pipeline.")
    return model_pipeline
