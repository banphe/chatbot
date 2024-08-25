from .tool import Tool
from .tool_registry import ToolRegistry
from youtube_transcript_api import YouTubeTranscriptApi
import re

def extract_video_id(url):
    patterns = [
        r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com|youtu\.be)\/(?:watch\?v=)?(?:embed\/)?(?:v\/)?(?:shorts\/)?(?P<id>[^\s&]+)',
        r'(?:https?:\/\/)?(?:www\.)?youtu\.be\/(?P<id>[^\s&]+)'
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group('id')
    return None

def get_you_tube_transcript(url):
    video_id = extract_video_id(url)
    if not video_id:
        return "Error: Invalid YouTube URL or video ID not found."
    
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return transcript
    except YouTubeTranscriptApi.NoTranscriptAvailable:
        return "Error: No transcript available for this video."
    except YouTubeTranscriptApi.TranscriptsDisabled:
        return "Error: Transcripts are disabled for this video."
    except YouTubeTranscriptApi.NoTranscriptFound:
        return "Error: No transcript found for this video."
    except Exception as e:
        return f"Error: An unexpected error occurred: {str(e)}"

def register(registry: ToolRegistry):
    registry.register_tool(Tool(
        name="get_you_tube_transcript",
        description="Retrieves the transcript of a YouTube video given its URL. The transcript is returned as a list of dictionaries, where each dictionary represents a segment of the video with 'text', 'start', and 'duration' keys. This tool is useful for analyzing or searching through the content of YouTube videos. It can handle various forms of YouTube URLs, including shortened forms. The tool returns error messages for videos without transcripts, disabled transcripts, or other issues.",
        function=get_you_tube_transcript,
        input_schema={
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "The URL of the YouTube video to transcribe. Can be a full URL or a shortened URL."
                }
            },
            "required": ["url"]
        }
    ))