import streamlit as st
import pandas as pd
from datetime import datetime
from utils.youtube_url_parser import YouTubeParser
from utils.youtube_info_extractor import YouTubeInfoExtractor
from utils.youtube_transcribe import YouTubeTranscriber
import json

# Page configuration
st.set_page_config(
    page_title="YouTube Video Summarizer",
    page_icon="📺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #FF0000;
        text-align: center;
        margin-bottom: 2rem;
    }
    .video-info-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .transcript-container {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        max-height: 400px;
        overflow-y: auto;
    }
    .error-message {
        color: #ff4444;
        background-color: #ffe6e6;
        padding: 1rem;
        border-radius: 5px;
        border-left: 4px solid #ff4444;
    }
    .success-message {
        color: #00aa00;
        background-color: #e6ffe6;
        padding: 1rem;
        border-radius: 5px;
        border-left: 4px solid #00aa00;
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


def format_upload_date(date_str):
    """Format upload date from YYYYMMDD to readable format"""
    if not date_str:
        return "Unknown"

    try:
        date_obj = datetime.strptime(date_str, "%Y%m%d")
        return date_obj.strftime("%B %d, %Y")
    except:
        return date_str


def main():
    # Main title
    st.markdown('<h1 class="main-header">📺 YouTube Video Summarizer</h1>',
                unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.header("🎬 Video Information")
        st.markdown(
            "Enter a YouTube URL to extract video information and transcript.")

        # Note: Language selection removed - will automatically detect available languages

        # Additional options
        st.subheader("Options")
        show_raw_json = st.checkbox("Show raw video data", value=False)
        download_transcript = st.checkbox(
            "Enable transcript download", value=True)

    # Main content area
    col1, col2 = st.columns([2, 1])

    with col1:
        # URL input
        st.subheader("🔗 Enter YouTube URL")
        url_input = st.text_input(
            "YouTube URL:",
            placeholder="https://www.youtube.com/watch?v=...",
            help="Paste any YouTube video URL here"
        )

        # Process button
        process_button = st.button("🔍 Extract Information", type="primary")

    with col2:
        st.subheader("📋 Supported URL Formats")
        st.markdown("""
        - `youtube.com/watch?v=...`
        - `youtu.be/...`
        - `youtube.com/embed/...`
        - `youtube.com/shorts/...`
        """)

    # Process the URL when button is clicked
    if process_button and url_input:
        with st.spinner("🔄 Processing video..."):
            try:
                # Parse URL to get video ID
                parser = YouTubeParser(url_input)
                video_id = parser.get_video_id()

                if not video_id:
                    st.markdown(
                        '<div class="error-message">❌ Invalid YouTube URL. Please check the URL and try again.</div>', unsafe_allow_html=True)
                    st.stop()

                st.markdown(
                    f'<div class="success-message">✅ Successfully parsed video ID: {video_id}</div>', unsafe_allow_html=True)

                # Extract video information
                info_extractor = YouTubeInfoExtractor()
                video_info = info_extractor.get_info(url_input)

                # Display video information
                st.header("📊 Video Information")

                # Create columns for video info display
                info_col1, info_col2 = st.columns(2)

                with info_col1:
                    st.markdown('<div class="video-info-card">',
                                unsafe_allow_html=True)
                    st.subheader("📝 Basic Information")
                    st.write(f"**Title:** {video_info.get('title', 'N/A')}")
                    st.write(
                        f"**Channel:** {video_info.get('uploader', 'N/A')}")
                    st.write(
                        f"**Duration:** {format_duration(video_info.get('duration_seconds'))}")
                    st.write(
                        f"**Views:** {format_views(video_info.get('views'))}")
                    st.write(
                        f"**Upload Date:** {format_upload_date(video_info.get('upload_date'))}")
                    st.markdown('</div>', unsafe_allow_html=True)

                with info_col2:
                    # Display thumbnail if available
                    if video_info.get('thumbnail'):
                        st.subheader("🖼️ Thumbnail")
                        st.image(video_info['thumbnail'],  # type: ignore
                                 use_container_width=True)

                # Description
                if video_info.get('description'):
                    st.subheader("📄 Description")
                    with st.expander("View full description"):
                        st.write(video_info['description'])

                # Extract transcript
                st.header("📝 Video Transcript")

                try:
                    transcriber = YouTubeTranscriber(video_id)

                    # Get all available transcripts at once
                    all_transcripts = transcriber.get_all_transcripts()

                    if not all_transcripts:
                        st.warning(
                            "⚠️ No transcripts available for this video.")
                    else:
                        st.success(
                            f"✅ Transcripts extracted successfully! Available in {len(all_transcripts)} language(s)")

                        # Display available languages info
                        lang_info = []
                        for lang_code, transcript_info in all_transcripts.items():
                            lang_name = transcript_info.get(
                                'language', lang_code)
                            is_generated = transcript_info.get(
                                'is_generated', False)
                            status = " (Auto-generated)" if is_generated else " (Manual)"
                            lang_info.append(
                                f"{lang_name} ({lang_code}){status}")

                        st.info(f"Available languages: {', '.join(lang_info)}")

                        # Create tabs for each available language
                        tab_labels = []
                        for lang_code, transcript_info in all_transcripts.items():
                            lang_name = transcript_info.get(
                                'language', lang_code)
                            tab_labels.append(
                                f"{lang_name.title()} ({lang_code})")

                        language_tabs = st.tabs(tab_labels)

                        for i, (lang_code, transcript_info) in enumerate(all_transcripts.items()):
                            with language_tabs[i]:
                                transcript_data = transcript_info['data']
                                lang_name = transcript_info.get(
                                    'language', lang_code)
                                is_generated = transcript_info.get(
                                    'is_generated', False)

                                # Show transcript type
                                if is_generated:
                                    st.caption("🤖 Auto-generated transcript")
                                else:
                                    st.caption("✍️ Manual transcript")

                                # Process transcript data for this language
                                transcript_text = ""
                                transcript_df_data = []

                                for entry in transcript_data:
                                    # Handle both dictionary and object formats
                                    if isinstance(entry, dict):
                                        start_time = entry.get('start', 0)
                                        duration = entry.get('duration', 0)
                                        text = entry.get('text', '')
                                    else:
                                        # If it's an object, use attribute access
                                        start_time = getattr(entry, 'start', 0)
                                        duration = getattr(
                                            entry, 'duration', 0)
                                        text = getattr(entry, 'text', '')

                                    transcript_text += f"{text} "
                                    transcript_df_data.append({
                                        'Start Time': f"{int(start_time//60):02d}:{int(start_time % 60):02d}",
                                        'Duration': f"{duration:.1f}s",
                                        'Text': text
                                    })

                                # Display transcript in different formats for this language
                                inner_tab1, inner_tab2, inner_tab3 = st.tabs(
                                    ["📖 Readable Text", "📊 Timestamped Table", "💾 Download"])

                                with inner_tab1:
                                    st.markdown(
                                        '<div class="transcript-container">', unsafe_allow_html=True)
                                    st.write(transcript_text.strip())
                                    st.markdown(
                                        '</div>', unsafe_allow_html=True)

                                with inner_tab2:
                                    df = pd.DataFrame(transcript_df_data)
                                    st.dataframe(
                                        df, use_container_width=True, height=400)

                                with inner_tab3:
                                    if download_transcript:
                                        # Prepare download data for this language
                                        # Convert transcript objects to serializable dictionaries
                                        serializable_transcript = []
                                        for entry in transcript_data:
                                            if isinstance(entry, dict):
                                                serializable_transcript.append(
                                                    entry)
                                            else:
                                                # Convert FetchedTranscriptSnippet to dictionary
                                                entry_dict = {
                                                    'start': getattr(entry, 'start', 0),
                                                    'duration': getattr(entry, 'duration', 0),
                                                    'text': getattr(entry, 'text', '')
                                                }
                                                serializable_transcript.append(
                                                    entry_dict)

                                        transcript_json = json.dumps(
                                            serializable_transcript, indent=2)

                                        col_download1, col_download2 = st.columns(
                                            2)

                                        with col_download1:
                                            st.download_button(
                                                label=f"📥 Download {lang_code.upper()} as Text",
                                                data=transcript_text.strip(),
                                                file_name=f"{video_id}_transcript_{lang_code}.txt",
                                                mime="text/plain"
                                            )

                                        with col_download2:
                                            st.download_button(
                                                label=f"📥 Download {lang_code.upper()} as JSON",
                                                data=transcript_json,
                                                file_name=f"{video_id}_transcript_{lang_code}.json",
                                                mime="application/json"
                                            )

                except Exception as e:
                    st.error(f"❌ Error extracting transcript: {str(e)}")

                # Raw JSON data (optional)
                if show_raw_json:
                    st.header("🔧 Raw Video Data")
                    with st.expander("View raw JSON data"):
                        st.json(video_info)

            except Exception as e:
                st.markdown(
                    f'<div class="error-message">❌ Error processing video: {str(e)}</div>', unsafe_allow_html=True)

    elif process_button and not url_input:
        st.warning("⚠️ Please enter a YouTube URL before processing.")

    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666666;'>"
        "Built with ❤️ using Streamlit | YouTube Video Summarizer v1.0"
        "</div>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
