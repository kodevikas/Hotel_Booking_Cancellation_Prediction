"""
Hotel Bookings Cancellation Classification
Converted from the original Jupyter notebook.

Required input:
    hotel_bookings.csv

Place this CSV in the same folder as this script before running.
"""

# ## Hotel_Bookings dataset Classification

# ---- Notebook cell 1 ----
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt 
import seaborn as sns

# ### Load the data

# ---- Notebook cell 3 ----
df = pd.read_csv("hotel_bookings.csv")
print(df.head())

# ## Explore the data

# ---- Notebook cell 5 ----
print("Shape:",df.shape)

# ---- Notebook cell 6 ----
df.info()

# ---- Notebook cell 7 ----
df["reservation_status_date"]=pd.to_datetime(df["reservation_status_date"])

# ---- Notebook cell 8 ----
print(df.head())

# ---- Notebook cell 9 ----
## Checking the missing values 

print(df.isnull().sum().sort_values(ascending=False))

# ---- Notebook cell 10 ----
df = df.drop(columns=['company'])

# ---- Notebook cell 11 ----
df['agent'] = df['agent'].fillna('Unknown')
df['country'] = df['country'].fillna('Unknown')

df['children'] = df['children'].fillna(df['children'].median())

# ---- Notebook cell 12 ----
## Checking duplicated values 

print("Duplicate rows:", df.duplicated().sum())

# ---- Notebook cell 13 ----
df = df.drop_duplicates()

# ---- Notebook cell 14 ----
categorical_col=df.select_dtypes(include="object").columns.tolist()
numerical_col = df.select_dtypes(include="number").columns.tolist()

print("Categotical Columns:",categorical_col)
print("Numerical Columns:",numerical_col)

# ---- Notebook cell 15 ----
print(df['is_canceled'].value_counts())

# ---- Notebook cell 16 ----
print(df['is_canceled'].value_counts(normalize=True) * 100)

# ---- Notebook cell 17 ----
## Visualize the target variable

sns.countplot(data=df,x='is_canceled')
plt.title('Booking Cancellation Distribution')
plt.savefig("target_distribution.png")
plt.close()

# ---- Notebook cell 18 ----
print(df[numerical_col].describe())

# ## outliners

# ---- Notebook cell 20 ----
num_cols = df.select_dtypes(include="number").columns.drop(
    'is_canceled', errors='ignore'
)

for col in num_cols:
    plt.figure(figsize=(8, 3))
    sns.boxplot(x=df[col])
    plt.title(f'Boxplot of {col}')
    plt.savefig("hotel_booking_plot.png")
    plt.savefig("target_distribution.png")
    plt.close()

# ---- Notebook cell 21 ----
# Detect outliers using IQR
numerical_cols = df.select_dtypes(include='number').columns

numerical_cols = numerical_cols.drop('is_canceled')

for col in numerical_cols:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)

    IQR = Q3 - Q1

    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR

    df[col] = df[col].clip(lower, upper)


## it control the row instead of removing the rows 

   ## like 800,900,1000,5000,8000 ----> this 8000 covert into 5000 

# ---- Notebook cell 22 ----
## Correlation using heatmap

plt.figure(figsize=(8,6))

corr = df.select_dtypes(include="number").corr()

sns.heatmap(
    corr,
    cmap='coolwarm',
    center=0
)

plt.title('Correlation Heatmap')
plt.close()

# ---- Notebook cell 23 ----
print(df.groupby('hotel')['is_canceled'].mean() * 100)

# ---- Notebook cell 24 ----
sns.barplot(data=df, x='hotel', y='is_canceled')
plt.title('Cancellation Rate by Hotel Type')
plt.ylabel('Cancellation Rate')
plt.savefig("target_distribution.png")
plt.close()

# ---- Notebook cell 25 ----
## Check data leakage

print(df[['reservation_status', 'reservation_status_date']].head())

# ---- Notebook cell 26 ----
df = df.drop(columns=['reservation_status', 'reservation_status_date'])

# ## sepearte the features and target variable

# ---- Notebook cell 28 ----
X=df.drop(["is_canceled"],axis=1)
y=df["is_canceled"]

# ---- Notebook cell 29 ----
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# ---- Notebook cell 30 ----
numerical_col = X_train.select_dtypes(include=['number']).columns.tolist()

categorical_col = X_train.select_dtypes(exclude=['number']).columns.tolist()

# ---- Notebook cell 31 ----
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

preprocessor = ColumnTransformer([
    ('num', StandardScaler(), numerical_col),
    ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_col)
])

# ---- Notebook cell 32 ----
for col in categorical_col:
    types = X_train[col].dropna().map(type).nunique()
    if types > 1:
        print(col, X_train[col].dropna().map(type).unique())

