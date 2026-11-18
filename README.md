# ML CI/CD Pipeline with GitHub Actions

An end-to-end Machine Learning CI/CD (Continuous Integration and Continuous Deployment) pipeline using **GitHub Actions**, **Scikit-Learn**, **Pytest**, **Streamlit**, and **Render**.

---

## 1. Project Overview

This project automates the entire lifecycle of a machine learning application:
- **Code Testing**: Automated unit tests using `pytest`.
- **Model Validation**: Automatically checks training performance and enforces an accuracy threshold ($\ge 90\%$).
- **Continuous Integration**: Triggers on every `push` or `pull_request` to the `main` branch.
- **Continuous Deployment**: Triggers automated cloud deployment to Render upon successful test and validation stages.

---

## 2. Project Structure

```text
ML-LAB/
├── .github/
│   └── workflows/
│       └── ml-pipeline.yml    # GitHub Actions 3-stage CI/CD workflow
├── .gitignore                 # Excludes environment, cache, and temp files
├── app.py                     # All-in-one: Model training, testing & Streamlit UI
├── requirements.txt           # Project dependencies
└── README.md                  # Project documentation
```

---

## 3. Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/2400080269/MLOOPS-lab.git
   cd MLOOPS-lab
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

## 4. Local Execution & Testing

### 4.1 Train the Model
Trains a `RandomForestClassifier` on the Iris dataset and validates accuracy:
```bash
python app.py
```
*Expected Output:*
```text
Model Accuracy: 1.0
```

### 4.2 Run Automated Tests
Executes unit tests verifying model training, accuracy threshold, and predictions:
```bash
pytest app.py -v
```
*Expected Output:*
```text
app.py::test_model_training PASSED
app.py::test_model_prediction PASSED
======================== 2 passed =========================
```

### 4.3 Run the Web Application
Launches the interactive prediction interface in your browser:
```bash
streamlit run app.py
```
*App URL:* `http://localhost:8501`

---

## 5. CI/CD Pipeline (GitHub Actions)

The workflow defined in `.github/workflows/ml-pipeline.yml` executes three automated stages:

| Stage | Trigger | Operation |
| :--- | :--- | :--- |
| **1. Testing** | `push` / `PR` | Runs `pytest app.py -v` |
| **2. Model Validation** | Needs `testing` | Runs `python app.py` (checks accuracy $\ge 0.90$) |
| **3. Deployment** | Needs `model-validation` (on `main`) | Triggers Render Deploy Hook via POST request |

---

## 6. Deployment Guide (Render)

1. Sign in to [Render](https://render.com) using your GitHub account.
2. Click **New +** $\to$ **Web Service**.
3. Connect your repository: `2400080269/MLOOPS-lab`.
4. Configure the service settings:
   - **Environment / Runtime**: `Python 3`
   - **Build Command**:
     ```bash
     pip install -r requirements.txt && python app.py
     ```
   - **Start Command**:
     ```bash
     streamlit run app.py --server.port $PORT --server.address 0.0.0.0
     ```
5. Click **Create Web Service**.
6. *(Optional)* Copy the **Deploy Hook URL** from Render Settings, navigate to your GitHub repository:
   - **Settings** $\to$ **Secrets and variables** $\to$ **Actions** $\to$ **New repository secret**
   - Name: `RENDER_DEPLOY_HOOK`
   - Value: `<Render Deploy Hook URL>`

---

## 7. Viva Questions & Quick Reference

1. **What is CI/CD?**
   - **CI (Continuous Integration)**: Automates building and testing code on every commit.
   - **CD (Continuous Deployment)**: Automates releasing and deploying validated code to production.

2. **What is GitHub Actions?**
   - A CI/CD automation tool integrated into GitHub that runs defined workflows triggered by repository events (`push`, `pull_request`).

3. **What is Model Validation in ML CI/CD?**
   - The process of testing a newly trained model against predefined performance benchmarks (e.g., accuracy $\ge 90\%$) before allowing deployment.

4. **Why use Pytest?**
   - Pytest is a Python test framework used to write clean, modular unit and integration tests.

5. **What is `model.pkl`?**
   - A serialized binary file created using `joblib` that stores the trained model weights and architecture for inference.

6. **What happens if a test fails in the pipeline?**
   - Subsequent dependent stages (`model-validation` and `deployment`) are blocked automatically, preventing broken code or low-performing models from reaching production.
