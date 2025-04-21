import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import numpy as np


def rotation_matrix_to_align_vector(v:np.ndarray, u:np.ndarray):
    """
    计算将矢量v旋转到矢量u方向且保持矢量长度不变的3x3旋转矩阵, 即满足以下关系:
    u = numpy.matmul(v, R)

    参数:
    v (numpy.ndarray): 原始矢量，形状为(3,)
    u (numpy.ndarray): 目标矢量，形状为(3,)

    返回:
    R (numpy.ndarray): 3x3的旋转矩阵
    """
    # 归一化原始矢量v
    v_norm = v / np.linalg.norm(v)

    # 归一化目标矢量u（如果需要）
    u_norm = u / np.linalg.norm(u)

    # 计算旋转轴
    n = np.cross(v_norm, u_norm)
    n_norm = n / np.linalg.norm(n)

    # 计算旋转角
    cos_theta = np.dot(v_norm, u_norm)
    theta = np.arccos(cos_theta)

    # 构建由旋转轴n_norm组成的反对称矩阵K
    K = np.array([[0, -n_norm[2], n_norm[1]],
                  [n_norm[2], 0, -n_norm[0]],
                  [-n_norm[1], n_norm[0], 0]])

    # 根据罗德里格斯旋转公式计算旋转矩阵R
    I = np.eye(3)
    sin_theta = np.sin(theta)
    cos_theta = np.cos(theta)
    R = np.linalg.inv(I + sin_theta * K + (1 - cos_theta) * K @ K)

    return R

# 设置一开始的拉伸方向
vec1 = np.array([1, 1, 6])
target = np.array([0, 0, 1])
# 计算旋转矩阵
rotation = rotation_matrix_to_align_vector(vec1, target)
#print(np.matmul(vec1, rotation))
# 创建绘图对象
fig = plt.figure()
ax1 = fig.add_subplot(111, projection='3d')

# 绘制汤普森四面体
ax1.plot([0,1],[0,0], [0,1], marker='o', markersize=10)
ax1.plot([0,1],[0,1], [0,0], marker='o', markersize=10)
ax1.plot([0,0],[0,1], [0,1], marker='o', markersize=10)
ax1.plot([1, 1], [1, 0], [0, 1], marker='o', markersize=10)
ax1.plot([1, 0], [1, 1], [0, 1], marker='o', markersize=10)
ax1.plot([1, 0], [0, 1], [1, 1], marker='o', markersize=10)

# 绘制拉伸矢量[1,1,6]
ax1.quiver(0, 0, 0, 1, 1, 6, length = 1, normalize=True, color='black')
ax1.quiver(0, 0, 0, 0, 0, 6.16, length = 1, normalize=True, color='red')
# 计算旋转之后的矢量
plt.show()