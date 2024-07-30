from spindle.abstracts import AbstractProcessor
import isodate

__all__ = ['YouTubeProcessor']


class YouTubeProcessor(AbstractProcessor):
    def __init__(self, youtube_service):
        self.youtube_service = youtube_service

    def process(self, video_id, options):
        video_details = self.youtube_service.get_video_details(video_id)

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

    def _process_duration(self, video_details):
        duration_iso = video_details["contentDetails"]["duration"]
        duration_seconds = isodate.parse_duration(duration_iso).total_seconds()
        return round(duration_seconds / 60)

    def _process_metadata(self, video_details):
        return {
            'id': video_details['id'],
            'title': video_details['snippet']['title'],
            'channel': video_details['snippet']['channelTitle'],
            'published_at': video_details['snippet']['publishedAt']
        }
