import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math

data = pd.read_csv('Jumps calculating.csv', index_col=0, header=1)
data = data.apply(pd.to_numeric)

fig, ax = plt.subplots()
threshold  = data.iloc[0,0]
offset = threshold*0.05
print(data.shape)

data = data[(data > threshold-offset) & (data < threshold+offset)].fillna(0)
indexNotNaN = np.flatnonzero(data)
x = indexNotNaN // data.shape[1]
y = indexNotNaN % data.shape[1]

x = [data.index[i] for i in x]
# x.append(6660)
print(x)

y = [int(data.columns[i]) for i in y]
# y.append(1)
print(y)

X = np.array([[1, math.log(i), 1/math.sqrt(i)] for i in x])
pX = np.linalg.pinv(X)
w = np.dot(pX, y)
print(w)

tmpX = range(1, 666)
tmpY = np.array([np.dot(np.array([1, math.log(i), 1/math.sqrt(i)]), w) for i in tmpX])

ax.scatter(x, y)
ax.plot(tmpX, tmpY)

plt.show()

print(data)
