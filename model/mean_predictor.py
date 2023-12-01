import numpy as np
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from util.utils import split_into_x_y, get_encoded_data
from statistics import mean, mode
import seaborn as sns
from fitter import Fitter, get_common_distributions, get_distributions

isTransformY = False
shouldFilterData = True
df_train, df_test = get_encoded_data(shouldFilterData)
import seaborn as sns
import matplotlib.pyplot as plt
x_train, y_train, x_test, y_test = split_into_x_y(df_train=df_train, df_test=df_test, isTransformY=isTransformY)

def mean_predictor():
    Y = np.array(y_test).reshape(-1, 1)
    mean_y = mean(Y.flatten())
    y_test['pred'] = mean_y


    mse = mean_squared_error(y_test['connectedDuration'], y_test['pred'])
    r2 = r2_score(y_test['connectedDuration'], y_test['pred'])

    print(y_test[0:5])

    print("RMSE ", np.sqrt(mse) / 1000, " Sec")
    print("R2 ", r2, "\n")


def fit_distribution():
    conDur_train = y_train['connectedDuration'].values
    conDur_test = y_test['connectedDuration'].values
    f_train = Fitter(conDur_train)
    f_train.fit()
    print("Train")
    print(f_train.summary())
    print(f_train.get_best(method = 'sumsquare_error'))
    plt.show()

    print("Test")
    f_test = Fitter(conDur_test)
    f_test.fit()
    print(f_test.summary())
    print(f_test.get_best(method='sumsquare_error'))
    plt.show()

fit_distribution()