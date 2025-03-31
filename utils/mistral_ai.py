import json
import os
import time
from typing import Dict, List

import requests

MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"
MAX_RETRIES = 3
RETRY_DELAY = 1  # seconds

def get_ai_response(messages: List[Dict[str, str]]) -> str:
    """
    Get response from Mistral AI API with retries and better error handling
    
    Args:
        messages: List of dicts with 'role' and 'content' keys
        
    Returns:
        str: The AI's response
        
    Raises:
        Exception: If the API request fails after all retries
    """
    headers = {
        "Authorization": f"Bearer {os.getenv('MISTRAL_API_KEY')}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mistral-tiny",  # Using the latest model
        "messages": messages,
        "temperature": 0.7,  # Add some creativity while keeping responses focused
        "max_tokens": 1000  # Limit response length
    }

    for attempt in range(MAX_RETRIES):
        try:
            response = requests.post(
                MISTRAL_API_URL, 
                headers=headers, 
                data=json.dumps(data),
                timeout=30  # Add timeout
            )
            
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
            elif response.status_code == 429:  # Rate limit
                if attempt < MAX_RETRIES - 1:
                    time.sleep(RETRY_DELAY * (attempt + 1))  # Exponential backoff
                    continue
                raise Exception("Rate limit exceeded. Please try again later.")
            else:
                error_msg = f"API Error: {response.status_code} - {response.text}"
                raise Exception(error_msg)
                
        except requests.exceptions.Timeout:
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY * (attempt + 1))
                continue
            raise Exception("Request timed out. Please try again.")
        except requests.exceptions.RequestException as e:
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY * (attempt + 1))
                continue
            raise Exception(f"Network error: {str(e)}")
        except (KeyError, json.JSONDecodeError) as e:
            raise Exception(f"Invalid API response: {str(e)}")
        except Exception as e:
            raise Exception(f"Unexpected error: {str(e)}")
            
    raise Exception("Failed to get AI response after all retries")
