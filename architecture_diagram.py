import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, ConnectionPatch
import numpy as np

# Create figure and axis
fig, ax = plt.subplots(1, 1, figsize=(16, 12))
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis('off')

# Define colors
colors = {
    'ui': '#4CAF50',        # Green for UI
    'controller': '#2196F3',  # Blue for main controller
    'service': '#FF9800',    # Orange for services/utils
    'external': '#9C27B0',   # Purple for external APIs
    'data': '#607D8B'        # Blue-grey for data flow
}

# Title
ax.text(5, 9.5, 'YouTube Video Summarizer - System Architecture',
        fontsize=20, fontweight='bold', ha='center')

# 1. User Interface Layer (Streamlit)
ui_box = FancyBboxPatch((0.5, 7.5), 9, 1.2,
                        boxstyle="round,pad=0.1",
                        facecolor=colors['ui'],
                        edgecolor='black',
                        alpha=0.7)
ax.add_patch(ui_box)
ax.text(5, 8.1, 'Streamlit Web Interface (main.py)',
        fontsize=14, fontweight='bold', ha='center', color='white')
ax.text(5, 7.8, '• URL Input • Video Information Display • Transcript Viewer',
        fontsize=10, ha='center', color='white')

# 2. Main Controller/Orchestrator
controller_box = FancyBboxPatch((3, 6), 4, 1,
                                boxstyle="round,pad=0.1",
                                facecolor=colors['controller'],
                                edgecolor='black',
                                alpha=0.7)
ax.add_patch(controller_box)
ax.text(5, 6.5, 'Main Application Logic',
        fontsize=12, fontweight='bold', ha='center', color='white')
ax.text(5, 6.2, 'Coordinates all utility services',
        fontsize=10, ha='center', color='white')

# 3. Utility Services Layer
# URL Parser
parser_box = FancyBboxPatch((0.5, 4), 2.5, 1.5,
                            boxstyle="round,pad=0.1",
                            facecolor=colors['service'],
                            edgecolor='black',
                            alpha=0.7)
ax.add_patch(parser_box)
ax.text(1.75, 4.9, 'YouTubeParser',
        fontsize=11, fontweight='bold', ha='center', color='white')
ax.text(1.75, 4.6, 'youtube_url_parser.py',
        fontsize=9, ha='center', color='white')
ax.text(1.75, 4.3, '• Extract Video ID\n• Support multiple URL formats',
        fontsize=8, ha='center', color='white')

# Info Extractor
info_box = FancyBboxPatch((3.5, 4), 2.5, 1.5,
                          boxstyle="round,pad=0.1",
                          facecolor=colors['service'],
                          edgecolor='black',
                          alpha=0.7)
ax.add_patch(info_box)
ax.text(4.75, 4.9, 'YouTubeInfoExtractor',
        fontsize=11, fontweight='bold', ha='center', color='white')
ax.text(4.75, 4.6, 'youtube_info_extractor.py',
        fontsize=9, ha='center', color='white')
ax.text(4.75, 4.3, '• Video metadata\n• Uses yt-dlp library',
        fontsize=8, ha='center', color='white')

# Transcriber
transcriber_box = FancyBboxPatch((6.5, 4), 2.5, 1.5,
                                 boxstyle="round,pad=0.1",
                                 facecolor=colors['service'],
                                 edgecolor='black',
                                 alpha=0.7)
ax.add_patch(transcriber_box)
ax.text(7.75, 4.9, 'YouTubeTranscriber',
        fontsize=11, fontweight='bold', ha='center', color='white')
ax.text(7.75, 4.6, 'youtube_transcribe.py',
        fontsize=9, ha='center', color='white')
ax.text(7.75, 4.3, '• Multi-language support\n• Auto/Manual transcripts',
        fontsize=8, ha='center', color='white')

# 4. External APIs Layer
# YouTube API
youtube_api_box = FancyBboxPatch((1, 1.5), 2, 1.2,
                                 boxstyle="round,pad=0.1",
                                 facecolor=colors['external'],
                                 edgecolor='black',
                                 alpha=0.7)
ax.add_patch(youtube_api_box)
ax.text(2, 2.2, 'YouTube Data API',
        fontsize=11, fontweight='bold', ha='center', color='white')
ax.text(2, 1.9, '(via yt-dlp)',
        fontsize=9, ha='center', color='white')

