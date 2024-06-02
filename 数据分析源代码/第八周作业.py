import cv2
import os
from PIL import Image
from PIL import ImageFilter
from functools import wraps
import numpy as np
class Test_class():
    def __init__(self,path,save_path):
        self.image=Image.open(path)
        self.save_path=save_path
        self.imged_lis=[]
    
    def blur_process(self):
        image_process=self.image.filter(ImageFilter.BLUR)
        self.imged_lis.append(image_process)
        return image_process
    
    def outline_process(self):
        image_process=self.image.filter(ImageFilter.CONTOUR)
        self.imged_lis.append(image_process)
        return image_process
    
    def relief_process(self):
        image_process=self.image.filter(ImageFilter.EMBOSS)
        self.imged_lis.append(image_process)
        return image_process
    
    def save_image(self):
        for i in range(len(self.imged_lis)):
            self.imged_lis[i].save(self.save_path+'image'+str(i+1)+'.'+'jpg')
        
    
class pre_pro:
    def __init__(self,path):
        self.path=path
    
    def __call__(self,func):
        @wraps(func)
        def wrapper(*args,**kwargs):
             image=cv2.imread(self.path)
             size=image.shape
             print('图像的大小为：',size)
             hsv=cv2.cvtColor(image,cv2.COLOR_RGB2HSV)
             
             #色调(H),饱和度(S),明度(V)
             H,S,V=cv2.split(hsv)
             
             #明度的均值
             v=V.ravel()[np.flatnonzero(V)] #亮度非零的值
             average_v=sum(v)/len(v)
             print('图像亮度的均值为：',average_v)
             #饱和度的均值
             s=S.ravel()[np.flatnonzero(S)]
             average_h=sum(s)/len(s)
             print('图像饱和度的均值为：',average_h)
             return func(*args,**kwargs)
        return wrapper

def check(save_path):
    def decorator(func):
        @wraps(func)
        def wrapper(*args,**kwargs):
            if os.path.exists(save_path)==False:
                print('The save_path does not exist, we will create it fo you!')
                os.mkdir(save_path) #创建对应文件夹
            else:
                print('The save_path already exists,please proceed with subsequent processing!')
            return func(*args,**kwargs)
        return wrapper
    return decorator 


def main():
    path="E:\\picture_test.jpg"
    save_path="C:\\Users\\范春\\Desktop\\picture\\"
    t=Test_class(path, save_path)
    t.blur_process()
    t.outline_process()
    t.relief_process()
    
    pre_pro(path)(Test_class)(path,save_path)
    check(save_path)(Test_class)(path,save_path)
    
    t.save_image()
              
if __name__=='__main__':
    main()           
             
