from youtube_transcript_api import FetchedTranscript, YouTubeTranscriptApi, TranscriptList


class YouTubeTranscriber:
    def __init__(self, video_id: str) -> None:
        self.transcriber = YouTubeTranscriptApi()
        self.video_id = video_id
        self.transcribe_language = "en"

    def get_list(self) -> TranscriptList:
        """Get transcribe information about the languages available"""
        return self.transcriber.list(self.video_id)

    def set_transcribe_language(self, language: str) -> None:
        """Set Transcribe Language"""
        self.transcribe_language = language

    def transcribe(self) -> FetchedTranscript | None:
        """Get transcription in the specified language"""
        allinfo = self.get_list()

        try:
            if not allinfo:
                raise ValueError("No transcripts found for the video.")

            langcode_list = [
                transcript.language_code for transcript in allinfo]

            if self.transcribe_language not in langcode_list:
                raise ValueError(
                    f"Transcription not available in {self.transcribe_language}.")

            transcript = next(
                (t for t in allinfo if t.language_code == self.transcribe_language), None)
            if transcript:
                return transcript.fetch(preserve_formatting=True)

            raise ValueError("Transcript not found.")

        except ValueError as e:
            print(f"Error: {e}")
            return None

    def get_all_transcripts(self) -> dict[str, list[dict]]:
        """Get transcripts for all available languages"""
        try:
            all_transcript_info = self.get_list()
            all_transcripts = {}

            for transcript_info in all_transcript_info:
                lang_code = transcript_info.language_code
                try:
                    # Fetch transcripts with formatting preserved
                    transcript_data = transcript_info.fetch(
                        preserve_formatting=True)
                    # Store transcript data directly in the language slot
                    all_transcripts[lang_code] = transcript_data
                except Exception as e:
                    print(f"Error fetching transcript for {lang_code}: {e}")
                    continue

            return all_transcripts
        except Exception as e:
            print(f"Error getting all transcripts: {e}")
            return {}
