from typing import List, Tuple, Callable
import math
Vector = List[float]
height_weight_age = [70, 170, 40] # inches, pounds, years
grades = [95, 80, 75, 62] # exam1, exam2, exam3, exam4
def add(v: Vector, w: Vector) -> Vector:
    """Adds corresponding elements"""
    assert len(v) == len(w), "vectors must be the same length"
    return [v_i + w_i for v_i, w_i in zip(v, w)]
assert add([1, 2, 3], [4, 5, 6]) == [5, 7, 9]

def subtract(v: Vector, w: Vector) -> Vector:
    """Subtracts corresponding elements"""
    assert len(v) == len(w), "vectors must be the same length"
    return [v_i - w_i for v_i, w_i in zip(v, w)]
assert subtract([5, 7, 9], [4, 5, 6]) == [1, 2, 3]

def vector_sum(vectors: List[Vector]) -> Vector:
    """Sums all corresponding elements"""
    # Check that vectors is not empty
    assert vectors, "no vectors provided!"
    # Check the vectors are all the same size
    num_elements = len(vectors[0])
    assert all(len(v) == num_elements for v in vectors), "different sizes!"
    # The i-th element of the result is the sum of every vector[i]
    return [sum(vector[i] for vector in vectors)
            for i in range(num_elements)]
assert vector_sum([[1, 2], [3, 4], [5, 6], [7, 8]]) == [16, 20]

def scalar_multiply(c: float, v: Vector) -> Vector:
    """Multiplies every element by c"""
    return [c * v_i for v_i in v]
assert scalar_multiply(2, [1, 2, 3]) == [2, 4, 6]

def vector_mean(vectors: List[Vector]) -> Vector:
    """Computes the element-wise average"""
    n = len(vectors)
    return scalar_multiply(1/n, vector_sum(vectors))
assert vector_mean([[1, 2], [3, 4], [5, 6]]) == [3, 4]

def dot(v: Vector, w: Vector) -> float:
    """Computes v_1 * w_1 + ... + v_n * w_n"""
    assert len(v) == len(w), "vectors must be same length"
    return sum(v_i * w_i for v_i, w_i in zip(v, w))
assert dot([1, 2, 3], [4, 5, 6]) == 32

def sum_of_squares(v: Vector) -> float:
    """Returns v_1 * v_1 + ... + v_n * v_n"""
    return dot(v, v)
assert sum_of_squares([1, 2, 3]) == 14

def magnitude(v: Vector) -> float:
    """Returns the magnitude (or length) of v"""
    return math.sqrt(sum_of_squares(v))
assert magnitude([3, 4]) == 5

def squared_distance(v: Vector, w: Vector) -> float:
    return sum_of_squares(subtract(v, w))

def distance(v: Vector, w: Vector) -> float:
    return math.sqrt(squared_distance(v, w))

def distance(v: Vector, w: Vector) -> float:
    return magnitude(subtract(v, w))

#Matrix
Matrix = List[List[float]]
A = [[1, 2, 3], # A has 2 rows and 3 columns
    [4, 5, 6]]
B = [[1, 2], # B has 3 rows and 2 columns
    [3, 4],
    [5, 6]]
def shape(A: Matrix) -> Tuple[int, int]:
    """Returns (# of rows of A, # of columns of A)"""
    num_rows = len(A)
    num_cols = len(A[0]) if A else 0 # number of elements in first row
    return num_rows, num_cols
assert shape([[1, 2, 3], [4, 5, 6]]) == (2, 3)

def get_row(A: Matrix, i: int) -> Vector:
    """Returns the i-th row of A (as a Vector)"""
    return A[i] # A[i] is already the ith row
def get_column(A: Matrix, j: int) -> Vector:
    """Returns the j-th column of A (as a Vector)"""
    return [A_i[j] # jth element of row A_i
            for A_i in A] # for each row A_i

def make_matrix(num_rows: int,
                num_cols: int,
                entry_fn: Callable[[int, int], float]) -> Matrix:
    """Returns a num_rows x num_cols matrix
    whose (i,j)-th entry is entry_fn(i, j)"""
    return [[entry_fn(i, j) # given i, create a list
            for j in range(num_cols)] # [entry_fn(i, 0), ... ]
            for i in range(num_rows)] # create one list for each i

def identity_matrix(n: int) -> Matrix:
    """Returns the n x n identity matrix"""
    return make_matrix(n, n, lambda i, j: 1 if i == j else 0)
assert identity_matrix(5) == [[1, 0, 0, 0, 0],
                            [0, 1, 0, 0, 0],
                            [0, 0, 1, 0, 0],
                            [0, 0, 0, 1, 0],
                            [0, 0, 0, 0, 1]]
#                0  1  2  3  4  5  6  7  8  9
friend_matrix = [[0, 1, 1, 0, 0, 0, 0, 0, 0, 0], # user 0
                [1, 0, 1, 1, 0, 0, 0, 0, 0, 0], # user 1
                [1, 1, 0, 1, 0, 0, 0, 0, 0, 0], # user 2
                [0, 1, 1, 0, 1, 0, 0, 0, 0, 0], # user 3
                [0, 0, 0, 1, 0, 1, 0, 0, 0, 0], # user 4
                [0, 0, 0, 0, 1, 0, 1, 1, 0, 0], # user 5
                [0, 0, 0, 0, 0, 1, 0, 0, 1, 0], # user 6
                [0, 0, 0, 0, 0, 1, 0, 0, 1, 0], # user 7
                [0, 0, 0, 0, 0, 0, 1, 1, 0, 1], # user 8
                [0, 0, 0, 0, 0, 0, 0, 0, 1, 0]] # user 9
assert friend_matrix[0][2] == 1, "user 0 and user 2 are friends"
assert friend_matrix[0][8] == 0, "user 0 and user 8 are not friends"

friend_of_five = [i for i, is_friend in enumerate(friend_matrix[5]) if is_friend]