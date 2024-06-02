#导入库
import jieba
import re
import random
import easygui as g
import matplotlib.pyplot as plt


def add_dic():
    '''
    将停用词表和五分类情绪词典加入jieba的自定义词典，
    以提高这些情绪词的识别能力
    '''
    #加入情绪词典
    jieba.load_userdict(r"C:\\Users\范春\\Desktop\\emotion_lexicon\\anger.txt")
    jieba.load_userdict(r"C:\\Users\范春\\Desktop\\emotion_lexicon\\disgust.txt")
    jieba.load_userdict(r"C:\\Users\范春\\Desktop\\emotion_lexicon\\fear.txt")
    jieba.load_userdict(r"C:\\Users\范春\\Desktop\\emotion_lexicon\\joy.txt")
    jieba.load_userdict(r"C:\\Users\范春\\Desktop\\emotion_lexicon\\sadness.txt")


def clear_data(text):
    '''
    对每一条微博进行清洗，去除无意义的评论
    '''
    text=re.sub(r"(回复)?(//)?\s*@\S*?\s*(:||$)"," ",text) #去除正文中的@和回复/转发中的用户名
    text=re.sub(r"\[\S+\]","",text) #去除表情符号
    URL_REGEX=re.compile(r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))',
        re.IGNORECASE)
    text=re.sub(URL_REGEX,"",text) #去除网址
    text=re.sub("转发微博","",text) 
    text=re.sub("我在：","",text)
    text=re.sub("我在这里：","",text)#去除无意义的词
    text=re.sub(r"\s+"," ",text) #合并正文中过多的空格
    
    return text.strip()

def get_file(adress):
    '''
    打开存储微博的文件，利用函数clear_data对微博进行清洗，将每一行作为一个
    元素存入列表
    '''
    lis_dataline=[] #用于存放清洗后的评论
   
    with open(adress,"r",encoding='utf-8') as f:
        lines=f.readlines()
        for line in lines:
            line=clear_data(line) #对评论进行清洗
            lis_dataline.append(line)
            

    return lis_dataline

       
def label_comment(lis_dataline):
    '''
    提取出每条微博的时间，经纬度以及情绪
    '''
    emotions_lis=[] #一个二维列表，用于存储五种情绪词典
    
    with open("C:\\Users\范春\\Desktop\\emotion_lexicon\\anger.txt",'r',encoding='utf-8') as f1:
        x1=f1.read().splitlines() #按行分词将文件内容变为列表
        emotions_lis.append(x1)
    with open("C:\\Users\范春\\Desktop\\emotion_lexicon\\disgust.txt",'r',encoding='utf-8') as f2:
        x2=f2.read().splitlines()
        emotions_lis.append(x2)
    with open("C:\\Users\范春\\Desktop\\emotion_lexicon\\fear.txt",'r',encoding='utf-8') as f3:
        x3=f3.read().splitlines()
        emotions_lis.append(x3)
    with open("C:\\Users\范春\\Desktop\\emotion_lexicon\\joy.txt",'r',encoding='utf-8') as f4:
        x4=f4.read().splitlines()
        emotions_lis.append(x4)
    with open("C:\\Users\范春\\Desktop\\emotion_lexicon\\sadness.txt",'r',encoding='utf-8') as f5:
        x5=f5.read().splitlines()
        emotions_lis.append(x5)
        
    def cut():
        nonlocal emotions_lis #将情绪列表传入
        nonlocal lis_dataline #将清洗好的评论列表传入
        
        location=[] #存放经纬度的列表
        time=[] #存放时间的列表
        emotions=[] #存放情绪的列表
        
        for com in lis_dataline:
            dic={'anger':0,'disgust':0,'fear':0,'joy':0,'sadness':0} #创建一个字典用于存储每条微博的情绪词个数
            t=com[-30:] #时间为每条微博的后三十个字符
            p=com.index(']') #对‘]'进行定位
            l=com[1:p] #获取经纬度
            location.append(l)
            time.append(t)
            
            sentence=com[p+1:-30] #获取评论文本
            words=jieba.lcut(sentence) #将文本进行分词并存入列表
            for word in words:
                #遍历找出其中的情绪词
                if word in emotions_lis[0]:
                    dic['anger']+=1
                if word in emotions_lis[1]:
                    dic['disgust']+=1
                if word in emotions_lis[2]:
                    dic['fear']+=1
                if word in emotions_lis[3]:
                    dic['joy']+=1
                if word in emotions_lis[4]:
                    dic['sadness']+=1
                else:
                    continue
            
            #若这五种情绪词的数目均为零，则将该条微博评论定义为中性
            if dic['anger']==dic['disgust']==dic['fear']==dic['joy']==dic['sadness']==0:
                emotions.append('neutral')
            #若不同情绪词出现的数目一样，则利用随机函数随机选择一个情绪词作为该条微博的情绪
            elif dic['anger']==dic['disgust']==dic['fear']==dic['joy']==dic['sadness']!=0:
                emotions.append(random.sample(['anger','disgust','fear','joy','sadness'],1))
            else:
                emotions.append(max(dic,key=dic.get)) #找出字典中最大值对应的键作为该条微博的情绪
        
        return location,time,emotions
    return cut


