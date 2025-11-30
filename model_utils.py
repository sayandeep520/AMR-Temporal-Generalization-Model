
import xgboost as xgb
from sklearn.model_selection import GridSearchCV, StratifiedKFold
from sklearn.metrics import accuracy_score, f1_score, recall_score, precision_score, make_scorer
import numpy as np

def train_model(X_train, y_train, model_type='xgb'):
    """Trains a specified model with optimized hyperparameters."""
    if model_type == 'xgb':
        xgb_model = xgb.XGBClassifier(
            objective='binary:logistic', eval_metric='logloss', random_state=42,
            use_label_encoder=False, scale_pos_weight=np.sum(y_train == 0) / np.sum(y_train == 1)
        )
        xgb_params = {'n_estimators': [50, 100], 'max_depth': [3, 5], 'learning_rate': [0.01, 0.1]}
        cv_strategy = StratifiedKFold(n_splits=3, shuffle=True, random_state=42)
        grid_search = GridSearchCV(xgb_model, xgb_params, cv=cv_strategy, scoring='f1', n_jobs=-1)
        grid_search.fit(X_train, y_train)
        return grid_search.best_estimator_
    # Add logic for other model types (e.g., Logistic Regression, RandomForest)
    return None

def evaluate_model(model, X_test, y_test):
    """Evaluates model performance and returns key metrics."""
    y_pred = model.predict(X_test)
    metrics = {
        'accuracy': accuracy_score(y_test, y_pred),
        'f1_score': f1_score(y_test, y_pred),
        'recall': recall_score(y_test, y_pred),
        'precision': precision_score(y_test, y_pred)
    }
    return metrics
