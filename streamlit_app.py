import streamlit as st
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
from io import BytesIO

def make_text_clip(text, start_time, end_time):
    # Ensure default parameters are adjusted as needed.
    return TextClip(txt=text, fontsize=66, color='white', font="Amiri-Bold", size=(960, 540)) \
        .set_position('center').set_start(start_time) \
        .set_duration(end_time - start_time).margin(bottom=50)

def process_video(video_clip, text_lines):
    # Create text clips and add to video
    text_clips = [make_text_clip(line['text'], line['start'], line['end']) for line in text_lines]
    final_clip = CompositeVideoClip([video_clip, *text_clips])
    return final_clip

st.title("Video Text Overlay App")

uploaded_file = st.file_uploader("Upload your video", type=['mp4'])
if uploaded_file is not None:
    video_bytes = uploaded_file.read()  # Read the uploaded file into bytes
    video_clip = VideoFileClip(BytesIO(video_bytes))  # Create a VideoFileClip object from bytes
    text_lines = [
        {'text': st.text_input(f"Text Line {i+1}", value=f"Text Line {i+1}"),
         'start': st.number_input(f"Start Time for Line {i+1}", min_value=0, value=i*5),
         'end': st.number_input(f"End Time for Line {i+1}", min_value=0, value=(i+1)*5)}
        for i in range(4)  # Configure for up to 4 lines of text
    ]

    if st.button("Create Video"):
        with st.spinner('Processing video...'):
            final_video = process_video(video_clip, text_lines)
            output_video_io = BytesIO()
            final_video.write_videofile(output_video_io, codec="libx264", temp_audiofile='temp-audio.m4a', remove_temp=True, audio_codec='aac')
            output_video_io.seek(0)  # Rewind to beginning of file
            st.video(output_video_io)
            output_video_io.seek(0)  # Rewind again for download button
            st.download_button('Download Video', data=output_video_io, file_name='output_video.mp4', mime='video/mp4')
else:
    st.warning("Please upload a video file.")
