import numpy as np

# 行列の足し算、掛け算
A = np.array([1, 2])
B = np.array([3, 4])
y = np.array([3, 4, 5])
print(A + B, A.dot(B), y, sep="\n")

A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])
print(A.dot(B))

# 転置
A = np.arange(1, 7).reshape(2, 3)
print(A, A.T, sep="\n")

# ベクトルの長さ、内積
a = np.array([2, 3])
print(a.dot(a))

# 単位行列、ゼロ行列
A = np.array([[1, 2], [3, 4]])
E = np.eye(2, 2)
Z = np.zeros((3, 3))
print(E, A.dot(E), Z, sep="\n")

# 逆行列（正方行列であることが前提）、正方行列＊逆行列＝単位行列
A = np.array([[1, 2, 3], [2, 4, 2], [-1, -1, 2]])
Ainv = np.linalg.inv(A)
E = A.dot(Ainv)
print(Ainv, E, sep="\n")


# 逆行列を用いた連立方程式の解法
A = np.array([[1, 1], [3, 2]])
C = np.array([10, 23])
b = np.linalg.inv(A) @ C
print(b)
