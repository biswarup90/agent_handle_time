import numpy as np
from sklearn.model_selection import GridSearchCV
import xgboost as xgb
from sklearn.inspection import permutation_importance
import pandas as pd
from util.utils import split_into_x_y, split_into_channel, get_encoded_data, generate_hist
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

model_names = ['GammaRegressor', 'LinearRegression', 'ridge', 'lasso', 'ElasticNet', 'DecisionTree', 'RandomForestRegressor', 'XGBoost','GradientBoostingRegressor', 'KNNRegressor']


grid_models = {
    'LinearRegression': LinearRegression(),
    'ridge': Ridge(),
    'lasso': Lasso(),
    'ElasticNet': ElasticNet(),
    'DecisionTree': DecisionTreeRegressor(),
    'RandomForestRegressor': RandomForestRegressor(),
   'XGBoost': xgb.XGBRegressor(objective="reg:squarederror", random_state=42),
    'GradientBoostingRegressor': GradientBoostingRegressor(),
    'KNNRegressor': KNeighborsRegressor(),

}


fixed_models = {
    'GammaRegressor': GammaRegressor(),
    'LinearRegression': LinearRegression(),
    'ridge': Ridge(alpha=10),
    'lasso': Lasso(alpha=0.1),
    'ElasticNet': ElasticNet(alpha=0.1, l1_ratio=1),
    'DecisionTree': DecisionTreeRegressor(max_depth=5, max_features='auto', max_leaf_nodes=None, min_samples_leaf=1,
                                          min_weight_fraction_leaf=0.1, splitter='best'),
    'RandomForestRegressor': RandomForestRegressor(bootstrap=True,
                                                   max_depth=90,
                                                   max_features=3,
                                                   min_samples_leaf=3,
                                                   min_samples_split=8,
                                                   n_estimators=1000),
    'XGBoost': xgb.XGBRegressor(objective="reg:squarederror", random_state=42, learning_rate=0.01, max_depth=10,
                                n_estimators=1000, subsample=0.9),
    'GradientBoostingRegressor': GradientBoostingRegressor(learning_rate=0.01, max_depth=10, n_estimators=1000,
                                                           subsample=0.9),
    'KNNRegressor': KNeighborsRegressor(n_neighbors=16)
}

model_parameters = {
    'GammaRegressor': {},
    'LinearRegression': [],
    'ridge': dict(alpha=[0.001, 0.01, 0.1, 1, 10, 100, 1000]),
    'lasso': dict(alpha=[0.001, 0.01, 0.1, 1, 10, 100, 1000]),
    'ElasticNet': dict(alpha=[0.001, 0.01, 0.1, 1, 10, 100, 1000],
                       l1_ratio=[0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]),
    'DecisionTree': {"splitter": ["best", "random"],
                     "max_depth": [1, 3, 5, 7, 9, 11, 12],
                     "min_samples_leaf": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                     "min_weight_fraction_leaf": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9],
                     "max_features": [1.0, "log2", "sqrt", None],
                     "max_leaf_nodes": [None, 10, 20, 30, 40, 50, 60, 70, 80, 90]},
    'RandomForestRegressor': {
        'bootstrap': [True],
        'max_depth': [80, 90, 100, 110],
        'max_features': [2, 3],
        'min_samples_leaf': [3, 4, 5],
        'min_samples_split': [8, 10, 12],
        'n_estimators': [100, 200, 300, 1000]
    },
    'XGBoost': {'learning_rate': [0.01, 0.02, 0.03, 0.04],
                'subsample': [0.9, 0.5, 0.2, 0.1],
                'n_estimators': [100, 500, 1000, 1500],
                'max_depth': [4, 6, 8, 10]
                },
    'GradientBoostingRegressor': {'learning_rate': [0.01, 0.02, 0.03, 0.04],
                                  'subsample': [0.9, 0.5, 0.2, 0.1],
                                  'n_estimators': [100, 500, 1000, 1500],
                                  'max_depth': [4, 6, 8, 10]
                                  },
    'KNNRegressor': {
        'n_neighbors': list(range(1, 31))
    }

}
isTransformY = False
shouldFilterData = True
df_train, df_test = get_encoded_data(shouldFilterData)

x_train, y_train, x_test, y_test = split_into_x_y(df_train=df_train, df_test=df_test, isTransformY=isTransformY)


def grid(model, parameters, x, y):
    g = GridSearchCV(estimator=model, param_grid=parameters, scoring='r2')
    g.fit(x, np.ravel(y))
    return g


def model_training(model, x, y):
    model.fit(x, np.ravel(y))
    return model


def train_and_predict(isWithGrid):
    scores = []

    ground_truth = []
    ground_truth.extend(inv_boxcox(y_test.to_numpy(), BOX_COX_LAMBDA) if isTransformY else y_test.to_numpy())
    for m in model_names:
        predicted = []
        model_parameter = model_parameters[m]
        trained_model = grid(grid_models[m], model_parameter, x_train, y_train) if isWithGrid else model_training(
            fixed_models[m],
            x_train,
            y_train)
        if isWithGrid:
            scores.append({
                'model': m,
                'best_score': trained_model.best_score_,
                'best_params': trained_model.best_params_,
                'best_model': trained_model.best_estimator_
            })
        print("**Model**")
        print(m)
        if isWithGrid:
            print("Scores\n")
            print(scores, "\n")
        pred = trained_model.predict(x_test)

        y_predicted = inv_boxcox(pred, BOX_COX_LAMBDA) if isTransformY else pred
        predicted.extend(y_predicted)
        mse = mean_squared_error(ground_truth, predicted)
        r2 = r2_score(ground_truth, predicted)
        print("RMSE ", np.sqrt(mse) / 1000, " Sec")
        print("R2 ", r2, "\n")
        if(m == 'RandomForestRegressor'):
            generate_hist(y_train, x_train, y_test, x_test, pred, m)





# train_model(False, False)
# predict(False)
train_and_predict(False)
