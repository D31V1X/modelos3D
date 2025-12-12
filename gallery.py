import streamlit as st
import os

def show_gallery(output_dir):
    st.header("My 3D Collection")
    
    files = [f for f in os.listdir(output_dir) if f.endswith(('.obj', '.glb', '.gltf'))]
    
    if not files:
        st.info("No models found yet. Go create one!")
        return

    # Create a grid
    cols = st.columns(3)
    for idx, file in enumerate(files):
        with cols[idx % 3]:
            st.markdown(f"**{file}**")
            # Streamlit 3D support is limited, we often use st.model or external components
            # For now, we'll provide a download button and a simple placeholder or use a 3rd party component if installed.
            # Ideally: st_model_viewer but that requires installing 'streamlit-3d-model-viewer' or similar.
            # We will default to a download button for V1.
            
            file_path = os.path.join(output_dir, file)
            with open(file_path, "rb") as f:
                st.download_button(
                    label="Download Model",
                    data=f,
                    file_name=file,
                    mime="model/gltf-binary" if file.endswith('.glb') else "application/octet-stream",
                    key=f"dl_{idx}"
                )