# ---- Notebook cell 33 ----
X_train['agent'] = X_train['agent'].astype(str)
X_test['agent'] = X_test['agent'].astype(str)

# ---- Notebook cell 34 ----
X_train_processed = preprocessor.fit_transform(X_train)

X_test_processed = preprocessor.transform(X_test)

# ## Base Model

# ---- Notebook cell 36 ----
from sklearn.linear_model import LogisticRegression

model_LR=LogisticRegression(max_iter=1000)
model_LR.fit(X_train_processed,y_train)

# ---- Notebook cell 37 ----
y_pred=model_LR.predict(X_test_processed)

# ---- Notebook cell 38 ----
from sklearn.metrics import accuracy_score,classification_report

accuracy=accuracy_score(y_test,y_pred)
print("Accuracy Score:", round(accuracy * 100, 2), "%")

# ---- Notebook cell 39 ----
print(classification_report(y_test, y_pred))

# ---- Notebook cell 40 ----
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

cm = confusion_matrix(y_test, y_pred)

disp = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=['Not Canceled', 'Canceled']
)

disp.plot(cmap='Blues')
plt.savefig("target_distribution.png")
plt.close()

# ---- Notebook cell 41 ----
from sklearn.tree import DecisionTreeClassifier

model_DT=DecisionTreeClassifier(random_state=42)
model_DT.fit(X_train_processed,y_train)

# ---- Notebook cell 42 ----
DT_y_pred=model_DT.predict(X_test_processed)

# ---- Notebook cell 43 ----
from sklearn.metrics import accuracy_score,classification_report

accuracy=accuracy_score(y_test,DT_y_pred)
print("Accuracy Score:", round(accuracy * 100, 2), "%")

# ---- Notebook cell 44 ----
print(classification_report(y_test, DT_y_pred))

# ---- Notebook cell 45 ----
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

cm = confusion_matrix(y_test, DT_y_pred)

disp = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=['Not Canceled', 'Canceled']
)

disp.plot(cmap='Blues')
plt.savefig("target_distribution.png")
plt.close()

# ---- Notebook cell 47 ----
from sklearn.ensemble import RandomForestClassifier

model_RF=RandomForestClassifier(n_estimators=100,
                                    random_state=42,
                                    n_jobs=-1)
model_RF.fit(X_train_processed,y_train)

# ---- Notebook cell 48 ----
yRF_pred=model_RF.predict(X_test_processed)

# ---- Notebook cell 49 ----
print("Accuracy Score:",accuracy_score(y_test,yRF_pred))

# ---- Notebook cell 50 ----
print("Classification Report :",classification_report(y_test,yRF_pred))

# ## Cross-Validitation

# ## Pipeline

# ---- Notebook cell 56 ----
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler,OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score,classification_report,confusion_matrix,confusion_matrix

# ---- Notebook cell 57 ----
# Pipeline object created; see subsequent fit/predict steps.
preprocessor = ColumnTransformer([
    ('num', StandardScaler(), numerical_col),
    ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_col)
])


# ---- Notebook cell 58 ----
# Pipeline object created; see subsequent fit/predict steps.
model_LR=Pipeline([
    ("preprocessor",preprocessor),
    ("model",LogisticRegression())
])

# ---- Notebook cell 59 ----
model_LR.fit(X_train,y_train)

# ---- Notebook cell 60 ----
LR_pred=model_LR.predict(X_test)

# ---- Notebook cell 61 ----
print("Accuracy Score:",accuracy_score(y_test,LR_pred)*100)
print("Classification_report:",classification_report(y_test,LR_pred))

# ---- Notebook cell 62 ----
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

cm = confusion_matrix(y_test, LR_pred)

disp = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=['Not Canceled', 'Canceled']
)

disp.plot(cmap='Blues')
plt.savefig("target_distribution.png")
plt.close()

# ---- Notebook cell 63 ----
preprocessor_without_scaling = ColumnTransformer([
    ('num', 'passthrough', numerical_col),
    ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_col)
])

# ---- Notebook cell 64 ----
# Pipeline object created; see subsequent fit/predict steps.
DT_pipeline=Pipeline([
    ("preprocessor",preprocessor_without_scaling),
    ("model",DecisionTreeClassifier())
])

# ---- Notebook cell 65 ----
DT_pipeline.fit(X_train,y_train)

# ---- Notebook cell 66 ----
DT_pred=DT_pipeline.predict(X_test)

# ---- Notebook cell 67 ----
print("Accuracy Score:",accuracy_score(y_test,DT_pred))

# ---- Notebook cell 68 ----
print("Classification Report:",classification_report(y_test,DT_pred))

# ---- Notebook cell 69 ----
print(confusion_matrix(y_test, DT_pred))

# ---- Notebook cell 70 ----
RF_pipeline=Pipeline([
    ("preprocessor",preprocessor),
    ("model",RandomForestClassifier(n_estimators=100,
                                    random_state=42,
                                    n_jobs=-1
                                   ))
])


