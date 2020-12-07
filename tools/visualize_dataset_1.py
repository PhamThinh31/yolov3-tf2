import cv2
from PIL import Image
import os
import lxml.etree
import shutil
import random
from tqdm import tqdm
import numpy as np
FOLDER_IMAGE = r'D:\Project\SCS\dataset\first_device\ToTrain_Ani_V3\Train\Foreign_Material'
FOLDER_ANNO = r'D:\Project\SCS\dataset\first_device\ToTrain_Ani_V3\Annotations'
FOLDER_OUTPUT = r'D:\Project\SCS\dataset\first_device\ToTrain_Ani_V3\Visual'
COLOR = [(0, 0, 255),(0, 255, 0),(255, 0, 0),(0, 0, 255)]
THICKNESS = 2


files=[f[:-4] for f in os.listdir(FOLDER_IMAGE)] # if len(f[:-4])>9]
print("leng file",len(files))

def parse_xml(xml):
    if not len(xml):
        return {xml.tag: xml.text}
    result = {}
    for child in xml:
        child_result = parse_xml(child)
        if child.tag != 'object':
            result[child.tag] = child_result[child.tag]
        else:
            if child.tag not in result:
                result[child.tag] = []
            result[child.tag].append(child_result[child.tag])
    return {xml.tag: result}

def read_xml(path):
    annotation_xml = lxml.etree.fromstring(open(path).read())
    annotation = parse_xml(annotation_xml)['annotation']
    return annotation

def draw_rect_and_save(path_image,xml_path,output_path,color=(0, 0, 255),thickness=2):
    anno = read_xml(xml_path)
    img = cv2.imread(path_image)
    for obj in anno['object']:
        bbox = obj['bndbox']
        label = obj['name']
        p1= (int(bbox['xmin']),int(bbox['ymin']))
        p2= (int(bbox['xmax']),int(bbox['ymax']))
        img = cv2.rectangle(img, p1, p2, color, thickness)
        img = cv2.putText(img,label,p1,cv2.FONT_HERSHEY_SIMPLEX,1,color,thickness)
    cv2.imwrite(output_path,img)
def check_valid(p1,p2,H,W):
    p1=list(p1)
    p2=list(p2)
    H=int(H)
    W=int(W)
    shift_pixels_h = 50#abs(int(p1[0]-p2[0]))
    # if shift_pixels_h>50:
    #     shift_pixels_h=50
    shift_pixels_w = 50#abs(int(p2[1]-p1[1]))
    # if shift_pixels_w>50:
    #     shift_pixels_w=50
    if p1[0] - shift_pixels_h <0:
        p1[0]=0
    else:
        p1[0]-=shift_pixels_h

    if p1[1]-shift_pixels_w<0:
        p1[1]=0
    else:
        p1[1]-=shift_pixels_w

    if p2[0]+shift_pixels_h>H:
        p2[0]=H
    else:
        p2[0]+=shift_pixels_h

    if p2[1]+shift_pixels_w>W:
        p2[1]=W
    else:
        p2[1]+=shift_pixels_w

    return p1,p2


def main():
        
    meta_data={'Chipping':[],'Foreign_Material':[],'Peeling':[],'Scratches':[]}
    meta_data_id={'Chipping':0,'Foreign_Material':0,'Peeling':0,'Scratches':0}
    id_data={'Chipping':0,'Foreign_Material':1,'Peeling':2,'Scratches':3}
    count=0
    # arr = np.arange(5026)
    # np.random.shuffle(arr)

    for file in tqdm(files):
        xml_file = os.path.join(FOLDER_ANNO,file+'.xml')
        image_file = os.path.join(FOLDER_IMAGE,file+'.jpg')
        out_put= os.path.join(FOLDER_OUTPUT,file+'.jpg')
        draw_rect_and_save(image_file,xml_file,out_put)
    #     anno = read_xml(xml_file)

    #     W=anno['size']['width']
    #     H=anno['size']['height']
    #     # print(H,W)
    #     img=Image.open(image_file)
    #     try:
    #         anno['object']
    #     except KeyError:
    #         print(KeyError,file)
    #         continue
    #     for obj in anno['object']:
    #         name=obj['name']
    #         bbox = obj['bndbox']
    #         p1= (int(bbox['xmin']),int(bbox['ymin']))
    #         p2= (int(bbox['xmax']),int(bbox['ymax']))

    #         p1,p2=check_valid(p1,p2,H,W)
    #         temp_img=img.crop((p1[0],p1[1],p2[0],p2[1]))
    #         if not os.path.isdir(os.path.join(FOLDER_OUTPUT,name)):
    #             os.makedirs(os.path.join(FOLDER_OUTPUT,name))
    #         path_save=os.path.join(FOLDER_OUTPUT,name,str(count)+'.jpg')
    #         temp_img.save(path_save)
    #         count+=1
    # print("Total have {} image".format(count))
            # cv2.imwrite(path_save,temp_img)
            # print(p1,p2)
    ## Thống kê trong dataset
    #     try:

    #         xml_file = os.path.join(FOLDER_ANNO,file+'.xml')
    #         # image_file = os.path.join(FOLDER_IMAGE,file+'.jpg')
    #         anno = read_xml(xml_file)
            
    #         #shutil.copy(image_file,out_image_1)
    #         # img = cv2.imread(image_file)
    #         # try:

    #         # for obj in anno['object'][0]:
    #             # bbox = obj['bndbox']

    #         label = anno['object'][0]['name']
    #         # meta_data[label].append(file)
    #         # if label == 'Scratches':
    #         #     print(file)
    #         # meta_data_id[label]+=1
    #     except:
    #         print(file)
        
    #     #     p1= (int(bbox['xmin']),int(bbox['ymin']))
    #     #     p2= (int(bbox['xmax']),int(bbox['ymax']))
    #     #     img = cv2.rectangle(img, p1, p2, COLOR[id_data[label]], THICKNESS)
    #     #     img = cv2.putText(img,label,p1,cv2.FONT_HERSHEY_SIMPLEX,1,COLOR[id_data[label]],THICKNESS)
    #     # cv2.imwrite(out_image,img)
    #     # except:
    #     #     print(image_file)
    # # print(type(meta_data['Chipping']))
    # print(meta_data_id)

    # # path_out = 'D:\Project\SCS\dataset\\new_dataset\\final_ani_edit\\Val_tem'
    # # path_out_1='D:\Project\SCS\dataset\\22_05_raw\Train'
    # # print(meta_data)
    # # for i in meta_data:
    # #     # if os.path.exists(os.path.join(path_out,i)) is False:
    # #     #     os.makedirs(os.path.join(path_out,i))
    # #     if os.path.exists(os.path.join(path_out_1,i)) is False:
    # #         os.makedirs(os.path.join(path_out_1,i))
    # #     # val = random.choices(meta_data[i],k=150)
    # #     train= [f for f in meta_data[i]]# if f not in val]
    # #     print(train)
    # #     # print(len(val),len(train),len(val)+len(train),len(meta_data[i]))
    # #     # for item in val:
    #     #     shutil.copy2(os.path.join(FOLDER_IMAGE,item+'.jpg'),os.path.join(path_out,i,item+'.jpg'))
    #     # for item in train:
    #     #     shutil.copy2(os.path.join(FOLDER_IMAGE,item+'.jpg'),os.path.join(path_out_1,i,item+'.jpg'))

if __name__ == "__main__":
    main()
    pass