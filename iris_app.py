from flask import Flask, render_template, request, redirect, url_for, session, flash
import pickle
import numpy as np
import pandas as pd

# ***Code to read in model, accept user input written in index.html, and predict using model***

app = Flask(__name__)
app.secret_key = "what_a_pain"

# Model's features that will appear on the form
FORM_FIELDS = ["sepal_length", "sepal_width", "petal_length", "petal_width"]

def make_prediction(form_data):
    pred = None

    def require_float(name):
        # Fail fast so we don't silently use zeros
        val = form_data.get(name, None)
        if val is None or str(val).strip() == "":
            raise ValueError(f"Missing value for '{name}'")
        try:
            return float(val)
        except ValueError:
            raise ValueError(f"Invalid number for '{name}': {val}")


    # Ensures entry is floating point number if they enter integer
    def to_float(x, default=0.0):
        try:
            return float(x)
        except (TypeError, ValueError):
            return default

    TRAIN_COLS = ["sepal_length", "sepal_width", "petal_length", "petal_width"]

    # Build a row in the exact training order
    row = {c: float(form_data[c]) for c in TRAIN_COLS}
    X_df = pd.DataFrame([row], columns=TRAIN_COLS)

    # Predict species
    prediction = final_model.predict(X_df)
    prediction_result = "ham" if prediction[0] == 0 else "spam"
    return f"Predicted species: {prediction_result}"

# Load model, scaler, and encoders
try:
  iris_model = pickle.load(open('lr.pkl', 'rb'))
except FileNotFoundError as e:
    raise Exception(f"Pickle file not found: {str(e)}")
except Exception as e:
    raise Exception(f"Error loading pickle file: {str(e)}")

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # which button did they click?
        if "predict" in request.form:

            # keep submitted values in session
            session["form_values"] = {i: request.form.get(i, "") for i in FORM_FIELDS}

            # run prediction
            session["prediction"] = make_prediction(session["form_values"])

            # redirect to avoid resubmission on refresh
            return redirect(url_for("index"))

        if "clear" in request.form:
            session.pop("form_values", None)
            session.pop("prediction", None)
            return redirect(url_for("index"))

    # GET: render with whatever is in session (or defaults)
    values = session.get("form_values", {i: "" for i in FORM_FIELDS})
    prediction = session.get("prediction")
    return render_template("index.html", values=values, prediction=prediction)


if __name__ == '__main__':
    debug = True