# Transcript API
transcript_api_box = FancyBboxPatch((7, 1.5), 2, 1.2,
                                    boxstyle="round,pad=0.1",
                                    facecolor=colors['external'],
                                    edgecolor='black',
                                    alpha=0.7)
ax.add_patch(transcript_api_box)
ax.text(8, 2.2, 'YouTube Transcript API',
        fontsize=11, fontweight='bold', ha='center', color='white')
ax.text(8, 1.9, '(youtube-transcript-api)',
        fontsize=9, ha='center', color='white')

# 5. Data Flow Arrows
# UI to Controller
arrow1 = ConnectionPatch((5, 7.5), (5, 7), "data", "data",
                         arrowstyle="->", shrinkA=0, shrinkB=0,
                         mutation_scale=20, fc=colors['data'])
ax.add_patch(arrow1)

# Controller to Services
arrow2 = ConnectionPatch((4.5, 6), (1.75, 5.5), "data", "data",
                         arrowstyle="->", shrinkA=0, shrinkB=0,
                         mutation_scale=20, fc=colors['data'])
ax.add_patch(arrow2)

arrow3 = ConnectionPatch((5, 6), (4.75, 5.5), "data", "data",
                         arrowstyle="->", shrinkA=0, shrinkB=0,
                         mutation_scale=20, fc=colors['data'])
ax.add_patch(arrow3)

arrow4 = ConnectionPatch((5.5, 6), (7.75, 5.5), "data", "data",
                         arrowstyle="->", shrinkA=0, shrinkB=0,
                         mutation_scale=20, fc=colors['data'])
ax.add_patch(arrow4)

# Services to External APIs
arrow5 = ConnectionPatch((4.75, 4), (2.5, 2.7), "data", "data",
                         arrowstyle="->", shrinkA=0, shrinkB=0,
                         mutation_scale=20, fc=colors['data'])
ax.add_patch(arrow5)

arrow6 = ConnectionPatch((7.75, 4), (7.5, 2.7), "data", "data",
                         arrowstyle="->", shrinkA=0, shrinkB=0,
                         mutation_scale=20, fc=colors['data'])
ax.add_patch(arrow6)

# 6. Data Flow Description
ax.text(0.5, 0.8, 'Data Flow:', fontsize=12, fontweight='bold')
ax.text(0.5, 0.5, '1. User inputs YouTube URL', fontsize=10)
ax.text(0.5, 0.3, '2. URL parsed to extract video ID', fontsize=10)
ax.text(0.5, 0.1, '3. Video info & transcripts fetched in parallel', fontsize=10)

ax.text(5.5, 0.8, 'Key Features:', fontsize=12, fontweight='bold')
ax.text(5.5, 0.5, '• Multiple URL format support', fontsize=10)
ax.text(5.5, 0.3, '• Multi-language transcript extraction', fontsize=10)
ax.text(5.5, 0.1, '• Rich video metadata display', fontsize=10)

# 7. Legend
legend_elements = [
    mpatches.Patch(color=colors['ui'], label='User Interface'),
    mpatches.Patch(color=colors['controller'], label='Main Controller'),
    mpatches.Patch(color=colors['service'], label='Utility Services'),
    mpatches.Patch(color=colors['external'], label='External APIs'),
    mpatches.Patch(color=colors['data'], label='Data Flow')
]
ax.legend(handles=legend_elements, loc='upper right',
          bbox_to_anchor=(0.98, 0.98))

# Technology Stack Box
tech_box = FancyBboxPatch((0.2, 3), 1.8, 0.8,
                          boxstyle="round,pad=0.05",
                          facecolor='lightgray',
                          edgecolor='black',
                          alpha=0.8)
ax.add_patch(tech_box)
ax.text(1.1, 3.6, 'Tech Stack', fontsize=10, fontweight='bold', ha='center')
ax.text(1.1, 3.4, '• Streamlit', fontsize=8, ha='center')
ax.text(1.1, 3.25, '• yt-dlp', fontsize=8, ha='center')
ax.text(1.1, 3.1, '• youtube-transcript-api', fontsize=8, ha='center')

plt.tight_layout()
plt.savefig('d:/YT-summerizer/architecture_diagram.png',
            dpi=300, bbox_inches='tight')
plt.show()
