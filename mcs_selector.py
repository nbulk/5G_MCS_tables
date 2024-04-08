import numpy as np
import h5py

mcs_table = np.genfromtxt("5G_MCS_tables/mcs_index_1.csv", delimiter=",")
mcs_table = mcs_table[1:]
mcs_table = mcs_table[:,1:3]

coderate = mcs_table[:,1]/1024

mcs_table[:,1] = coderate

#REMOVE Coderate <1/5 and >11/12

lower_bound = np.where(mcs_table[:,1]<1/5)
upper_bound = np.where(mcs_table[:,1]>11/12)

mcs_table = np.delete(mcs_table,upper_bound,0)
mcs_table = np.delete(mcs_table,lower_bound,0)

temp = np.ones((4))*-5
mcs_config = np.ones((4))*-5

for i in range(0, mcs_table.shape[0]):
    for j in range(0, mcs_table.shape[0]):
        temp[0:2] = mcs_table[i]
        temp[2:4] = mcs_table[j]
        mcs_config = np.vstack((mcs_config, temp))

mcs_config = np.delete(mcs_config, 0, 0)
qm_bound = np.where(mcs_config[:,0]+mcs_config[:,2]>8)
mcs_config = np.delete(mcs_config, qm_bound, 0)


oma_modulation = mcs_config[:,0]+mcs_config[:,2]
oma_coderate = (mcs_config[:,0]*mcs_config[:,1]+mcs_config[:,2]*mcs_config[:,3])/oma_modulation
oma_modulation = oma_modulation.reshape(-1,1)
oma_coderate = oma_coderate.reshape(-1,1)
oma_equivalent = np.hstack((oma_modulation,oma_coderate))

file = h5py.File("noma_mcs_config.hdf", "w")
dataset = file.create_dataset("noma_mcs", data=mcs_config)
dataset = file.create_dataset("oma_equivalent", data=oma_equivalent)
file.close()