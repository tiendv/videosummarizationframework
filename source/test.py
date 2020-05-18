import h5py
import scipy.io as sio

path = "/mmlabstorage/workingspace/VideoSum/thinhplg/LSTM/data/Data_TVSum_google_p5.h5"
kts_tvsum = "/mmlabstorage/workingspace/VideoSum/thinhplg/LSTM/data/shot_TVSum.mat"

f = h5py.File(path, 'r')
# print(list(f.keys()))
_tvsum_shot_boundaries = sio.loadmat(kts_tvsum)
print(list(_tvsum_shot_boundaries.keys()))
