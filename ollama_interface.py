import requests
import json

OLLAMA_API_URL = "http://localhost:11434/api/generate"
OLLAMA_TIMEOUT = 200  # Seconds

def get_mistral_insight(prompt, model="mistral"):
    headers = {"Content-Type": "application/json"}
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_API_URL, headers=headers, data=json.dumps(payload), timeout=OLLAMA_TIMEOUT)
        response.raise_for_status()
        result = response.json()
        return result.get("response", "No response received.")
    except requests.exceptions.RequestException as e:
        return f"Error communicating with Ollama/Mistral: {e}"

# Alias
def query_mistral(prompt, model="mistral"):
    return get_mistral_insight(prompt, model)
