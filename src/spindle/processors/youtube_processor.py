from spindle.abstracts import AbstractProcessor
import isodate
from typing import Any, Dict

__all__ = ['YouTubeProcessor']


class YouTubeProcessor(AbstractProcessor):
    def __init__(self, youtube_service):
        self.youtube_service = youtube_service

    def _preprocess(self, content: Any) -> Any:
        """
        Preprocess the content before extraction.
        In this case, we'll just return the video_id and options.
        """
        return content  # content is already (video_id, options)

    def _extract_content(self, preprocessed_content: Any) -> Any:
        """
        Extract the video details using the YouTube service.
        """
        video_id, options = preprocessed_content
        return self.youtube_service.get_video_details(video_id), options

    def _main_process(self, extracted_content: Any) -> Any:
        """
        Main processing step to gather all required information.
        """
        video_details, options = extracted_content
        video_id = video_details['id']

        result = {}
        if options['duration'] or not any(options.values()):
            result['duration'] = self._process_duration(video_details)
        if options['transcript'] or not any(options.values()):
            result['transcript'] = self.youtube_service.get_transcript(video_id, options['lang'])
        if options['comments'] or not any(options.values()):
            result['comments'] = self.youtube_service.get_comments(video_id)
        if options['metadata'] or not any(options.values()):
            result['metadata'] = self._process_metadata(video_details)

        return result

    def _postprocess(self, processed_content: Any) -> Dict[str, Any]:
        """
        Postprocess the content. In this case, we'll just return the processed content as is.
        """
        return processed_content

    def process(self, video_id: str, options: Dict[str, Any]) -> Dict[str, Any]:
        """
        The main process method that orchestrates the entire processing workflow.
        """
        preprocessed = self._preprocess((video_id, options))
        extracted = self._extract_content(preprocessed)
        processed = self._main_process(extracted)
        return self._postprocess(processed)

    def _process_duration(self, video_details: Dict[str, Any]) -> int:
        duration_iso = video_details["contentDetails"]["duration"]
        duration_seconds = isodate.parse_duration(duration_iso).total_seconds()
        return round(duration_seconds / 60)

    def _process_metadata(self, video_details: Dict[str, Any]) -> Dict[str, str]:
        return {
            'id': video_details['id'],
            'title': video_details['snippet']['title'],
            'channel': video_details['snippet']['channelTitle'],
            'published_at': video_details['snippet']['publishedAt']
        }
