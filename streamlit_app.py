import streamlit as st
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import os
import tempfile

def make_text_clip(text, start_time, end_time):
    return TextClip(txt=text, fontsize=66, color='white', font='Arial') \
        .set_position('center').set_start(start_time) \
        .set_duration(end_time - start_time).margin(bottom=50)

def process_video(video_file_path, text_lines):
    video_clip = VideoFileClip(video_file_path)  # Use file path
    text_clips = [make_text_clip(line['text'], line['start'], line['end']) for line in text_lines]
    final_clip = CompositeVideoClip([video_clip, *text_clips])
    return final_clip

st.title("Video Text Overlay App")

uploaded_file = st.file_uploader("Upload your video", type=['mp4'])
if uploaded_file is not None:
    # Save uploaded file to a temporary directory
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmpfile:
        tmpfile.write(uploaded_file.getvalue())
        video_file_path = tmpfile.name

    text_lines = [
        {'text': st.text_input(f"Text Line {i+1}", value=f"Text Line {i+1}"),
         'start': st.number_input(f"Start Time for Line {i+1}", min_value=0, value=i*5),
         'end': st.number_input(f"End Time for Line {i+1}", min_value=0, value=(i+1)*5)}
        for i in range(4)  # Assuming up to 4 lines of text
    ]

    if st.button("Create Video"):
        with st.spinner('Processing video...'):
            final_video = process_video(video_file_path, text_lines)
            output_video_path = "output_video.mp4"
            final_video.write_videofile(output_video_path, codec="libx264")
            st.video(output_video_path)
            with open(output_video_path, 'rb') as file:
                st.download_button('Download Video', file.read(), file_name='output_video.mp4')
            # Optionally, clean up the temporary file
            os.remove(video_file_path)
else:
    st.warning("Please upload a video file.")
