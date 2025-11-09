# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.18.1
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# # 1. Data Exploration and Cleaning
#

# %%
# 1.	Data Exploration and Cleaning   
        # 1.1	Load the provided customer dataset    

import pandas as pd
import numpy as np

np.random.seed(42)  
num_customers = 2000


data = {

    'CustomerID': [f'CUST{1000+i}' for i in range(num_customers)],

    'Gender': np.random.choice(['Male', 'Female'], num_customers, p=[0.5, 0.5]),

    'SeniorCitizen': np.random.choice([0, 1], num_customers, p=[0.84, 0.16]),

    'Partner': np.random.choice(['Yes', 'No'], num_customers, p=[0.48, 0.52]),

    'Dependents': np.random.choice(['Yes', 'No'], num_customers, p=[0.3, 0.7]),

    'Tenure': np.random.randint(1, 73, num_customers), # Months

    'PhoneService': np.random.choice(['Yes', 'No'], num_customers, p=[0.9, 0.1]),

    'MultipleLines': np.random.choice(['Yes', 'No', 'No phone service'], num_customers, p=[0.42, 0.48, 0.1]),

    'InternetService': np.random.choice(['DSL', 'Fiber optic', 'No'], num_customers, p=[0.34, 0.44, 0.22]),

    'OnlineSecurity': np.random.choice(['Yes', 'No', 'No internet service'], num_customers, p=[0.28, 0.50, 0.22]),

    'OnlineBackup': np.random.choice(['Yes', 'No', 'No internet service'], num_customers, p=[0.34, 0.44, 0.22]),

    'DeviceProtection': np.random.choice(['Yes', 'No', 'No internet service'], num_customers, p=[0.34, 0.44, 0.22]),

    'TechSupport': np.random.choice(['Yes', 'No', 'No internet service'], num_customers, p=[0.29, 0.49, 0.22]),

    'StreamingTV': np.random.choice(['Yes', 'No', 'No internet service'], num_customers, p=[0.38, 0.40, 0.22]),

    'StreamingMovies': np.random.choice(['Yes', 'No', 'No internet service'], num_customers, p=[0.39, 0.39, 0.22]),

    'Contract': np.random.choice(['Month-to-month', 'One year', 'Two year'], num_customers, p=[0.55, 0.24, 0.21]),

    'PaperlessBilling': np.random.choice(['Yes', 'No'], num_customers, p=[0.59, 0.41]),

    'PaymentMethod': np.random.choice(['Electronic check', 'Mailed check', 'Bank transfer (automatic)', 'Credit card (automatic)'], num_customers, p=[0.34, 0.23, 0.22, 0.21]),

    'MonthlyCharges': np.random.normal(loc=65, scale=30, size=num_customers).clip(18, 120).round(2), 
    # generates num_customers random numbers from a normal (Gaussian) distribution
    # the mean (average) monthly charge is $65
    # the standard deviation is $30, so values will generally fall between $35 and $95
    # clips the values to be within a realistic range:Minimum = $18, Maximum = $120
    # and rounds to 2 decimal places

}
df_customers = pd.DataFrame(data)
# df_customers.to_csv('customer_data.xlsx', index=False)
df_customers




# %% [markdown]
# #### Generate Total Charges based on Tenure and Monthly Charges with some noise

# %%
df_customers["Total Charges"] = (df_customers['Tenure'] * df_customers ['MonthlyCharges'] * np.random.uniform(0.95, 1.05, num_customers)).round(2)
# 0.95: This is the minimum possible value (inclusive).
# 1.05: This is the maximum possible value (exclusive).

# %% [markdown]
# #### Make some Total Charges empty for realism (e.g., new customers with 0 tenure)

# %%
df_customers.loc[df_customers['Tenure'] == 1, 'Total Charges'] = df_customers['MonthlyCharges']
# For customers with only 1 month of tenure, TotalCharges is set equal to MonthlyCharges, assuming they've only been billed once.


#  Introduce some missing TotalCharges for customers with low tenure
# This mimics a real-world scenario, where: (a) Some new customers' bills might not be generated yet. OR (b) The system has incomplete data for a few records.
low_tenure_mask = df_customers['Tenure'] < 3  # picks customers with tenure = 1 or 2 months.
low_tenure_indices = df_customers[low_tenure_mask].sample(frac = 0.1, random_state=42).index # Randomly selecting 10% of those low-tenure customers

