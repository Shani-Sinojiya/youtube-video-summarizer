# 📺 YouTube Video Summarizer

A powerful web application built with Streamlit that extracts comprehensive information and transcripts from YouTube videos. This tool allows you to analyze YouTube videos by extracting metadata, thumbnails, and full transcripts in multiple languages.

![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.48.1+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## ✨ Features

### 🔍 Video Information Extraction

- **Comprehensive Metadata**: Extract title, channel, duration, views, upload date
- **Thumbnail Display**: High-quality video thumbnails
- **Description Access**: Full video descriptions with expandable view
- **Multiple URL Formats**: Support for various YouTube URL formats

### 📝 Transcript Extraction

- **Multi-language Support**: Extract transcripts in 10+ languages (English, Spanish, French, German, Italian, Portuguese, Russian, Japanese, Korean, Chinese)
- **Multiple View Formats**:
  - Readable continuous text
  - Timestamped table format
  - Raw JSON data
- **Download Options**: Export transcripts as TXT or JSON files
- **Language Detection**: Automatic detection of available transcript languages

### 🎨 User Interface

- **Modern Design**: Clean, responsive Streamlit interface
- **Real-time Processing**: Live feedback during video processing
- **Error Handling**: Comprehensive error messages and validation
- **Customizable Options**: Toggle raw data view and download features

## 🚀 Supported URL Formats

The application supports all major YouTube URL formats:

- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://youtube.com/embed/VIDEO_ID`
- `https://youtube.com/v/VIDEO_ID`
- `https://youtube.com/shorts/VIDEO_ID`
- URLs with additional parameters (timestamps, playlists, etc.)

## 🛠️ Installation

### Prerequisites

- Python 3.12 or higher
- uv package manager (recommended) or pip

### Quick Start

1. **Clone the repository**

   ```bash
   git clone https://github.com/Shani-Sinojiya/youtube-video-summarizer.git
   cd youtube-video-summarizer
   ```

2. **Install dependencies**

   Using uv (recommended):

   ```bash
   uv sync
   ```

   Using pip:

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**

   ```bash
   streamlit run main.py
   ```

4. **Access the application**
   Open your browser and navigate to `http://localhost:8501`

## 📦 Dependencies

- **streamlit** (≥1.48.1) - Web application framework
- **pytube** (≥15.0.0) - YouTube video information extraction
- **youtube-transcript-api** (≥1.2.2) - Transcript extraction
- **pandas** - Data manipulation and analysis
- **yt-dlp** - Enhanced YouTube video information extraction

## 🔧 Project Structure

```
YT-summerizer/
├── main.py                          # Main Streamlit application
├── pyproject.toml                   # Project configuration and dependencies
├── uv.lock                          # Dependency lock file
├── README.md                        # Project documentation
├── testing.ipynb                    # Development and testing notebook
└── utils/                           # Utility modules
    ├── youtube_url_parser.py        # URL parsing and video ID extraction
    ├── youtube_info_extractor.py    # Video metadata extraction
    └── youtube_transcribe.py        # Transcript extraction and processing
```

## 💻 Usage

### Basic Usage

1. **Launch the application**

   ```bash
   streamlit run main.py
   ```

2. **Enter a YouTube URL**

   - Paste any valid YouTube URL in the input field
   - Select your preferred transcript language from the sidebar
   - Click "🔍 Extract Information"

3. **View Results**
   - Browse video information (title, channel, duration, views, etc.)
   - Read transcripts in multiple formats
   - Download transcripts as needed

### Advanced Options

- **Language Selection**: Choose from 10+ supported languages for transcript extraction
- **Raw Data View**: Enable to see complete JSON metadata
- **Download Options**: Export transcripts in TXT or JSON format
- **Error Handling**: Comprehensive error messages for troubleshooting

### Example URLs for Testing

```
https://www.youtube.com/watch?v=dQw4w9WgXcQ
https://youtu.be/dQw4w9WgXcQ
https://youtube.com/shorts/abc123def456
```

## 🔨 Development

### Setting up Development Environment

1. **Clone and setup**

   ```bash
   git clone https://github.com/Shani-Sinojiya/youtube-video-summarizer.git
   cd youtube-video-summarizer
   uv sync
   ```

2. **Run in development mode**
   ```bash
   streamlit run main.py --server.runOnSave true
   ```

### Testing

Use the included Jupyter notebook for testing and development:

```bash
jupyter notebook testing.ipynb
```

### Code Structure

- **`main.py`**: Streamlit web application with UI components
- **`utils/youtube_url_parser.py`**: Handles URL parsing and video ID extraction
- **`utils/youtube_info_extractor.py`**: Extracts video metadata using yt-dlp
- **`utils/youtube_transcribe.py`**: Manages transcript extraction and language handling

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🐛 Known Issues & Limitations

- Some videos may not have transcripts available in all languages
- Private or age-restricted videos cannot be processed
- Very long videos may take longer to process
- Transcript accuracy depends on YouTube's automatic captioning quality

## 🆘 Troubleshooting

### Common Issues

1. **"Invalid YouTube URL" Error**

   - Ensure the URL is a valid YouTube link
   - Check if the video is public and accessible

2. **"No transcript available" Warning**

   - Try a different language option
   - Some videos may not have transcripts

3. **Installation Issues**
   - Ensure Python 3.12+ is installed
   - Try using `uv sync` instead of pip install

### Getting Help

- Create an issue on GitHub for bugs or feature requests
- Check existing issues for solutions to common problems

## 🔮 Future Enhancements

- [ ] AI-powered video summarization
- [ ] Batch processing for multiple videos
- [ ] Export to more formats (PDF, DOCX)
- [ ] Transcript search and filtering
- [ ] Video chapter detection
- [ ] Integration with note-taking applications

## 👨‍💻 Author

**Shani Sinojiya**

- GitHub: [@Shani-Sinojiya](https://github.com/Shani-Sinojiya)

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io/) for the amazing web framework
- [pytube](https://github.com/pytube/pytube) for YouTube API integration
- [youtube-transcript-api](https://github.com/jdepoix/youtube-transcript-api) for transcript extraction
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) for enhanced video information extraction

---

<div align="center">
  <p>Built with ❤️ using Streamlit</p>
  <p>⭐ Star this repository if you find it helpful!</p>
</div>
