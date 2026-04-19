
##  Customer Churn Prediction for Telecom

**Organization:** Kangaroo Ventures (Remote Internship Project)
**Tech Stack:** Python · Pandas · Scikit-learn · XGBoost · SMOTE · Matplotlib · Seaborn

---

###  Project Overview

This project focuses on predicting **customer churn** for a telecom company using supervised machine learning.
The goal was to build an intelligent classification system that identifies customers who are likely to discontinue their service, allowing the company to proactively implement **retention strategies** and reduce customer loss.

---

###  Objectives

* Predict customer churn (Yes/No) as a binary classification problem.
* Handle **class imbalance** between churners and non-churners using SMOTE.
* Compare performance across multiple algorithms and select the best model.
* Identify **key factors influencing churn** to support data-driven decision-making.

---

### Tools & Technologies

* **Programming Language:** Python
* **Libraries & Frameworks:**

  * `pandas`, `numpy` – data cleaning and preprocessing
  * `matplotlib`, `seaborn` – data visualization and exploratory analysis
  * `scikit-learn` – ML model building and evaluation
  * `xgboost` – gradient boosting classifier
  * `imblearn` – SMOTE (Synthetic Minority Oversampling Technique)

---

### Methodology

1. **Data Preprocessing**

   * Cleaned real-world telecom dataset (2000 records).
   * Handled missing values and categorical variables via one-hot encoding.
   * Addressed class imbalance (many “No Churn” vs few “Yes Churn”) using **SMOTE**.
   * Applied **StandardScaler** for consistent feature scaling.

2. **Exploratory Data Analysis (EDA)**

   * Visualized churn distribution, customer demographics, and service usage.
   * Identified imbalance and key patterns driving churn.

3. **Model Development**

   * Trained multiple models: Logistic Regression, Random Forest, and XGBoost.
   * Used **GridSearchCV** for hyperparameter tuning (XGBoost).
   * Evaluated models using Accuracy, Recall, F1-score, and ROC-AUC metrics.

4. **Feature Importance Analysis**

   * Extracted and visualized top predictors from XGBoost (e.g., contract type, tenure, monthly charges).
   * Interpreted how each feature influences churn probability.

---

### Results & Model Performance


**Final Model:** XGBoost (After Hyperparameter Tuning)

* Improved minority class (churners) recall from **0% → 20%**, a significant step for early customer retention.
* Achieved a **balanced trade-off** between accuracy and recall.
* Identified critical churn drivers for actionable business insights.

---

### Visualizations

* Churn Distribution (Imbalanced vs. Balanced using SMOTE)
* Confusion Matrices for each model
* Feature Importance Plot (XGBoost)

---

### Key Insights

* Long-term customers with **month-to-month contracts** and **high monthly charges** are more likely to churn.
* **Contract type** and **tenure** were the most influential predictors.
* The model provides an early warning system for **targeted retention offers** and **personalized communication**.

---

### Future Improvements

* Integrate cross-validation with stratified sampling for improved generalization.
* Implement ensemble stacking (combining RF + XGB).
* Deploy the model via a Flask/Dash web dashboard for live churn prediction.

---



### Author

**Muhammad Hannan Baig**
M.S. Computer Science | NUST
📧 [muhammadhannanbaig@gmail.com] | 🌐 [https://www.linkedin.com/in/hannan-baig-b10320325]

---

