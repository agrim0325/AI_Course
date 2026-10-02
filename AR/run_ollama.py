# Run Ollama Locally via LangChain
# NOTE: You must have Ollama installed on your system (https://ollama.com/download)
# and have pulled the mistral model by running ollama run mistral in your terminal.

from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM

template = "Question: {question}\n\nAnswer: Let's think step by step."

prompt = ChatPromptTemplate.from_template(template)
model = OllamaLLM(model="mistral")

chain = prompt | model

question = "Who is Sir Isaac Newton?"
print(f"Asking Ollama (mistral): {question}\n")

try:
    response = chain.invoke({"question": question})
    print("Ollama Response:")
    print(response)
except Exception as e:
    print(f"Error connecting to Ollama: {e}")
    print("\nPlease ensure Ollama is installed and running, and the 'mistral' model is downloaded.")
