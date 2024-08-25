import matplotlib
import cv2
import numpy as np
from matplotlib import pyplot as plt
from nodule import NoduleDataset
import config

fig,ax = plt.subplots(1,2,figsize=(15,20))
input_file = "C:/Users/zanco/OneDrive - Brunel University London/Year 3/CS3072 - Final Year Project/datasets/lung-PET-CT-Dx/Lung-PET-CT-Dx Subjects collected/subjectA22/2.000000-5mm-82416/1-50.dcm"
image = NoduleDataset(input_file)
image.read_file_type()
ax[0].imshow(image.get_image(),cmap="gray")
image.get_segmented_lungs()
image.remove_noise()
image.standardize()
output_file = image.get_image()
ax[1].imshow(output_file,cmap="gray")
fig.show()
fig.waitforbuttonpress()


