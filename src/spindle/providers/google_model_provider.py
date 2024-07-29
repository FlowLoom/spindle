import os
from typing import List, Optional
from spindle.abstracts import AbstractModelProvider

__All__ = ["GoogleModelProvider"]


class GoogleModelProvider(AbstractModelProvider):
    def __init__(self):
        super().__init__("Google")
        self.models = []
        self.initialize_client()

    def initialize_client(self):
        try:
            import google.generativeai as genai
            api_key = os.getenv("GOOGLE_API_KEY")
            if api_key:
                genai.configure(api_key=api_key)
                self.models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        except ImportError:
            self.logger.warning("Google GenerativeAI library is not installed.")
        except Exception as e:
            self.logger.error(f"Error initializing Google AI client: {str(e)}")

    def _fetch_models(self) -> List[str]:
        return self.models

    def _check_availability(self) -> bool:
        return bool(os.getenv("GOOGLE_API_KEY")) and bool(self.models)

    def _get_default_model(self) -> Optional[str]:
        return self.models[0] if self.models else None

    def _validate_model(self, model_name: str) -> bool:
        return model_name in self.models