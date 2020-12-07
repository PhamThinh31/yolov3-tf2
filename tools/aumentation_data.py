from pascal_voc_writer import Writer

import os
import cv2
from PIL import Image
from tqdm import tqdm
from read_xml import read_xml
from Rotate_image import Rotate_image,Flip_image
import numpy as np

# # Writer(path, width, height)
# writer = Writer('path/to/img.jpg', 800, 400)
# # ::addObject(name, xmin, ymin, xmax, ymax)
# writer.addObject('cat', 100, 100, 200, 200)
# # ::save(path)
# writer.save('path/to/img.xml')

PATH_ANNO=r'D:\Project\SCS\dataset\first_device\ToTrain_Ani_V3\Annotations'
PATH_IMAGE=r'D:\Project\SCS\dataset\first_device\ToTrain_Ani_V3\Train\NoBox'
_SAVE_ANNO =r'D:\Project\SCS\dataset\first_device\ToTrain_Ani_V3\Annotations'
_SAVE_IMAGE=PATH_IMAGE#r'D:\Project\SCS\dataset\first_device\ToTrain_Ani_V3\Train\Scratches'
if not os.path.isdir(_SAVE_ANNO):
    print("Make Dir: ",_SAVE_ANNO)
    os.makedirs(_SAVE_ANNO)
if not os.path.isdir(_SAVE_IMAGE):
    print("Make Dir: ",_SAVE_IMAGE)
    os.makedirs(_SAVE_IMAGE)

list_images = [f for f in os.listdir(PATH_IMAGE) if '_' not in f]

angle=[90,180,270,'Flip']
for image in tqdm(list_images):
    root_name=image[:-4]
    _image=os.path.join(PATH_IMAGE,image)
    _anno=os.path.join(PATH_ANNO,root_name+'.xml')
    #read and save image
    r_img=cv2.imread(_image)
    data_anno = read_xml(_anno)
    r_bbox=[]
    r_obj_name=[]
    if 'object' not in data_anno:
        r_bbox=[[0,0,0,0]]

        for idx,ang in enumerate(angle):
            if ang =='Flip':
                temp_img,temp_bbox=Flip_image(r_img.copy(),r_bbox.copy())
            else:
                temp_img,temp_bbox=Rotate_image(ang,r_img.copy(),r_bbox.copy())

            _name= root_name+'_'+str(ang)
            writer = Writer(os.path.join(_SAVE_IMAGE,_name+'.jpg'), r_img.shape[0], r_img.shape[1])
            # for idx_1,box in enumerate(temp_bbox):
            #     __label = r_obj_name[idx_1]
                # writer.addObject(__label, int(box[0]), int(box[1]),int(box[2]),int(box[3]) )
            writer.save(os.path.join(_SAVE_ANNO,_name+'.xml'))
            cv2.imwrite(os.path.join(_SAVE_IMAGE,_name+'.jpg'),temp_img)
    else:
        for obj in data_anno['object']:
            temp=obj['bndbox']
            r_bbox.append([float(temp['xmin']), float(temp['ymin']), float(temp['xmax']), float(temp['ymax'])])
            r_obj_name.append(obj['name'])
        r_bbox = np.asarray(r_bbox)
    # for idx,ang in enumerate(angle):
    #     if ang =='Flip':
    #         temp_img,temp_bbox=Flip_image(r_img.copy(),r_bbox.copy())
    #     else:
    #         temp_img,temp_bbox=Rotate_image(ang,r_img.copy(),r_bbox.copy())

    #     _name= root_name+'_'+str(ang)
    #     writer = Writer(os.path.join(_SAVE_IMAGE,_name+'.jpg'), r_img.shape[0], r_img.shape[1])
    #     for idx_1,box in enumerate(temp_bbox):
    #         __label = r_obj_name[idx_1]
    #         writer.addObject(__label, int(box[0]), int(box[1]),int(box[2]),int(box[3]) )
    #     writer.save(os.path.join(_SAVE_ANNO,_name+'.xml'))
    #     cv2.imwrite(os.path.join(_SAVE_IMAGE,_name+'.jpg'),temp_img)