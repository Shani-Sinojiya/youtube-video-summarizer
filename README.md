# 🤖 YouTube Video Q&A Assistant

A powerful Streamlit-based web application that transforms YouTube videos into interactive Q&A sessions using AI. Extract transcripts, analyze content, and chat with your videos using Google's Gemini AI.

![Python](https://img.shields.io/badge/python-v3.12+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-v1.48+-red.svg)

## 🌟 Features

### 🎬 Video Processing

- **Multi-format URL Support**: Works with all YouTube URL formats (youtube.com, youtu.be, shorts, embed)
- **Comprehensive Video Info**: Extract title, duration, views, uploader, and metadata
- **Multi-language Transcripts**: Support for auto-generated and manual transcripts
- **Smart Parsing**: Robust URL validation and video ID extraction

### 🤖 AI-Powered Analysis

- **Interactive Q&A**: Ask questions about video content and get AI-powered answers
- **Intelligent Summarization**: Generate comprehensive video summaries
- **Context-Aware Responses**: AI understands video context for accurate answers
- **Chat History**: Keep track of your conversation with the video

### 🎨 Modern UI/UX

- **Chat Interface**: WhatsApp-style conversation bubbles
- **Dark/Light Theme**: Automatic theme detection with manual override
- **Responsive Design**: Works perfectly on desktop and mobile
- **Real-time Processing**: Live updates without page refresh

### ⚡ Quick Actions

- **Instant Questions**: Pre-built quick questions for immediate insights
- **Export Options**: Download transcripts and chat history
- **Full Video Analysis**: One-click comprehensive video breakdown
- **Settings Panel**: Customizable chat experience

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- Google API Key for Gemini AI ([Get yours here](https://aistudio.google.com/app/apikey))

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/Shani-Sinojiya/youtube-video-summarizer.git
   cd youtube-video-summarizer
   ```

2. **Install dependencies using uv (recommended)**

   ```bash
   # Install uv if you don't have it
   pip install uv

   # Install project dependencies
   uv sync
   ```

   Or use pip:

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**

   ```bash
   # Create .env file
   echo "GOOGLE_API_KEY=your_google_api_key_here" > .env
   ```

4. **Run the application**

   ```bash
   # Using uv
   uv run streamlit run main.py

   # Or using streamlit directly
   streamlit run main.py
   ```

5. **Open your browser**
   - Navigate to `http://localhost:8501`
   - Paste a YouTube URL and start chatting!

## 📖 Usage Guide

### Basic Workflow

1. **Enter YouTube URL**: Paste any YouTube video URL in the input field
2. **Process Video**: Click "Process" to extract transcript and metadata
3. **Ask Questions**: Use the chat interface to ask questions about the video
4. **Get AI Answers**: Receive intelligent, context-aware responses

### Advanced Features

#### Quick Questions

Use pre-built questions for instant insights:

- "What is this video about?"
- "Summarize the main points"
- "What are the key takeaways?"
- "Who is the target audience?"

#### Chat Settings

Customize your experience:

- **Theme Selection**: Auto, Light, or Dark mode
- **Chat History**: Set maximum conversation length
- **Timestamps**: Toggle timestamp display
- **Auto-scroll**: Keep latest messages in view

#### Export & Analysis

- **Export Chat**: Download your Q&A session
- **Full Analysis**: Generate comprehensive video breakdown
- **Clear History**: Start fresh conversations

## 🛠️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# Required
GOOGLE_API_KEY=your_google_api_key_here

# Optional
DEFAULT_MODEL=gemini-1.5-flash
```

### Supported Models

- `gemini-1.5-flash` (default, fast responses)
- `gemini-1.5-pro` (more detailed analysis)
- `gemini-pro` (legacy support)

## 📁 Project Structure

```
YT-summerizer/
├── main.py                          # Main Streamlit application
├── pyproject.toml                   # Project configuration
├── README.md                        # This file
├── ARCHITECTURE.md                  # Detailed architecture guide
├── .env                            # Environment variables
├── utils/                          # Core utilities
│   ├── youtube_url_parser.py       # URL parsing and validation
│   ├── youtube_info_extractor.py   # Video metadata extraction
│   ├── youtube_transcribe.py       # Transcript processing
│   └── youtube_analyzer.py         # AI analysis engine
└── __pycache__/                    # Python cache
```

## 🔧 API Reference

### Core Classes

#### `YouTubeParser`

```python
from utils.youtube_url_parser import YouTubeParser

parser = YouTubeParser("https://youtube.com/watch?v=VIDEO_ID")
video_id = parser.get_video_id()
```

#### `YouTubeInfoExtractor`

```python
from utils.youtube_info_extractor import YouTubeInfoExtractor

extractor = YouTubeInfoExtractor()
info = extractor.get_info("https://youtube.com/watch?v=VIDEO_ID")
```

#### `YouTubeTranscriber`

```python
from utils.youtube_transcribe import YouTubeTranscriber

transcriber = YouTubeTranscriber("VIDEO_ID")
transcripts = transcriber.get_all_transcripts()
```

#### `YouTubeAnalyzer`

```python
from utils.youtube_analyzer import YouTubeAnalyzer

analyzer = YouTubeAnalyzer("your_api_key")
answer = analyzer.ask_question(transcript, "What is this about?")
```

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes**: Follow the existing code style
4. **Add tests**: Ensure your changes work correctly
5. **Commit changes**: `git commit -m 'Add amazing feature'`
6. **Push to branch**: `git push origin feature/amazing-feature`
7. **Open a Pull Request**: Describe your changes

### Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/youtube-video-summarizer.git

# Install development dependencies
uv sync --dev

# Run tests
pytest

# Format code
black .
isort .
```

## 📋 Requirements

### Core Dependencies

- `streamlit>=1.48.1` - Web framework
- `youtube-transcript-api>=1.2.2` - Transcript extraction
- `google-generativeai>=0.5.4` - AI analysis
- `yt-dlp>=2025.8.27` - Video metadata
- `python-dotenv>=1.0.0` - Environment management

### Development Dependencies

- `pytest` - Testing framework
- `black` - Code formatting
- `isort` - Import sorting
- `flake8` - Linting

## 🐛 Troubleshooting

### Common Issues

**API Key Error**

```
❌ Please enter your Google API Key in the sidebar
```

- Solution: Set `GOOGLE_API_KEY` in your `.env` file

**No Transcripts Available**

```
❌ No transcripts available for this video
```

- Solution: Try a different video or check if captions are enabled

**Invalid YouTube URL**

```
❌ Invalid YouTube URL
```

- Solution: Ensure you're using a valid YouTube video URL

### Getting Help

1. **Check the [Issues](https://github.com/Shani-Sinojiya/youtube-video-summarizer/issues)** page
2. **Read the [Architecture Guide](ARCHITECTURE.md)** for technical details
3. **Create a new issue** with detailed error information

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Google AI** for the Gemini API
- **Streamlit** for the amazing web framework
- **YouTube Transcript API** for transcript access
- **yt-dlp** for reliable video data extraction

## 🔗 Links

- **Live Demo**: [Coming Soon]
- **Documentation**: [ARCHITECTURE.md](ARCHITECTURE.md)
- **Issues**: [GitHub Issues](https://github.com/Shani-Sinojiya/youtube-video-summarizer/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Shani-Sinojiya/youtube-video-summarizer/discussions)

---

**Made with ❤️ by [Shani Sinojiya](https://github.com/Shani-Sinojiya)**

_Transform any YouTube video into an interactive learning experience!_
