import glob
from PIL import Image
from PIL import ImageFilter
import matplotlib.pyplot as plt

class ImageProcessor:
    def __init__(self,im,plist):
        '''
        两个数据属性
        image:待处理的图片实例，即PIL库的Image实例
        plist:参数列表，用于存储图片处理时需要的参数
        '''
        self.image=im
        self.plist=plist
        
    def process(self):
        '''
        对Image实例进行特定处理，在子类中实现
        '''
        pass

class BLUR_process(ImageProcessor):
    '''
    模糊
    '''
    def __init__(self,im,plist):
        super().__init__(im, plist)
        
        
    def process(self):
        image_process=self.image.filter(ImageFilter.BLUR)
        return image_process
    
    
class outline_process(ImageProcessor):
    '''
    轮廓
    '''
    def __init__(self,im,plist):
        super().__init__(im,plist)
        
    def process(self):
        image_process=self.image.filter(ImageFilter.CONTOUR)
        return image_process

    
class sharpen_process(ImageProcessor):
    '''
    锐化
    '''
    def __init__(self,im,plist):
        super().__init__(im,plist)
        
    def process(self):
        image_process=self.image.filter(ImageFilter.SHARPEN)
        return image_process


class edge_find_process(ImageProcessor):
    '''
    边缘提取
    '''
    def __init__(self,im,plist):
        super().__init__(im,plist)
        
    def process(self):
        image_process=self.image.filter(ImageFilter.FIND_EDGES)
        return image_process
    
class relief_process(ImageProcessor):
    '''
    浮雕
    '''
    def __init__(self,im,plist):
        super().__init__(im,plist)
        
    def process(self):
        image_process=self.image.filter(ImageFilter.EMBOSS)
        return image_process
        
        
class resize_process(ImageProcessor):
    '''
    调整大小
    '''
    def __init__(self,im,plist):
        super().__init__(im, plist)
    
    def process(self):
        image_process=self.image.resize((self.plist[0],self.plist[1]),Image.ANTIALIAS)
        return image_process
    


class ImageShop():
    def __init__(self,form,file_path):
        '''
        form:图片格式
        file_path:图片文件
        par_lis:存储图片处理参数
        img_lis:存储未处理图片的列表
        imged_lis:存储处理后的图片
        '''
        self.form=form
        self.file_path=file_path
        self.par_lis=[]
        self.img_lis=[]
        self.imged_lis=[]
        
    def load_images(self):
        '''
        从某一路径加载统一格式的图片
        '''
        file_name=glob.glob(self.file_path+'/*'+self.form)
        for file in file_name:
            pic=Image.open(file)
            self.img_lis.append(pic)
        return self.img_lis
        
    def __batch_ps(self,pro):
        '''
        处理图片的内部方法
        '''
        if issubclass(pro,ImageProcessor):#判断pro是否是ImageProcessor的一个派生类
            for i in range(len(self.img_lis)):
                pic=self.img_lis[i]
                s=pro(pic,self.par_lis)
                picture=s.process()
                self.imged_lis.append(picture)

        return self.imged_lis
            
    def batch_ps(self,args):
        '''
        批量处理图片的对外公开方法
        args:不定长操作参数，按特定格式的tuple输入，比如（操作数，参数）
        '''
        for i in range(len(args)):
            ope=args[i][0]
            self.par_lis=args[i][1]
            self.__batch_ps(ope)
    
        return self.imged_lis
                    
    def display(self,row,col):
        '''
        处理效果的展示
        row:展示多张图片时需要的行
        col:展示多张图片时需要的列
        '''
        for i in range(len(self.imged_lis)):
            plt.subplot(row,col,i+1)
            plt.imshow(self.imged_lis[i])
            plt.axis('off') #去除坐标轴，更美观
        plt.show()
        
    def save(self,save_path,save_form):
        '''
        保存图片
        save_path:输出路径
        save_form:保存形式
        '''
        for i in range(len(self.imged_lis)):
            img=self.imged_lis[i]
            img.save(save_path+'image'+str(i+1)+'.'+save_form)
            
            
class TestImageShop(ImageShop):
    '''
    测试类
    '''
    def __init__(self,form,file_path,args,save_path,save_form):
        super().__init__(form,file_path)
        self.args=args
        self.save_path=save_path
        self.save_form=save_form
        
    def test_load_images(self):
        ImageShop.load_images(self)
        
    def test_batch_ps(self,args):
        print("正在处理……")
        self.imged_lis=ImageShop.batch_ps(self,args)
        
    def test_display(self,row,col):
        print("正在展示……")
        ImageShop.display(self,row,col)
        
    def test_save(self,save_path,save_form):
        print("正在保存……")
        ImageShop.save(self,save_path,save_form)
    


def main():
    '''
    任务一、二
    '''
    im=Image.open("C:\\Users\\范春\\Desktop\\a69b7cbc8245373f8efa67eeba2b51f.jpg")
    plist=[128,128]
    r1=BLUR_process(im, plist)
    r2=outline_process(im, plist)
    r3=sharpen_process(im, plist)
    r4=edge_find_process(im,plist)
    r5=relief_process(im, plist)
    r6=resize_process(im, plist)
    
    blur=r1.process()
    outline=r2.process()
    sharpen=r3.process()
    edge=r4.process()
    relief=r5.process()
    resize=r6.process()
    
    blur.show()
    outline.show()
    sharpen.show()
    edge.show()
    relief.show()
    resize.show()  
    
    '''
    任务三、四
    '''
    x=3
    y=4
    form='jpg'
    save_form='jpg'
    file_path="C:\\Users\\范春\\Pictures\\week6"
    save_path="C:\\Users\\范春\\Pictures\\week6\\result\\"
    
    args=[(outline_process,[]),(sharpen_process,[])]
    
    t=TestImageShop(form, file_path, args,save_path,save_form)
    t.test_load_images()
    t.test_batch_ps(args)
    t.test_save(save_path, save_form)
    t.test_display(x, y)
    
if __name__=='__main__':
    main()
    
    
    