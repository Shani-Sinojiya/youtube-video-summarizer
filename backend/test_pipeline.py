from utils.youtube_info_extractor import YouTubeInfoExtractor
from utils.youtube_transcribe import YouTubeTranscriber

# Test the video processing pipeline
video_url = 'https://www.youtube.com/watch?v=HjPxiSEKilc'
video_id = 'HjPxiSEKilc'

print("Testing YouTube video processing pipeline...")
print(f"Video URL: {video_url}")
print("=" * 50)

# Test 1: Video Info Extraction
print("1. Testing video info extraction...")
try:
    extractor = YouTubeInfoExtractor()
    info = extractor.get_info(video_url)
    print(f"✅ Video info extraction successful!")
    print(f"   Title: {info.get('title')}")
    print(f"   Uploader: {info.get('uploader')}")
    print(f"   Duration: {info.get('duration_seconds')} seconds")
    print(f"   Views: {info.get('views')}")
except Exception as e:
    print(f"❌ Video info extraction failed: {e}")

print("\n" + "=" * 50)

# Test 2: Transcript Extraction
print("2. Testing transcript extraction...")
try:
    transcriber = YouTubeTranscriber(video_id)
    all_transcripts = transcriber.get_all_transcripts()
    print(f"✅ Transcript extraction successful!")
    print(f"   Available languages: {list(all_transcripts.keys())}")

    if all_transcripts:
        first_lang = list(all_transcripts.keys())[0]
        first_transcript = all_transcripts[first_lang]
        print(
            f"   Sample from '{first_lang}': {len(first_transcript)} segments")
        if first_transcript:
            print(f"   First segment: {first_transcript[0]}")
    else:
        print("   No transcripts available")

except Exception as e:
    print(f"❌ Transcript extraction failed: {e}")

print("\n" + "=" * 50)
print("Pipeline test completed!")
