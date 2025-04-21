from ovito.io import import_file
from ovito.modifiers import DislocationAnalysisModifier as DXA
from tqdm import tqdm

if __name__ == '__main__':
  pipeline = import_file('./dump/dump_*.shear')
  frames = pipeline.source.num_frames
  # 注意这里输入的晶体类型是FCC
  pipeline.modifiers.append(DXA(input_crystal_structure=DXA.Lattice.FCC))
  # 打开文件将结果写入到txt里面
  with open("DXA_result.txt", 'w') as fdata:
    fdata.write('#Frame 1/2<110> 1/3<100> 1/3<111> 1/6<110> 1/6<112> other Total\n')
    for i in tqdm(range(frames), desc="Calcalating DXA......"):
      # 计算第i帧轨迹文件的结果
      data = pipeline.compute(frame=i)
      # 获取盒子体积以用于计算位错密度
      volume:float = data.attributes['DislocationAnalysis.cell_volume'] 
      # 获取不同种类的位错的长度
      length_of_1_2_110:float = data.attributes['DislocationAnalysis.length.1/2<110>']
      length_of_1_3_100:float = data.attributes['DislocationAnalysis.length.1/3<100>']
      length_of_1_3_111:float = data.attributes['DislocationAnalysis.length.1/3<111>']
      length_of_1_6_110:float = data.attributes['DislocationAnalysis.length.1/6<110>']
      length_of_1_6_112:float = data.attributes['DislocationAnalysis.length.1/6<112>']
      length_of_other:float = data.attributes['DislocationAnalysis.length.other']
      length_of_total:float = data.attributes['DislocationAnalysis.total_line_length']
      fdata.write(f'{i} {length_of_1_2_110} {length_of_1_3_100} {length_of_1_3_111} {length_of_1_6_110} {length_of_1_6_112} {length_of_other} {length_of_total}\n')
      
