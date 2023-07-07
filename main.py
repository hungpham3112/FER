import streamlit as st
import cv2
from PIL import Image
import numpy as np
from keras.models import model_from_json
from lib import detect_expression

# Load pre-trained facial expression recognition model
# (Assuming you have a pre-trained model stored as 'model.h5')
json_file = open('./model/emotion_model1.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
model = model_from_json(loaded_model_json)

# load weights into new model
model.load_weights("./model/emotion_model1.h5")

# Define class labels for facial expressions
class_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

    
def main():
    st.title("Facial Expression Recognition")

    option = st.sidebar.selectbox(
        "Choose an option to detect and classify facial expressions.",
        ("Built-in Webcam", "External Camera", "Image or Video")
    )

    if option == "Built-in Webcam":
        video_capture = cv2.VideoCapture(0)
        if not video_capture.isOpened():
            st.error("Failed to recognize built-in camera. Please choose other options.")
        else:
            while True:
                ret, frame = video_capture.read()
                frame = detect_expression(frame)
                st.image(frame, channels="BGR", caption="Facial Expression Recognition")

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            video_capture.release()
            cv2.destroyAllWindows()

    elif option == "External Camera":
        camera_address = st.text_input("Camera Address (e.g: http://192.168.137.101:4747/video )")
        if camera_address:
            vid = cv2.VideoCapture(camera_address)
            st.title( 'Using Mobile Camera with Streamlit' )
            frame_window = st.image( [] )

            while True:
                got_frame , frame = vid.read()
                frame = cv2.cvtColor(frame , cv2.COLOR_BGR2RGB)
                if got_frame:
                    #  frame_window.image(detect_expression(frame))
                    frame_window.image(frame)

    elif option == "Image or Video":
        uploaded_file = st.file_uploader("Choose an image or video file", type=["jpg", "jpeg", "png", "mp4"])
        if uploaded_file is not None:
            file_extension = uploaded_file.name.split(".")[-1]
            if file_extension in ["jpg", "jpeg", "png"]:
                image = Image.open(uploaded_file)
                image = np.array(image.convert("RGB"))
                image = detect_expression(image)
                st.image(image, channels="RGB", caption="Processed Image")
            elif file_extension == "mp4":
                st.warning("Video playback is not supported in the current version.")
                # Add your code here to process the video file

if __name__ == "__main__":
    main()
