import numpy as np
import matplotlib.pyplot as plt

from all_functions import boxPlot, readBinaryArray, readBinaryMatrix, readBinaryVolume, analyticalRefraction

nx = 481
ny = 41
nz = 51

dh = 12.5

v = np.array([2000,3500])
z = np.array([500]) 

refractiveModel = np.zeros((nz,nx,ny))

refractiveModel[:int(z[0]/dh),:,:] = v[0]
refractiveModel[int(z[0]/dh):,:,:] = v[1]

refractiveModel.flatten("F").astype("float32", order = "F").tofile(f"../../inputs/models/refractiveModel_{nz}x{nx}x{ny}_{dh:.1f}m.bin")

shots = np.loadtxt("../../outputs/geometry/shots.txt", delimiter = ",")
nodes = np.loadtxt("../../outputs/geometry/nodes.txt", delimiter = ",")

dh = np.array([dh,dh,dh])
slices = np.array([int(nz/2), int(nx/2), int(ny/2)], dtype = int)

n = 112272

xRay = readBinaryArray(n, f"../../outputs/rayPosition/xRay_{n}_shot_1.bin")
yRay = readBinaryArray(n, f"../../outputs/rayPosition/yRay_{n}_shot_1.bin")
zRay = readBinaryArray(n, f"../../outputs/rayPosition/zRay_{n}_shot_1.bin")
iRay = readBinaryArray(n, f"../../outputs/rayPosition/iRay_{n}_shot_1.bin")

xzRay = np.zeros((2, n))

xzRay[0,:] = xRay
xzRay[1,:] = zRay

eikonal = readBinaryVolume(nz,nx,ny,f"../../outputs/travelTimes/eikonal_nz{nz}_nx{nx}_ny{ny}_shot_1.bin")

# boxPlot(refractiveModel, dh, shots, nodes, slices, xzRay, eikonal, colorbarFix = 2.0)
# # print it
# plt.show()

#--------------------------------

offsets = nodes[:,0] - shots[0]

td, tr = analyticalRefraction(v,z,offsets)

analyticalArrivals = np.zeros(len(offsets))

for i in range(len(offsets)):
    if td[i] < tr[0,i]:
        analyticalArrivals[i] = td[i]
    else:
        analyticalArrivals[i] = tr[0,i]
        
dt = 1e-3        
nt = 2501
ns = 330
ntf = 2001

seismic = readBinaryMatrix(nt,len(offsets), f"../../inputs/seismograms/zeroPhase_seismogram_{nt}x{len(offsets)}_shot_1.bin")

seismic = seismic[int(ns/2):,:] # removing anti causal 
seismic = seismic[:ntf,:]
seismic[1700:,:40] = 5e-6

perc = 0.5 * np.std(seismic)

plt.figure(2, figsize = (10, 8))

plt.imshow(seismic, aspect = "auto", cmap = "Greys", vmin = -perc, vmax = perc)

plt.plot(analyticalArrivals/dt)

# plt.gca().invert_yaxis()
plt.show()
