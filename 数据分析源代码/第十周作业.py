import abc
import matplotlib.pyplot as plt
import jieba
import wordcloud
from collections import Counter
import glob
from PIL import Image
import librosa.display

class Plotter(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def plot(self,data,*args,**kwargs):
        pass

class PointPlotter(Plotter):
    def plot(self,data,*args,**kwargs):
        x=[point[0] for point in data]
        y=[point[1] for point in data]
        plt.scatter(x,y,*args,**kwargs)
        
class ArrayPlotter(Plotter):
    def plot(self,data,*args,**kwargs):
        if len(data)==2:
            x=data[0]
            y=data[1]
            plt.scatter(x,y,*args,**kwargs)
        if len(data)==3:
            x=data[0]
            y=data[1]
            z=data[2]
            ax=plt.subplot(111,projection='3d')
            ax.scatter(x,y,z)

class TextPlotter(Plotter):
    def plot(self,data,*args,**kwargs):
        word_lis=[word for word in jieba.lcut(data) if word.isalnum()]
        word_dic=dict(Counter(word_lis))
        wd=wordcloud.WordCloud(
            max_words=50,
            max_font_size=300,
            background_color='white',
            width=1500,
            height=960,
            margin=10, 
            font_path="C:/Windows/Fonts/simkai.ttf"
            )
        wd.generate_from_frequencies(word_dic)
        plt.imshow(wd)
        plt.axis('off')

class ImagePlotter(Plotter):
    def plot(self,data,*args,**kwargs):
        img_lis=[]
        file_name=glob.glob(data+'/*'+'jpg')
        for file in file_name:
            pic=Image.open(file)
            img_lis.append(pic)
        for i in range(len(img_lis)):
            plt.subplot(2,2,i+1)
            plt.imshow(img_lis[i])
            plt.axis('off')
        plt.show()

class MusickPlotter(Plotter):
    def plot(self,data,*args,**kwargs):
        y,sr=librosa.load(data)
        librosa.display.waveplot(y,sr=sr)
        plt.show()

def main():
    
    point1=[(1,1),(1,2),(2,1),(3,1),(3,2),(3,3)]
    point2=[[1,5,3,7,2,3],[2,8,3,4,2,4],[1,5,2,6,3,2]]
    PP=PointPlotter()
    AP=ArrayPlotter()
    PP.plot(point1)
    AP.plot(point2)
    
    text='''我不断地眺望那最初之在：一方天地，一条小街，阳光中缥缈可闻的一缕
    钟声。爱，原是自卑弃暗投明的时刻。自卑，或者在自卑的洞穴里步步深陷，或者转身，
    在爱的路途上迎候解放。所谓命运，就是说，这一出“人间戏剧”需要各种各样的角色，你
    只能是其中之一，不可以随意调换。我们一起坐在地坛的老柏树下，看天看地，听上帝一
    声不响。上帝他在等待。'''
    TP=TextPlotter()
    TP.plot(text)
    
    file_path="C:\\Users\\范春\\Pictures\\week10"
    IP=ImagePlotter()
    IP.plot(file_path)
    
    music_path="C:\\Users\\范春\Desktop\\穿越时空的思念（DiESi_Remix）(单曲版)-DiESi-14257672.mp3"
    MP=MusickPlotter()
    MP.plot(music_path)
    
if __name__=='__main__':
    main()