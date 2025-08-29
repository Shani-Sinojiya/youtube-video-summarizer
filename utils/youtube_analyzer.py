
import google.generativeai as genai
from typing import Dict, List
import os

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
        
        # Try to get model from environment, fallback to latest available
        model_name = os.getenv('DEFAULT_MODEL', 'gemini-1.5-flash')
        
        # List of models to try in order of preference
        models_to_try = [
            model_name,
            'gemini-1.5-flash',
            'gemini-1.5-pro',
            'gemini-pro'
        ]
        
        self.model = None
        for model in models_to_try:
            try:
                self.model = genai.GenerativeModel(model)
                print(f"Successfully initialized with model: {model}")
                break
            except Exception as e:
                print(f"Failed to initialize model {model}: {e}")
                continue
        
        if self.model is None:
            raise Exception("Failed to initialize any Gemini model. Please check your API key and available models.")

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
        You are a helpful AI assistant specialized in analyzing YouTube video content. 
        Your task is to answer questions based on the provided video transcript accurately and comprehensively.

        Instructions:
        - Answer questions directly and concisely
        - Use specific details from the transcript when relevant
        - If information is not available in the transcript, state that clearly
        - Provide structured answers when appropriate (bullet points, numbered lists)
        - Focus on being helpful and informative

        Video Transcript:
        {transcript}

        User Question:
        {question}

        Answer:
        """
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"An error occurred while generating the answer: {e}"

    def summarize_video(self, transcript: str) -> str:
        """
        Generates a comprehensive summary of the video based on its transcript.

        Args:
            transcript: The transcript of the YouTube video.

        Returns:
            A summary of the video content.
        """
        prompt = f"""
        Create a comprehensive summary of this YouTube video based on its transcript.
        
        Please structure your summary as follows:
        1. Main Topic/Theme
        2. Key Points (3-5 bullet points)
        3. Important Details or Examples
        4. Conclusion/Takeaways

        Video Transcript:
        {transcript}

        Summary:
        """
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"An error occurred while generating the summary: {e}"

    def extract_key_points(self, transcript: str) -> List[str]:
        """
        Extracts key points from the video transcript.

        Args:
            transcript: The transcript of the YouTube video.

        Returns:
            A list of key points.
        """
        prompt = f"""
        Extract the key points from this YouTube video transcript.
        Return only the key points as a numbered list, one point per line.
        Focus on the most important information and insights.

        Video Transcript:
        {transcript}

        Key Points:
        """
        try:
            response = self.model.generate_content(prompt)
            # Parse the response to extract individual points
            points = response.text.strip().split('\n')
            return [point.strip() for point in points if point.strip()]
        except Exception as e:
            return [f"An error occurred while extracting key points: {e}"]

    def analyze_sentiment(self, transcript: str) -> Dict[str, str]:
        """
        Analyzes the sentiment and tone of the video.

        Args:
            transcript: The transcript of the YouTube video.

        Returns:
            A dictionary containing sentiment analysis results.
        """
        prompt = f"""
        Analyze the sentiment and tone of this YouTube video transcript.
        
        Provide your analysis in the following format:
        Overall Sentiment: [Positive/Negative/Neutral]
        Tone: [Professional/Casual/Educational/Entertainment/etc.]
        Emotional Appeal: [High/Medium/Low]
        Target Audience: [Description]

        Video Transcript:
        {transcript}

        Analysis:
        """
        try:
            response = self.model.generate_content(prompt)
            return {"analysis": response.text}
        except Exception as e:
            return {"analysis": f"An error occurred while analyzing sentiment: {e}"}

    def generate_tags(self, transcript: str) -> List[str]:
        """
        Generates relevant tags/keywords for the video.

        Args:
            transcript: The transcript of the YouTube video.

        Returns:
            A list of relevant tags.
        """
        prompt = f"""
        Generate relevant tags/keywords for this YouTube video based on its transcript.
        Return 10-15 relevant tags that capture the main topics, themes, and concepts.
        Separate each tag with a comma.

        Video Transcript:
        {transcript}

        Tags:
        """
        try:
            response = self.model.generate_content(prompt)
            # Parse the response to extract individual tags
            tags = [tag.strip() for tag in response.text.split(',')]
            return tags[:15]  # Limit to 15 tags
        except Exception as e:
            return [f"Error generating tags: {e}"]
