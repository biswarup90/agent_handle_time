import numpy as np
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from util.utils import split_into_x_y, get_encoded_data, generate_hist
from sklearn import linear_model
import numpy as np
from sklearn.tree import DecisionTreeRegressor
import statsmodels.api as sm
from sklearn.ensemble import GradientBoostingRegressor

isTransformY = False
shouldFilterData = False
df_train, df_test = get_encoded_data(shouldFilterData)

x_train, y_train, x_test, y_test = split_into_x_y(df_train=df_train, df_test=df_test, isTransformY=isTransformY)

# Fit the GLM
model = linear_model.GammaRegressor(max_iter=10000)


model.fit(x_train, y_train)


pred = model.predict(x_test)
mse = mean_squared_error(np.array(y_test), pred)
r2 = r2_score(np.array(y_test), pred)

print("RMSE ", np.sqrt(mse) / 1000, " Sec")
print("R2 ", r2, "\n")

generate_hist(y_train, x_train, y_test, x_test, pred)


