import numpy as np
from matplotlib import pyplot as plt

from PIL import Image

# filename = "images/black_circle.png"
# img = Image.open(filename).convert('L')
# img_arr = np.array(img) # these are our intensities
# img.save('greyscale.png')

#get gray scale intensity histogram of image

class GrayScaleImg:
    #@param img => grayscale MxN dimension image
    def __init__(self, img_filename):
        self.img = Image.open(img_filename).convert('L')
        self.intensities = np.array(self.img)
        self.histogram = []
        self.adjMatrix = None
        self.adjList = []

    #creates adjacency list from image 
    def getAdjList(self):
        if (self.adjList == []):
            # take care of s to vertex edges
            s = {}
            cols = self.intensities.shape[1]
            rows = self.intensities.shape[0]
            # remember that id = 0 is assigned to s, so
            # id's for pixels starts from 1
            id = 0
            # loop over all pixels in img
            for i in range(0, rows):
                for j in range(0, cols):
                    id += 1
                    s[id] = 100*self.regionalPenalty(self.intensities[i, j], True)
            
            self.adjList.append(s)

            # now add all u-v edges for u,v in P, where P = set of pixels
            id = 0
            for i in range(0, rows):
                for j in range(0, cols):
                    id += 1
                    id_adj = {}
                    curr_pixel_intensity = self.intensities[i, j]
                    #our id increases along columns and down rows,
                    #look at the 4 adjacent pixels
                    if ((id % cols) != 1):
                        # pixel "id" not on left edge, can check left neighbor
                        left_id = id - 1
                        left_pixel_intensity = self.intensities[i, j - 1]
                        id_adj[left_id] = int(100*separationPenalty(curr_pixel_intensity, left_pixel_intensity))
                        
                    if (not (id <= cols)):
                        # pixel "id" not on top edge can check top neighbor
                        top_id = id - cols
                        top_pixel_intensity = self.intensities[i - 1, j]
                        id_adj[top_id] = int(100*separationPenalty(curr_pixel_intensity, top_pixel_intensity))

                    if (not (id > rows * cols - cols)):
                        # pixel "id" not on bottom edge can check bottom neighbor
                        bottom_id = id + cols
                        bottom_pixel_intensity = self.intensities[i + 1, j]
                        id_adj[bottom_id] = int(100*separationPenalty(curr_pixel_intensity, bottom_pixel_intensity))

                    if ((id % cols) != 0):
                        # pixel "id" not on right edge can check right neighbor
                        right_id = id + 1
                        right_pixel_intensity = self.intensities[i, j + 1]
                        id_adj[right_id] = int(100*separationPenalty(curr_pixel_intensity, right_pixel_intensity))

                    # take care of edge to t
                    t = rows*cols + 1
                    id_adj[t] = int(100*self.regionalPenalty(curr_pixel_intensity, False))

                    self.adjList.append(id_adj)
            # add t adjacency list
            self.adjList.append({})
        return self.adjList
                            

    def intensityHistogram(self):
        if (self.histogram == []):
            self.histogram = [0]*256
            width = int(self.intensities.shape[0])
            height = int(self.intensities.shape[1])
            print(height)
            print(width)

            for v in range(0, height):
                for u in range(0, width- 1):
                    pixelIntensity = int(self.intensities[u, v])
                    self.histogram[pixelIntensity] += 1

        return self.histogram
            
    #returns regional penalty based on 5-6 in paper by Boykov
    def regionalPenalty(self, intensity, inObject):
        self.intensityHistogram()
        width = int(self.intensities.shape[0])
        height = int(self.intensities.shape[1])

        count = 0
        sep = 0
        for i in range(256):
            count += self.histogram[i]
            if (count > (height * width) / 2):
                sep = i
                break

        penalty = 0
        if (intensity < sep):
            #dark
            if (inObject):
                penalty = 0
            else:
                penalty = 10000000000 #to represent infinity
        else:
            #light
            if (inObject):
                penalty = 0.1
            else:
                penalty = 0
        return 100*penalty
        
# test = GrayScaleImg(img_arr)
# print(test.intensityHistogram())

#calculates B_{p,q}
# sigma = 15 works well on Daisy_field
def separationPenalty(pixel_p, pixel_q):
    sigma = 13
    Ip = int(pixel_p)
    Iq = int(pixel_q)
    Bpq = 100*np.exp(-1*(np.power((Ip-Iq), 2)/(2*np.power(sigma, 2))))
    return Bpq