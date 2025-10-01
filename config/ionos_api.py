"""
IONOS API integration for working with LLM models
"""
import requests
import json
from typing import Optional, Dict, Any
from token_loader import load_token_from_file

def query_ionos_model(model_name: str, prompt: str, max_tokens: int = 1000, temperature: float = 0.1) -> Optional[str]:
    """
    Sends request to IONOS LLM API

    Args:
        model_name: model name (e.g., 'meta-llama/Llama-3.3-70B-Instruct')
        prompt: query text
        max_tokens: maximum number of tokens in response
        temperature: creativity parameter (0.0 - 1.0)

    Returns:
        str: response from model or None in case of error
    """

    # Load token
    api_key = load_token_from_file('ionos_token.txt')
    if not api_key:
        print("❌ IONOS API key not found")
        return None

    # API settings
    endpoint = "https://openai.inference.de-txl.ionos.com/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model_name,
        "messages": [
            {
                "role": "system",
                "content": "Du bist ein präziser CNC-Datenanalyst."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "max_tokens": max_tokens,
        "temperature": temperature
    }

    try:
        response = requests.post(endpoint, json=payload, headers=headers, timeout=60)
        response.raise_for_status()

        data = response.json()
        return data['choices'][0]['message']['content'].strip()

    except requests.exceptions.RequestException as e:
        print(f"❌ IONOS API error: {e}")
        return None
    except KeyError as e:
        print(f"❌ Unexpected response format: {e}")
        return None
    except Exception as e:
        print(f"❌ Unknown error: {e}")
        return None

def test_ionos_connection() -> bool:
    """
    Tests connection to IONOS API

    Returns:
        bool: True if connection successful
    """
    result = query_ionos_model(
        model_name="meta-llama/Llama-3.1-8B-Instruct",
        prompt="Hello, can you confirm the connection is working?",
        max_tokens=50
    )

    return result is not None

if __name__ == "__main__":
    # Connection test
    if test_ionos_connection():
        print("✅ IONOS API connection works")
    else:
        print("❌ IONOS API connection failed")