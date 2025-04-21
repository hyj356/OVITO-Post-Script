import numpy as np

# FCC晶体中只有4个滑移面
slip_plane = np.array([
  [1,1,1],
  [-1,1,1],
  [1,-1,1],
  [1,1,-1]
])

# FCC中共有12种完美位错的柏氏矢量, 但是撇去正负号的区别, 实际上线性无关的只有6个
perfect_dislocation = 0.5*np.array([
  [1,0,1],
  [-1,1,0],
  [0,1,1],
  [-1,0,1],
  [0,-1,1],
  [1,1,0]
])
# 定义拉伸方向的晶向指数
normal_orientation = np.array([1,0,2])
schmid_factor = []
# 遍历所有滑移面上的所有可滑位错的柏氏矢量
for vector in slip_plane:
  for burgers in perfect_dislocation:
    # 注意要添加下述的判断, 才能保证位错矢量在对应的滑移面上
    if(abs(np.dot(vector, burgers)) < 1e-3):
      cos_λ = np.dot(normal_orientation, burgers) / (np.linalg.norm(normal_orientation, ord=2)*np.linalg.norm(burgers, ord=2))
      cos_Φ = np.dot(normal_orientation, vector) / (np.linalg.norm(normal_orientation, ord=2)*np.linalg.norm(vector, ord=2))
      schmid_factor.append(abs(cos_λ*cos_Φ))
# 将结果打印出来
print(f"The schmid factor is {max(schmid_factor):.5f}, when normal orientation is {normal_orientation}.")