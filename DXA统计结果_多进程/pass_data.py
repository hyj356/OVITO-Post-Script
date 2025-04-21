from ovito.io import import_file
from ovito.pipeline import Pipeline
from ovito.modifiers import DislocationAnalysisModifier as DXA
import multiprocessing as mul


def compute_DXA(item:tuple[int, Pipeline]):
  frame, pipeline = item  # 获取数据
  data = pipeline.compute(frame=frame)  # 进行计算
  # 获取不同种类的位错的长度
  length_of_1_2_110:float = data.attributes['DislocationAnalysis.length.1/2<110>']
  length_of_1_3_100:float = data.attributes['DislocationAnalysis.length.1/3<100>']
  length_of_1_3_111:float = data.attributes['DislocationAnalysis.length.1/3<111>']
  length_of_1_6_110:float = data.attributes['DislocationAnalysis.length.1/6<110>']
  length_of_1_6_112:float = data.attributes['DislocationAnalysis.length.1/6<112>']
  length_of_other:float = data.attributes['DislocationAnalysis.length.other']
  length_of_total:float = data.attributes['DislocationAnalysis.total_line_length']
  # 将结果打包返回
  return (length_of_1_2_110, length_of_1_3_100, length_of_1_3_111, length_of_1_6_110, length_of_1_6_112, length_of_other, length_of_total)

if __name__ == "__main__":
  # 定义轨迹文件的模板
  filename = './dump/dump_*.shear'
  # 导入文件
  pipeline = import_file(filename, input_format='lammps/dump')
  pipeline.modifiers.append(DXA(input_crystal_structure=DXA.Lattice.FCC))
  # 构建输入列表
  input_list = [(i, pipeline) for i in range(pipeline.source.num_frames)]
  # 开启多线程, 开始执行函数
  with mul.Pool(processes=4) as pool:
    result = pool.map(compute_DXA, input_list)
