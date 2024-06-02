from PIL import Image
import os
import numpy as np

class FaceDataset:
    def __init__(self,path):
        self._path=path
        self.img_paths=[os.path.join(path,name) for name in os.listdir(path)]
        self.img_lis=[Image.open(img_path) for img_path in self.img_paths]
    
    def image_generator(self):
        for img in self.img_lis:
            yield np.array(img)
    
    def __iter__(self):
        self.index=0
        return self
    
    def __next__(self):
        if self.index>=len(self.img_paths):
            raise StopIteration
        else:
            img_path=self.img_paths[self.index]
            img=Image.open(img_path)
            self.index+=1
            return np.array(img)
    def __len__(self):
        return len(self.img_paths)
    
    def __getitem__(self,i):
        return np.array(Image.open(self.img_paths[i]))
               
def main():
    path="C:\\Users\\范春\\Pictures\\week6"
    FD=FaceDataset(path)
    for image in FD:
        print(image)
        
    lenth=FD.__len__()
    print(lenth)
    
    print(FD.__getitem__(2))
        
if __name__=="__main__":
    main()
            
                                                       