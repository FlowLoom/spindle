from typing import Dict, List, Generator
import asyncio
from ollama import AsyncClient
from spindle.config import ConfigManager
from spindle.exceptions import SpindleException

__All__ = ['OllamaService']


class OllamaService:
    def __init__(self, config: ConfigManager):
        self.config = config

    async def _send_message_async(self, messages: List[Dict[str, str]], args: Dict) -> str:
        try:
            async with AsyncClient(host=args.get('host', '')) as client:
                response = await client.chat(
                    model=args.get('model', self.config.get('DEFAULT_MODEL')),
                    messages=messages
                )
            return response['message']['content']
        except Exception as e:
            raise SpindleException(f"Ollama error: {str(e)}")

    def send_message(self, messages: List[Dict[str, str]], args: Dict) -> str:
        return asyncio.run(self._send_message_async(messages, args))

    async def _stream_message_async(self, messages: List[Dict[str, str]], args: Dict) -> Generator[str, None, None]:
        try:
            async with AsyncClient(host=args.get('host', '')) as client:
                async for part in await client.chat(
                        model=args.get('model', self.config.get('DEFAULT_MODEL')),
                        messages=messages,
                        stream=True
                ):
                    yield part['message']['content']
        except Exception as e:
            raise SpindleException(f"Ollama streaming error: {str(e)}")

    def stream_message(self, messages: List[Dict[str, str]], args: Dict) -> Generator[str, None, None]:
        return asyncio.run(self._stream_message_async(messages, args))