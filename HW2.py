import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score

file_path = 'C:\\Users\\gabei\\OneDrive\\aug_train.csv'
try:
    df = pd.read_csv(file_path)
    print("First few rows of the DataFrame:")
    print(df.head())

except Exception as e:
    print(f"An error occurred: {str(e)}")

df['gender'].fillna('Unknown', inplace=True)
df = pd.get_dummies(df, columns=['gender'], prefix='gen')

df = pd.get_dummies(df, columns=['relevent_experience'], prefix='exp')

education_mapping = { 'Primary School': 0,'High School': 1,'Graduate': 2,'Masters': 3,'Phd': 4, 'nan':2.5}
df['education_level'] = df['education_level'].map(education_mapping)

df['last_new_job'].replace({'>4': '5', 'never': '0'}, inplace=True)
mode_value = df['last_new_job'].mode()[0]
df['last_new_job'].fillna(mode_value, inplace=True)

df = pd.get_dummies(df, columns=['enrolled_university'], prefix='enrolled')

mapping_dict = {'>20': 21, '<1': 0}
for i in range(1, 21):
    mapping_dict[str(i)] = i

df['experience'] = df['experience'].map(mapping_dict)
mean_value = df['experience'].mean()
df['experience'].fillna(mean_value, inplace=True)

df = pd.get_dummies(df, columns=['major_discipline'], prefix='major')
mean_value = df['education_level'].mean()
# Replace NaN values with the mean
df['education_level'].fillna(mean_value, inplace=True)

df.drop('company_size', axis=1, inplace=True)
df.drop('company_type', axis=1, inplace=True)
df['last_new_job'] = df['last_new_job'].astype(int)

print(df.columns)
df.drop('city', axis=1, inplace=True)



X = df.drop('target', axis=1) 
y = df['target'] 

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

logistic_regression_model = LogisticRegression()
logistic_regression_model.fit(X_train, y_train)

feature_coefficients = logistic_regression_model.coef_[0]
coefficients_df = pd.DataFrame({'Feature': X.columns, 'Coefficient': feature_coefficients})

coefficients_df['Abs_Coefficient'] = abs(coefficients_df['Coefficient'])
coefficients_df = coefficients_df.sort_values(by='Abs_Coefficient', ascending=False)


y_pred = logistic_regression_model.predict(X_test)


accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)

print(f"Accuracy: {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall: {recall:.4f}")

import keras
# Define the DNN model
model = keras.Sequential([
    keras.layers.Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
    keras.layers.Dense(32, activation='relu'),
    keras.layers.Dense(16, activation='relu'),
    keras.layers.Dense(1, activation='sigmoid')
])

# Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train the model
history = model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test))

# Evaluate the model
y_pred = model.predict(X_test)
y_pred_binary = (y_pred > 0.5).astype(int)

accuracy = accuracy_score(y_test, y_pred_binary)
precision = precision_score(y_test, y_pred_binary)
recall = recall_score(y_test, y_pred_binary)

print(f"Accuracy: {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall: {recall:.4f}")

import joblib
joblib.dump(model,'model.pkl')
