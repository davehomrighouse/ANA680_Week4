from flask import Flask
app = Flask(__name__)

import joblib
import os
import glob
import pandas as pd

from sklearn.linear_model import LinearRegression

if __name__ == '__main__':

    train_dir = os.environ.get("SM_CHANNEL_TRAIN", "data")
    model_dir = os.environ.get("SM_MODEL_DIR", "model")
    output_dir = os.environ.get("SM_OUTPUT_DATA_DIR", "output")

    # Collect only CSV files
    csv_files = sorted(glob.glob(os.path.join(train_dir, "*.csv")))

    if not csv_files:
        raise FileNotFoundError(
            f"No CSV files found under {train_dir}." +
            "Check the Estimator.fit({...}) channel name ('train'), S3 path," +
            " and IAM permissions.")

    # 2) Read and concatenate
    raw_dfs = (pd.read_csv(p) for p in csv_files)
    train_data = pd.concat(raw_dfs, ignore_index=True)
    print(f"Loaded {len(csv_files)} files → shape: {train_data.shape}")

    # labels are in the first column
    y_train = train_data.iloc[:, 0]
    x_train = train_data.iloc[:, 1:]

    # Train a linear regression model
    lr = LinearRegression()
    lr = lr.fit(x_train, y_train)

    # Saves the fitted model
    os.makedirs(model_dir, exist_ok=True)
    joblib.dump(lr, os.path.join(model_dir, "lr_model.joblib"))


def model_fn(model_dir):
    lr = joblib.load(os.path.join(model_dir, "lr_model.joblib"))
    return lr