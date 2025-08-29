import streamlit as st
import pandas as pd
from datetime import datetime
from utils.youtube_url_parser import YouTubeParser
from utils.youtube_info_extractor import YouTubeInfoExtractor
from utils.youtube_transcribe import YouTubeTranscriber
from utils.youtube_analyzer import YouTubeAnalyzer
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="YouTube Video Q&A Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for chat-focused design with dark/light theme support
st.markdown("""
<style>
    /* Theme-aware variables */
    :root {
        --bg-primary: #ffffff;
        --bg-secondary: #f8f9fa;
        --bg-tertiary: #e9ecef;
        --text-primary: #212529;
        --text-secondary: #6c757d;
        --border-color: #dee2e6;
        --accent-blue: #007bff;
        --accent-green: #28a745;
        --accent-gray: #6c757d;
        --shadow-light: rgba(0, 0, 0, 0.1);
        --shadow-medium: rgba(0, 0, 0, 0.2);
    }
    
    /* Dark theme variables */
    [data-theme="dark"] {
        --bg-primary: #1a1d23;
        --bg-secondary: #2d3339;
        --bg-tertiary: #3a4047;
        --text-primary: #ffffff;
        --text-secondary: #adb5bd;
        --border-color: #495057;
        --accent-blue: #4dabf7;
        --accent-green: #51cf66;
        --accent-gray: #868e96;
        --shadow-light: rgba(0, 0, 0, 0.3);
        --shadow-medium: rgba(0, 0, 0, 0.5);
    }
    
    /* Auto-detect dark theme from Streamlit */
    @media (prefers-color-scheme: dark) {
        :root {
            --bg-primary: #1a1d23;
            --bg-secondary: #2d3339;
            --bg-tertiary: #3a4047;
            --text-primary: #ffffff;
            --text-secondary: #adb5bd;
            --border-color: #495057;
            --accent-blue: #4dabf7;
            --accent-green: #51cf66;
            --accent-gray: #868e96;
            --shadow-light: rgba(0, 0, 0, 0.3);
            --shadow-medium: rgba(0, 0, 0, 0.5);
        }
    }

    .main-header {
        font-size: 2.5rem;
        text-align: center;
        margin-bottom: 1rem;
        background: linear-gradient(45deg, var(--accent-blue), #ff7f0e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .chat-container {
        background: var(--bg-secondary);
        padding: 1.5rem;
        border-radius: 20px;
        margin: 1rem 0;
        min-height: 400px;
        max-height: 600px;
        overflow-y: auto;
        border: 2px solid var(--border-color);
        box-shadow: 0 4px 12px var(--shadow-light);
    }
    
    .question-bubble {
        background: linear-gradient(135deg, var(--accent-blue) 0%, #0056b3 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 20px 20px 5px 20px;
        margin: 0.8rem 0 0.8rem 20%;
        box-shadow: 0 4px 12px rgba(77, 171, 247, 0.3);
        animation: slideInRight 0.3s ease-out;
        position: relative;
    }
    
    .answer-bubble {
        background: linear-gradient(135deg, var(--accent-green) 0%, #1e7e34 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 20px 20px 20px 5px;
        margin: 0.8rem 20% 0.8rem 0;
        box-shadow: 0 4px 12px rgba(81, 207, 102, 0.3);
        animation: slideInLeft 0.3s ease-out;
        position: relative;
    }
    
    .video-info-compact {
        background: linear-gradient(135deg, var(--accent-gray) 0%, var(--bg-tertiary) 100%);
        color: var(--text-primary);
        padding: 1rem;
        border-radius: 15px;
        margin: 1rem 0;
        display: flex;
        align-items: center;
        gap: 1rem;
        border: 1px solid var(--border-color);
        box-shadow: 0 2px 8px var(--shadow-light);
    }
    
    .chat-input-area {
        background: var(--bg-primary);
        padding: 1.5rem;
        border-radius: 20px;
        border: 2px solid var(--accent-blue);
        margin: 1rem 0;
        box-shadow: 0 4px 12px var(--shadow-light);
    }
    
    .url-input-compact {
        background: var(--bg-secondary);
        padding: 1rem;
        border-radius: 15px;
        margin-bottom: 1rem;
        border: 1px solid var(--accent-blue);
        box-shadow: 0 2px 8px var(--shadow-light);
    }
    
    .welcome-section {
        background: linear-gradient(135deg, var(--bg-secondary) 0%, var(--bg-tertiary) 100%);
        color: var(--text-primary);
        padding: 3rem;
        border-radius: 20px;
        margin: 2rem 0;
        text-align: center;
        border: 1px solid var(--border-color);
        box-shadow: 0 4px 16px var(--shadow-light);
    }
    
    .welcome-section h2 {
        color: var(--text-primary);
        margin-bottom: 1rem;
    }
    
    .welcome-section h4 {
        color: var(--accent-blue);
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    
    .welcome-section p {
        color: var(--text-secondary);
        font-size: 1.1rem;
        line-height: 1.6;
    }
    
    .chat-empty-state {
        text-align: center;
        padding: 2rem;
        color: var(--text-secondary);
        background: var(--bg-secondary);
        border-radius: 15px;
        border: 2px dashed var(--border-color);
        margin: 1rem 0;
    }
    
    .status-indicator {
        padding: 0.5rem 1rem;
        border-radius: 25px;
        font-size: 0.85rem;
        margin: 0.5rem 0;
        text-align: center;
        border: 1px solid var(--border-color);
    }
    
    .status-success {
        background: rgba(81, 207, 102, 0.1);
        color: var(--accent-green);
        border-color: var(--accent-green);
    }
    
    .status-processing {
        background: rgba(255, 193, 7, 0.1);
        color: #ffc107;
        border-color: #ffc107;
    }
    
    /* Button styling improvements */
    .stButton > button {
        border-radius: 25px !important;
        border: none !important;
        padding: 0.5rem 2rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        background: var(--accent-blue) !important;
        color: white !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px var(--shadow-medium) !important;
        filter: brightness(110%) !important;
    }
    
    /* Text input styling */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background-color: var(--bg-primary) !important;
        color: var(--text-primary) !important;
        border-color: var(--border-color) !important;
        border-radius: 15px !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--accent-blue) !important;
        box-shadow: 0 0 0 0.2rem rgba(77, 171, 247, 0.25) !important;
    }
    
    /* Footer styling */
    .footer-section {
        text-align: center;
        color: var(--text-secondary);
        padding: 1rem;
        background: var(--bg-secondary);
        border-radius: 15px;
        margin-top: 2rem;
        border: 1px solid var(--border-color);
    }
    
    .timestamp {
        font-size: 0.75rem;
        opacity: 0.8;
        margin-top: 0.5rem;
    }
    
    @keyframes slideInRight {
        from { transform: translateX(20px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    @keyframes slideInLeft {
        from { transform: translateX(-20px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    @keyframes slideInRight {
        from { transform: translateX(20px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    @keyframes slideInLeft {
        from { transform: translateX(-20px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    .timestamp {
        font-size: 0.75rem;
        opacity: 0.8;
        margin-top: 0.5rem;
    }
    .status-indicator {
        padding: 0.5rem 1rem;
        border-radius: 25px;
        font-size: 0.85rem;
        margin: 0.5rem 0;
        text-align: center;
    }
    .status-success {
        background: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
    }
    .status-processing {
        background: #fff3cd;
        color: #856404;
        border: 1px solid #ffeaa7;
    }
    .stButton > button {
        border-radius: 25px !important;
        border: none !important;
        padding: 0.5rem 2rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2) !important;
    }
</style>
""", unsafe_allow_html=True)


