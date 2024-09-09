from nodule import NoduleDataset as nd

img_path = "input/The IQ-OTHNCCD lung cancer dataset/Malignant cases/Malignant case (266).jpg"
dcm_path = "input/1-038.dcm"
img = nd()
img.convertToHU(image_path=img_path, dcm_path=dcm_path)