from MaxFlow import MaxFlowAdjList
from ProcessImage import GrayScaleImg
import numpy as np
from PIL import Image



#NEED to add adjacency matrix support for flow network,
# graph is way too sparse otherwise

filename = "images/hooman100x50.png"
gs_img = GrayScaleImg(filename)
flowNet = gs_img.getAdjList()
#print(flowNet)

mf_finder = MaxFlowAdjList(flowNet, 0, len(flowNet) - 1)
min_cut = mf_finder.getMinCut()
#print(min_cut)
img_copy = Image.open(filename).convert('L')
img_copy_arr = np.array(img_copy)

copy_index = 1
for i in range(img_copy_arr.shape[0]):
    for j  in range(img_copy_arr.shape[1]):
        if (min_cut[copy_index] == 1):
            #foreground => white
            img_copy_arr[i, j] = 255
        else:
            #background => black
            img_copy_arr[i, j] = 0
        copy_index+=1

new_img = Image.fromarray(img_copy_arr, mode="L")
new_img.show()
