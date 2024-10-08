import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image

# Load the saved model
loaded_model = tf.keras.models.load_model('model.h5')

# Define the class names (replace with your actual class names)
class_names = ['Class 1', 'Class 2', 'Class 3', 'Class 4', 'Class 5', 
               'Class 6', 'Class 7', 'Class 8', 'Class 9', 'Class 10', 
               'Class 11', 'Class 12']

# Streamlit app starts here
st.title("Image Classification App")

# File uploader in Streamlit
uploaded_file = st.file_uploader("Upload an image for classification", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Read and display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image.', use_column_width=True)
    
    # Preprocess the image
    img = image.resize((224, 224))  # Resize image to match model's input
    img = np.array(img) / 255.0  # Normalize the image
    img = np.expand_dims(img, axis=0)  # Add batch dimension

    # Make predictions
    predictions = loaded_model.predict(img)
    
    # Get predicted class index
    predicted_class_idx = np.argmax(predictions, axis=1)[0] + 1
    predicted_class = class_names[predicted_class_idx]
    
    # Get the probability of the predicted class
    predicted_probability = np.max(predictions)

    # Prepare the final prediction based on class index
    final_pred = {}
    if predicted_class_idx in [1, 7, 5, 11, 12]:
        final_pred = {
            'predicted_class': 'metal/rubber/cotton',
            'predicted_probability': float(predicted_probability),
            'class_num': 1,
            'real_class': int(predicted_class_idx)
        }
    elif predicted_class_idx == 2:
        final_pred = {
            'predicted_class': 'biological',
            'predicted_probability': float(predicted_probability),
            'class_num': 2,
            'real_class': int(predicted_class_idx)
        }
    elif predicted_class_idx in [3, 4, 6, 8, 9, 10]:
        final_pred = {
            'predicted_class': 'plastic/glass/paper',
            'predicted_probability': float(predicted_probability),
            'class_num': 3,
            'real_class': int(predicted_class_idx)
        }

    # Display the result in Streamlit
    st.write("Prediction:", final_pred['predicted_class'])
    st.write("Confidence:", final_pred['predicted_probability'])
    st.write("Class Number:", final_pred['class_num'])
    st.write("Real Class Index:", final_pred['real_class'])
