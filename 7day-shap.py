import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
import shap
import matplotlib.pyplot as plt

data = pd.read_csv('/Users/leontang/Downloads/skunkworks_data_v5_full.csv')

data['Date'] = pd.to_datetime(data['Date'])

data = data.sort_values(by='Date')

data['Amount_MA_7'] = data['Amount'].rolling(window=7, min_periods=1).mean()

X = data.drop(columns=["Amount", "Date"])
y = data["Amount"]

categorical_columns = X.select_dtypes(include=['object']).columns
label_encoders = {col: LabelEncoder().fit(X[col]) for col in categorical_columns}

for col, le in label_encoders.items():
    X[col] = le.transform(X[col])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestRegressor(n_estimators=20, random_state=42)  
model.fit(X_train, y_train)

explainer = shap.TreeExplainer(model)
sample_X_train = X_train.sample(n=1000, random_state=42)  
sample_shap_values = explainer.shap_values(sample_X_train)

shap.summary_plot(sample_shap_values, sample_X_train, plot_type="bar")
plt.show()  

shap.summary_plot(sample_shap_values, sample_X_train)
plt.show()  