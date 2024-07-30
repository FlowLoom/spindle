from spindle.abstracts import AbstractFetcher
from spindle.interfaces import IProcessor
import re

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
    def _get_video_id(url) -> str:
        pattern = r"(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})"
        match = re.search(pattern, url)
        return match.group(1) if match else None