df_customers.loc[low_tenure_indices, 'Total Charges']  = np.nan # nan = Not a Number" or missing value.

df_customers

# %% [markdown]
# ### Exploratory Data Analysis

# %%
df_customers.head()

# %%
df_customers.info()

# %%
df_customers.describe()

# %%
# from IPython.display import FileLink

# df_customers.to_excel('customer_data.xlsx', index=False)
# FileLink('customer_data.xlsx')  # This will create a link to download the file in Jupyter Notebook or Google Colab

# %% [markdown]
# ### Simulate Churn 
#

# %%
# We’re building a formula that estimates a customer’s chance of leaving the company based on their data.
# We assume everyone starts with 10% chance to leave
churn_probability = 0.1\

# If a customer has a month-to-month contract, their chance of leaving increases by 15% (they are less committed).
+ 0.15 * (df_customers['Contract'] == 'Month-to-month') \

+ 0.1 * (df_customers['InternetService'] == 'Fiber optic') \
# If a customer uses Fiber Optic internet, their chance of leaving increases by 10% (perhaps due to poor service quality or high cost).

+ 0.001 * (df_customers['MonthlyCharges'] - 65) \
# If their monthly bill is higher than $65, their chance of leaving slightly increases (for every dollar above $65, the chance goes up by 0.001 or 0.1%). If it's less than $65, the chance decreases.


- 0.002 * (df_customers['Tenure'] - 36) \
# If they've been a customer for more than 36 months (3 years), their chance of leaving slightly decreases (they are more loyal). If less than 36 months, the chance increases.

+ 0.1 * (df_customers['OnlineSecurity'] == 'No') \
# If they don't have Online Security, their chance of leaving increases by 10% (they might feel their service is incomplete).

+ 0.1 * (df_customers['TechSupport'] == 'No')
# If they don't have Tech Support, their chance of leaving increases by 10% (they might get frustrated when things go wrong).


churn_probability = np.clip(churn_probability, 0.01, 0.99)
# After adding up all the changes, the code makes sure that no customer's chance of leaving is below 1% or above 99%. 
# It assumes that in the real world, nothing is ever a 0% or 100% certainty

df_customers['Churn'] = np.random.binomial(1, churn_probability, num_customers).astype(str)
# np.random.binomial(1, p) returns 1 (Yes) or 0 (No) based on the churn probability p. gives you a list of 0s and 1s:
#1 = Customer left (churned)
#0 = Customer stayed
# For example, if churn probability = 0.9, there’s a 90% chance this customer gets a 1 (churns).
# Adds randomness, mimics real-world uncertainty in customer behavior

df_customers['Churn'] = df_customers['Churn'].replace({'1': 'Yes', '0': 'No'})
# makes the column more readable and suitable for modeling/visualization.

df_customers

# %% [markdown]
# ###  Data Cleaning - Replace 'No phone service' and 'No internet service' for consistency

# %%
for col in ['MultipleLines']:
    df_customers[col] = df_customers.apply(lambda row: 'No' if row['PhoneService'] == 'No' else row[col], axis=1)

# %% [markdown]
# ###  Data Cleaning - Dealing with services that require internet

# %%
for x in['OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies']:
    df_customers[x] =df_customers.apply(lambda row: 'No' if row['InternetService'] == 'No' else row[x], axis=1)

# %%
from IPython.display import FileLink

df_customers.to_excel('customer_data.xlsx', index=False)
FileLink('customer_data.xlsx')  # This will create a link to download the file 

# %%
df_customers['Churn'].value_counts()

# %% [markdown]
# ### Check for Missing Values

# %%
df_customers.isnull().sum()

# %% [markdown]
# ### Handle Missing Values of Total Charges
# ### Fill missing values in 'Total Charges' with the median of the column

# %%
# Median handles outliers better
# Mode makes more sense for categorical (non-numeric) data
df_customers['Total Charges'] = df_customers['Total Charges'].fillna(df_customers['Total Charges'].median())

# %% [markdown]
# ### Visualize Missing Values

# %%
import missingno as msno
msno.bar(df_customers)


# %% [markdown]
# ### Calculate value_counts of each categorical column

# %%
categorical_cols = ['Gender', 'SeniorCitizen', 'Partner', 'Dependents', 'PhoneService',
                    'MultipleLines', 'InternetService', 'OnlineSecurity', 'OnlineBackup',
                    'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies',
                    'Contract', 'PaperlessBilling', 'PaymentMethod', 'Churn']

