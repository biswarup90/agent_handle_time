import xgboost as xgb

from utils import simple_model_eval, model_with_kmeans_eval
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import GradientBoostingRegressor


def xgb_with_kmeans():
    x0 = xgb.XGBRegressor(objective="reg:squarederror", random_state=42)
    x1 = xgb.XGBRegressor(objective="reg:squarederror", random_state=42)
    x0 = get_model(x0, True)
    x1 = get_model(x1, True)

    x0, x1, x_train_0, y_train_0, x_train_1, y_train_1, x_test_0, y_test_0, x_test_1, y_test_1 \
        = model_with_kmeans_eval(x0, x1)

    print("Training Scores 0: ", x0.score(x_train_0, y_train_0))
    print("Training Scores 1: ", x1.score(x_train_1, y_train_1))

    print("Testing score 0:", x0.score(x_test_0, y_test_0))
    print("Testing score 1:", x1.score(x_test_1, y_test_1))


def xgb_model(isWithCV):
    x = xgb.XGBRegressor(objective="reg:squarederror", random_state=42)

    x = get_model(x, isWithCV)
    x, x_train, y_train, x_test, y_test = simple_model_eval(x)

    if(isWithCV):
        print("\n The best estimator for XGB across ALL searched params:\n", x.best_params_)

    x = x.best_estimator_ if isWithCV else x

    print("XGB Training Scores: ", x.score(x_train, y_train))
    print("XGB Testing score:", x.score(x_test, y_test))



def grad_boost_model(isWithCV):
    x = GradientBoostingRegressor()

    x = get_model(x, isWithCV)

    x, x_train, y_train, x_test, y_test = simple_model_eval(x)

    if(isWithCV):
        print("\nGradient Booster The best estimator across ALL searched params:\n", x.best_params_)

    x = x.best_estimator_ if isWithCV else x

    print("Gradient booster Training Scores: ", x.score(x_train, y_train))
    print("Gradient booster Testing score:", x.score(x_test, y_test))


def get_model(model, isWithCV):
    parameters = {'learning_rate': [0.01, 0.02, 0.03, 0.04],
                  'subsample': [0.9, 0.5, 0.2, 0.1],
                  'n_estimators': [100, 500, 1000, 1500],
                  'max_depth': [4, 6, 8, 10]
                  }
    grid_GBR = GridSearchCV(estimator=model, param_grid=parameters, cv=2, n_jobs=-1, scoring='r2')
    if(isWithCV):
        return grid_GBR
    else:
        return model


grad_boost_model(True)
