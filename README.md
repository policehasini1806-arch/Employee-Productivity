# AI-Based Employee Productivity Digital Twin

## 📌 Project Overview

The **AI-Based Employee Productivity Digital Twin** is a web application that uses Machine Learning to predict employee productivity levels based on workplace and performance-related attributes.

The system uses a trained **Logistic Regression classification model** to categorize employee productivity as **High, Moderate, or Low**. A Django-based web interface allows users to explore employee data, view productivity distributions, predict productivity for new employee records, and simulate changes to selected work-related parameters.

The project demonstrates how Machine Learning and web technologies can be combined to support data-driven employee performance analysis.

## 🎯 Objectives

- Predict employee productivity levels using Machine Learning.
- Develop an interactive dashboard for exploring employee data.
- Allow users to enter employee details and obtain productivity predictions.
- Visualize productivity class distribution and model evaluation metrics.
- Simulate hypothetical changes in workplace parameters and compare model predictions.

## ✨ Features

- **Productivity Prediction:** Classifies employees into High, Moderate, or Low productivity categories.
- **Interactive Dashboard:** Displays dataset statistics and productivity distribution.
- **Employee Input Form:** Accepts employee attributes for individual predictions.
- **Scenario Simulator:** Allows users to modify selected parameters and compare predictions.
- **Prediction Probabilities:** Displays model-generated class probabilities when supported by the trained model.
- **Custom User Interface:** Built with HTML, CSS, and JavaScript without Bootstrap.
- **Django Backend:** Connects the frontend with the trained Machine Learning model.
- **Prediction API:** Provides a JSON endpoint for productivity predictions.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Django | Web framework and backend |
| Scikit-learn | Machine Learning model |
| Pandas | Dataset handling |
| NumPy | Numerical operations |
| Joblib | Loading the saved model |
| HTML | Webpage structure |
| CSS | Custom styling and responsive layout |
| JavaScript | Dashboard interactions and simulations |
| Chart.js | Productivity distribution visualization |

## 🤖 Machine Learning Model

The project uses **Multiclass Logistic Regression** to predict employee productivity.

### Input Features

The following 11 features are used by the model:

1. Age
2. Experience Years
3. Attendance
4. Working Hours
5. Tasks Completed
6. Task Delay Count
7. Training Hours
8. Meeting Hours
9. Project Count
10. Performance Score
11. Job Satisfaction

**Target variable:** `Productivity_Level`

**Target classes:** High, Moderate, Low

`Employee_ID` is used as an identifier and is not included as a model input feature.

### Dataset Information

- Dataset file: `06_employee_productivity_digital_twin.csv`
- Total records: 500
- Training records: 400
- Testing records: 100
- Missing values: None reported in the initial dataset inspection

### Reported Model Performance

| Metric | Score |
|---|---:|
| Accuracy | 96% |
| Macro F1-score | 0.85 |
| Weighted F1-score | 0.96 |

These are the reported evaluation results for the current train-test split. The dataset has an imbalanced class distribution, particularly for the High productivity category. Therefore, accuracy should be considered alongside precision, recall, F1-score, and class-wise support. Results may vary with a different split or dataset.

## 🏗️ System Architecture

The application follows a simple three-layer architecture:

1. **Presentation Layer:** HTML, CSS, JavaScript, and Chart.js provide the dashboard, employee form, and simulator.
2. **Application Layer:** Django views process requests, validate employee inputs, and return HTML pages or JSON responses.
3. **Machine Learning Layer:** The saved Logistic Regression model generates productivity predictions and class probabilities.

### Prediction Workflow

1. The user selects an existing employee or enters employee details.
2. The frontend submits the data to the Django backend.
3. Django validates the submitted values.
4. The model service prepares the input in the required feature order.
5. The saved model predicts the productivity category.
6. The result and available class probabilities are displayed on the webpage.

## 📁 Project Structure

