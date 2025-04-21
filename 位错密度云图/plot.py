import matplotlib.pyplot as plt
import numpy as np

density = np.loadtxt('./density.txt')
plt.imshow(X=density, interpolation="bicubic",vmin=0.0, vmax=0.01,
           extent=[0, 250, 0, 186], cmap="jet")
cbar = plt.colorbar()
cbar.set_label("Dislocation density")
plt.savefig("Density.png", dpi=600)
plt.show()