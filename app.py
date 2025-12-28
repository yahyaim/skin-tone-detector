import streamlit as st
import cv2
import numpy as np
from PIL import Image

# Load face detector
face_cascade = cv2.CascadeClassifier(".venv/lib/python3.13/site-packages/cv2/data/haarcascade_frontalface_default.xml")

# -----------------------------
# Helper Functions
# -----------------------------
def get_brightness_feedback(brightness):
    if brightness < 80:
        return "💡 Too low"
    elif brightness > 180:
        return "☀️ Too harsh"
    else:
        return "👌 Good"

def get_skin_feedback(skin_uniformity):
    if skin_uniformity > 35:
        return "⚠️ Uneven"
    else:
        return "✨ Even"

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

    # -----------------------------
    # Display face
    # -----------------------------
    st.image(face, caption="Detected Face", width=300)

    # -----------------------------
    # Metrics in columns
    # -----------------------------
    col1, col2 = st.columns(2)
    col1.metric("Lighting Score", f"{brightness:.1f}", delta=get_brightness_feedback(brightness))
    col2.metric("Skin Tone Variation", f"{skin_uniformity:.1f}", delta=get_skin_feedback(skin_uniformity))

    # -----------------------------
    # Feedback messages
    # -----------------------------
    if brightness < 80:
        st.markdown("### ⚠️ Lighting is too low. Try natural daylight.")
    elif brightness > 180:
        st.markdown("### ☀️ Lighting is too harsh. Avoid direct sunlight.")
    else:
        st.markdown("### ✅ Lighting looks good!")

    if skin_uniformity > 35:
        st.markdown("### ⚠️ Some uneven skin tone detected. Could be shadows or pigmentation.")
    else:
        st.markdown("### ✅ Skin tone looks fairly even!")

    # -----------------------------
    # Skincare tips
    # -----------------------------
    with st.expander("💡 Skincare Photo Tips"):
        st.write("""
        - Use even lighting for selfies
        - Avoid harsh shadows
        - Natural daylight works best
        - Remove sunglasses or hats
        """)

# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="Skin Tone & Lighting Analyzer", layout="centered")

st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🧴 Skin Tone & Lighting Analyzer</h1>", unsafe_allow_html=True)
st.write("Analyze your selfie for lighting quality and skin tone uniformity. Choose your input mode from the sidebar.")

# Sidebar
st.sidebar.title("Settings")
mode = st.sidebar.radio("Choose input mode:", ["Upload Photo", "Live Webcam"])
st.sidebar.write("Use the webcam for live analysis or upload a selfie for quick results.")

# -----------------------------
# Handle modes
# -----------------------------
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