#calculate value_counts of each column
for x in categorical_cols:
    print(f"Value_Counts for {x}:")
    print(df_customers[x].value_counts())
    print("\n")



# %% [markdown]
# ### Calculate value_counts of each numerical column

# %%
# how can i represent value_counts of each numerical column
numerical_cols = ['CustomerID', 'Tenure', 'MonthlyCharges', 'Total Charges']
for col in numerical_cols:
    print(f"Value Counts for {col}:")
    print(df_customers[col].value_counts())
    print("\n")


# %% [markdown]
# ### Visualizing Each Categorical Column

# %%
import matplotlib.pyplot as plt
import seaborn as sns
categorical_cols = ['Gender', 'SeniorCitizen', 'Partner', 'Dependents', 'PhoneService',
                    'MultipleLines', 'InternetService', 'OnlineSecurity', 'OnlineBackup',
                    'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies',
                    'Contract', 'PaperlessBilling', 'PaymentMethod', 'Churn']


for xx in categorical_cols:
    sns.countplot(x = xx, data = df_customers)
    plt.xticks(rotation = 45)
    plt.show()

# %% [markdown]
# ### Visualizing Each Numerical Column

# %%
numerical_cols = ['Tenure', 'MonthlyCharges', 'Total Charges']

df_customers[numerical_cols].hist(bins = 30)
plt.suptitle("Histogram of Numerical Features")
plt.show()

# %% [markdown]
# ### Encoding Categorical Variables:

# %% [markdown]
# #### Step1: List out all columns that contain textual data (categorical columns) and need to be encoded before model training.

# %%
categorical_cols = df_customers.select_dtypes(include = 'object').columns.tolist()

# Remove the target columns 'churn' if its in the list

categorical_cols.remove("Churn")

print("Categorical columns to encode: ")
print(categorical_cols)



# %%
# df_customers.to_excel("Data Before Encoding.xlsx", index = False)

# from IPython.display import FileLink

# FileLink("Data Before Encoding.xlsx")

# %% [markdown]
# #### Step2: List out all columns that are categorical and need to be encoded before model training.
# ##### > CustomerID is a unique identifier, not a feature — so we will drop it before modeling.
# ##### > Churn is the target variable, which will be label-encoded  (Yes → 1, No → 0).
# ##### > The rest need One-Hot Encoding or Label Encoding

# %%
# drop the identifier column 'CustomerID' as it is not useful for modeling. It has no predictive power
df_customers = df_customers.drop('CustomerID', axis = 1)

# Label encode Churn
df_customers['Churn'] = df_customers['Churn'].map({'Yes': 1, 'No':0})

#one hot encode all other categorical columns
df_encoded = pd.get_dummies(df_customers, drop_first = True)


# %%
print(df_encoded.dtypes)

# %% [markdown]
# ### Convert the Data Type of the entire data to int

# %%
df_encoded = df_encoded.astype(int)

# %%
print(df_encoded.dtypes)

# %%
# from IPython.display import FileLink

# df_encoded.to_excel("Data After Encoding1.xlsx", index = False)

# FileLink("Data After Encoding1.xlsx")

# %%
print(df_encoded.dtypes)

# %% [markdown]
# #### Step 3: Handle Missing Values
# ##### > To ensure that our dataset has no NaNs or nulls, because:
#
# ##### > Most machine learning models cannot handle missing values directly.
#
# ##### > They can cause bias or errors during training or prediction.

# %%
df_encoded.isnull().sum()

# %%
df_encoded.isnull().sum().sum()

# %% [markdown]
# # 2- Feature Engineering

# %% [markdown]
# ### a. Convert Months to Years of Tenure

# %%
df_encoded["TenureYears"] = (df_encoded["Tenure"] / 12) .round(1)
df_encoded

# %%
df_encoded.drop("TenureGroup", axis = 1, inplace = True)
df_encoded

# %% [markdown]
# ### b. Count number of services being availed by each customer and create a new column. More services might reduce churn

# %%
service_cols = ['PhoneService_Yes', 'MultipleLines_Yes', 'InternetService_Fiber optic', 'InternetService_No', 'OnlineSecurity_Yes', 'OnlineBackup_Yes', 'DeviceProtection_Yes', 'TechSupport_Yes', 'StreamingTV_Yes', 'StreamingMovies_Yes', 'PaperlessBilling_Yes' ]

