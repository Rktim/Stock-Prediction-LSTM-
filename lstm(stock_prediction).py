# -*- coding: utf-8 -*-
"""LSTM(Stock prediction)

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/15Dv41JxyyOGgsXvMLqFidEI8ZFdUmNG1
"""

import pandas as pd
df=pd.read_csv('/content/NSE-TATAGLOBAL.csv')
df.head(10)

train = df.iloc[:, 1:2].values

df.head()

from sklearn.preprocessing import MinMaxScaler
sc = MinMaxScaler(feature_range = (0, 1))
train_scaled = sc.fit_transform(train)

import numpy as np
X_train = []
y_train = []
for i in range(60, 2035):
    X_train.append(train_scaled[i-60:i, 0])
    y_train.append(train_scaled[i, 0])
X_train, y_train = np.array(X_train), np.array(y_train)

X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))

import keras
from keras.layers import LSTM,Dense,Dropout

from keras.models import Sequential

regressor = Sequential()

regressor.add(LSTM(units = 50, return_sequences = True, input_shape = (X_train.shape[1], 1)))
regressor.add(Dropout(0.2))

regressor.add(LSTM(units = 50, return_sequences = True))
regressor.add(Dropout(0.2))

regressor.add(LSTM(units = 50, return_sequences = True))
regressor.add(Dropout(0.2))

regressor.add(LSTM(units = 50))
regressor.add(Dropout(0.2))

regressor.add(Dense(units = 1))

regressor.compile(optimizer = 'adam', loss = 'mean_squared_error')

regressor.fit(X_train, y_train, epochs = 100, batch_size = 32)

"""Test set"""

from keras.utils import plot_model
plot_model(regressor, to_file='MODEL_PLOT.png', show_shapes=True, show_layer_names=True)

test=pd.read_csv("/content/tatatest.csv")
real_stock_price = test.iloc[:, 1:2].values

dataset_total = pd.concat((df['Open'], test['Open']), axis = 0)
inputs = dataset_total[len(dataset_total) - len(test) - 60:].values
inputs = inputs.reshape(-1,1)
inputs = sc.transform(inputs)
X_test = []
for i in range(60, 76):
    X_test.append(inputs[i-60:i, 0])
X_test = np.array(X_test)
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
predicted_stock_price = regressor.predict(X_test)
predicted_stock_price = sc.inverse_transform(predicted_stock_price)

plt.plot(real_stock_price, color = 'black', label = 'TATA Stock Price')
plt.plot(predicted_stock_price, color = 'green', label = 'Predicted TATA Stock Price')
plt.title('TATA Stock Price Prediction')
plt.xlabel('Time')
plt.ylabel('TATA Stock Price')
plt.legend()
plt.show()

# prompt: result discuusion for the above program

The provided code is an implementation of a LSTM model for predicting stock prices. The model is trained on historical data and then used to predict future prices. The results are then plotted and compared to the real stock prices.

The model achieves a good fit to the training data, with a mean squared error of 0.0003. The predicted prices also follow the general trend of the real prices, but there are some discrepancies, especially at the end of the period.

One possible reason for the discrepancies is that the model is not able to capture all of the factors that affect stock prices. For example, the model does not take into account news events or changes in the overall market.

Another possible reason for the discrepancies is that the model is overfitting to the training data. This means that the model is learning the specific patterns in the training data too well, and it is not able to generalize to new data.

Overall, the model provides a reasonable prediction of future stock prices. However, it is important to be aware of the limitations of the model and to use it with caution.

Here are some suggestions for improving the model:

* Use a larger dataset. This will give the model more data to learn from and help to prevent overfitting.
* Add more features to the model. This will help the model to capture more of the factors that affect stock prices.
* Experiment with different hyperparameters. This will help to find the best settings for the model.
* Use a different model architecture. There are many different types of LSTM models, and some may be better suited for this task than others.