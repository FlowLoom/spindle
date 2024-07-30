from spindle.abstracts import AbstractFetcher
from typing import Any, Dict
import sys

__all__ = ['SaveFetcher']


class SaveFetcher(AbstractFetcher):
    def _fetch_content(self, source: Any, **kwargs: Any) -> str:
        return sys.stdin.read()

    def _process_content(self, content: str, **kwargs: Any) -> Dict[str, Any]:
        return self.processor.process(content, **kwargs)

    def _format_output(self, processed_content: Dict[str, Any], **kwargs: Any) -> Dict[str, Any]:
        return processed_content
