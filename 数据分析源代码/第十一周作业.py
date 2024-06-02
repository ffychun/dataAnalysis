import os
import librosa
from multiprocessing import Process,Queue

def get_files(file):
    files=[os.path.join(file,f) for f in os.listdir(file) if f.endswith('.wav')]
    return files

def compute_features(audio_file,feature_path):
    '''
    计算音高和声强的函数
    '''
    y,sr=librosa.load(audio_file)
    pitch=librosa.yin(y,fmin=librosa.note_to_hz('C1'),fmax=librosa.note_to_hz('C7'))
    sdb = librosa.amplitude_to_db(librosa.feature.rms(y=y), ref=0.00002)
    with open(feature_path,'w',encoding='utf-8') as f:
        f.write(str(pitch)+'\n')
        f.write(str(sdb)+'\n')

class FeatureProcess(Process):
    def __init__(self,queue):
        super().__init__()
        self.queue=queue
        
    def run(self):
        while True:
            try:
                audio_file = self.queue.get(timeout=1)
            except Empty:
                continue
            if audio_file is None:
                break
            feature_file = os.path.splitext(audio_file)[0] + '_process2.txt'
            compute_features(audio_file, feature_file)

if __name__=='__main__':
    file="C:\\Users\\范春\\Desktop\\音频"
    files=get_files(file)
    
    #直接使用Process类构建子进程
    for audio_file in files:
        feature_file = os.path.splitext(audio_file)[0] + '_process1.txt'
        p = Process(target=compute_features, args=(audio_file, feature_file))
        p.start()
        p.join()
  
    #通过继承Process类来构建子进程
    queue = Queue()
    for audio_file in files:
        queue.put(audio_file)
    plist1=[FeatureProcess(queue) for i in range(4)]
    for p in plist1:
        p.start()
    for p in plist1:
        p.join()
    queue.put(None)
    
    # 在主进程中启动利用2，3中构建的子进程，并分发参数
    plist2=[]
    queue=Queue()    
    for audio_file in files:
        queue.put(audio_file)
    for audio_file in files:
        p=Process(target=compute_features, args=(queue.get(), os.path.splitext(audio_file)[0] + '_process3.txt'))
        plist2.append(p)
    for p in plist2:
        p.start()
    for p in plist2:
        p.join()