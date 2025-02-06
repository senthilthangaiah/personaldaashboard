import ollama

def summarize_text(text):
    """
    Summarize the given text using the Ollama LLaVA model.
    """
    try:
        response = ollama.generate(model='llava:latest', prompt=f"Summarize: {text}")
        return response['response']
    except Exception as e:
        print(f"Error summarizing text: {e}")
        return "Unable to summarize at the moment."