def format_duration(seconds):
    """Convert seconds to HH:MM:SS format"""
    if not seconds:
        return "Unknown"
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    else:
        return f"{minutes:02d}:{seconds:02d}"


def format_views(views):
    """Format view count in a readable format"""
    if not views:
        return "Unknown"
    if views >= 1_000_000:
        return f"{views / 1_000_000:.1f}M views"
    elif views >= 1_000:
        return f"{views / 1_000:.1f}K views"
    else:
        return f"{views} views"


def display_chat_history():
    """Display chat history in a chat-like interface"""
    if not st.session_state.qa_history:
        st.markdown("""
        <div class="chat-empty-state">
            <h4>💬 Start Your Conversation</h4>
            <p>Ask your first question about the video to begin!</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    for qa in st.session_state.qa_history:
        # Question bubble
        st.markdown(f"""
        <div class="question-bubble">
            <strong>You asked:</strong><br>
            {qa['question']}
            <div class="timestamp">🕒 {qa['timestamp']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Answer bubble
        st.markdown(f"""
        <div class="answer-bubble">
            <strong>AI Assistant:</strong><br>
            {qa['answer']}
            <div class="timestamp">🤖 Answered at {qa['timestamp']}</div>
        </div>
        """, unsafe_allow_html=True)


def main():
    # Main title
    st.markdown('<h1 class="main-header">🤖 YouTube Video Q&A Chat</h1>', unsafe_allow_html=True)
    
    # Sidebar configuration
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # Theme selection
        st.subheader("🎨 Theme")
        theme_option = st.radio(
            "Choose theme:",
            ["Auto (Follow System)", "Light Theme", "Dark Theme"],
            index=0
        )
        
        # Apply theme based on selection
        if theme_option == "Dark Theme":
            st.markdown('<style>:root { color-scheme: dark; }</style>', unsafe_allow_html=True)
        elif theme_option == "Light Theme":
            st.markdown('<style>:root { color-scheme: light; }</style>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # API key input with environment variable support
        st.subheader("🔑 API Key")
        env_api_key = os.getenv('GOOGLE_API_KEY')
        
        if env_api_key and env_api_key != 'your_google_api_key_here':
            st.success("✅ API Key loaded from .env file")
            api_key = env_api_key
        else:
            api_key = st.text_input("Enter your Google API Key:", type="password")
            if not api_key:
                st.warning("⚠️ No API key found")
                st.markdown("[Get your key here](https://aistudio.google.com/app/apikey)")
        
        st.markdown("---")
        
        # Chat settings
        st.subheader("💬 Chat Settings")
        auto_scroll = st.checkbox("Auto-scroll to latest", value=True)
        show_timestamps = st.checkbox("Show timestamps", value=True)
        max_history = st.slider("Max chat history", 5, 50, 20)
        
        # Clear chat button
        if st.button("🗑️ Clear Chat History", use_container_width=True):
            st.session_state.qa_history = []
            st.rerun()

    # Initialize session state
    if 'qa_history' not in st.session_state:
        st.session_state.qa_history = []
    if 'current_video_id' not in st.session_state:
        st.session_state.current_video_id = None
    if 'current_transcript' not in st.session_state:
        st.session_state.current_transcript = ""
    if 'video_processed' not in st.session_state:
        st.session_state.video_processed = False
    if 'current_video_info' not in st.session_state:
        st.session_state.current_video_info = {}

    # Compact URL input section
    st.markdown('<div class="url-input-compact">', unsafe_allow_html=True)
    col_url, col_btn = st.columns([4, 1])
    
    with col_url:
        url_input = st.text_input(
            "🔗 YouTube URL:",
            placeholder="Paste YouTube video URL here...",
            key="url_input"
        )
    
    with col_btn:
        st.markdown("<br>", unsafe_allow_html=True)
        process_btn = st.button("🎬 Process", type="primary", use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

    # Video processing
    if process_btn and url_input:
        if not api_key:
            st.error("❌ Please enter your Google API Key in the sidebar")
        else:
            with st.spinner("🔄 Processing video..."):
                try:
                    # Parse URL
                    parser = YouTubeParser(url_input)
                    video_id = parser.get_video_id()
                    
                    if not video_id:
                        st.error("❌ Invalid YouTube URL")
                    else:
                        # Extract video info
                        info_extractor = YouTubeInfoExtractor()
                        video_info = info_extractor.get_info(url_input)
                        st.session_state.current_video_info = video_info
                        
                        # Extract transcript
                        transcriber = YouTubeTranscriber(video_id)
                        all_transcripts = transcriber.get_all_transcripts()
                        
                        if all_transcripts:
                            # Get the first available transcript
                            first_lang = list(all_transcripts.keys())[0]
                            transcript_data = all_transcripts[first_lang]['data']
                            
                            transcript_text = ""
                            for entry in transcript_data:
                                if isinstance(entry, dict):
                                    text = entry.get('text', '')
                                else:
                                    text = getattr(entry, 'text', '')
                                transcript_text += f"{text} "
                            
                            st.session_state.current_transcript = transcript_text.strip()
                            st.session_state.current_video_id = video_id
                            st.session_state.video_processed = True
                            
                            st.success("✅ Video processed successfully!")
                        else:
                            st.error("❌ No transcripts available for this video")
                            
                except Exception as e:
                    st.error(f"❌ Error processing video: {str(e)}")

    # Display current video info (compact)
    if st.session_state.video_processed and st.session_state.current_video_info:
        video_info = st.session_state.current_video_info
        title = video_info.get('title', 'Unknown Title') or 'Unknown Title'
        st.markdown(f"""
        <div class="video-info-compact">
            <div>
                <strong>{title[:60]}{'...' if len(title) > 60 else ''}</strong><br>
                <small>{video_info.get('uploader', 'Unknown')} • {format_duration(video_info.get('duration_seconds'))} • {format_views(video_info.get('views'))}</small>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Main chat interface
    if st.session_state.video_processed and api_key:
        # Chat container
        st.markdown("### 💬 Chat with Your Video")
        
        # Display chat history
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        display_chat_history()
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Chat input area
        st.markdown('<div class="chat-input-area">', unsafe_allow_html=True)
        
        # Quick questions
        quick_questions = [
            "What is this video about?",
            "Summarize the main points",
            "What are the key takeaways?",
            "Who is the target audience?",
            "What examples are mentioned?"
        ]
        
        selected_quick = st.selectbox(
            "💡 Quick Questions:",
            ["Choose a quick question..."] + quick_questions,
            key="quick_select"
        )
        
        # Question input
        col_input, col_send = st.columns([4, 1])
        
        with col_input:
            if selected_quick != "Choose a quick question...":
                question = st.text_area(
                    "Your question:",
                    value=selected_quick,
                    height=80,
                    key="question_input"
                )
            else:
                question = st.text_area(
                    "Your question:",
                    placeholder="Type your question about the video...",
                    height=80,
                    key="question_input_manual"
                )
        
        with col_send:
            st.markdown("<br>", unsafe_allow_html=True)
            ask_btn = st.button("💬 Ask", type="primary", use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Process question without page refresh
        if ask_btn and question and question.strip():
            with st.spinner("🤔 AI is thinking..."):
                try:
                    analyzer = YouTubeAnalyzer(api_key)
                    answer = analyzer.ask_question(st.session_state.current_transcript, question.strip())
                    
                    # Add to history
                    qa_entry = {
                        "question": question.strip(),
                        "answer": answer,
                        "timestamp": datetime.now().strftime("%H:%M:%S")
                    }
                    st.session_state.qa_history.append(qa_entry)
                    
                    # Keep only recent history
                    if len(st.session_state.qa_history) > max_history:
                        st.session_state.qa_history = st.session_state.qa_history[-max_history:]
                    
                    # Force refresh to show new Q&A
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
        
        elif ask_btn and not question.strip():
            st.warning("⚠️ Please enter a question")

    elif not st.session_state.video_processed:
        # Welcome message with theme-aware styling
        st.markdown("""
        <div class="welcome-section">
            <h2>🎬 Welcome to YouTube Video Q&A Chat!</h2>
            <p>Paste a YouTube URL above to start chatting with your video</p>
            <div>
                <h4>🌟 What you can do:</h4>
                <p>✨ Ask any question about the video content<br>
                💬 Get instant AI-powered answers<br>
                📱 Enjoy a chat-like experience<br>
                🔄 Keep track of your conversation history</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    elif not api_key:
        st.info("🔑 Please enter your Google API Key in the sidebar to start chatting")

    # Export chat history
    if st.session_state.qa_history:
        st.markdown("---")
        col_export1, col_export2 = st.columns(2)
        
        with col_export1:
            chat_export = "\n\n".join([
                f"🙋 You: {qa['question']}\n🤖 AI: {qa['answer']}\n⏰ Time: {qa['timestamp']}"
                for qa in st.session_state.qa_history
            ])
            st.download_button(
                "📥 Export Chat History",
                chat_export,
                f"chat_history_{st.session_state.current_video_id or 'session'}.txt",
                mime="text/plain",
                use_container_width=True
            )
        
        with col_export2:
            if st.button("🔄 Analyze Full Video", use_container_width=True):
                if api_key and st.session_state.current_transcript:
                    with st.spinner("📊 Generating video analysis..."):
                        try:
                            analyzer = YouTubeAnalyzer(api_key)
                            summary = analyzer.summarize_video(st.session_state.current_transcript)
                            
                            # Add summary as special Q&A entry
                            qa_entry = {
                                "question": "📊 Full Video Analysis (Auto-generated)",
                                "answer": summary,
                                "timestamp": datetime.now().strftime("%H:%M:%S")
                            }
                            st.session_state.qa_history.append(qa_entry)
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Error generating analysis: {str(e)}")

    # Footer
    st.markdown("---")
    st.markdown("""
        <div class="footer-section">
            🤖 YouTube Video Q&A Chat Assistant | Built with ❤️ using Streamlit & Google AI
        </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
