import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 

plt.rcParams['font.sans-serif'] = ['SimHei']
class Data_re:
    def __init__(self,path_lis,location_lis):
        self.path_lis=path_lis
        self.location_lis=location_lis
        
    def read_csv(self,location):
        i=self.location_lis.index(location)
        data=pd.read_csv(self.path_lis[i],header=0)
        return data
    
class Data_plt:
    def __init__(self,path_lis,location_lis):
        self.path_lis=path_lis
        self.location_lis=location_lis
        
    def data_chuli(self,location):
        Dr=Data_re(self.path_lis,self.location_lis)
        data=Dr.read_csv(location)
        cols=['PM2.5','PM10','SO2','NO2','CO','O3']#由于数据存在缺失，将NA值替换为该列的平均值
        means=data.loc[:,cols].mean()
        data.loc[:,cols]=data.loc[:,cols].fillna(means)
        data_lis=np.array(data).tolist()
        return data_lis
        
    def location_pollutant_line(self,location,pollutant):
        Dr=Data_re(self.path_lis,self.location_lis)
        data=Dr.read_csv(location)
        data_lis=self.data_chuli(location)
        y=np.array(data[[pollutant]])
        
        time_lis=[]
        for i in range(len(data_lis)):
            time_lis.append(str(data_lis[i][1])+'.'+str(data_lis[i][2])+'.'+str(data_lis[i][3])+'.'+str(data_lis[i][4]))
        
        plt.plot(time_lis,y,c='red')
        plt.xlabel('时间')
        plt.ylabel(pollutant)
        plt.xticks(range(0,len(time_lis),8000))
        plt.title(f'{location}{pollutant}含量随时间的变化曲线')
        plt.show()
        
    def time_location_pie(self,time_str,location):
        data_lis=self.data_chuli(location)
        time=time_str.split('.')
        year = int(time[0]);month = int(time[1]);day = int(time[2]);hour = int(time[3])
        
        i = 0;flag = 1
        while i < len(data_lis) and flag == 1:
            if year == data_lis[i][1] and month == data_lis[i][2] and day == data_lis[i][3] and hour == data_lis[i][4]:
                num_lis= data_lis[i][5:11]
                flag = 0
            i = i + 1
        pollutants=['PM2.5','PM10','SO2','NO2','CO','O3']
        
        total=sum(num_lis)
        sizes=[num_lis[0]/total*100,num_lis[1]/total*100,num_lis[2]/total*100,num_lis[3]/total*100,num_lis[4]/total*100,num_lis[5]/total*100]
        
        plt.pie(sizes,labels=pollutants,autopct='%3.1f%%')
        plt.title(f'{time_str} {location}各污染物占比')
        plt.axis('equal')
        plt.show()

def main():
    path_lis=["C:\\Users\\范春\Desktop\PRSA_Data_20130301-20170228\PRSA_Data_Aotizhongxin_20130301-20170228.csv",
                 "C:\\Users\\范春\Desktop\PRSA_Data_20130301-20170228\PRSA_Data_Changping_20130301-20170228.csv",
                 "C:\\Users\\范春\Desktop\PRSA_Data_20130301-20170228\PRSA_Data_Dingling_20130301-20170228.csv",
                 "C:\\Users\\范春\Desktop\PRSA_Data_20130301-20170228\PRSA_Data_Dongsi_20130301-20170228.csv",
                 "C:\\Users\\范春\Desktop\PRSA_Data_20130301-20170228\PRSA_Data_Guanyuan_20130301-20170228.csv",
                 "C:\\Users\\范春\Desktop\PRSA_Data_20130301-20170228\PRSA_Data_Gucheng_20130301-20170228.csv",
                 "C:\\Users\\范春\Desktop\PRSA_Data_20130301-20170228\PRSA_Data_Huairou_20130301-20170228.csv",
                 "C:\\Users\\范春\Desktop\PRSA_Data_20130301-20170228\PRSA_Data_Nongzhanguan_20130301-20170228.csv",
                 "C:\\Users\\范春\Desktop\PRSA_Data_20130301-20170228\PRSA_Data_Shunyi_20130301-20170228.csv",
                 "C:\\Users\\范春\Desktop\PRSA_Data_20130301-20170228\PRSA_Data_Tiantan_20130301-20170228.csv",
                 "C:\\Users\\范春\Desktop\PRSA_Data_20130301-20170228\PRSA_Data_Wanliu_20130301-20170228.csv",
                 "C:\\Users\\范春\Desktop\PRSA_Data_20130301-20170228\PRSA_Data_Wanshouxigong_20130301-20170228.csv"]
    location_lis=['奥体中心','昌平','定陵','东四','官园','古城','怀柔','农展馆','顺义','天坛','万柳','万寿西宫']
    Dp=Data_plt(path_lis, location_lis)
    #Dp.location_pollutant_line('奥体中心', 'PM2.5')
    Dp.time_location_pie('2016.5.20.20', '顺义')
    
if __name__=='__main__':
    main()