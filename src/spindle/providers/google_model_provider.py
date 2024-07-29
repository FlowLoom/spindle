from typing import List, Dict, Any, Generator, Optional
import google.generativeai as genai
from spindle.abstracts import AbstractModelProvider

__all__ = ["GoogleModelProvider"]


class GoogleModelProvider(AbstractModelProvider):
    def __init__(self, api_key: str):
        super().__init__("Google")
        genai.configure(api_key=api_key)
        self.models = []
        self._fetch_models()

    def _fetch_models(self) -> List[str]:
        try:
            self.models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            return self.models
        except Exception as e:
            self.logger.error(f"Error fetching Google AI models: {str(e)}")
            return []

    def _check_availability(self) -> bool:
        return len(self.models) > 0

    def _get_default_model(self) -> Optional[str]:
        return self.models[0] if self.models else None

    def _validate_model(self, model_name: str) -> bool:
        return model_name in self.models

    def _send_message(self, messages: List[Dict[str, str]], model: str, args: Dict[str, Any]) -> str:
        try:
            genai_model = genai.GenerativeModel(model_name=model)
            chat = genai_model.start_chat(history=[])

            for message in messages:
                if message['role'] == 'user':
                    chat.send_message(message['content'])
                elif message['role'] == 'assistant':
                    # Simulating assistant messages in the chat history
                    chat._history.append(genai.types.ContentType(role='model', parts=[message['content']]))

            response = chat.send_message(
                messages[-1]['content'],
                generation_config=genai.types.GenerationConfig(
                    temperature=args.get('temp', 0),
                    top_p=args.get('top_p', 1),
                    top_k=args.get('top_k', 1),
                    max_output_tokens=args.get('max_tokens', 1000),
                )
            )
            return response.text
        except Exception as e:
            self.logger.error(f"Error sending message to Google AI: {str(e)}")
            raise

    def _stream_message(self, messages: List[Dict[str, str]], model: str, args: Dict[str, Any]) -> Generator[str, None, None]:
        try:
            genai_model = genai.GenerativeModel(model_name=model)
            chat = genai_model.start_chat(history=[])

            for message in messages:
                if message['role'] == 'user':
                    chat.send_message(message['content'])
                elif message['role'] == 'assistant':
                    # Simulating assistant messages in the chat history
                    chat._history.append(genai.types.ContentType(role='model', parts=[message['content']]))

            response = chat.send_message(
                messages[-1]['content'],
                generation_config=genai.types.GenerationConfig(
                    temperature=args.get('temp', 0),
                    top_p=args.get('top_p', 1),
                    top_k=args.get('top_k', 1),
                    max_output_tokens=args.get('max_tokens', 1000),
                ),
                stream=True
            )
            for chunk in response:
                yield chunk.text
        except Exception as e:
            self.logger.error(f"Error streaming message from Google AI: {str(e)}")
            raise
