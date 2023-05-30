import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from joblib import dump
from datetime import datetime

data = pd.read_csv('../data/dataset_with_target.csv', index_col=0)

X = data.drop('mark', axis=1)
X = X.drop('name', axis=1)
y = data['mark']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

categorical_features = ['c_cat', 'c_type']
numeric_features = list(set(X.columns.tolist()) - set(categorical_features))

preprocessor = ColumnTransformer(
    transformers=[
        ('numeric', SimpleImputer(strategy='median'), numeric_features),
        ('categorical', OneHotEncoder(handle_unknown='ignore'), categorical_features)
    ])

regressor = Pipeline(
    steps=[
        ('preprocessor', preprocessor),
        # ('scaler', StandardScaler()),
        ('model', RandomForestRegressor())
    ])

regressor.fit(X_train, y_train)

y_pred = regressor.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print('Mean Squared Error: ', mse)
print('R^2 Score: ', r2)

toBePersisted = dict({
    'model': regressor,
    'metadata': {
        'name': 'Company score regressor',
        'author': 'Uvarov Ilya',
        'date': str(datetime.now()),
        'source_code_version': '2',
        'metrics': {
            'r2': r2,
            'mse': mse,
        },
    }
})

dump(toBePersisted, '../data/models/model.joblib')
