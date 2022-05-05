# import numpy as np
# import nibabel as nib
#
# datapath = "C:\\Users\\Seven\\Desktop\\t1_icbm_normal_1mm_pn0_rf0.rawb"
# savepath = "C:\\Users\\Seven\\Desktop\\t1_icbm_normal_1mm_pn0_rf0.nii"
# # LI:读.rawb文件的数据，path是文件所在路径，自己加上就可以
# img_data = np.fromfile(datapath, dtype='uint8')
# # LI:将一维数据转换成三维数据，z*y*x：181*217*181
# data_new_shape = img_data.reshape(181, 217, 181)
# # LI:转换成nii图像，并存储
# raw_affine = np.diag([-1, -1, 1, 1])
# array_img = nib.Nifti1Image(data_new_shape, raw_affine)
# nib.save(array_img, savepath)
import numpy as np
import random
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import time

# 随机颜色
def randomcolor():
    colorArr = ['1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']
    color = ""
    for i in range(6):
        color += colorArr[random.randint(0,14)]
    return "#"+color

# N表示阵元数目，M表示
N = 128
M = 128
R = 10
ALL_NUM = N * M

# 随机产生N*M个0~1范围内的坐标
theta = np.array(random.sample(range(0,ALL_NUM), ALL_NUM))/ALL_NUM
radius = R * np.sqrt(np.array(random.sample(range(0,ALL_NUM), ALL_NUM))/ALL_NUM)
X = radius * np.sin(theta * 2 * np.pi - np.pi)
Y = radius * np.cos(theta * 2 * np.pi - np.pi)
points = np.zeros((ALL_NUM, 2))
points[:,0]=X
points[:,1]=Y

# K-means聚类并计时,聚类中心随机，数目为N
begin = time.clock()
kmeans = KMeans(n_clusters=N, random_state=0).fit(points)
end = time.clock()
print('耗时%.3f s' % ((end-begin)))

# 画图，plt.scatter用法参考https://www.runoob.com/matplotlib/matplotlib-scatter.html
for index in range(N):
    plt.scatter(X[np.where(kmeans.labels_ == index)[0]],
                Y[np.where(kmeans.labels_ == index)[0]],
                s = 2,
                c = randomcolor(),
                cmap = 'gist_ncar')
plt.show()