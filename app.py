import joblib
import numpy as np
import streamlit as st
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

def train_model():
    iris = load_iris()
    X_train, X_test, y_train, y_test = train_test_split(iris.data, iris.target, test_size=0.2, random_state=42)
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)
    acc = accuracy_score(y_test, model.predict(X_test))
    if acc < 0.90:
        raise ValueError("Model validation failed")
    joblib.dump(model, "model.pkl")
    print(f"Model Accuracy: {acc}")
    return model, acc

def test_model_training():
    model, acc = train_model()
    assert model is not None and acc >= 0.90

def test_model_prediction():
    model, _ = train_model()
    assert model.predict([[5.1, 3.5, 1.4, 0.2]])[0] in [0, 1, 2]

def run_app():
    try:
        model = joblib.load("model.pkl")
    except:
        model, _ = train_model()
    st.title("Iris Flower Classification")
    sl = st.number_input("Sepal Length", 0.0, 10.0, 5.1)
    sw = st.number_input("Sepal Width", 0.0, 10.0, 3.5)
    pl = st.number_input("Petal Length", 0.0, 10.0, 1.4)
    pw = st.number_input("Petal Width", 0.0, 10.0, 0.2)
    if st.button("Predict"):
        pred = model.predict([[sl, sw, pl, pw]])[0]
        classes = ["Setosa", "Versicolor", "Virginica"]
        st.success(f"Predicted Flower: {classes[pred]}")

if __name__ == "__main__":
    import sys
    if any("streamlit" in arg for arg in sys.argv):
        run_app()
    else:
        train_model()
