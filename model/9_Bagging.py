from utils import simple_model_eval
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import BaggingRegressor


import warnings
warnings.filterwarnings("ignore")

def bagging_model(isWithCV):
    x = BaggingRegressor(estimator=GradientBoostingRegressor(), n_estimators=100, random_state=42)

    x = get_model(x, isWithCV)
    x, x_train, y_train, x_test, y_test = simple_model_eval(x)

    print("Training Scores: ", x.score(x_train, y_train))
    print("Testing score:", x.score(x_test, y_test))
    if(isWithCV):
        print("\n The best estimator across ALL searched params:\n", x.best_params_)


def get_model(model, isWithCV):
    parameters = {
        'base_estimator__C': [1e-15, 1e-10, 1e-8, 1e-4, 1e-3, 1e-2, 1, 5, 10, 20, 50, 100, 1000], # lambdas for regularization
        'max_samples': [0.05, 0.1, 0.2, 0.5],  # for bootstrap sampling
        'max_features': [0.3, 0.5, 0.7, 0.9]}
    grid_GBR = GridSearchCV(estimator=model, param_grid=parameters, cv=3, n_jobs=-1, verbose=0, scoring='r2')
    if(isWithCV):
        return grid_GBR.best_estimator_
    else:
        print("without CV")
        return model


bagging_model(False)
