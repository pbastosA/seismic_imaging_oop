import numpy as np
import matplotlib.pyplot as plt

files = [["point_shots", "point_nodes"], ["xLine_shots", "xLine_nodes"], 
         ["yLine_shots", "yLine_nodes"], ["carpet_shots", "carpet_nodes"], 
         ["reciprocity_carpet_shots", "reciprocity_carpet_nodes"],  
         ["circular_shots", "circular_nodes"]]

fig, axs = plt.subplots(2,3, figsize = (13, 8))

titles = ["Point geometry", "xline geometry", "yline geometry", 
          "carpet geometry", "carpet reciprocity geometry", "circular geometry"]

ind = 0
for i in range(len(axs)):
    for j in range(len(axs[0])):
        [xs, ys, zs] = np.loadtxt(f"outputs/{files[ind][0]}.txt", delimiter = ",", unpack = True)    
        [xr, yr, zr] = np.loadtxt(f"outputs/{files[ind][1]}.txt", delimiter = ",", unpack = True)    

        axs[i,j].scatter(xs, ys, c = 'green')
        axs[i,j].scatter(xr, yr, c = 'black')
    
        axs[i,j].set_xlim([0,10000])
        axs[i,j].set_ylim([0,10000])

        axs[i,j].set_xlabel("x coordinate [m]", fontsize = 12)
        axs[i,j].set_ylabel("y coordinate [m]", fontsize = 12)
        axs[i,j].set_title(titles[ind], fontsize = 15)

        ind += 1

plt.tight_layout()
plt.savefig("allGeometries.png", dpi = 200)
plt.show(block = False)