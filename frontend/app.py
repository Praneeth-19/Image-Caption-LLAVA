import streamlit as st
import requests
import json
from PIL import Image
import io

st.title("Image Caption Generator (LLaVA)")

uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Display the original image
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
        
    if st.button("Generate Caption"):
        # Resize and optimize the image
        image = Image.open(uploaded_file)
        max_size = (800, 800)  # Set a reasonable max size
        image.thumbnail(max_size, Image.LANCZOS)
        
        # Convert to JPEG format with compression
        buffer = io.BytesIO()
        image.save(buffer, format="JPEG", quality=85)
        optimized_image = buffer.getvalue()
        
        # Show loading indicator
        with st.spinner("Generating caption... This may take a minute for complex images."):
            # Send the optimized image
            files = {"file": optimized_image}
            try:
                res = requests.post("http://localhost:8000/caption/", files=files)
                
                if res.status_code == 200:
                    try:
                        response_data = res.json()
                        if "error" in response_data:
                            st.error(response_data["error"])
                        else:
                            caption = response_data.get("caption", "Error generating caption.")
                            st.subheader("Caption:")
                            st.write(caption)
                    except json.JSONDecodeError:
                        st.error(f"Received non-JSON response from server. Response text: {res.text[:100]}...")
                else:
                    st.error(f"Server returned status code {res.status_code}. Response: {res.text[:100]}...")
                    
            except requests.RequestException as e:
                st.error(f"Error connecting to the backend server: {str(e)}")
