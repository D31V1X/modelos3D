import streamlit as st
import os
from gallery import show_gallery
from generator import generate_3d_model
import tempfile
from PIL import Image

st.set_page_config(page_title="3D Magic Gallery", layout="wide")

st.title("✨ 3D Magic Gallery")
st.markdown("Upload a photo to create a 3D model, or browse your collection.")

# Directories
UPLOAD_DIR = "uploads"
OUTPUT_DIR = "output"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

tab1, tab2 = st.tabs(["🆕 Create New", "🖼️ Gallery"])

with tab1:
    st.header("Create new 3D Model")
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        col1, col2 = st.columns(2)
        with col1:
            st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
        
        with col2:
            st.write("Processing options...")
            if st.button("Generate 3D Model", type="primary"):
                with st.spinner('Magic is happening... This might take a minute!'):
                    try:
                        # Save temp file
                        temp_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
                        with open(temp_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())
                        
                        # Generate
                        model_path = generate_3d_model(temp_path, OUTPUT_DIR)
                        
                        st.success(f"Done! Model saved to {model_path}")
                        st.balloons()
                        
                        # Show result preview (if feasible in streamlit directly, or just link)
                        st.info("Go to the Gallery tab to view your new model!")
                        
                    except Exception as e:
                        st.error(f"Error generating model: {e}")

with tab2:
    show_gallery(OUTPUT_DIR)
