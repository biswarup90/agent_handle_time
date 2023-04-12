from utils import nn_model_eval
from sklearn.model_selection import GridSearchCV
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

import warnings
warnings.filterwarnings("ignore")

def nn_model(isWithCV):
    x = Sequential()
    x.add(Dense(12, input_shape=(8,), activation='relu'))
    x.add(Dense(8, activation='relu'))
    x.add(Dense(1, activation='sigmoid'))
    x.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    x = get_model(x, isWithCV)
    x, x_train, y_train, x_test, y_test = nn_model_eval(x)

    if (isWithCV):
        print("\n The best estimator across ALL searched params:\n", x.best_params_)

    x = x.best_estimator_ if isWithCV else x

    print("Training Scores: ", x.score(x_train, y_train))
    print("Testing score:", x.score(x_test, y_test))



def get_model(model, isWithCV):
    k_range = list(range(1, 31))
    param_grid = {
        'n_neighbors': k_range
    }
    grid_nn = GridSearchCV(estimator=model, param_grid=param_grid, cv=3, n_jobs=-1, verbose=0, scoring='r2')
    if(isWithCV):
        return grid_nn
    else:
        return model


nn_model(True)
