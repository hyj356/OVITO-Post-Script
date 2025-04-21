from ovito.io import import_file, export_file
from ovito.modifiers import DislocationAnalysisModifier as DXA, SpatialBinningModifier as SBM, SliceModifier as SM
import numpy as np

# 导入轨迹文件
pipeline = import_file("./Tension_20000.gz", input_format="lammps/dump")
# 设置晶体为FCC晶体
pipeline.modifiers.append(DXA(input_crystal_structure=DXA.Lattice.FCC))
# 调用Slice对模型进行切割
pipeline.modifiers.append(SM(distance=101.22, normal = (0, 0, 1), slab_width=50))
# 计算位错密度, 这里我们设置在x和y方向上分别划分50个网格绘制云图
pipeline.modifiers.append(SBM(bin_count=(100,100), direction = SBM.Direction.XY, 
                              operate_on="dislocations"))
data = pipeline.compute(frame=0)
grid_data = data.grids["binning"].view("Density")
# 将计算出来的结果导出到txt中, 以便于用matplotlib进行处理
np.savetxt(X=grid_data, fname="density.txt")
# 导出VTK文件, 以便于用paraview处理
export_file(pipeline, 'dislocation_density.vtk', 'vtk/grid', key='binning')