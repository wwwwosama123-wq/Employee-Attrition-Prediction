# Employee Attrition Prediction

A Machine Learning project that predicts whether an employee is likely to leave the company based on their personal and job-related information.

## 📌 Project Overview

This project uses Machine Learning techniques to analyze employee data and predict **employee attrition**. The system takes employee information as input and provides a prediction of whether the employee is likely to leave the organization.

The project also includes a simple graphical user interface that allows users to enter employee information and obtain the prediction easily.

## 📊 Dataset

The project uses the **IBM HR Analytics Employee Attrition & Performance Dataset**, which contains employee-related information and a target variable indicating whether an employee left the company.

## 🤖 Machine Learning

The project uses a **Random Forest Classifier** for prediction.

The preprocessing and modeling steps are integrated into a Machine Learning pipeline to ensure that the same data transformations are applied during both training and prediction.

### Evaluation Metrics

The model is evaluated using:

* Accuracy
* Precision
* Recall
* F1-Score
* ROC-AUC
* Confusion Matrix

## 🖥️ Application

The project includes a graphical user interface that allows the user to:

1. Enter employee information.
2. Validate the entered data.
3. Process the input using the trained pipeline.
4. Predict employee attrition.
5. Display the prediction result.

## 🛠️ Technologies

* Python
* Pandas
* NumPy
* Scikit-learn
* Imbalanced-learn
* Joblib
* Tkinter

## 📁 Project Structure

```text
Employee-Attrition-Prediction/
│
├── app.py
├── train.py
├── config.py
└──WA_Fn-UseC_-HR-Employee-Attrition.csv
└── README.md
```

## 🚀 How to Run

Install the required libraries:

```bash
pip install pandas numpy scikit-learn imbalanced-learn joblib
```

Then run the application:

```bash
train_model.py
python app.py
```

## 🎯 Objective

The main objective of this project is to demonstrate how Machine Learning can be used to analyze HR data and predict potential employee attrition, providing a decision-support tool for Human Resources departments.

## 📚 Dataset Source

IBM HR Analytics Employee Attrition & Performance Dataset.

> This project is developed for educational and research purposes.
