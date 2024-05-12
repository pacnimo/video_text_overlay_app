import streamlit as st
from moviepy.editor import VideoFileClip, CompositeVideoClip, TextClip
import tempfile
import os

def make_text_clip(text, start_time, end_time):
    # Use simple TextClip without advanced formatting
    return TextClip(txt=text, fontsize=24, color='white', font="Arial") \
        .set_position('center').set_start(start_time) \
        .set_duration(end_time - start_time).margin(bottom=50)

def process_video(video_file_path, text_lines):
    # Ensure the video file path exists
    if not video_file_path or not os.path.exists(video_file_path):
        raise ValueError(f"Invalid video file path: {video_file_path}")
    
    video_clip = VideoFileClip(video_file_path)
    text_clips = [make_text_clip(line['text'], line['start'], line['end']) for line in text_lines]
    final_clip = CompositeVideoClip([video_clip, *text_clips])
    return final_clip

st.title("Video Text Overlay App")

uploaded_file = st.file_uploader("Upload your video", type=['mp4'])
if uploaded_file is not None:
    # Save the uploaded file to a temporary file and ensure it's written completely
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmpfile:
        tmpfile.write(uploaded_file.read())
        tmpfile.flush()  # Ensure all data is written to disk
        video_file_path = tmpfile.name

    st.write("Debug: Temporary file created at", video_file_path)  # Debug output

    text_lines = [
        {'text': st.text_input(f"Text Line {i+1}", value=f"Text Line {i+1}"),
         'start': st.number_input(f"Start Time for Line {i+1}", min_value=0, value=i*5),
         'end': st.number_input(f"End Time for Line {i+1}", min_value=0, value=(i+1)*5)}
        for i in range(4)
    ]

    if st.button("Create Video"):
        try:
            final_video = process_video(video_file_path, text_lines)
            output_video_path = "output_video.mp4"
            final_video.write_videofile(output_video_path, codec="libx264")
            st.video(output_video_path)
            with open(output_video_path, 'rb') as file:
                st.download_button('Download Video', file.read(), file_name='output_video.mp4')
            os.remove(video_file_path)  # Clean up the temporary file
        except Exception as e:
            st.error(f"Failed to process video: {e}")
else:
    st.warning("Please upload a video file.")
