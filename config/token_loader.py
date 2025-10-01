"""
Module for loading API tokens from files
"""
from pathlib import Path
from typing import Optional

def load_token_from_file(filename: str) -> Optional[str]:
    """
    Loads token from file, ignoring comments and empty lines

    Args:
        filename: name of the file containing the token

    Returns:
        str: token or None if file not found or empty
    """
    config_dir = Path(__file__).parent
    token_file = config_dir / filename

    try:
        if token_file.exists():
            with open(token_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    # Skip comments and empty lines
                    if line and not line.startswith('#'):
                        return line
        return None
    except Exception as e:
        print(f"⚠️  Error reading {filename}: {e}")
        return None

def get_api_keys() -> dict:
    """
    Loads all API keys from configuration files

    Returns:
        dict: dictionary with API keys
    """
    return {
        'openai': load_token_from_file('openai_token.txt') or '',
        'anthropic': load_token_from_file('anthropic_token.txt') or '',
        'ionos': load_token_from_file('ionos_token.txt') or '',
    }

# Example usage:
if __name__ == "__main__":
    keys = get_api_keys()
    for provider, key in keys.items():
        status = "✅ configured" if key else "❌ not found"
        print(f"{provider}: {status}")