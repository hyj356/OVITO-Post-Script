from ovito.pipeline import Pipeline
from ovito.io import import_file
from ovito.modifiers import DislocationAnalysisModifier as DXA
import glob
import multiprocessing as mul
import time

def compute_DXA(single_frame:str):
  # 导入轨迹文件
  pipeline:Pipeline = import_file(single_frame, input_format="lammps/dump")
  # 添加DXA分析模块, 注意这里我们需要手动选择的DXA输入晶体类型为FCC
  pipeline.modifiers.append(DXA(input_crystal_structure=DXA.Lattice.FCC))
  # 开始计算
  data = pipeline.compute(frame=0)
  # 获取当前轨迹的帧数
  step:int = data.attributes['Timestep']
  # 获取不同种类的位错的长度
  length_of_1_2_110:float = data.attributes['DislocationAnalysis.length.1/2<110>']
  length_of_1_3_100:float = data.attributes['DislocationAnalysis.length.1/3<100>']
  length_of_1_3_111:float = data.attributes['DislocationAnalysis.length.1/3<111>']
  length_of_1_6_110:float = data.attributes['DislocationAnalysis.length.1/6<110>']
  length_of_1_6_112:float = data.attributes['DislocationAnalysis.length.1/6<112>']
  length_of_other:float = data.attributes['DislocationAnalysis.length.other']
  length_of_total:float = data.attributes['DislocationAnalysis.total_line_length']
  # 将结果打包返回
  return (step, length_of_1_2_110, length_of_1_3_100, length_of_1_3_111, length_of_1_6_110, length_of_1_6_112, length_of_other, length_of_total)

if __name__ == '__main__':
  # 定义轨迹文件名称
  filename = './dump/dump_*.shear'
  # 必须以含有通配符的形式将轨迹文件名传入
  if not '*' in filename:
    raise ValueError("You must provide a track file name template that contains the wildcard '*'.")
  # 获取轨迹文件的帧数
  tmp_pipeline = import_file(filename, input_format="lammps/dump")
  frames = tmp_pipeline.source.num_frames
  print(f"There are totoal {frames} frames.")
  # 调用普通for循环进行计算数据
  st = time.perf_counter()
  result_list = []
  tmp_pipeline.modifiers.append(DXA(input_crystal_structure=DXA.Lattice.FCC))
  for i in range(frames):
    data = tmp_pipeline.compute(frame=i)
  ed = time.perf_counter()
  print(f'For loop cost {ed-st} seconds.')
  # 搜索符合条件的所有轨迹文件名构成的列表
  if frames != 0:
    filelist:list = glob.glob(filename)
  # 创建进程池
  st = time.perf_counter()
  with mul.Pool(processes=6) as pool:
  # 将参数序列并行的映射到目标函数中执行
    result = pool.map(func=compute_DXA, iterable=filelist)
  ed = time.perf_counter()
  print(f'multiprocessing cost {ed-st} seconds.')
  # 对输出的结果进行排序
  result = sorted(result, key=lambda x:x[0])
  # 打开文件将结果写入到txt里面
  with open("tmp.txt", 'w') as fdata:
    fdata.write('#Step 1/2<110> 1/3<100> 1/3<111> 1/6<110> 1/6<112> other Total\n')
    for length in result:
      fdata.write(f'{length[0]} {length[1]} {length[2]} {length[3]} {length[4]} {length[5]} {length[6]} {length[7]}\n')
