
from utils import simple_model_eval
from sklearn.model_selection import GridSearchCV
from sklearn.tree import DecisionTreeRegressor

import warnings
warnings.filterwarnings("ignore")

def dt_model(isWithCV):
    x=DecisionTreeRegressor()

    x = get_model(x, isWithCV)
    x, x_train, y_train, x_test, y_test = simple_model_eval(x)

    if(isWithCV):
        print("\n The best estimator across ALL searched params:\n", x.best_params_)

    x = x.best_estimator_ if isWithCV else x

    print("Training Scores: ", x.score(x_train, y_train))
    print("Testing score:", x.score(x_test, y_test))



def get_model(model, isWithCV):
    parameters = {"splitter": ["best", "random"],
                  "max_depth": [1, 3, 5, 7, 9, 11, 12],
                  "min_samples_leaf": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                  "min_weight_fraction_leaf": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9],
                  "max_features": ["auto", "log2", "sqrt", None],
                  "max_leaf_nodes": [None, 10, 20, 30, 40, 50, 60, 70, 80, 90]}
    grid_GBR = GridSearchCV(estimator=model, param_grid=parameters, cv=3, n_jobs=-1, verbose=0, scoring='r2')
    if(isWithCV):
        return grid_GBR
    else:
        return model


dt_model(True)
