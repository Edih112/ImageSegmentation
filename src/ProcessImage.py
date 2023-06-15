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
            # remember that id = 0 is assigned to s, so
            # id's for pixels starts from 1
            id = 0
            # loop over all pixels in img
            for i in range(0, self.intensities.shape[0]):
                for j in range(0, self.intensities.shape[1]):
                    id += 1
                    s[id] = regionalPenalty(self.intensities[i, j], True)

            # now add all u-v edges for u,v in P, where P = set of pixels
            id = 0
            for i in range(0, self.intensities.shape[0]):
                for j in range(0, self.intensities.shape[1]):
                    id += 1
                    #our id increases along columns and down rows,
                    #need to be able to get id of the 4 adjacent pixels to each pixel

    #DO NOT CALL THIS FUNCTION creates adjacency matrix from image 
    #need to add size limit as this fails for most images
    def getAdjMatrix(self):
        if (self.adjMatrix == None):
            size = self.intensities.shape[0]*self.intensities.shape[1]
            self.adjMatrix = np.zeros([size + 2, size + 2]) # 0 and size - 1 are s and t

            for i in range(size + 2):
                if (i == 0):
                    # loop over all pixel vertices
                    for j in range(1, size + 1):
                        intensity = self.intensities[i, j]
                        self.adjMatrix[i, j] = regionalPenalty(intensity, True)
                else:
                    # loop over all pixel vertices
                    for j in range(1, size + 1):
                        if (j == size):
                            #t connections
                            intensity == self.intensities[i, j]
                            self.adjMatrix[i, j] = regionalPenalty(intensity, False)
                        else:
                            # curr pixel, want to iterate over its 4 neighbors
                            intensity = self.intensities[i, j]
                            # go over neighbors
                            # (i, j) center
                            # (i + 1, j), (i-1, j), (i, j+1), (i, j-1)
                            if (i + 1 < self.img.shape[0]):
                                self.adjMatrix[i + 1, j] = separationPenalty(self.intensities[i, j], self.intensities[i + 1, j])
                            if (i - 1 >= 0):
                                self.adjMatrix[i - 1, j] = separationPenalty(self.intensities[i, j], self.intensities[i - 1, j])
                            if (j + 1 < self.img.shape[1]):
                                self.adjMatrix[i, j + 1] = separationPenalty(self.intensities[i, j], self.intensities[i, j + 1])
                            if (j - 1 >= 0):
                                self.adjMatrix[i, j - 1] = separationPenalty(self.intensities[i, j], self.intensities[i, j - 1])
        return self.adjMatrix
                            

    def intensityHistogram(self):
        if (self.histogram == []):
            self.histogram = [0]*256
            width = int(self.intensities.shape[0])
            height = int(self.intensities.shape[1])
            print(height)
            print(width)

            for v in range(0, height):
                for u in range(0, width- 1):
                    pixelIntensity = int(self.img[u, v])
                    self.histogram[pixelIntensity] += 1

        return self.histogram
            
# test = GrayScaleImg(img_arr)
# print(test.intensityHistogram())

#calculates B_{p,q}
def separationPenalty(pixel_p, pixel_q):
    sigma = 20
    Ip = pixel_p
    Iq = pixel_q
    Bpq = np.exp(-1*((Ip-Iq)*(Ip-Iq))/(2*sigma*sigma))
    return Bpq

#returns regional penalty based on 5-6 in paper by Boykov
def regionalPenalty(intensity, inObject):
    penalty = 0
    if (intensity < 128):
        #dark
        if (inObject):
            penalty = 0
        else:
            penalty = float('inf')
    else:
        #light
        if (inObject):
            penalty = 0.1
        else:
            penalty = 0
    return penalty