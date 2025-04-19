import os
import sys
import torch
import logging
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from config.config import HUGGINGFACE_TOKEN, MISTRAL_LOCAL_PATH

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Setup logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variables to cache the model and tokenizer after loading once
_cached_model = None
_cached_tokenizer = None

def check_cuda_availability():
    """Checks and logs whether CUDA is available."""
    if torch.cuda.is_available():
        logger.info("🔋 CUDA is available. Using GPU for inference.")
    else:
        logger.warning("⚠️ CUDA not available. Falling back to CPU.")

def load_mistral_model(model_path=None):
    """Loads the Mistral model and tokenizer from the local path using 4-bit quantization. Caches them for reuse."""
    global _cached_model, _cached_tokenizer

    model_path = os.path.abspath(model_path or MISTRAL_LOCAL_PATH)

    # Return cached model and tokenizer if already loaded
    if _cached_model is not None and _cached_tokenizer is not None:
        logger.info("🔁 Returning cached Mistral model and tokenizer.")
        return _cached_tokenizer, _cached_model

    logger.info(f"🔍 Attempting to load Mistral model from: {model_path}")

    try:
        # Use 4-bit quantization for optimized performance
        quant_config = BitsAndBytesConfig(load_in_4bit=True)

        tokenizer = AutoTokenizer.from_pretrained(
            model_path,
            token=HUGGINGFACE_TOKEN,
            local_files_only=True
        )

        model = AutoModelForCausalLM.from_pretrained(
            model_path,
            token=HUGGINGFACE_TOKEN,
            local_files_only=True,
            device_map="auto",  # Use GPU if available
            quantization_config=quant_config,
            trust_remote_code=True
        )

        # Cache the loaded model and tokenizer
        _cached_model = model
        _cached_tokenizer = tokenizer

        logger.info(f"✅ Mistral model loaded successfully from: {model_path}")
        return tokenizer, model

    except Exception as e:
        logger.error(f"❌ Failed to load model or tokenizer.\n{e}")
        raise

if __name__ == "__main__":
    check_cuda_availability()
    load_mistral_model()