# ---- Notebook cell 71 ----
# Pipeline object created; see subsequent fit/predict steps.

# ---- Notebook cell 72 ----
RF_pipeline.fit(X_train,y_train)

# # ---- Random Forest Cross-Validation ----
# from sklearn.model_selection import StratifiedKFold, cross_val_score

# skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
# cv_scores = cross_val_score(
#     RF_pipeline,
#     X_train,
#     y_train,
#     cv=skf,
#     scoring="accuracy",
#     n_jobs=-1
# )
# print("CV scores:", cv_scores)
# print("Mean CV accuracy:", cv_scores.mean())
# print("Mean CV accuracy (%):", cv_scores.mean() * 100)


# # ---- Notebook cell 73 ----
# RF_pred=RF_pipeline.predict(X_test)

# # ---- Notebook cell 74 ----
# print("Accuracy Score:",accuracy_score(y_test,RF_pred))

# # ---- Notebook cell 75 ----
# print("Classification Report:",classification_report(y_test,RF_pred))

# # ## HyperParameter Tuning

# # ---- Notebook cell 77 ----
# from sklearn.model_selection import RandomizedSearchCV
# from sklearn.ensemble import RandomForestClassifier

# param_dist = {
#     "n_estimators": [100, 200, 300],
#     "max_depth": [10, 20, None],
#     "min_samples_leaf": [1, 2, 5],
# }

# random_search = RandomizedSearchCV(
#     RandomForestClassifier(random_state=42),
#     param_distributions=param_dist,
#     n_iter=15,
#     cv=3,
#     scoring="f1",
#     n_jobs=-1,
#     random_state=42,
# )
# random_search.fit(X_train_processed, y_train)
# print(random_search.best_params_)

# # ---- Notebook cell 78 ----
# best_rf = random_search.best_estimator_

# print("Best Parameters:", random_search.best_params_)
# print("Best CV F1 Score:", random_search.best_score_)

# # ---- Notebook cell 79 ----
# y_pred = best_rf.predict(X_test_processed)


# ---- Notebook cell 80 ----
from sklearn.metrics import accuracy_score, precision_score,recall_score,f1_score,classification_report


print("Accuracy:", accuracy_score(y_test, y_pred))
print("Precision:", precision_score(y_test, y_pred))
print("Recall:", recall_score(y_test, y_pred))
print("F1 Score:", f1_score(y_test, y_pred))

print(classification_report(y_test, y_pred))

# ---- Notebook cell 81 ----
from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

cm = confusion_matrix(y_test, y_pred)

plt.figure(figsize=(6, 4))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')

plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Random Forest Confusion Matrix')
plt.close()

# ## Ensemble Method

# ---- Notebook cell 83 ----
from sklearn.pipeline import Pipeline
from sklearn.ensemble import VotingClassifier

# ---- Notebook cell 84 ----
model_LR=Pipeline([
    ("preprocessing",preprocessor),
    ("model",LogisticRegression(max_iter=1000))
])

model_RF=Pipeline([
    ("preprocessing",preprocessor),
    ("model",RandomForestClassifier(random_state=42))
])

model_DT=Pipeline([
    ("preprocessing",preprocessor_without_scaling),
    ("model",DecisionTreeClassifier(random_state=42))
])

# # ---- Notebook cell 85 ----
# voting_model = VotingClassifier(
#     estimators=[
#         ('lr', model_LR),
#         ('rf', model_RF),
#         ('dt', model_DT)

#     ],
#     voting='soft',
#     n_jobs=-1
# )

# # ---- Notebook cell 86 ----
# voting_model.fit(X_train,y_train)

# # ---- Notebook cell 87 ----
# y_pred_voting = voting_model.predict(X_test)

# # ---- Notebook cell 88 ----
# print(classification_report(y_test, y_pred_voting))

# # ---- Notebook cell 89 ----
# print("Accuracy_score:",accuracy_score(y_test, y_pred_voting))

# ## hard Voting

# ---- Notebook cell 91 ----
hard_voting_model = VotingClassifier(
    estimators=[
        ('lr', model_LR),
        ('rf', model_RF),
        ('dt', model_DT)

    ],
    voting='hard',

)

# ---- Notebook cell 92 ----
hard_voting_model.fit(X_train,y_train)

# ---- Notebook cell 93 ----
y_pred_voting_hard = hard_voting_model.predict(X_test)

# ---- Notebook cell 94 ----
print(classification_report(y_test, y_pred_voting_hard))

# ---- Notebook cell 95 ----
print("Accuracy_score:", accuracy_score(y_test, y_pred_voting_hard))


import joblib

joblib.dump(hard_voting_model, "hotel_booking_cancellation_model.joblib")

print("Model saved successfully!")


