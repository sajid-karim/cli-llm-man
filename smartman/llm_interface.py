import os
import requests
import json
from typing import Optional, Dict, Any

# Import official clients when available
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

# Modify llm_interface.py to use caching
from smartman.cache import ResponseCache

class LLMInterface:
    def __init__(self, api_key: Optional[str] = None, provider: Optional[str] = None, model: Optional[str] = None, use_cache: bool = True):
        """
        Initialize the LLM interface with an API key, provider, and model.
        If api_key is not provided, will look for OPENAI_API_KEY or ANTH_API_KEY in environment.

        Args:
            api_key: API key for the selected provider (optional if env vars are set)
            provider: "openai", "anthropic", or "custom" (optional if env vars are set)
            model: API-specific model name. If None, uses provider-specific defaults
            use_cache: Whether to cache responses
        """
        # Auto-detect provider and API key if not explicitly provided
        if api_key is None:
            openai_key = os.environ.get("OPENAI_API_KEY")
            anthropic_key = os.environ.get("ANTH_API_KEY")
            
            if openai_key:
                self.api_key = openai_key
                self.provider = "openai"
            elif anthropic_key:
                self.api_key = anthropic_key
                self.provider = "anthropic"
            else:
                error_msg = (
                    "No API key found. Please set one of the following environment variables:\n"
                    "For OpenAI: export OPENAI_API_KEY='your-key-here'\n"
                    "For Anthropic: export ANTH_API_KEY='your-key-here'"
                )
                raise ValueError(error_msg)
        else:
            # Use provided API key with specified or default provider
            self.api_key = api_key
            self.provider = provider.lower() if provider else "openai"
        
        # Set default models based on provider
        if model is None:
            if self.provider == "openai":
                self.model = "gpt-4o"  # Using GPT-4o as the default
            elif self.provider == "anthropic":
                self.model = "claude-3-opus-20240229"  # Using Claude 3 Opus as default
            else:
                self.model = "default-model"
        else:
            self.model = model
            
        print(f"Using {self.provider} with model {self.model}")
            
        # Initialize clients based on provider
        if self.provider == "openai":
            if OPENAI_AVAILABLE:
                self.client = openai.OpenAI(api_key=self.api_key)
            else:
                self.api_url = "https://api.openai.com/v1/chat/completions"
                print("Warning: OpenAI Python library not installed. Using requests instead.")
        
        elif self.provider == "anthropic":
            if ANTHROPIC_AVAILABLE:
                self.client = anthropic.Anthropic(api_key=self.api_key)
            else:
                self.api_url = "https://api.anthropic.com/v1/messages"
                print("Warning: Anthropic Python library not installed. Using requests instead.")
        
        else:
            # Custom provider
            self.api_url = "https://api.example.com/v1/completions"

        self.use_cache = use_cache
        if self.use_cache:
            self.cache = ResponseCache()

    def generate_summary(self, man_text: str) -> str:
        """Generate a concise summary of the given man page."""
        prompt = f"Summarize this man page concisely highlighting its core functionality, main options, and typical use cases:\n\n{man_text}"
        
        if self.use_cache:
            cached = self.cache.get_cached_response(man_text, 'summary')
            if cached:
                return cached
                
        result = self._send_request(prompt)
        
        if self.use_cache:
            self.cache.cache_response(man_text, 'summary', result)
            
        return result

    def generate_example(self, man_text: str) -> str:
        """Generate practical usage examples based on the man page."""
        prompt = f"Based on this man page, provide 3-5 practical, real-world usage examples with explanations. Include both simple and advanced use cases:\n\n{man_text}"
        return self._send_request(prompt)

    def generate_command(self, intent: str) -> str:
        """Generate a command based on the user's natural language intent."""
        prompt = f"Generate the most appropriate command line syntax for this intent. Include a brief explanation of what each part does:\n\n{intent}"
        return self._send_request(prompt)

    def _send_request(self, prompt: str) -> str:
        """Send request to the LLM API and return the response text."""
        if self.provider == "openai":
            return self._call_openai(prompt)
        elif self.provider == "anthropic":
            return self._call_anthropic(prompt)
        else:
            return self._call_custom_api(prompt)

    def _call_openai(self, prompt: str) -> str:
        """Call OpenAI API using either the official client or requests."""
        if OPENAI_AVAILABLE:
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are a helpful CLI assistant that explains man pages and generates commands."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.2,
                    max_tokens=500
                )
                return response.choices[0].message.content
            except Exception as e:
                raise Exception(f"OpenAI API error: {str(e)}")
        else:
            # Fallback to requests
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            data = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": "You are a helpful CLI assistant that explains man pages and generates commands."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.2,
                "max_tokens": 500
            }
            
            response = requests.post(self.api_url, headers=headers, json=data)
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
            else:
                self._handle_error(response)

    def _call_anthropic(self, prompt: str) -> str:
        """Call Anthropic API using either the official client or requests."""
        if ANTHROPIC_AVAILABLE:
            try:
                message = self.client.messages.create(
                    model=self.model,
                    system="You are a helpful CLI assistant that explains man pages and generates commands.",
                    max_tokens=500,
                    messages=[{"role": "user", "content": prompt}]
                )
                return message.content[0].text
            except Exception as e:
                raise Exception(f"Anthropic API error: {str(e)}")
        else:
            # Fallback to requests
            headers = {
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json"
            }
            data = {
                "model": self.model,
                "system": "You are a helpful CLI assistant that explains man pages and generates commands.",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 500
            }
            
            response = requests.post(self.api_url, headers=headers, json=data)
            if response.status_code == 200:
                return response.json()["content"][0]["text"]
            else:
                self._handle_error(response)

    def _call_custom_api(self, prompt: str) -> str:
        """Call a custom LLM API endpoint."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model,
            "prompt": prompt,
            "max_tokens": 500
        }
        
        response = requests.post(self.api_url, headers=headers, json=data)
        if response.status_code == 200:
            # Custom API response handling
            return response.json().get("text", "")
        else:
            self._handle_error(response)

    def _handle_error(self, response) -> None:
        """Handle API error responses."""
        try:
            error_data = response.json()
            error_message = error_data.get("error", {}).get("message", "Unknown error")
        except (ValueError, KeyError):
            error_message = f"HTTP error {response.status_code}: {response.text}"
            
        raise Exception(f"LLM API error ({self.provider}): {error_message}")