from MaxFlow import MaxFlowAdjList
from ProcessImage import GrayScaleImg
import numpy as np



#NEED to add adjacency matrix support for flow network,
# graph is way too sparse otherwise



# gs_img = GrayScaleImg("images/batman.png")
# flowNet = gs_img.makeGraphFromImage()
# print(flowNet.shape)
# mf_finder = MaxFlow(flowNet, 0, flowNet.shape[0] - 1)