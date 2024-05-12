# Streamlit Video Text Overlay App

Transform your videos by adding customizable text overlays directly through a user-friendly web interface. This Streamlit app allows you to dynamically add text to your videos with ease, perfect for content creators, marketers, and anyone looking to enhance their video content without the complexity of traditional video editing software.

## Features

- **Drag-and-Drop Video Upload**: Easily upload your video files using a simple drag-and-drop interface.
- **Customizable Text Lines**: Add up to four lines of text overlays at specified times during your video.
- **Real-Time Video Processing**: See the changes you make with an in-app preview of your video.
- **Downloadable Output**: Download your modified video directly from the app.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Ensure you have Python installed on your system. The app is built with Python and uses several dependencies listed in the `requirements.txt` file.

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/pacnimo/video_text_overlay_app.git

2. Install the required packages:

pip install -r requirements.txt

3. give tempDir the requiered rules

   chmod 777 tempDir

4. Run the application:

streamlit run streamlit_app.py --server.enableCORS=false --server.enableXsrfProtection=false

### Usage

After launching the app, follow the on-screen instructions to upload a video, add text overlays, and process your video. The app provides intuitive controls for specifying the text content, start time, end time, and style for each line of text.

### Contributing

We welcome contributions from the community, whether it's improving the code, adding new features, or reporting bugs. Please feel free to fork the repository and submit pull requests.

### Future Enhancements

For reaching 10 stars, further features will be considered such as:
- Additional font selections
- Distance adjustments for text
- Additional text overlay customization options

Feel free to contribute to the code or suggest other features!

### License

This project is licensed under the Open Source Apache License 2.0.

### Acknowledgments

- Thanks to the Streamlit community for their continuous support and resources.
- MoviePy for providing the tools necessary for video processing.

Feel inspired? Star and fork this project to get started with your enhancements!


### Key Elements of the README

1. **Introduction**: Clearly states the purpose of the app and its target audience.
2. **Features**: Highlights the main functionalities that differentiate your app.
3. **Getting Started**: Provides step-by-step instructions on how to set up and run the application.
4. **Contributing**: Encourages community involvement and details the rewards for engagement (like new features for reaching star goals).
5. **License**: Clarifies the licensing under which the project is released, promoting freedom in usage and modifications.

This README should effectively guide any new users or developers through setting up and using your application, as well as inspire them to contribute to its future development.
