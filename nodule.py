import numpy as np
import cv2
import matplotlib.pyplot as plt
import pydicom as pyd
from PIL import Image
from IPython.display import Image as show_gif
from tqdm import tqdm
from scipy.spatial.qhull import QhullError
from scipy import spatial
spatial.QhullError = QhullError
from scipy import ndimage as ndi
from skimage.morphology import ball, disk, dilation, binary_erosion, remove_small_objects, erosion, closing, reconstruction, binary_closing
from skimage.measure import label,regionprops, perimeter
from skimage.segmentation import clear_border

class NoduleDataset:
    def __init__(self, file_path=None, res=512, image=None):
        self.file_path = str(file_path)
        self.image = image
        self.image_width = None
        self.image_height = None
        self.res = res 
        self.image_dataset = []
        
    def get_image(self):
        return self.image
            
    def read_file_type(self):
        if ".jpg" in self.file_path.lower() or ".png" in self.file_path.lower() or ".jpeg" in self.file_path.lower():
            image = cv2.imread(self.file_path)
            image[image<0]=0
            self.image = image
            return(self.image)
        elif ".dcm" in self.file_path.lower():
            image = pyd.dcmread(self.file_path)
            image = image.pixel_array
            image[image<0]=0
            self.image = image
            return(self.image)
        else:
            raise ValueError(f"{self.file_path.lower() }File Format not supported. Try using .png, .jpg or .dcm")
    
    def resize(self):
        self.image = cv2.resize(self.image,(self.res,self.res))
    
    def standardize(self,unique_vals=False,to_decimal=False):
        image = self.image
        old = np.unique(image)
        image = image - np.min(image)
        image = image / np.max(image)
        image = (image*255).astype(np.uint16)
        if to_decimal:
            image = image/255.0
        self.image = image
        
        new = np.unique(self.image)
        if unique_vals:
            print(f"Before Standardization:\n{old}\nAfter Standardization:\n{new}")
    
    def colorCvt(self,color):
        '''
        "gray" converts the image from RGB to GRAY.
        "rgb" converts the image from GRAY to RGB
        '''
        if color == "gray" and len(self.image.shape) > 2:
            cnvt_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        elif color == "rgb" and len(self.image.shape)==2:
            cnvt_image = cv2.cvtColor(self.image, cv2.COLOR_GRAY2BGR)
        self.image = cnvt_image
    
    
    def image_center_crop(self,dim=(400,400)):
        w = self.image.shape[1]
        h = self.image.shape[0]
        crop_width = self.image.shape[1]
        if dim[0]<self.image.shape[1]:
            crop_width = dim[0]
        crop_height = self.image.shape[0]
        if dim[1]<self.image.shape[0]:
            crop_height = dim[1]
        mid_x, mid_y = int(w/2), int(h/2)
        mid_crop_width, mid_crop_height = int(crop_width/2), int(crop_height/2) 
        self.image = self.image[mid_y-mid_crop_height:mid_y+mid_crop_height, mid_x-mid_crop_width:mid_x+mid_crop_width]

    
    def gen_augmented_data(self, iterations: int=1, filename: str=None, save_filepath: str=None, save: bool=False):
        image = self.image
        if iterations>1:
            aug_images = []
            for i in range(iterations):
                if len(image.shape)==2:
                    image = self.colorCvt(image,"rgb")
                image=random_rotation(image,rg=360, row_axis=0, col_axis=1, channel_axis=2, fill_mode="constant")
                image=random_zoom(image,zoom_range=(0.7,0.9), row_axis=0, col_axis=1, channel_axis=2,fill_mode="constant")
                aug_images.append(image)
                self.image = aug_images
        else:
            if len(image.shape)==2:
                image = self.colorCvt(image,"rgb")
            image=random_rotation(image,rg=360, row_axis=0, col_axis=1, channel_axis=2, fill_mode="constant")
            image=random_zoom(image,zoom_range=(0.7,0.9), row_axis=0, col_axis=1, channel_axis=2,fill_mode="constant")
            if save:
                img = Image.fromarray(image)
                img.save(f"{save_filepath}/{filename}.jpg")
            else:
                self.image = image
    
    
    def get_segmented_lungs(self, plot=False, thres=604):
        im = self.image
        print(im.shape)
        '''
        source: https://www.kaggle.com/code/arnavkj95/candidate-generation-and-luna16-preprocessing#Segmentation-of-Lungs

        This funtion segments the lungs from the given 2D slice.
        '''
        if plot == True:
            f, plots = plt.subplots(8, 1, figsize=(5, 40))
            plots[0].set_title("Original Image")
            plots[0].axis('off')
            plots[0].imshow(im,cmap="gray")
        
        '''
        Step 1: Convert into a binary image. 
        '''
        '''
        Using Houndsfeld units where lungs are found between -600 and -400 we can adjust the images between those
        values to find the image that resemble the best features
        '''
        binary = im < thres
        if plot == True:
            plots[1].set_title("Step 1: Convert into a binary image.")
            plots[1].axis('off')
            plots[1].imshow(binary, cmap=plt.cm.bone) 
        '''
        Step 2: Remove the blobs connected to the border of the image.
        '''
        cleared = clear_border(binary)
        if plot == True:
            plots[2].set_title("Step 2: Remove the blobs connected to the border of the image.")
            plots[2].axis('off')
            plots[2].imshow(cleared, cmap=plt.cm.bone) 
        '''
        Step 3: Label the image.
        '''
        label_image = label(cleared)
        if plot == True:
            plots[3].set_title("Step 3: Label the image")
            plots[3].axis('off')
            plots[3].imshow(label_image, cmap=plt.cm.bone) 
        '''
        Step 4: Keep the labels with 2 largest areas.
        '''
        areas = [r.area for r in regionprops(label_image)]
        areas.sort()
        if len(areas) > 2:
            for region in regionprops(label_image):
                if region.area < areas[-2]:
                    for coordinates in region.coords:                
                           label_image[coordinates[0], coordinates[1]] = 0
        binary = label_image > 0
        if plot == True:
            plots[4].set_title("Step 4: Keep the labels with 2 largest areas.")
            plots[4].axis('off')
            plots[4].imshow(binary, cmap=plt.cm.bone)
            
        '''
        Step 5: Erosion operation with a disk of radius 2. This operation is 
        seperate the lung nodules attached to the blood vessels.
        '''
        selem = disk(2)
        binary = binary_erosion(binary, selem)
        if plot == True:
            plots[5].set_title("Step 5: This operation is seperate the lung nodules attached to blood vessels")
            plots[5].axis('off')
            plots[5].imshow(binary, cmap=plt.cm.bone) 
        '''
        Step 6: Closure operation with a disk of radius 10. This operation is 
        to keep nodules attached to the lung wall.
        '''
        selem = disk(10)
        binary = binary_closing(binary, selem)
        if plot == True:
            plots[6].set_title("Step 6: This operation is to keep nodules attached to the lung wall",)
            plots[6].axis('off')
            plots[6].imshow(binary, cmap=plt.cm.bone) 
            
