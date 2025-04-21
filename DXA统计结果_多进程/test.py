from ovito.io import import_file
from ovito.modifiers import DislocationAnalysisModifier as DXA
import time
import multiprocessing as mul

pipeline = import_file('./dump/dump_*.shear')
pipeline.modifiers.append(DXA(input_crystal_structure=DXA.Lattice.FCC))

def process_frame(frame):
  data = pipeline.compute(frame=frame)
  return data.attributes['DislocationAnalysis.total_line_length']

if __name__ == '__main__':
  # 设置多进程方法为spawn, 因为ovito与默认的fork方法不兼容
  mul.set_start_method('spawn')
  # 开始计算与运行
  st = time.time()
  with mul.Pool(processes=6) as pool:
    results = pool.map(process_frame, range(pipeline.source.num_frames))
  end = time.time()
  print(f"Cost {end-st}s.")
  # 将结果打印出来
  # for item in results:
  #   print(item)

