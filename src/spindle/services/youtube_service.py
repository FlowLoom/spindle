from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from youtube_transcript_api import YouTubeTranscriptApi
import isodate

__all__ = ['YouTubeService']


class YouTubeService:
    def __init__(self, api_key):
        self.youtube = build("youtube", "v3", developerKey=api_key)

    def get_video_details(self, video_id):
        video_response = self.youtube.videos().list(
            id=video_id, part="contentDetails,snippet").execute()
        return video_response["items"][0]

    def get_transcript(self, video_id, lang='en'):
        try:
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=[lang])
            return " ".join([item["text"] for item in transcript_list])
        except Exception as e:
            return f"Transcript not available in the selected language ({lang}). ({e})"

    def get_comments(self, video_id):
        comments = []
        try:
            request = self.youtube.commentThreads().list(
                part="snippet,replies",
                videoId=video_id,
                textFormat="plainText",
                maxResults=100
            )
            while request:
                response = request.execute()
                for item in response['items']:
                    comments.append(item['snippet']['topLevelComment']['snippet']['textDisplay'])
                    if 'replies' in item:
                        for reply in item['replies']['comments']:
                            comments.append("    - " + reply['snippet']['textDisplay'])
                request = self.youtube.commentThreads().list_next(request, response) if 'nextPageToken' in response else None
        except HttpError as e:
            print(f"Failed to fetch comments: {e}")
        return comments