#         '''
#         Step 7: Fill in the small holes inside the binary mask of lungs.
#         ''' 
#         edges = roberts(binary)
        
#         binary = ndi.binary_fill_holes(edges)
#         if plot == True:
#             plots[7].set_title("Step 7: Fill in the small holes inside the binary mask of lungs.")
#             plots[7].axis('off')
#             plots[7].imshow(binary, cmap=plt.cm.bone)
        '''
        Step 8: Superimpose the binary mask on the input image.
        '''
        get_high_vals = binary == 0
        im[get_high_vals] = 0
        if plot == True:
            plots[7].set_title("Step 7: Superimpose the binary mask on the input image.")
            plots[7].axis('off')
            plots[7].imshow(im, cmap="gray") 
        self.image = im

    
    def remove_noise(self):
        image = self.image
        if np.max(image)>1:
            image[image<(255*0.1)]=0
        elif np.max(image)<=1:
            image[image<0.1]=0
        else:
            raise "image have invalid pixel values"
        self.image=image
            
    def contrast_arr(self,contrast=10,brightness=0):
        out = cv2.convertScaleAbs(self.image,alpha=contrast,beta=brightness)
        self.image = out
        
    def process(self,dataframe):
        for path in tqdm(iterable=dataframe,desc="pre-processing images..."):
            self.file_path=path
            self.read_file_type()
            self.get_segmented_lungs(False)
            self.standardize()
            self.remove_noise()
            self.resize()
            self.image_dataset.append(self.image)
            image_dataset = np.asarray(self.image_dataset)
        return(image_dataset)

