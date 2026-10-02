import os
# Suppress warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import warnings
warnings.filterwarnings('ignore')

print("--- 1. Encoder-Decoder Architecture (Machine Translation) ---")
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

# Using a lightweight translation model for fast execution
model_name_t5 = "google-t5/t5-small"
print(f"Loading {model_name_t5}...")
tokenizer_t5 = AutoTokenizer.from_pretrained(model_name_t5)
model_t5 = AutoModelForSeq2SeqLM.from_pretrained(model_name_t5)

input_ids = tokenizer_t5("translate English to French: Let's go have some wine, cause thats how we shine", return_tensors="pt").input_ids
output = model_t5.generate(input_ids, max_length=30)
translated_text = tokenizer_t5.decode(output[0], skip_special_tokens=True)
print(f"Translated text: {translated_text}")

print("\n--- 2. Decoder-Only Architecture (Text Generation) ---")
# Load the text generation pipeline with a decoder-only GPT-2 model
generator = pipeline(task="text-generation", model="gpt2")
prompt = "The future of AI is"
output = generator(prompt, max_length=30, num_return_sequences=1, pad_token_id=50256)
print("Generated text:")
print(output[0]["generated_text"])

print("\n--- 3. Encoder-Only Architecture (Sentiment Analysis) ---")
# Initialize a text classification pipeline with a pre-trained BERT model
classifier = pipeline('sentiment-analysis')
sentiment_text = "I'd want to kick you and ensure that you are hurt"
result = classifier(sentiment_text)
print(f"Text: {sentiment_text}")
print(f"Sentiment: {result}")
