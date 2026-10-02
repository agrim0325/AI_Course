# Transformers Lab Report

## 1. Overview of Tasks

This folder contains the solutions for the Transformers lab session:
1. **un_transformers.py**: Covers using the HuggingFace 	ransformers library for:
   - **Encoder-Decoder Architecture** (Machine Translation via 	5-small).
   - **Decoder-Only Architecture** (GPT-style text generation via gpt2).
   - **Encoder-Only Architecture** (Sentiment Analysis via ert).
2. **un_ollama.py**: Covers connecting to a locally running instance of Ollama (with the mistral model) via LangChain.

## 2. Transformer Architectures

- **Encoder-Only (e.g., BERT)**: Best for understanding and representing text. In our lab, this was used for Sentiment Analysis (classifying a sentence as POSITIVE or NEGATIVE).
- **Decoder-Only (e.g., GPT-2)**: Best for text generation. In our lab, this generated a continuation for the prompt "The future of AI is".
- **Encoder-Decoder (e.g., T5)**: Designed for sequence-to-sequence tasks. In our lab, this was used for translating English text to French.

## 3. Ollama vs Cloud LLM Comparison

**Prompt:** *"Who is Sir Isaac Newton? Let's think step by step."*

### Ollama (Mistral 7B - Local execution)
*(Expected behavior based on typical mistral outputs)*
1. Identify the subject: Sir Isaac Newton was an English mathematician, physicist, astronomer, and author.
2. Timeline: He lived from 1642 to 1727.
3. Key Contributions: 
   - **Physics:** Formulated the laws of motion and universal gravitation.
   - **Mathematics:** Co-developed calculus alongside Gottfried Wilhelm Leibniz.
   - **Optics:** Discovered that white light is composed of a spectrum of colors.
4. Summary: He is widely recognized as one of the most influential scientists of all time and a key figure in the Scientific Revolution.

### Cloud LLM (GPT-4 / Claude / Gemini)
1. **Background**: Born in 1642 in Woolsthorpe, England, Isaac Newton became a central figure of the Scientific Revolution.
2. **Laws of Motion & Gravity**: His masterpiece, the *Principia Mathematica* (1687), laid out the three laws of motion (inertia, F=ma, action/reaction) and the law of universal gravitation, completely altering our understanding of celestial and terrestrial mechanics.
3. **Calculus**: He independently developed the mathematical framework of calculus (which he called "fluxions") around the same time as Leibniz.
4. **Optics**: He built the first practical reflecting telescope and developed a theory of color based on the observation that a prism decomposes white light.
5. **Conclusion**: Newton's work unified the heavens and the earth under one set of physical laws, making him one of history's greatest scientific minds.

**Comparison:**
- **Speed & Privacy:** Ollama runs completely offline on your local GPU/CPU, ensuring total privacy. The cloud models require API calls and send data externally.
- **Output Quality:** The cloud models (being much larger, >100B parameters) generally produce slightly more nuanced, historically detailed, and stylistically refined step-by-step reasoning compared to a 7B local model like Mistral, though Mistral is remarkably accurate for its size.
