import numpy as np
import pandas as pd
from csv import writer
       
def mean_error(y, curr_y):
    error = 0
    for i in range(len(y)):
        error += abs(y[i] - curr_y[i])
    return error / len(y)

def predict(X, y, x):
    weights = np.zeros(X.shape[1])
    free_coef = 0
    curr_y = None
    
    for i in range(1000):
        curr_y = np.dot(X, weights) + free_coef
        
        inacc_weight = (2 * np.dot(X.T, (curr_y - y))) / X.shape[0]
        inacc_FC = (2 * np.sum(curr_y - y)) / X.shape[0]
        weights -= 0.01 * inacc_weight
        free_coef -= 0.01 * inacc_FC

    return (np.dot(x, weights) + free_coef, mean_error(y, curr_y))

data = pd.read_csv('result.csv')
data['time'] = data['time'].div(100).round(6)
X = data[['hp', 'kill', 'time']].to_numpy()
Y = data['score'].to_numpy()

X_train = X[:-5]
X_test = X[-5:]
Y_train = Y[:-5]
Y_test = Y[-5:]

prediction = predict(X_train, Y_train, X_test)
df_predicted = pd.DataFrame({'hp': X_test[:, 0], 'kill': X_test[:, 1], 'time': X_test[:, 2] * 100, 'real_score': Y_test, 'prediced_score': prediction[0]})
print(df_predicted)
print("Inaccuracy = " + str(prediction[1]))

df_predicted.to_csv("predict.csv", index = False)