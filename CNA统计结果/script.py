from ovito.io import import_file
from ovito.modifiers import CommonNeighborAnalysisModifier as CNA, ReplicateModifier as RM
from tqdm import tqdm

if __name__ == '__main__':
  pipeline = import_file('./dump/dump_*.shear')
  frames = pipeline.source.num_frames
  # 将原子的数量增加为原来的27倍, 这样可以让OVITO算的久一点, 就可以看到更稳定的CPU利用率情况
  pipeline.modifiers.append(RM(num_x=2, num_y=2, num_z=2))
  # 调用CNA进行计算
  pipeline.modifiers.append(CNA())
  # 开始计算
  with open("CNA_result.txt", 'w') as fdata:
    fdata.write('#Frame FCC BCC HCP ICO OTHER\n')
    # 如果没有tqdm库又不想安装的话, 将下列for循环改为for in range(frames): 即可
    for i in tqdm(range(frames), desc="Calcalating CNA......"):
      data = pipeline.compute(frame=i)
      fcc_count:int = data.attributes['CommonNeighborAnalysis.counts.FCC']
      bcc_count:int = data.attributes['CommonNeighborAnalysis.counts.BCC']
      hcp_count:int = data.attributes['CommonNeighborAnalysis.counts.HCP']
      ico_count:int = data.attributes['CommonNeighborAnalysis.counts.ICO']
      other_count:int = data.attributes['CommonNeighborAnalysis.counts.OTHER']
      fdata.write(f'{i} {fcc_count} {bcc_count} {hcp_count} {ico_count} {other_count}\n')
