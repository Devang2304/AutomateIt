from langchain_google_genai import GoogleGenerativeAI
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi
import os
load_dotenv()

class YtSummariser:
    def __init__(self):
        self.googleAPIKey = os.getenv("googleAPIkey")
        self.llm = GoogleGenerativeAI(model="gemini-2.0-flash",google_api_key='')

    def get_video_id(self, url: str) -> str:
        if 'youtu.be' in url:
            return url.split('/')[-1]
        elif 'youtube.com' in url:
            return url.split('v=')[1].split('&')[0]
        return url

    def getSubtitle(self, video_url: str) -> str:
        try:
            video_id = self.get_video_id(video_url)
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            return ' '.join([entry['text'] for entry in transcript])
        except Exception as e:
            return f"Error getting subtitles: {str(e)}"
    
    def getSummary(self,video_url)->str:
        subtitle = self.getSubtitle(video_url)
        prompt = f"""
        You are a helpful assistant that summarises youtube videos.
        Here is the subtitle of the video:
        {subtitle}
        Please summarise the video correctly in precise and concise manner without 
        losing any important information.
        """
        response = self.llm.invoke(prompt)
        return response
    


def main():
    ytSummariser = YtSummariser()
    video_url = input("Enter the video url: ")
    summary = ytSummariser.getSummary(video_url)
    print(summary)

if __name__ == "__main__":
    main()
