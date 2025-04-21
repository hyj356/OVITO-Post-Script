from ovito.pipeline import Pipeline
from ovito.io import import_file
from ovito.modifiers import CommonNeighborAnalysisModifier as CNA
import multiprocessing as mul

def compute_CNA(item:tuple)-> tuple[int, int, int, int, int]:
  i, step, filename = item
  single_frame:str = filename.replace('*', str(i*step))
  pipeline:Pipeline = import_file(single_frame, input_format="lammps/dump")
  pipeline.modifiers.append(CNA())
  data = pipeline.compute()
  fcc_count:int = data.attributes['CommonNeighborAnalysis.counts.FCC']
  bcc_count:int = data.attributes['CommonNeighborAnalysis.counts.BCC']
  hcp_count:int = data.attributes['CommonNeighborAnalysis.counts.HCP']
  ico_count:int = data.attributes['CommonNeighborAnalysis.counts.ICO']
  other_count:int = data.attributes['CommonNeighborAnalysis.counts.OTHER']

  return (fcc_count, bcc_count, hcp_count, ico_count, other_count)

def multicore_compute_CNA(filename:str, step:int, cores:int) -> list[tuple[int, int, int, int, int]]:
  # 必须以通配符的形式将轨迹文件名传入
  if not '*' in filename:
    raise ValueError("You must provide a track file name template that contains the wildcard '*'.")
  # 获取轨迹文件的帧数
  tmp_pipeline = import_file(filename, input_format="lammps/dump")
  frames = tmp_pipeline.source.num_frames
  print(f"There are totoal {frames} frames.")
  # 设置每次循环需要用到的参数
  filelist:list = [(i, step, filename) for i in range(frames)]
  # 创建进程池
  with mul.Pool(processes=cores) as pool:
  # 将参数序列并行的映射到目标函数中执行
    result = pool.map(func=compute_CNA, iterable=filelist)
  return result

if __name__ == '__main__':
  # 设置轨迹文件的字符串模板
  filename:str = './dump/dump_*.shear'
  step:int = 500
  # 调用多核计算函数
  result = multicore_compute_CNA(filename=filename, step=step, cores=4)
  # 执行完毕, 将结果写入到文本文件中
  with open("CNA_result1.txt", 'w') as fdata:
    fdata.write('#Frame FCC BCC HCP ICO OTHER\n')
    for i, count in enumerate(result):
      fdata.write(f"{i} {count[0]} {count[1]} {count[2]} {count[3]} {count[4]}\n")
