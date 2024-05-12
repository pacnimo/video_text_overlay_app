import tempfile  # Make sure to include this import at the top of your script
import streamlit as st
import numpy as np
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

def process_video(video_file_path, text_lines):
    video_clip = VideoFileClip(video_file_path)
    text_clips = [TextClip(txt=line['text'], fontsize=66, color='white').set_position('center').set_start(line['start']).set_duration(line['end'] - line['start']).margin(bottom=50) for line in text_lines]
    final_clip = CompositeVideoClip([video_clip, *text_clips])
    return final_clip

st.title("Video Text Overlay App")

uploaded_file = st.file_uploader("Upload your video", type=['mp4'])

# Only proceed if a file has been uploaded
if uploaded_file is not None:
    video_file_path = uploaded_file  # Assuming you have already handled the temporary file issue
    text_lines = [
        {'text': st.text_input(f"Text Line {i+1}", value=f"Text Line {i+1}"),
         'start': st.number_input(f"Start Time for Line {i+1}", min_value=0, value=i*5),
         'end': st.number_input(f"End Time for Line {i+1}", min_value=0, value=(i+1)*5)}
        for i in range(4)  # Up to 4 lines of text
    ]

    if st.button("Create Video"):
        with st.spinner('Processing video...'):
            final_video = process_video(video_file_path, text_lines)
            output_video_path = "output_video.mp4"
            final_video.write_videofile(output_video_path, codec="libx264")
            st.video(output_video_path)
            st.download_button('Download Video', open(output_video_path, 'rb').read(), file_name='output_video.mp4')
else:
    st.warning("Please upload a video file.")
