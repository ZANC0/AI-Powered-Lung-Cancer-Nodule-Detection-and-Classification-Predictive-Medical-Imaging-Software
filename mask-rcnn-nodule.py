'''
source - https://github.com/matterport/Mask_RCNN?tab=readme-ov-file
       - https://github.com/matterport/Mask_RCNN/blob/master/samples/nucleus/nucleus.py
       - https://blog.paperspace.com/mask-r-cnn-in-tensorflow-2-0/
'''
import sys
import numpy as np
import cv2
import matplotlib.pyplot as plt
import pydicom as pyd
import scipy
import skimage
import pathlib
from pathlib import Path
import pandas as pd
import os
import tensorflow
import keras

from pydicom import filereader
from PIL import Image
from IPython.display import Image as show_gif
from tqdm import tqdm
from sklearn.model_selection import train_test_split

from keras.preprocessing.image import random_rotation, random_zoom
from keras.layers import Conv2D, MaxPooling2D, Dropout

from scipy.spatial.qhull import QhullError
from scipy import spatial
spatial.QhullError = QhullError
from scipy import ndimage as ndi
from scipy import ndimage

from skimage import morphology
from skimage.morphology import ball, disk, dilation, binary_erosion, remove_small_objects, erosion, closing, reconstruction, binary_closing
from skimage.measure import label,regionprops, perimeter
from skimage.morphology import binary_dilation, binary_opening
from skimage.filters import roberts, sobel
from skimage import measure, feature
from skimage.segmentation import clear_border
from skimage import data




# source - https://www.kaggle.com/code/frlemarchand/maskrcnn-for-chest-x-ray-anomaly-detection/notebook#Mask-RCNN-for-Chest-X-ray-Diagnostic---Starter
DATA_DIR = Path('../output')
ROOT_DIR = "C:/Users/zanco/Documents/GitHub/Mask-RCNN_TF2.14.0-edited"
COCO_WEIGHTS_PATH = "./input/mask_rcnn_coco.h5"
# os.chdir('../Mask-RCNN_TF2.14.0-edited')

sys.path.append(ROOT_DIR)

import mrcnn
from mrcnn import utils
from mrcnn import visualize
from mrcnn.visualize import display_images
from mrcnn import model as modellib
from mrcnn.model import log
import mrcnn.visualize
import mrcnn.config

CLASS_NAMES = ['BG','nodule']
class NoduleConfig(mrcnn.config.Config):
    NAME = "lung-nodule"
     # Adjust depending on your GPU memory
    IMAGES_PER_GPU = 6
    GPU_COUNT = 1
    # Number of classes (including background)
    NUM_CLASSES = len(CLASS_NAMES)  # Background + nucleus
    LEARNING_RATE = 0.006
    # Don't exclude based on confidence. Since we have two classes
    # then 0.5 is the minimum anyway as it picks between nucleus and BG
    DETECTION_MIN_CONFIDENCE = 0

    # Backbone network architecture
    # Supported values are: resnet50, resnet101
    BACKBONE = "resnet50"

    # Input image resizing
    # Random crops of size 512x512
    IMAGE_RESIZE_MODE = "none"
    IMAGE_MIN_DIM = 512
    IMAGE_MAX_DIM = 512
    # changing the channel count from 3 to 1, making the input shape [512,512,1] instead of [512,512,3]
    IMAGE_CHANNEL_COUNT = 1
    DETECTION_MAX_INSTANCES = 20
    MEAN_PIXEL = np.array([123.7])

class NoduleDataset(mrcnn.utils.Dataset):
    '''
    dataset_dir: These are iamges that previously been extracted from their sources, preprocessed and saved into new directory
                 such that it is a suitable format to use with MASK R-CNN
                         
                 
    def add_image(self, source, image_id, path, **kwargs):
        image_info = {
            "id": image_id,
            "source": source,
            "path": path,
        }
        image_info.update(kwargs)
        self.image_info.append(image_info)
        
    '''
    
    def load_dataset(self, dataset_dict, is_train=True):
        
        self.add_class("dataset", 1, "nodule")
        image_data = dataset_dict.get("images")
        annotations = dataset_dict.get("targets")


        for img_index in range(len(image_data)):
            image_id = img_index
            img_path = image_data[img_index]
            ann_path = annotations[img_index]
            self.add_image('dataset', image_id=image_id, path=img_path, annotation=ann_path)

    
#     def extract_boxes(self,annotation_cords):
#         '''
#         Using target_data.npy for the coords but need to standardize to 512 from 1/512
#         '''
#         boxes = list()
        
#         standardized_cords = annotation_cords*512
#         return boxes

    def load_mask(self,image_id):
        info = self.image_info[image_id]
        boxes = np.load("./input/512x512mrcnnData/512x512_target_data.npy")
        w, h = len(info["path"][0]), len(info["path"][1])
        masks = np.zeros([h, w, len(boxes)], dtype='uint8')
        
        class_ids = list()
        for i in range(len(boxes)):
            box = boxes[i]
            row_s, row_e = box[1], box[3]
            col_s, col_e = box[0], box[2]
            masks[row_s:row_e, col_s:col_e, i] = 1
            class_ids.append(self.class_names.index("nodule"))
        return masks, np.asarray(class_ids,dtype='int32')
    
    def load_image(self, image_id):
        """Load the specified image and return a [H,W,3] Numpy array.
        """
        # Load image
        image = self.image_info[image_id]
        image = image["path"]
        image = np.expand_dims(image, axis=-1).astype(np.uint8)
#         # If grayscale. Convert to RGB for consistency.
#         if image.ndim != 3:
#             image = skimage.color.gray2rgb(image)
#         # If has an alpha channel, remove it for consistency
#         if image.shape[-1] == 4:
#             image = image[..., :3]
        return image
    

image_data = np.load("./input/512x512mrcnnData/512x512_image_data.npy")
target_data = np.load("./input/512x512mrcnnData/512x512_target_data.npy")
train_image_data, val_image_data, train_target_data, val_target_data = train_test_split(image_data,target_data, test_size=0.2)
training_dict = {
    "images":train_image_data,
    "targets":train_target_data
}
val_dict = {
    "images":val_image_data,
    "targets":val_target_data
}

train_set = NoduleDataset()
train_set.load_dataset(dataset_dict=training_dict, is_train=True)
train_set.prepare()

valid_dataset = NoduleDataset()
valid_dataset.load_dataset(dataset_dict=val_dict, is_train=False)
valid_dataset.prepare()

nodule_config = NoduleConfig()
model = mrcnn.model.MaskRCNN(mode='training', 
                             model_dir='./', 
                             config=nodule_config)

model.load_weights(filepath=COCO_WEIGHTS_PATH, 
                   by_name=False, 
                   exclude=["mrcnn_class_logits", "mrcnn_bbox_fc",  "mrcnn_bbox", "mrcnn_mask","conv1"])

model.train(train_dataset=train_set, 
            val_dataset=valid_dataset, 
            learning_rate=nodule_config.LEARNING_RATE, 
            epochs=2,
            layers="heads")
# history = model.keras_model.history.history
# model_path = 'nodules_mask_rcnn.h5'
# model.keras_model.save_weights(model_path)