import streamlit as st
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import os
import sys
from contextlib import redirect_stdout
import io

# Define the directory path for stored files
dir_path = "tempDir"

# Ensure the directory exists
os.makedirs(dir_path, exist_ok=True)

def save_uploaded_file(uploaded_file):
    try:
        file_path = os.path.join(dir_path, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return file_path
    except Exception as e:
        st.error(f"Failed to save file: {e}")
        return None

def make_text_clip(text, start_time, end_time, style='Regular'):
    return TextClip(text, fontsize=66, font=f'Arial-{style}', color='white') \
        .set_position(('center', 'bottom')) \
        .set_start(start_time) \
        .set_duration(end_time - start_time) \
        .set_end(end_time) \
        .margin(bottom=50, opacity=0)

def process_video(video_path, text_lines, progress_bar):
    video = VideoFileClip(video_path)
    text_clips = [
        make_text_clip(
            text=text_lines[i]['text'],
            start_time=text_lines[i]['start'],
            end_time=text_lines[i]['end'],
            style=text_lines[i]['style']
        )
        for i in range(len(text_lines))
    ]
    final_clip = CompositeVideoClip([video, *text_clips])

    output_path = os.path.join(dir_path, f"output_{os.path.basename(video_path)}")

    # Capture stdout to parse for progress updates
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    
    try:
        final_clip.write_videofile(output_path, codec='libx264', verbose=True, logger=None)
        sys.stdout.seek(0)
        output = sys.stdout.read()
        progress_updates = [line for line in output.split('\n') if 'chunk:' in line]
        total_chunks = len(progress_updates)
        for i, update in enumerate(progress_updates):
            progress = (i + 1) / total_chunks
            progress_bar.progress(progress)
    finally:
        sys.stdout = old_stdout

    return output_path

st.title("Video Text Overlay App")

uploaded_file = st.file_uploader("Upload your video", type=['mp4'])
if uploaded_file is not None:
    video_path = save_uploaded_file(uploaded_file)
    if video_path:
        text_lines = [
            {'text': st.text_input(f"Text Line {i+1}", value=f"Text Line {i+1}"), 
             'start': st.number_input(f"Start Time for Line {i+1}", min_value=0, value=i*5), 
             'end': st.number_input(f"End Time for Line {i+1}", min_value=0, value=(i+1)*5),
             'style': st.selectbox(f"Style for Line {i+1}", options=['Regular', 'Bold', 'Italic'], index=0)}
            for i in range(4)
        ]

        if st.button("Create Video"):
            with st.spinner('Processing video...'):
                progress_bar = st.progress(0)
                output_video = process_video(video_path, text_lines, progress_bar)
                progress_bar.empty()
                st.video(output_video)
                st.download_button('Download Video', data=open(output_video, 'rb'), file_name='output_video.mp4')
    else:
        st.error("Failed to save uploaded video.")
else:
    st.warning("Please upload a video file.")

if st.button('Clean Temporary Files'):
    for f in os.listdir(dir_path):
        os.remove(os.path.join(dir_path, f))

