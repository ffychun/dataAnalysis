import requests
from lxml import etree
import re
import threading
import queue
import librosa

class Get_Link(threading.Thread):
    def __init__(self,page_num,link_queue):
        super(Get_Link, self).__init__()
        self.page_num=page_num
        self.link_queue=link_queue
        
    def run(self):
        links=[]
        url=f'https://www.51voa.com/VOA_Standard_{self.page_num}.html'
        response=requests.get(url)
        html=etree.HTML(response.text)
        for j in range(0,50):
            links = links+html.xpath('//*[@id="righter"]/div[3]/ul/li[%s]/a/@href'%str(j))
        for i in range(len(links)):
            self.link_queue.put(links[i])

class Mp3_Link(threading.Thread):
    def __init__(self,link_queue,mp3_queue):
        super(Mp3_Link, self).__init__()
        self.link_queue=link_queue
        self.mp3_queue=mp3_queue
    
    def run(self):
        while True:
            link=self.link_queue.get()
            if link == None:
                break
            url = 'https://www.51voa.com' + link
            response = requests.get(url)
            mp3_links = re.findall(r'https://.+?\.mp3', response.text)
            if mp3_links:
                self.mp3_queue.put(mp3_links[0])
            self.link_queue.task_done()
            if self.link_queue.empty():
                break

class Download(threading.Thread):
    def __init__(self,mp3_queue,fname_queue):
        super(Download,self).__init__()
        self.mp3_queue=mp3_queue
        self.fname_queue=fname_queue
        
    def run(self):
        while True:
            mp3_link=self.mp3_queue.get()
            if mp3_link==None:
                break
            mp3_stream=requests.get(mp3_link).content
            fname = mp3_link[mp3_link.rfind('/')+1:]
            print(fname)
            self.fname_queue.put(fname)
            with open(fname,'wb') as f:
                f.write(mp3_stream)
            self.mp3_queue.task_done()
            if self.mp3_queue.empty():
                break

class Speech_Rate(threading.Thread):
    def __init__(self,fname_queue,speed_queue):
        super(Speech_Rate,self).__init__()
        self.fname_queue=fname_queue
        self.speed_queue=speed_queue
    
    def run(self):
        while True:
            fname=self.fname_queue.get()
            print(fname)
            if fname==None:
                break
            y,sr=librosa.load(fname,sr=None)
            onsets = librosa.onset.onset_detect(y=y,sr=sr,units="time",hop_length=128,backtrack=False) 
            number_of_words = len(onsets)
            duration = len(y)/sr
            words_per_second = number_of_words/duration
            self.speed_queue.put(words_per_second)
            self.fname_queue.task_done()
            if self.fname_queue.empty():
                break
def main():
    link_queue=queue.Queue()
    mp3_queue=queue.Queue()
    fname_queue=queue.Queue()
    speed_queue=queue.Queue()
    
    plist1=[Get_Link(i, link_queue) for i in range(3,4)]
    for p in plist1:
        p.start()
    for p in plist1:
        p.join()
    link_queue.put(None)
    '''
    while not link_queue.empty():
        print(link_queue.get())
    '''
    plist2=[Mp3_Link(link_queue, mp3_queue) for i in range(10)]
    for p in plist2:
        p.start()
    for p in plist2:
        p.join()
    mp3_queue.put(None)
    '''
    while not mp3_queue.empty():
        print(mp3_queue.get())
    '''
    plist3=[Download(mp3_queue,fname_queue) for i in range(10)]
    for p in plist3:
        p.start()
    for p in plist3:
        p.join()
    fname_queue.put(None)

    plist4=[Speech_Rate(fname_queue, speed_queue) for i in range(10)]
    for p in plist4:
        p.start()
    for p in plist4:
        p.join()
    speed_queue.put(None)
    
    while not speed_queue.empty(): 
        item=speed_queue.get()
        if item !=None:
            print('Speech_rate：',item)
 
if __name__=='__main__':
    main()
