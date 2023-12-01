from sklearn import linear_model
from util.utils import split_into_x_y, get_encoded_data
from constants.constants import *
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import GradientBoostingRegressor
import xgboost as xgb
import numpy as np
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score

isTransformY = False
shouldFilterData = True
df_train, df_test = get_encoded_data(shouldFilterData)

x_train, y_train, x_test, y_test = split_into_x_y(df_train=df_train, df_test=df_test, isTransformY=isTransformY)

for item in ['agent_encoded', 'team_encoded', 'queue_encoded', 'Operator', 'T2', 'holdCount']:
  print(item)
  model = linear_model.LinearRegression()
  X = np.array(x_train[item]).reshape(-1, 1)
  Y = np.array(y_train).reshape(-1, 1)

  model.fit(X, Y)
  pred = model.predict(np.array(x_test[item]).reshape(-1, 1))
  mse = mean_squared_error(y_test, pred)
  r2 = r2_score(y_test, pred)

  print("RMSE ", np.sqrt(mse) / 1000, " Sec")
  print("R2 ", r2, "\n")
