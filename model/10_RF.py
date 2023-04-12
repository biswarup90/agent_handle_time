from utils import simple_model_eval
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestRegressor


import warnings
warnings.filterwarnings("ignore")

def rf_model(isWithCV):
    x = RandomForestRegressor()

    x = get_model(x, isWithCV)
    x, x_train, y_train, x_test, y_test = simple_model_eval(x)

    if (isWithCV):
        print("\n The best estimator across ALL searched params:\n", x.best_params_)

    x = x.best_estimator_ if isWithCV else x

    print("Training Scores: ", x.score(x_train, y_train))
    print("Testing score:", x.score(x_test, y_test))


def get_model(model, isWithCV):
    param_grid = {
        'bootstrap': [True],
        'max_depth': [80, 90, 100, 110],
        'max_features': [2, 3],
        'min_samples_leaf': [3, 4, 5],
        'min_samples_split': [8, 10, 12],
        'n_estimators': [100, 200, 300, 1000]
    }
    grid_GBR = GridSearchCV(estimator=model, param_grid=param_grid, cv=3, n_jobs=-1, verbose=0, scoring='r2')
    if(isWithCV):
        return grid_GBR
    else:
        return model


rf_model(True)
