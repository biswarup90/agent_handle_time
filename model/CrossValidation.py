import numpy as np
from sklearn.model_selection import GridSearchCV
import xgboost as xgb
from sklearn.inspection import permutation_importance
import pandas as pd

from ewt.ewt_util.utils import get_encoded_data, split_into_x_y, generate_hist
from sklearn.linear_model import Ridge, Lasso, ElasticNet, GammaRegressor
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import RandomForestRegressor
import joblib
from scipy.special import inv_boxcox
from sklearn.metrics import mean_squared_error
from constants.constants import *
import matplotlib.pyplot as plt
import pickle

from sklearn.model_selection import cross_validate

def cross_validation(model, _X, _y, _cv=5):
    _scoring = ['neg_root_mean_squared_error']
    results = cross_validate(estimator=model,
                             X=_X,
                             y=_y,
                             cv=_cv,
                             scoring=_scoring,
                             return_train_score=True)

    return results

def plot_result(x_label: object, y_label: object, plot_title: object, train_data: object, val_data: object) -> object:
    plt.figure(figsize=(12, 6))
    labels = ["1st Fold", "2nd Fold", "3rd Fold", "4th Fold", "5th Fold"]
    X_axis = np.arange(len(labels))
    ax = plt.gca()
    plt.ylim(0.40000, 1)
    plt.bar(train_data, 0.4, color='blue', label='Training')
    plt.bar(val_data, 0.4, color='red', label='Validation')
    plt.title(plot_title, fontsize=30)
    plt.xticks(X_axis, labels)
    plt.xlabel(x_label, fontsize=14)
    plt.ylabel(y_label, fontsize=14)
    plt.legend()
    plt.grid(True)
    plt.show()


def model_training():
    shouldFilterData = True
    df_train, df_test = get_encoded_data(shouldFilterData)

    x_train, y_train, x_test, y_test = split_into_x_y(df_train=df_train, df_test=df_test, isTransformY=False)
    model = RandomForestRegressor(bootstrap=True,
                          max_depth=90,
                          max_features=3,
                          min_samples_leaf=3,
                          min_samples_split=8,
                          n_estimators=1000)

    result = cross_validation(model, x_test, y_test, 5)
    print(result)

    plot_result("RandomForest Regressor",
                "Negative Root Mean Square Error",
                "Accuracy scores in 5 Folds",
                result["train_neg_root_mean_squared_error"],
                result["test_neg_root_mean_squared_error"])


model_training()



