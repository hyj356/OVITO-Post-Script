from ovito.io import import_file
from ovito.data import CutoffNeighborFinder as CNF, DataCollection
from ovito.modifiers import AtomicStrainModifier as ASM
import numpy as np
from math import sqrt

def calculate_jacobi(list0:CNF, deform_frame:DataCollection, index:int) :
  '''
  此函数用于计算从参考帧变换到变形帧的3x3的Jacobi矩阵
  list0: 参考帧构建的近邻列表
  list0: 变形帧构建的近邻列表
  index: 计算id为index的原子的原子应变
  '''
  neigh_id = []
  delta_ji0, delta_ji1 = [], []
  # 遍历参考帧的近邻列表, 计算参考帧的近邻原子和中心原子之间的向量
  for neigh0 in list0.find(index=index):
    neigh_id.append(neigh0.index)
    delta_ji0.append(-neigh0.delta) # 默认的delta是d_ij, 加一个负号变成d_ji
  # 获取变形帧的原子位置信息
  position = deform_frame.particles
  # 遍历变形帧的原子位置信息, 计算变形帧的近邻原子和中心原子之间的向量
  for neigh in neigh_id:
    delta_ji1.append(position.delta_vector(neigh, index, cell=deform_frame.cell, return_pbcvec=False))
  # 转为numpy矩阵
  delta_ji0, delta_ji1 = np.array(delta_ji0), np.array(delta_ji1)
  # 计算两个系数矩阵
  factor_matrix0, factor_matrix1 = np.zeros((3, 3)), np.zeros((3, 3))
  # 遍历所有的邻居向量
  for delta0, delta1 in zip(delta_ji0, delta_ji1):
    factor_matrix0 += np.outer(delta0, delta0)
    factor_matrix1 += np.outer(delta0, delta1)
  # 计算雅可比矩阵
  jacobi = np.matmul(np.linalg.inv(factor_matrix0), factor_matrix1)
  # 计算应变矩阵
  strain = 0.5 * (np.matmul(jacobi, jacobi.T) - np.eye(3, 3))
  return strain

def calculate_shear_volume_strain(strain_matrix):
  '''
  根据输入的3x3的应变矩阵strain_matrix计算原子的剪切和体积应变
  '''
  # 获取拉伸应变分量
  xx, yy, zz = strain_matrix[0, 0], strain_matrix[1, 1], strain_matrix[2, 2]
  # 获取剪切应变分量
  xy, xz, yz = strain_matrix[0, 1], strain_matrix[0, 2], strain_matrix[1, 2]
  # 计算体积应变
  volume_strain = (xx + yy + zz) / 3
  # 计算剪切应变
  shear_strain = sqrt(xy**2 + xz**2 + yz**2 + ((yy-zz)**2 + (xx-zz)**2 + (xx-yy)**2)/6)

  return volume_strain, shear_strain


if __name__ == "__main__":
  # 定义计算原子应变的截断半径
  cutoff = 3.0
  # 导入轨迹文件
  pipeline = import_file("./Deform_*.gz", sort_particles=True)
  # 添加原子应变模块, 设置截断半径为3埃
  pipeline.modifiers.append(ASM(cutoff=cutoff, reference_frame=0))
  # 获得参考帧和变形帧的原子位置信息
  data0, data1 = pipeline.compute(frame=0), pipeline.compute(frame=1)
  # 构建两个参考帧在当前截断半径设置下的邻居列表
  neigh_list0, neigh_list1 = CNF(cutoff=cutoff, data_collection=data0), CNF(cutoff=cutoff, data_collection=data1)
  a = calculate_jacobi(neigh_list0, data1, 0)
  print(a)
  volume, shear = calculate_shear_volume_strain(strain_matrix=a)
  # 计算第1个原子的原子应变
  print(volume, shear)
  # 参考值
  # -0.0426481 0.0987744 -0.0250645 -0.00380163 0.00451191 -0.00357163
  # Volume strain : 0.0103539
  # Shear strain  : 0.0773854

