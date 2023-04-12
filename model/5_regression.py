import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import GridSearchCV
from utils import model_with_kmeans_eval, simple_model_eval
from sklearn.linear_model import Ridge, Lasso, ElasticNet
import pickle

def get_lin_model(isWithCV, model=''):
    if isWithCV:
        if model == 'ridge':
            alpha = [0.001, 0.01, 0.1, 1, 10, 100, 1000]
            param_grid = dict(alpha=alpha)
            ridge = Ridge()
            return GridSearchCV(estimator=ridge, param_grid=param_grid, scoring='r2', verbose=1, n_jobs=-1)
        elif model == 'lasso':
            alpha = [0.001, 0.01, 0.1, 1, 10, 100, 1000]
            param_grid = dict(alpha=alpha)
            lasso = Lasso()
            return GridSearchCV(estimator=lasso, param_grid=param_grid, scoring='r2', verbose=1, n_jobs=-1)
        else:
            elastic_net = ElasticNet()
            alpha = [0.001, 0.01, 0.1, 1, 10, 100, 1000]
            l1_ratio = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
            param_grid = dict(alpha=alpha, l1_ratio=l1_ratio)
            return GridSearchCV(estimator=elastic_net, param_grid=param_grid, scoring='r2', verbose=1, n_jobs=-1)
    else:
        return LinearRegression()


def linear_reg_with_kmeans():
    # Linear regression
    linear_reg_0 = get_lin_model(False)
    linear_reg_1 = get_lin_model(False)

    linear_reg_0, linear_reg_1, x_train_0, y_train_0, x_train_1, y_train_1, x_test_0, y_test_0, x_test_1, y_test_1 \
        = model_with_kmeans_eval(linear_reg_0, linear_reg_1)

    print("Linear Regression Training Scores 0: ", linear_reg_0.score(x_train_0, y_train_0))
    print("Linear Regression Training Scores 1: ", linear_reg_1.score(x_train_1, y_train_1))

    print("Linear Regression Testing score 0:", linear_reg_0.score(x_test_0, y_test_0))
    print("Linear Regression Testing score 1:", linear_reg_1.score(x_test_1, y_test_1))

    # Ridge regression
    ridge_reg_0 = get_lin_model(True, 'ridge')
    ridge_reg_1 = get_lin_model(True, 'ridge')

    ridge_reg_0, ridge_reg_1, x_train_0, y_train_0, x_train_1, y_train_1, x_test_0, y_test_0, x_test_1, y_test_1 \
        = model_with_kmeans_eval(ridge_reg_0, ridge_reg_1)

    print("Ridge regression Training Scores 0: ", ridge_reg_0.score(x_train_0, y_train_0))
    print("Ridge regression Training Scores 1: ", ridge_reg_1.score(x_train_1, y_train_1))

    print("Ridge regression Testing score 0:", ridge_reg_0.score(x_test_0, y_test_0))
    print("Ridge regression Testing score 1:", ridge_reg_1.score(x_test_1, y_test_1))

    # Lasso regression
    lasso_reg_0 = get_lin_model(True, 'lasso')
    lasso_reg_1 = get_lin_model(True, 'lasso')

    lasso_reg_0, lasso_reg_1, x_train_0, y_train_0, x_train_1, y_train_1, x_test_0, y_test_0, x_test_1, y_test_1 \
        = model_with_kmeans_eval(lasso_reg_0, lasso_reg_1)

    print("Lasso regression Training Scores 0: ", lasso_reg_0.score(x_train_0, y_train_0))
    print("Lasso regression Training Scores 1: ", lasso_reg_1.score(x_train_1, y_train_1))

    print("Lasso regression Testing score 0:", lasso_reg_0.score(x_test_0, y_test_0))
    print("Lasso regression Testing score 1:", lasso_reg_1.score(x_test_1, y_test_1))

    #Elastic net Linear regression
    el_reg_0 = get_lin_model(True, 'elastic')
    el_reg_1 = get_lin_model(True, 'elastic')

    el_reg_0, el_reg_1, x_train_0, y_train_0, x_train_1, y_train_1, x_test_0, y_test_0, x_test_1, y_test_1 \
        = model_with_kmeans_eval(el_reg_0, el_reg_1)

    print("Elastic net Training Scores 0: ", el_reg_0.score(x_train_0, y_train_0))
    print("Elastic net Training Scores 1: ", el_reg_1.score(x_train_1, y_train_1))

    print("Elastic net Testing score 0:", el_reg_0.score(x_test_0, y_test_0))
    print("Elastic net Testing score 1:", el_reg_1.score(x_test_1, y_test_1))

def linear_reg():
    isWithCV = True
    #Linear regression
    linear_reg = get_lin_model(False)

    linear_reg, x_train, y_train, x_test, y_test = simple_model_eval(linear_reg)

    pickle.dump(linear_reg, open('../saved_models/linear_reg.pkl', 'wb'))
    linear_reg = pickle.load(open('../saved_models/linear_reg.pkl', 'rb'))

    print("Linear regression Training Scores 0: ", linear_reg.score(x_train, y_train))
    print("Linear Regression Testing score 0:", linear_reg.score(x_test, y_test))

    #Ridge regression
    ridge = get_lin_model(isWithCV, 'ridge')

    ridge, x_train, y_train, x_test, y_test = simple_model_eval(ridge)

    if (isWithCV):
        print("\n The best estimator for ridge across ALL searched params:\n", ridge.best_params_)
    ridge = ridge.best_estimator_ if isWithCV else ridge

    print("Ridge regression Training Scores 0: ", ridge.score(x_train, y_train))
    print("Ridge regression Testing score 0:", ridge.score(x_test, y_test))


    #Lasso regression
    lasso_reg = get_lin_model(isWithCV, 'lasso')

    lasso_reg, x_train, y_train, x_test, y_test = simple_model_eval(lasso_reg)

    if (isWithCV):
        print("\n The best estimator for lasso across ALL searched params:\n", lasso_reg.best_params_)
    lasso_reg = lasso_reg.best_estimator_ if isWithCV else lasso_reg

    print("Lasso regression Training Scores 0: ", lasso_reg.score(x_train, y_train))
    print("Lasso regressionTesting score 0:", lasso_reg.score(x_test, y_test))


    #Elastic-net regression
    elastic_net = get_lin_model(isWithCV, 'elasticnet')

    elastic_net, x_train, y_train, x_test, y_test = simple_model_eval(elastic_net)

    if (isWithCV):
        print("\n The best estimator for elastic net across ALL searched params:\n", elastic_net.best_params_)
    elastic_net = elastic_net.best_estimator_ if isWithCV else elastic_net

    print("Elastic-net regression Training Scores 0: ", elastic_net.score(x_train, y_train))
    print("Elastic-net regression Testing score 0:", elastic_net.score(x_test, y_test))


def histograms(df):
    df['connectedDuration'].hist(figsize=(20, 15))
    plt.show()


linear_reg()
