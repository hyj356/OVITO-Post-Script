from ovito.pipeline import Pipeline
from ovito.io import import_file
from ovito.modifiers import DislocationAnalysisModifier as DXA
import glob
import time
import multiprocessing as mul
import argparse 

def compute_DXA(single_frame:str):
  # 导入轨迹文件
  pipeline:Pipeline = import_file(single_frame, input_format="lammps/dump")
  # 添加DXA分析模块, 注意这里我们需要手动选择的DXA输入晶体类型为FCC
  pipeline.modifiers.append(DXA(input_crystal_structure=DXA.Lattice.HCP))
  # 开始计算
  data = pipeline.compute(frame=0)
  # 获取当前轨迹的帧数
  step:int = data.attributes['Timestep']
  # 获取不同种类的位错的长度
  length_of_1_3_1100:float = data.attributes['DislocationAnalysis.length.1/3<-1100>']
  length_of_1_3_1120:float = data.attributes['DislocationAnalysis.length.1/3<11-20>']
  length_of_1_3_1123:float = data.attributes['DislocationAnalysis.length.1/3<11-23>']
  length_of_1100:float = data.attributes['DislocationAnalysis.length.<-1100>']
  length_of_0001:float = data.attributes['DislocationAnalysis.length.<0001>']
  length_of_other:float = data.attributes['DislocationAnalysis.length.other']
  length_of_total:float = data.attributes['DislocationAnalysis.total_line_length']
  # 将结果打包返回
  return (step, length_of_1_3_1100, length_of_1_3_1120, length_of_1_3_1123, length_of_1100, length_of_0001, length_of_other, length_of_total)

def multicore_compute_DXA(filename:str, cores:int):
  # 必须以通配符的形式将轨迹文件名传入
  if not '*' in filename:
    raise ValueError("You must provide a track file name template that contains the wildcard '*'.")
  # 获取轨迹文件的帧数
  tmp_pipeline = import_file(filename, input_format="lammps/dump")
  frames = tmp_pipeline.source.num_frames
  print(f"There are totoal {frames} frames.")
  # 搜索符合条件的所有轨迹文件名构成的列表
  if frames != 0:
    filelist:list = glob.glob(filename)
  # 创建进程池
  with mul.Pool(processes=cores) as pool:
  # 将参数序列并行的映射到目标函数中执行
    result = pool.map(func=compute_DXA, iterable=filelist)
  # 由于多进程执行的顺序并不是固定的, 所以需要对其进行排序
  result = sorted(result, key=lambda x:x[0])
  # 返回结果
  return result

def read_parameter():
  # 创建ArgumentParser对象
  parser = argparse.ArgumentParser(description='Select the number of processes.')
  # 设置用户应该输入的参数
  parser.add_argument('-n', '--nthreads', dest='cores', 
                       type=int, help='The number of processes open simultaneously.')
  parser.add_argument('-f', '--file', dest='filename', 
                      type=str, help="The filename of the track file.")
  # 获取所有参数
  args = parser.parse_args()
  # 对命令行的参数进行解析
  if args.cores and args.filename:
    return args.cores, args.filename
  else:
    parser.print_help()
    exit()

if __name__ == '__main__':
  # 从命令行获取进程数量
  cores, filename = read_parameter()
  print(f'{cores} processes will be called to process the track file: {filename} in parallel.')
  # 开始计算与运行
  st = time.time()
  # 调用cores核进行计算
  result = multicore_compute_DXA(filename=filename, cores=cores)
  end = time.time()
  print(f"Cost {end-st}s.")
  # 打开文件将结果写入到txt里面
  with open("DXA_result_HCP.txt", 'w') as fdata:
    fdata.write('#Step 1/3<-1100> 1/3<11-20> 1/3<11-23> <-1100> <0001> other Total\n')
    for length in result:
      fdata.write(f'{length[0]} {length[1]} {length[2]} {length[3]} {length[4]} {length[5]} {length[6]} {length[7]}\n')
