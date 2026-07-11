"""
gemini_client.py
-----------------
Thin wrapper around the Google Gemini API (google-genai SDK).
Keeps all API-specific error handling (rate limits, connection issues,
malformed responses) in one place so the rest of the app never has to
deal with the SDK directly.
"""

import time
from google import genai
from google.genai import errors as genai_errors

from . import config


class GeminiClientError(Exception):
    """Raised when the Gemini API call ultimately fails."""


class GeminiClient:
    def __init__(self, api_key: str = None, model_name: str = None, max_retries: int = 3):
        self.api_key = api_key or config.GEMINI_API_KEY
        self.model_name = model_name or config.GEMINI_MODEL
        self.max_retries = max_retries

        self.client = genai.Client(api_key=self.api_key)

    def generate(self, prompt: str) -> str:
        """
        Sends a prompt to Gemini and returns the raw text response.
        Retries on rate-limit / transient errors with exponential backoff.
        Raises GeminiClientError with a friendly message on final failure.
        """
        last_error = None

        for attempt in range(1, self.max_retries + 1):
            try:
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=prompt,
                )

                if not response or not getattr(response, "text", None):
                    raise GeminiClientError(
                        "The model returned an empty response. Try again "
                        "or shorten the input text."
                    )
                return response.text

            except genai_errors.ClientError as e:
                code = getattr(e, "code", None)
                if code == 429:
                    last_error = e
                    wait_time = 2 ** attempt
                    print(
                        f"  Rate limit hit (attempt {attempt}/{self.max_retries}). "
                        f"Waiting {wait_time}s before retrying..."
                    )
                    time.sleep(wait_time)
                elif code in (401, 403):
                    raise GeminiClientError(
                        f"Permission denied - check that your GEMINI_API_KEY is valid: {e}"
                    )
                elif code == 400:
                    raise GeminiClientError(f"Invalid request sent to Gemini API: {e}")
                else:
                    last_error = e
                    wait_time = 2 ** attempt
                    print(
                        f"  Client error (attempt {attempt}/{self.max_retries}): {e}. "
                        f"Retrying in {wait_time}s..."
                    )
                    time.sleep(wait_time)

            except genai_errors.ServerError as e:
                last_error = e
                wait_time = 2 ** attempt
                print(
                    f"  Server error (attempt {attempt}/{self.max_retries}). "
                    f"Waiting {wait_time}s before retrying..."
                )
                time.sleep(wait_time)

            except ConnectionError as e:
                last_error = e
                wait_time = 2 ** attempt
                print(
                    f"  Connection issue (attempt {attempt}/{self.max_retries}). "
                    f"Waiting {wait_time}s before retrying..."
                )
                time.sleep(wait_time)

            except GeminiClientError:
                raise

            except Exception as e:
                last_error = e
                wait_time = 2 ** attempt
                print(
                    f"  Unexpected error (attempt {attempt}/{self.max_retries}): {e}. "
                    f"Retrying in {wait_time}s..."
                )
                time.sleep(wait_time)

        raise GeminiClientError(
            f"Failed to get a response from Gemini after {self.max_retries} attempts. "
            f"Last error: {last_error}"
        )