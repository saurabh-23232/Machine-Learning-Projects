import streamlit as st
import cv2
import numpy as np
from keras.models import load_model
from PIL import Image
import io

# Load the pre-trained model
model = load_model('CNN__model.h5')
face_cascade = cv2.CascadeClassifier('haarcascade/haarcascade_frontalface_alt.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade/haarcascade_eye.xml')
leye_cascade = cv2.CascadeClassifier('haarcascade/haarcascade_lefteye_2splits.xml')
reye_cascade = cv2.CascadeClassifier('haarcascade/haarcascade_righteye_2splits.xml')

# Function to preprocess image
def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    eyes = eye_cascade.detectMultiScale(gray)
    left_eye = leye_cascade.detectMultiScale(gray)
    right_eye = reye_cascade.detectMultiScale(gray)
    
    rpred = None
    lpred = None
    
    for (x, y, w, h) in right_eye:
        r_eye = gray[y:y+h, x:x+w]
        r_eye = cv2.resize(r_eye, (100, 100)) / 255
        r_eye = r_eye.reshape(1, 100, 100, 1)
        rpred = (model.predict(r_eye) > 0.5).astype("int32")

    for (x, y, w, h) in left_eye:
        l_eye = gray[y:y+h, x:x+w]
        l_eye = cv2.resize(l_eye, (100, 100)) / 255
        l_eye = l_eye.reshape(1, 100, 100, 1)
        lpred = (model.predict(l_eye) > 0.5).astype("int32")

    if rpred is not None and lpred is not None:
        if rpred[0] == 0 and lpred[0] == 0:
            return "Closed"
        else:
            return "Open"
    return "Not Detected"

# Streamlit UI
st.title("Drowsiness Detection System")
option = st.sidebar.selectbox("Choose Option", ["Open Camera", "Upload Image"])

if option == "Upload Image":
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        image = np.array(image)
        
        # Process the image
        result = preprocess_image(image)
        
        st.image(image, caption='Uploaded Image', use_column_width=True)
        st.write(f"Detection Result: {result}")

elif option == "Open Camera":
    st.write("Click the button below to start the camera:")
    if st.button("Start Camera", key="start_camera"):
        st.write("Camera is opening...")
        
        # Use OpenCV to access the camera
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            st.write("Error: Unable to access the camera.")
        else:
            stframe = st.empty()
            stop_camera_button = st.button("Stop Camera", key="stop_camera")
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    st.write("Failed to capture image")
                    break
                
                # Process the frame
                result = preprocess_image(frame)
                
                # Convert the image to RGB for display
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                stframe.image(frame_rgb, channels="RGB", use_column_width=True)
                
                # Display detection result
                st.write(f"Detection Result: {result}")
                
                # Check if the user clicked "Stop Camera"
                if stop_camera_button:
                    break
            
            cap.release()
            cv2.destroyAllWindows()
