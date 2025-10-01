# API Token Configuration

## File Structure

```
config/
├── README.md           # This file with instructions
├── token_loader.py     # Module for loading tokens
├── ionos_api.py       # IONOS API integration
├── openai_token.txt   # OpenAI API key
├── anthropic_token.txt # Anthropic API key
└── ionos_token.txt    # IONOS API key
```

## Token Setup

### 1. OpenAI API
1. Open the file `openai_token.txt`
2. Replace the content with your OpenAI API key:
   ```
   sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

### 2. Anthropic API
1. Open the file `anthropic_token.txt`
2. Replace the content with your Anthropic API key:
   ```
   sk-ant-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

### 3. IONOS API ⚠️ (requires correct token)
1. File `ionos_token.txt` contains a UUID, but needs a proper API token
2. **Current token is invalid for API access**
3. See `IONOS_TOKEN_SETUP.md` for instructions on getting the correct token

## Usage in Notebook

The notebook `8-phase3_Numerical_Accuracy_Evaluation_API.ipynb` automatically loads tokens from these files when started.

### Supported Models:

**OpenAI:**
- gpt-3.5-turbo
- gpt-4
- gpt-4-turbo
- gpt-4o
- gpt-4o-mini

**Anthropic:**
- claude-3-haiku-20240307
- claude-3-sonnet-20240229
- claude-3-opus-20240229
- claude-3-5-sonnet-20241022

**IONOS:**
- meta-llama/Llama-3.3-70B-Instruct
- meta-llama/Llama-3.1-8B-Instruct
- meta-llama/Llama-3.1-70B-Instruct

## Connection Testing

Run from config directory:
```python
python ionos_api.py
```

## Security

⚠️ **IMPORTANT**:
- Do not add token files to git repository
- Keep tokens in a secure place
- Regularly update tokens according to provider policy