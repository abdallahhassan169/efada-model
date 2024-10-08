import streamlit as st
from PIL import Image
import os
import json

# Set the title of the app
st.title("Image Upload and Processing App")

# Create a directory to save uploaded images if it doesn't exist
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# File uploader
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png", "gif"])

# Placeholder to display uploaded image
if uploaded_file is not None:
    # Open and display the image
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)

    # Save the image to the upload folder
    image_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
    image.save(image_path)
    
    st.success(f"Image saved successfully to {image_path}!")

    # Assuming you want to perform some processing on the image
    # Example: Return the image size as JSON
    image_size = {"width": image.size[0], "height": image.size[1]}
    st.json(image_size)

    # Use AJAX to send the image path or data
    if st.button("Process Image"):
        # This is where you'd normally send an AJAX request
        # Since Streamlit doesn't have traditional AJAX, we'll just simulate it
        response = {"status": "success", "message": "Image processed successfully!"}
        st.json(response)

# Optionally add a file download or other features as needed
