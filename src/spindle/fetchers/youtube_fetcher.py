from spindle.abstracts import AbstractFetcher
from spindle.interfaces import IProcessor
import re
from urllib.parse import urlparse, parse_qs, unquote

__all__ = ['YouTubeFetcher']


class YouTubeFetcher(AbstractFetcher):
    def __init__(self, processor: IProcessor):
        super().__init__(processor)

    def _fetch_content(self, url):
        video_id = self._get_video_id(url)
        if not video_id:
            raise ValueError("Invalid YouTube URL")
        return video_id

    def _process_content(self, video_id, options):
        return self.processor.process(video_id, options)

    def _format_output(self, processed_content):
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
