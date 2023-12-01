import numpy as np
import statsmodels.api as sm

# Generate some sample data
np.random.seed(42)
n = 100  # number of observations
X = np.random.normal(0, 1, size=(n, 2))  # predictor variables
true_params = np.array([1.5, -0.5])  # true coefficients
linear_pred = np.dot(X, true_params)
y = np.random.gamma(shape=2, scale=np.exp(linear_pred))  # gamma-distributed response variable
new_X = np.random.normal(0, 1, size=(10, 2))
print(y.shape)
print(X.shape)
print(new_X.shape)
# Fit the GLM
glm_model = sm.GLM(y, X, family=sm.families.Gamma())
glm_results = glm_model.fit()

# Print the summary of the model
print(glm_results.summary())

# Make predictions
new_X = np.random.normal(0, 1, size=(10, 2))  # new predictor variables for prediction
predicted_values = glm_results.predict(new_X)

print("Predicted values:")
print(predicted_values)
