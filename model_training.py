import joblib
from sklearn.datasets import load_iris
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix

if __name__ == "__main__":
    # Load data
    iris = load_iris()
    x, y = iris.data, iris.target
    target_names = iris.target_names

    # Train/test split (as requested)
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, random_state=42, stratify=y
    )

    # Simple, solid baseline model
    pipe = Pipeline([
        ("scaler", StandardScaler()),
        ("lr", LogisticRegression(max_iter=500, n_jobs=None, random_state=42)),
    ])

    # Train
    pipe.fit(x_train, y_train)

    # Evaluate
    y_pred = pipe.predict(x_test)
    accuracy = accuracy_score(y_test, y_pred)
    print("\nAccuracy: {:.3f}".format(accuracy))
    print("\nConfusion matrix (rows=true, cols=pred):\n", confusion_matrix(y_test, y_pred))
    print("\nClassification report:\n")
    print(classification_report(y_test, y_pred, target_names=target_names))

    # Save model artifact for your app
    joblib.dump(pipe, "iris_lr.joblib")
    print("\nSaved trained model to iris_lr.joblib")