```text
employee_productivity_digital_twin/
│
├── manage.py
├── requirements.txt
├── employee_productivity_model.pkl
├── 06_employee_productivity_digital_twin.csv
│
├── productivity_project/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
└── productivity/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── urls.py
    ├── views.py
    ├── model_service.py
    │
    ├── templatetags/
    │   ├── __init__.py
    │   └── productivity_tags.py
    │
    ├── templates/
    │   └── productivity/
    │       ├── base.html
    │       ├── dashboard.html
    │       ├── employee_form.html
    │       └── result.html
    │
    └── static/
        └── productivity/
            ├── css/
            │   └── style.css
            └── js/
                └── dashboard.js
```

## ⚙️ Installation and Setup

### Prerequisites

Install the following before running the project:

- Python 3.10 or a compatible version supported by your dependencies
- pip
- Visual Studio Code or another code editor

### Step 1: Clone or Download the Project

If the project is hosted on GitHub:

```bash
git clone <your-repository-url>
cd employee_productivity_digital_twin
```

Alternatively, open the downloaded project folder in VS Code.

### Step 2: Create a Virtual Environment

On Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### Step 3: Install Dependencies

```bash
python -m pip install -r requirements.txt
```

Example `requirements.txt`:

```text
Django>=5.2,<6.0
pandas>=2.2
numpy>=1.26
scikit-learn>=1.5
joblib>=1.4
```

Use versions compatible with the environment in which the model was trained, especially the installed scikit-learn version.

### Step 4: Configure the Django Project

If you have not already created the Django project and app, run these commands from the root directory:

```bash
django-admin startproject productivity_project .
python manage.py startapp productivity
```

If these folders and files already exist, **do not run these creation commands again**.

Ensure that `productivity` is added to `INSTALLED_APPS` in `productivity_project/settings.py`.

### Step 5: Apply Database Migrations

```bash
python manage.py migrate
```

### Step 6: Start the Development Server

```bash
python manage.py runserver
```

Open the following URL in your browser:

**http://127.0.0.1:8000/**

## 🌐 Application Routes

| Route | Purpose |
|---|---|
| `/` | Main productivity dashboard |
| `/employee/` | Employee input form |
| `/predict/` | Processes form-based predictions |
| `/api/predict/` | Accepts JSON prediction requests |

The prediction API is intended to receive a POST request containing the required employee features. Input field names must match the names expected by the backend.

## 🧪 Example Use Case

Suppose a user wants to estimate the productivity category of an employee.

1. Open the dashboard.
2. Select an existing employee or navigate to the employee form.
3. Enter the employee's work-related and performance-related attributes.
4. Submit the details.
5. View the predicted productivity category and available class probabilities.
6. Use the simulator to compare predictions under a hypothetical scenario.

**Note:** Scenario comparisons represent changes in the model's predictions, not proof that changing a particular workplace factor will cause a productivity improvement.

## 🔒 Important Considerations

- The project is intended for educational and demonstration purposes.
- Predictions depend on the quality and representativeness of the training dataset.
- The current dataset has an imbalanced target distribution.
- Model probabilities are estimates produced by the classifier and may not be calibrated.
- Predictions should not be used as the sole basis for employee evaluation, hiring, promotion, or disciplinary decisions.
- Employee information should be handled securely and in accordance with applicable privacy policies.

## 🚀 Future Enhancements

- Evaluate class imbalance using class weights or resampling techniques.
- Compare Logistic Regression with Random Forest and Support Vector Machine models.
- Add confusion matrix and class-wise performance visualizations.
- Store prediction history in a database.
- Add authentication and role-based access control.
- Include model explainability to help users understand individual predictions.
- Improve validation using stratified cross-validation and a separate test dataset.

## 👩‍💻 Conclusion

The AI-Based Employee Productivity Digital Twin integrates Machine Learning with Django to provide an interactive platform for employee productivity prediction and scenario analysis. It combines a trained Logistic Regression model, an interactive dashboard, and a custom frontend to demonstrate how predictive analytics can support responsible, data-informed workplace analysis.

---

**Project Type:** Machine Learning + Web Development  
**Model:** Multiclass Logistic Regression  
**Backend:** Django  
**Frontend:** HTML, CSS, JavaScript  
**Dataset Size:** 500 records