import PIL
import scipy.stats
from PIL import Image

class ImageQueryError(Exception):
    def __init__(self,user):
        self.user=user
class ImageQueryShapeNotMatchError(ImageQueryError):
    def __init__(self,user,image1,image2):
        self.user=user
        self.image1=image1
        self.image2=image2
        self.message="{} and {} are not the same size!".format(image1,image2)
        
    

class ImageQuery:
    def __init__(self,path1,path2):
        self.path1=path1
        self.path2=path2
    
    def _create_and_image(self):
        try:
            self._image=Image.open(self.path1)
        except FileNotFoundError:
            print("文件路径：",self.path1)
            print("Sorry, the path does not exist!")
        except PIL.UnidentifiedImageError:
            print("文件路径：",self.path1)
            print("Sorry, unidentified image!")
        else:
            print("未触发异常")
            
    def get_image(self):
        '''
        获取Image实例
        '''
        img_lis=[]
        self._image1=Image.open(self.path1)
        self._image2=Image.open(self.path2)
        img_lis.append(self._image1)
        img_lis.append(self._image2)
        return img_lis
    
    def compare(self,wd1,hgt1,wd2,hgt2):
        '''
        判断两个图片大小是否一样
        '''
        if (wd1!=wd2) or (hgt1!=hgt2):
            print("Image1: width:{} height:{}\t\tImage2: width:{} height:{}".format(wd1,hgt1,wd2,hgt2))
            raise ImageQueryShapeNotMatchError('fanchun','image1','image2')
    
    def pixel_difference(self):
        img_lis=self.get_image()
        
        #获取图片的形状信息
        width1=img_lis[0].size[0]
        height1=img_lis[0].size[1]
        
        width2=img_lis[1].size[0]
        height2=img_lis[1].size[1]
        
        try:
            self.compare(width1,height1,width2,height2)
        except ImageQueryShapeNotMatchError as IQSNME:
            print(IQSNME.message)
        else:
            answer=0
            for i in range(height1):
                for j in range(width1):
                    if i<1 and j<200:
                        rgb1=img_lis[0].getpixel((j,i))
                        rgb2=img_lis[1].getpixel((j,i))
                        ans=abs(sum(rgb1)/3-sum(rgb2)/3)
                        answer+=ans
            print(answer)
        
    def pixel_differ(self):
        '''
        获取更多的相似性，例如pearson,spearman,kendall等
        '''
        img_lis=self.get_image()
        #获取图片像素直方图
        c_hist_1=img_lis[0].histogram()
        c_hist_2=img_lis[1].histogram()
        
        p_cor=scipy.stats.pearsonr(c_hist_1,c_hist_2)
        s_cor=scipy.stats.spearmanr(c_hist_1,c_hist_2)
        k_cor=scipy.stats.kendalltau(c_hist_1,c_hist_2)
        print(p_cor)
        print(s_cor)
        print(k_cor)
                    
                    
def main():
    IQ=ImageQuery("C:\\Users\\范春\Desktop\\week7\\微信图片_20230331132707.jpg","C:\\Users\\范春\\Desktop\\week7\\微信图片_20230331132718.jpg")
    #IQ.pixel_difference()
    IQ.pixel_differ()
    
    
if __name__=='__main__':
    main()
    



        
    