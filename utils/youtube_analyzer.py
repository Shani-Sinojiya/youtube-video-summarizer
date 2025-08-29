
import google.generativeai as genai

class YouTubeAnalyzer:
    """
    A class to analyze YouTube video transcripts using a generative AI model.
    """

    def __init__(self, api_key: str):
        """
        Initializes the YouTubeAnalyzer with a Google Generative AI API key.

        Args:
            api_key: The API key for accessing the Google Generative AI service.
        """
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')

    def ask_question(self, transcript: str, question: str) -> str:
        """
        Asks a question about the video transcript and returns the AI-generated answer.

        Args:
            transcript: The transcript of the YouTube video.
            question: The user's question about the video.

        Returns:
            The AI-generated answer.
        """
        prompt = f"""
        You are a helpful assistant who answers questions based on the provided YouTube video transcript.

        Transcript:
        {transcript}

        Question:
        {question}

        Answer:
        """
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"An error occurred while generating the answer: {e}"