# Ensure all are present in the DataFrame
available_cols = [col for col in service_cols if col in df_encoded.columns]

df_encoded["NoOfServicesAvailed"] = df_encoded[available_cols].astype(int).sum(axis=1)
df_encoded

# %% [markdown]
# ### 3. Count how many security-related services the customer use and create a new column, May indicate customer loyalty—secure customers are less likely to churn.

# %%
security_cols = ['OnlineSecurity_Yes', 'OnlineBackup_Yes', 'DeviceProtection_Yes']

available_sec_cols = [col for col in security_cols if col in df_encoded.columns]

df_encoded["NoofSecServicesAvailed"] = df_encoded[available_sec_cols].astype(int).sum(axis=1)

df_encoded

# %%
# from IPython.display import FileLink
# df_encoded.to_excel("Data after Encoding2.xlsx", index=False)
# FileLink("Data after Encoding2.xlsx")

# %%
df_encoded.info()

# %% [markdown]
# # 3- Model Selection and Training

# %%
from sklearn.model_selection import train_test_split

#define feature and target variables

X = df_encoded.drop('Churn', axis = 1) #features x
y = df_encoded['Churn'] # target y

# Train test split
#20% of the data goes to testing, and 80% goes to training
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42, stratify = y)
#  stratify=y = Keep the same balance of churned vs not churned in both the training and testing groups


# %% [markdown]
# ### Check the class balance to verify stratification

# %%
print(y.value_counts(normalize=True))       # Original distribution
print()
print(y_train.value_counts(normalize=True)) # Training set distribution
print()
print(y_test.value_counts(normalize=True))  # Test set distribution


# %% [markdown]
# ### Implement Logistic Regression

# %%
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score

# Initialize the Model

logreg = LogisticRegression(max_iter=1000)

# Logistic regression works by calculating a weighted sum of the input features and then applying a function called the sigmoid function to squash that sum into a value between 0 and 1.

logreg.fit(X_train, y_train) # This line teaches the model using the training data.

y_pred = logreg.predict(X_test) 
# This line uses the trained model to make predictions on new data called X_test
# .predict() applies a threshold of 0.5 by default:
#     > If the probability ≥ 0.5, it assigns class 1
#     > If the probability < 0.5, it assigns class 0


y_proba = logreg.predict_proba(X_test)[:, 1]

# This line gives the predicted probabilities of the positive class (Churn = 1) for each customer in the test set.

print("Confusion Matrix: \n", confusion_matrix(y_test, y_pred))
print("\nClassification Report: \n", classification_report(y_test, y_pred))
print("ROC-AUC Score: ", roc_auc_score(y_test, y_proba))

#The ROC-AUC (Receiver Operating Characteristic - Area Under Curve) measures how well your model can distinguish between the two classes across all possible classification thresholds
# A score of 0.5 means the model is no better than random guessing, while a score of 1.0 means perfect classification.

# %% [markdown]
# ### Problem: Your dataset is imbalanced — many more "No Churn" than "Yes Churn".
#
# Impact: The model learns to predict "No Churn" always, because it's safe — it gets high accuracy without learning anything useful.
#
# Solution (SMOTE - Synthetic Minority Oversampling Technique):
#
# SMOTE creates synthetic examples of the minority class by interpolating between real samples.
#
# This augments your training data in a way that helps models better learn class boundaries.

# %%
from imblearn.over_sampling import SMOTE
from collections import Counter

smote = SMOTE(random_state=42)
X_train_smote, y_train_smote = smote.fit_resample(X_train, y_train)

print("Before SMOTE:", Counter(y_train))
print("After SMOTE:", Counter(y_train_smote))

# %% [markdown]
# ### Apply Feature Scaling with StandardScaler

# %%
from sklearn.preprocessing import StandardScaler

s = StandardScaler()

X_train_smote_scaled = s.fit_transform(X_train_smote)

X_test_scaled = s.transform(X_test) 

# %% [markdown]
# ### Retrain Again (Logistic Regression and Random FOrest)

# %%
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
from sklearn.ensemble import RandomForestClassifier

log_reg_smote = LogisticRegression(max_iter=1000, random_state = 42)
rf_clf_smote = RandomForestClassifier(random_state = 42)

log_reg_smote.fit(X_train_smote_scaled, y_train_smote) # This line teaches the model using the training data.
rf_clf_smote.fit(X_train_smote, y_train_smote) # This line teaches the model using the training data.

