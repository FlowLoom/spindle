import asyncio
from typing import List, Dict, Any, Generator, Optional
from ollama import AsyncClient
from spindle.abstracts.abstract_model_provider import AbstractModelProvider

__all__ = ["OllamaModelProvider"]


class OllamaModelProvider(AbstractModelProvider):
    def __init__(self, host: str = "http://localhost:11434"):
        super().__init__("Ollama")
        self.host = host
        self.models = []
        self._fetch_models()

    def _fetch_models(self) -> List[str]:
        try:
            client = AsyncClient(host=self.host)
            self.models = asyncio.run(self._async_fetch_models(client))
            return self.models
        except Exception as e:
            self.logger.error(f"Error fetching Ollama models: {str(e)}")
            return []

    async def _async_fetch_models(self, client: AsyncClient) -> List[str]:
        response = await client.list()
        return [model['name'] for model in response['models']]

    def _check_availability(self) -> bool:
        return len(self.models) > 0

    def _get_default_model(self) -> Optional[str]:
        return self.models[0] if self.models else None

    def _validate_model(self, model_name: str) -> bool:
        return model_name in self.models

    def _send_message(self, messages: List[Dict[str, str]], model: str, args: Dict[str, Any]) -> str:
        try:
            return asyncio.run(self._async_send_message(messages, model, args))
        except Exception as e:
            self.logger.error(f"Error sending message to Ollama: {str(e)}")
            raise

    async def _async_send_message(self, messages: List[Dict[str, str]], model: str, args: Dict[str, Any]) -> str:
        async with AsyncClient(host=self.host) as client:
            response = await client.chat(
                model=model,
                messages=messages,
                options={
                    "temperature": args.get('temp', 0.7),
                    "top_p": args.get('top_p', 1),
                    "num_predict": args.get('max_tokens', 100),
                }
            )
            return response['message']['content']

    def _stream_message(self, messages: List[Dict[str, str]], model: str, args: Dict[str, Any]) -> Generator[str, None, None]:
        try:
            for chunk in asyncio.run(self._async_stream_message(messages, model, args)):
                yield chunk
        except Exception as e:
            self.logger.error(f"Error streaming message from Ollama: {str(e)}")
            raise

    async def _async_stream_message(self, messages: List[Dict[str, str]], model: str, args: Dict[str, Any]) -> Generator[str, None, None]:
        async with AsyncClient(host=self.host) as client:
            async for part in await client.chat(
                    model=model,
                    messages=messages,
                    options={
                        "temperature": args.get('temp', 0.7),
                        "top_p": args.get('top_p', 1),
                        "num_predict": args.get('max_tokens', 100),
                    },
                    stream=True
            ):
                yield part['message']['content']
