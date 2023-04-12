
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from utils import model_with_kmeans_eval, simple_model_eval


def get_model(isWithCV):
    if isWithCV:
        parameters = [{'solver': ['newton-cg', 'lbfgs', 'liblinear', 'sag', 'saga']},
                      {'penalty': ['none', 'elasticnet', 'l1', 'l2']},
                      {'C': [0.001, 0.01, 0.1, 1, 10, 100]}]
        lr = LogisticRegression()
        return GridSearchCV(estimator=lr, param_grid=parameters, scoring='r2', verbose=1, n_jobs=-1, cv=5).best_estimator_
    else:
        print("Without CV")
        return LogisticRegression(tol=0.0001)


def linear_reg_with_kmeans():
    # Linear regression
    linear_reg_0 = get_model(False)
    linear_reg_1 = get_model(False)

    linear_reg_0, linear_reg_1, x_train_0, y_train_0, x_train_1, y_train_1, x_test_0, y_test_0, x_test_1, y_test_1 \
        = model_with_kmeans_eval(linear_reg_0, linear_reg_1)

    print("Linear Regression Training Scores 0: ", linear_reg_0.score(x_train_0, y_train_0))
    print("Linear Regression Training Scores 1: ", linear_reg_1.score(x_train_1, y_train_1))

    print("Linear Regression Testing score 0:", linear_reg_0.score(x_test_0, y_test_0))
    print("Linear Regression Testing score 1:", linear_reg_1.score(x_test_1, y_test_1))

    # Ridge regression
    ridge_reg_0 = get_model(True, 'ridge')
    ridge_reg_1 = get_model(True, 'ridge')

    ridge_reg_0, ridge_reg_1, x_train_0, y_train_0, x_train_1, y_train_1, x_test_0, y_test_0, x_test_1, y_test_1 \
        = model_with_kmeans_eval(ridge_reg_0, ridge_reg_1)

    print("Ridge regression Training Scores 0: ", ridge_reg_0.score(x_train_0, y_train_0))
    print("Ridge regression Training Scores 1: ", ridge_reg_1.score(x_train_1, y_train_1))

    print("Ridge regression Testing score 0:", ridge_reg_0.score(x_test_0, y_test_0))
    print("Ridge regression Testing score 1:", ridge_reg_1.score(x_test_1, y_test_1))

    # Lasso regression
    lasso_reg_0 = get_model(True, 'lasso')
    lasso_reg_1 = get_model(True, 'lasso')

    lasso_reg_0, lasso_reg_1, x_train_0, y_train_0, x_train_1, y_train_1, x_test_0, y_test_0, x_test_1, y_test_1 \
        = model_with_kmeans_eval(lasso_reg_0, lasso_reg_1)

    print("Lasso regression Training Scores 0: ", lasso_reg_0.score(x_train_0, y_train_0))
    print("Lasso regression Training Scores 1: ", lasso_reg_1.score(x_train_1, y_train_1))

    print("Lasso regression Testing score 0:", lasso_reg_0.score(x_test_0, y_test_0))
    print("Lasso regression Testing score 1:", lasso_reg_1.score(x_test_1, y_test_1))

    #Elastic net Linear regression
    el_reg_0 = get_model(True, 'elastic')
    el_reg_1 = get_model(True, 'elastic')

    el_reg_0, el_reg_1, x_train_0, y_train_0, x_train_1, y_train_1, x_test_0, y_test_0, x_test_1, y_test_1 \
        = model_with_kmeans_eval(el_reg_0, el_reg_1)

    print("Elastic net Training Scores 0: ", el_reg_0.score(x_train_0, y_train_0))
    print("Elastic net Training Scores 1: ", el_reg_1.score(x_train_1, y_train_1))

    print("Elastic net Testing score 0:", el_reg_0.score(x_test_0, y_test_0))
    print("Elastic net Testing score 1:", el_reg_1.score(x_test_1, y_test_1))

def logistic_reg(isWithCV):
    #logistic regression
    lr = get_model(isWithCV)

    lr, x_train, y_train, x_test, y_test = simple_model_eval(lr)

    print("Logistic regression Training Scores 0: ", lr.score(x_train, y_train))
    print("Logistic Regression Testing score 0:", lr.score(x_test, y_test))

    if (isWithCV):
        print("\nGradient Booster The best estimator across ALL searched params:\n", lr.best_params_)



logistic_reg(False)