def pic_tre(feeling,time):
    '''
    通过情绪和时间两个参数来讨论不同时间情绪比例的变化趋势
    '''
    #利用easygui库实现Gui的可视化参数选择
    fel=g.buttonbox("请选择您要分析的情绪：",choices=('anger','disgust','fear','joy','sadness'))
    tim=g.buttonbox("请选择您要分析的时间：",choices=('month','week','hour'))
    
    #对time中的数据进行进一步切割，分别获得月份、星期、小时的数据
    months=[i[4:7] for i in time]
    weeks=[i[0:3] for i in time]
    hours=[i[11:13] for i in time]
   
    
    #初始化时间字典
    months_dic={'Jan':0,'Feb':0,'Mar':0,'Apr':0,'May':0,'Jun':0,'Jul':0,'Aug':0,'Sep':0,'Oct':0,'Nov':0,'Dec':0}
    weeks_dic={'Mon':0,'Tue':0,'Wed':0,'Thu':0,'Fri':0,'Sat':0,'Sun':0}
    hours_dic={'01':0, '02':0, '03':0, '04':0, '05':0, '06':0, '07':0, '08':0, '09':0, '10':0, '11':0, '12':0, '13':0, '14':0, '15':0, '16':0, '17':0, '18':0, '19':0, '20':0, '21':0, '22':0, '23':0, '00':0}
    
    
    #根据选择的时间参数绘制折线图
    if tim=='month':
        for i in range(len(feeling)):
            if fel==feeling[i] and months[i] in months_dic:
                months_dic[months[i]]+=1
        x=list(months_dic.keys()) #将字典的键转化为列表，作为x值
        y=list(months_dic.values()) #将相应的值转化为列表，作为y值
        plt.plot(x,y) #绘制图像
        plt.xlabel("month") #横坐标
        plt.ylabel('times') #纵坐标
        
    elif tim=='week':
        for i in range(len(feeling)):
            if fel==feeling[i] and weeks[i] in weeks_dic:
                weeks_dic[weeks[i]]+=1
        x=list(weeks_dic.keys())
        y=list(weeks_dic.values())
        plt.plot(x,y)
        plt.xlabel("week")
        plt.ylabel('times')        
    
    elif tim=='hour':
        for i in range(len(feeling)):
            if fel==feeling[i] and hours[i] in hours_dic:
                hours_dic[hours[i]]+=1 
        x=list(hours_dic.keys())
        y=list(hours_dic.values())
        plt.plot(x,y)
        plt.xlabel("hour") 
        plt.ylabel('times')   
                
    plt.title(fel+'--'+tim) #标题
    plt.show()
    

def main():
    add_dic()
    lis_dataline=get_file("E:\\weibo.txt") 
    fm=label_comment(lis_dataline)
    location,time,emotion=fm()
    pic_tre(emotion,time)
    
    
    
if __name__=='__main__':
    main()
     



















         

