from flask import Flask, render_template, request
import joblib
import numpy as np
from config.paths_config import *

app = Flask(__name__)

# Load model and scaler
model_path = MODEL_SAVED_PATH
scaler_path = SCALER_PATH

model = joblib.load(model_path)
scaler = joblib.load(scaler_path)

# Label Mapping
LABELS = {0: "High", 1: "Low", 2: "Medium"}

@app.route("/", methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        # Extract form data
        error_rate = float(request.form["error_rate"])
        production_speed = float(request.form["production_speed"])

        # Prepare input for model (scaled)
        input_data = np.array([[error_rate, production_speed]])
        input_scaled = scaler.transform(input_data)

        # Prediction
        prediction = model.predict(input_scaled)
        predicted_label = LABELS[prediction[0]]

        return render_template("index.html", prediction=predicted_label)

    return render_template("index.html", prediction=None)

if __name__ == "__main__":
    app.run(debug=True , host="0.0.0.0" , port=5000)
    