# Predict on original test set (X_test)
y_pred_log = log_reg_smote.predict(X_test_scaled)
y_pred_rf = rf_clf_smote.predict(X_test)

# Evaluate Logistic Regression
print("Logistic Regression")
print(confusion_matrix(y_test, y_pred_log))
print(classification_report(y_test, y_pred_log))
print("ROC-AUC Score:", roc_auc_score(y_test, log_reg_smote.predict_proba(X_test_scaled)[:,1]))

print("\nRandom Forest")
print(confusion_matrix(y_test, y_pred_rf))
print(classification_report(y_test, y_pred_rf))
print("ROC-AUC Score:", roc_auc_score(y_test, rf_clf_smote.predict_proba(X_test)[:,1]))






# %% [markdown]
# # LOGISTIC REGRESSION DIDNOT WORK

# %% [markdown]
# # Lets Try XGBoost Now

# %%
from xgboost import XGBClassifier
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score

# Initialize the XGBoost classifier
# scale_pos_weight = majority / minority = 1422 / 178 ≈ 7.9
xgb_model = XGBClassifier(use_label_encoder=False, eval_metric='logloss',
                          scale_pos_weight=7.9, random_state=42)

# Fit the model on the original (imbalanced) training set
xgb_model.fit(X_train, y_train)

# Predict on the original test set
y_pred_xgb = xgb_model.predict(X_test)

# Evaluate the model
print("XGBoost Results")
print(confusion_matrix(y_test, y_pred_xgb))
print(classification_report(y_test, y_pred_xgb))
print("ROC-AUC Score:", roc_auc_score(y_test, xgb_model.predict_proba(X_test)[:, 1]))


# %% [markdown]
# ### Hyperparameter Tuning for XGBoost

# %%
from xgboost import XGBClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score

# Define base model
xgb = XGBClassifier(random_state=42, eval_metric='logloss')

# Define parameter grid
param_grid = {
    'n_estimators': [100, 200],
    'max_depth': [3, 5, 7],
    'learning_rate': [0.01, 0.1, 0.2],
    'subsample': [0.8, 1.0],
    'colsample_bytree': [0.8, 1.0],
    'scale_pos_weight': [1, 5, 10]  # Important for imbalanced data!
}

# GridSearch with 5-fold cross-validation
grid = GridSearchCV(estimator=xgb, param_grid=param_grid,
                    scoring='roc_auc', cv=5, verbose=1, n_jobs=-1)

# Fit on training data (SMOTE-applied features for XGBoost)
grid.fit(X_train_smote, y_train_smote)

# Best model
best_xgb = grid.best_estimator_

# Evaluate on original test set
y_pred_xgb = best_xgb.predict(X_test)
y_proba_xgb = best_xgb.predict_proba(X_test)[:, 1]

print("XGBoost Tuned Results")
print(confusion_matrix(y_test, y_pred_xgb))
print(classification_report(y_test, y_pred_xgb))
print("ROC-AUC Score:", roc_auc_score(y_test, y_proba_xgb))


# %% [markdown]
# ### Top 15 Feature Importances

# %%
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from xgboost import plot_importance

# 1. If you used GridSearchCV:
best_xgb_model = grid.best_estimator_


# 2. Extract feature importances
importances = best_xgb_model.feature_importances_
feature_names = X_train.columns  # Use this if X_train is a DataFrame

# 3. Create a DataFrame for visualization
feat_imp_df = pd.DataFrame({
    'Feature': feature_names,
    'Importance': importances
}).sort_values(by='Importance', ascending=False)

# 4. Plot top 15 important features
plt.figure(figsize=(10, 6))
sns.barplot(data=feat_imp_df.head(15), x='Importance', y='Feature', palette='viridis')
plt.title("Top 15 Feature Importances - Tuned XGBoost Model")
plt.tight_layout()
plt.show()


# %%
import pickle

# Save the tuned XGBoost model
with open('xgboost_tuned_model.pkl', 'wb') as file:
    pickle.dump(best_xgb, file)


# %%
# code for xgboost version
import sklearn
print(sklearn.__version__)

# %%
import nbformat

# Load the notebook file
with open('Untitled-1.ipynb') as f:
    notebook = nbformat.read(f, as_version=4)

# Extract code cells
code_cells = [cell['source'] for cell in notebook.cells if cell.cell_type == 'code']

# Print the code or save it to a file
for code in code_cells:
    print(code)

