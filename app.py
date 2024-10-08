from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
from PIL import Image
from io import BytesIO
from flask_cors import CORS
# Initialize Flask app
app = Flask(__name__)
CORS(app)
# Load the saved model
loaded_model = tf.keras.models.load_model('model.h5')

# Define the class names (replace with your actual class names)
class_names = ['Class 1', 'Class 2', 'Class 3', 'Class 4', 'Class 5', 
               'Class 6', 'Class 7', 'Class 8', 'Class 9', 'Class 10', 
               'Class 11', 'Class 12']

# Define route to receive image and return predictions
@app.route('/predict', methods=['POST','GET'])
def predict():
    try:
        # Receive image file
        file = request.files['image']
        
        # Read image
        img = Image.open(file.stream)
        
        # Preprocess image
        img = img.resize((224, 224))  # Resize image to match model's expected input size
        img = np.array(img) / 255.0  # Normalize pixel values to [0, 1]
        img = np.expand_dims(img, axis=0)  # Add batch dimension
        
        # Make predictions
        predictions = loaded_model.predict(img)
        
        # Get predicted class index (for multi-class classification)
        predicted_class_idx = np.argmax(predictions, axis=1)[0] +1
        predicted_class = class_names[predicted_class_idx]  # Get class name
        
        # Get the probability of the predicted class
        predicted_probability = np.max(predictions)
        
        # Prepare the final prediction based on class index
        final_pred = {}
        if predicted_class_idx in [1, 7, 5, 11, 12]:
            final_pred = {
                'predicted_class': 'metal /rubber/ cotton',   
                'predicted_probability': float(predicted_probability),
                'class_num': 1,
                'real_class':int(predicted_class_idx)
            }
        elif predicted_class_idx == 2:
            final_pred = {
                'predicted_class': 'biological',   
                'predicted_probability': float(predicted_probability),
                'class_num': 2,
                'real_class':int(predicted_class_idx)
            }
        elif predicted_class_idx in [3, 4, 6, 8, 9, 10]:
            final_pred = {
                'predicted_class': 'plastic/glass/paper',   
                'predicted_probability': float(predicted_probability),
                'class_num': 3,
                'real_class':int(predicted_class_idx)
            }

        # Return prediction and probability
        return jsonify(final_pred)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/a', methods=['GET'])
def pred():
    return "aaaaa"

# Run the app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', threaded=True)
