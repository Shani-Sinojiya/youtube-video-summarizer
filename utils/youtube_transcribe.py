from youtube_transcript_api import YouTubeTranscriptApi, TranscriptList


class YouTubeTranscriber:
    def __init__(self, video_id: str):
        self.transcriber = YouTubeTranscriptApi()
        self.video_id = video_id
        self.transcribe_language = "en"

    def get_list(self) -> TranscriptList:
        return self.transcriber.list(self.video_id)

    def set_transcribe_language(self, language: str):
        self.transcribe_language = language

    def transcribe(self):
        allinfo = self.get_list()

        try:
            if not allinfo:
                raise ValueError("No transcripts found for the video.")
            else:
                langcode_list = [
                    transcript.language_code for transcript in allinfo]

                if self.transcribe_language not in langcode_list:
                    raise ValueError(
                        f"Transcription not available in {self.transcribe_language}.")
                else:
                    # Fetch and return the transcript for the specified language
                    transcript = next(
                        (t for t in allinfo if t.language_code == self.transcribe_language), None)
                    if transcript:
                        return transcript.fetch(preserve_formatting=True)
                    else:
                        raise ValueError("Transcript not found.")

        except ValueError as e:
            print(f"Error: {e}")
            return None
