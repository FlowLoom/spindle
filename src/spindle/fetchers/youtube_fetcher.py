from spindle.abstracts import AbstractFetcher
from spindle.interfaces import IProcessor
from urllib.parse import urlparse, parse_qs, unquote
from typing import Any, Dict

__all__ = ['YouTubeFetcher']


class YouTubeFetcher(AbstractFetcher):
    def __init__(self, processor: IProcessor):
        super().__init__(processor)

    def _fetch_content(self, source: str, **kwargs: Any) -> str:
        video_id = self._get_video_id(source)
        if not video_id:
            raise ValueError("Invalid YouTube URL")
        return video_id

    def _process_content(self, video_id: str, **kwargs: Any) -> Dict[str, Any]:
        options = kwargs.get('options', {})
        return self.processor.process(video_id, options=options)

    def _format_output(self, processed_content: Dict[str, Any], **kwargs: Any) -> Dict[str, Any]:
        return processed_content

    @staticmethod
    def _get_video_id(url) -> str or None:
        url = unquote(url).replace("\\", "")
        parsed_url = urlparse(url)
        if parsed_url.hostname == 'youtu.be':
            return parsed_url.path[1:12]
        if parsed_url.hostname in {'www.youtube.com', 'youtube.com'}:
            if parsed_url.path == '/watch':
                return parse_qs(parsed_url.query).get('v', [None])[0]
            if parsed_url.path.startswith('/embed/'):
                return parsed_url.path.split('/')[2]
            if parsed_url.path.startswith('/v/'):
                return parsed_url.path.split('/')[2]
        return None
