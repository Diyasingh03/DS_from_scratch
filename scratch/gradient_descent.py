from scratch.Lin_Alg import dot,Vector, distance, add, subtract, scalar_multiply, vector_mean
import random

def sum_of_squares(v: Vector) -> float:
    return dot(v,v)

from typing import Callable
def difference_quotient(f: Callable[[float], float], x: float, h: float) -> float:
    return (f(x + h) - f(x)) / h

def square(x: float) -> float:
    return x * x
def derivative(x: float) -> float:
    return 2 * x

xs = range(-10, 11)
actuals = [derivative(x) for x in xs]
estimates = [difference_quotient(square, x, h=0.001) for x in xs]

import matplotlib.pyplot as plt
plt.title("Actual Derivatives vs. Estimates")
plt.plot(xs, actuals, 'rx', label='Actual')
plt.plot(xs, estimates, 'b+', label='Estimate')
plt.legend(loc = 9)
# plt.show()

def partial_difference_quotient(f: Callable[[Vector], float], v: Vector, i: int, h: float) -> float:
    w = [v_j + (h if j == i else 0) for j, v_j in enumerate(v)]
    return (f(w) - f(v)) / h

def estimate_gradient(f: Callable[[Vector], float], v: Vector, h: float = 0.0001) -> Vector:
    return [partial_difference_quotient(f, v, i, h) for i in range(len(v))]

def gradient_step(v: Vector, gradient: Vector, step_size: float) -> Vector:
    assert len(v) == len(gradient)
    step = scalar_multiply(step_size, gradient)
    return add(v, step)

def sum_of_squares_gradient(v: Vector) -> Vector:
    return [2 * v_i for v_i in v]

v = [random.uniform(-10, 10) for i in range(3)]
for epoch in range(1000):
    grad = sum_of_squares_gradient(v)
    v = gradient_step(v, grad, -0.01)
    print(epoch, v)
assert distance(v, [0, 0, 0]) < 0.001

#gradient based on error from single point
def linear_gradient(x:float, y:float, theta:Vector) -> Vector:
    slope,intercept = theta
    predicted = slope * x + intercept
    error = predicted - y #predicted - actual
    squared_error = error ** 2 #minimising squared error
    gradient = [2 * error * x, 2 * error] #partial derivative of squared error w.r.t slope and intercept
    return gradient
inputs = [(x,20*x + 5) for x in range(-50, 50)]
theta = [random.uniform(-1,1), random.uniform(-1,1)]
learning_rate = 0.001
# for epoch in range(2000):
#     grad = vector_mean([linear_gradient(x, y, theta) for x, y in inputs])
#     theta = gradient_step(theta, grad, -learning_rate)
#     print(epoch, theta)
# slope, intercept = theta
# assert 19.9 < slope < 20.1
# assert 4.9 < intercept < 5.1

#Minibatch and stochastic gradient descent

from typing import List,Iterator, TypeVar
T = TypeVar('T')
def minibatches(data:List[T], batch_size:int, shuffle:bool = True) -> Iterator[List[T]]:
    #starts i=0, batch_size, 2*batch_size, ...
    batch_starts =[start for start in range(0, len(data), batch_size)]
    if shuffle:
        random.shuffle(batch_starts)
    for start in batch_starts:
        end = start + batch_size
        yield data[start:end] 
# for epoch in range(1000):
#     for batch in minibatches(inputs, 20):
#         grad = vector_mean([linear_gradient(x, y, theta) for x, y in batch])
#         theta = gradient_step(theta, grad, -learning_rate)
#     print(epoch, theta)
# slope, intercept = theta
# assert 19.9 < slope < 20.1
# assert 4.9 < intercept < 5.1

#Stochastic gradient descent
# for epoch in range(100):
#     for x, y in inputs:
#         grad = linear_gradient(x, y, theta)
#         theta = gradient_step(theta, grad, -learning_rate)
#     print(epoch, theta)
# slope, intercept = theta
# assert 19.9 < slope < 20.1
# assert 4.9 < intercept < 5.1

#vecorising would increase performance