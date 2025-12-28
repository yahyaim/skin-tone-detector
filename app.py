import streamlit as st
import cv2
import numpy as np
from PIL import Image

# Load face detector
face_cascade = cv2.CascadeClassifier(".venv/lib/python3.13/site-packages/cv2/data/haarcascade_frontalface_default.xml")


st.title("🧴 Skin Tone & Lighting Analyzer")
st.write("Choose how you want to input your selfie:")

mode = st.radio("Choose input mode:", ["Upload Photo", "Live Webcam"])

def analyze_face(img):
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) == 0:
        st.error("No face detected. Please try again.")
        return

    x, y, w, h = faces[0]
    face = img[y:y+h, x:x+w]

    hsv = cv2.cvtColor(face, cv2.COLOR_RGB2HSV)
    h_channel, s_channel, v_channel = cv2.split(hsv)

    brightness = np.mean(v_channel)
    skin_uniformity = np.std(h_channel) + np.std(s_channel)

    st.image(face, caption="Detected Face", width=300)
    st.metric("Lighting Score", f"{brightness:.1f}")
    st.metric("Skin Tone Variation", f"{skin_uniformity:.1f}")

    # Feedback
    if brightness < 80:
        st.warning("Lighting is too low. Try natural daylight.")
    elif brightness > 180:
        st.warning("Lighting is too harsh. Avoid direct sunlight.")
    else:
        st.success("Lighting looks good 👍")

    if skin_uniformity > 35:
        st.info("Some uneven skin tone detected. Could be shadows or pigmentation.")
    else:
        st.success("Skin tone looks fairly even ✨")

# Handle modes
if mode == "Upload Photo":
    uploaded_file = st.file_uploader("Upload a selfie", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        image = Image.open(uploaded_file)
        img = np.array(image)
        analyze_face(img)

elif mode == "Live Webcam":
    camera_image = st.camera_input("Take a selfie")
    if camera_image:
        image = Image.open(camera_image)
        img = np.array(image)
        analyze_face(img)
