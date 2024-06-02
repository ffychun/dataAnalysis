import jieba
from gensim.models import Word2Vec
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import numpy as np
my_font=FontProperties(fname="E:\\字体包\\中文\\方正楷体_GBK.TTF")



class TextAnalyzer:
    def __init__(self,text_path,stopwords_path,model_path,vector_size,window,min_count):
        '''
        初始化函数：初始化类
        '''
        self.text_path=text_path
        self.stopwords_path=stopwords_path
        self.model_path=model_path
        self.vector_size=vector_size
        self.window=window
        self.min_count=min_count
        
    def get_stopwords(self):
        '''
        获取停用词表
        '''
        path=self.stopwords_path
        with open (path,"r",encoding='utf-8') as m:
            stoplist=m.read().splitlines()
        return stoplist
        
    def text_preprocess(self):
        '''
        文本预处理：分词、去除停用词、标点等
        '''
        self.text_lis=[]
        stoplist=self.get_stopwords()
        path=self.text_path
        with open (path,"r",encoding='utf-8') as f:
            for line in f:
                fields=line.strip().split('\t')
                text=fields[1]
                words=[word for word in jieba.cut(text) if word.isalnum()]
                for word in words:
                    if word in stoplist:
                        words.remove(word)
                self.text_lis.append(words)
        return self.text_lis

    def model_create(self):
        '''
        Word2Vec模型建立
        '''
        self.text_preprocess()
        self.model = Word2Vec(self.text_lis,vector_size=self.vector_size,window=self.window,min_count=self.min_count)
        self.model.save("C:\\Users\\范春\\Desktop\\Word2Vec.model")
        return self.model
    
    def mostsimilar_infer(self):
        '''
        推断最相近的十个词
        '''
        most_similar=self.model_create().wv.most_similar("春天",topn=10)
        return most_similar
    
    def leastsimilar_infer(self):
        '''
        推断最不相近的十个词
        '''
        least_similar=self.model_create().wv.most_similar(negative=["春天"],topn=10)
        return least_similar
    
    def model_comparison(self):
        '''
        模型比较
        '''
        #模型1为本题训练的模型
        model1=self.model_create() 
        #模型二为作业提供的模型
        model2=Word2Vec.load("C:\\Users\\范春\\Desktop\\model\\weibo_59g_embedding_200.model")
        
        most_similar1=model1.wv.most_similar("春天",topn=10)
        least_similar1=model1.wv.most_similar(negative=["春天"],topn=10)
        
        most_similar2=model2.wv.most_similar("春天",topn=10)
        least_similar2=model2.wv.most_similar(negative=["春天"],topn=10)
        
        print("最相关词汇比较：")
        print("         model1         \t         model2         ")
        for i in range(10):
            print(most_similar1[i],'\t',most_similar2[i])
        print()
        print("最不相关词汇比较：")
        print("         model1         \t         model2         ")
        for i in range(10):
            print(least_similar1[i],'\t',least_similar2[i])
            
    def visualization(self):
        '''
        降维和可视化
        '''
        model=self.model_create()
        most_similar=self.mostsimilar_infer()
        least_similar=self.leastsimilar_infer()
        
        #将最相关和最不相关的词汇向量合并为一个数组
        vectors=np.array([model.wv[word] for word, similarity in most_similar + least_similar])
        print(vectors.shape)
        words=[word for word,similarity in most_similar + least_similar]
        
        #使用t-SNE算法对词向量进行降维
        tsne=TSNE(n_components=2,perplexity=10)
        vectors_tsne=tsne.fit_transform(vectors)
        
        #可视化降维后的词向量
        fig,ax=plt.subplots()
        ax.set_title("春天",fontproperties=my_font)
        ax.scatter(vectors_tsne[:10,0],vectors_tsne[:10,1],color="blue")
        ax.scatter(vectors_tsne[10:,0],vectors_tsne[10:,1],color="red")
        for i,word in enumerate(words):
            ax.annotate(word,(vectors_tsne[i,0],vectors_tsne[i,1]),fontproperties=my_font)
        plt.show()
        
            

def main():
    text_path="E:\\weibo.txt"
    stopwords_path="C:\\Users\\范春\\Desktop\\大二下\\数据分析\\stoplist.txt"
    model_path=Word2Vec
    vector_size=300
    window=5
    min_count=1
    t=TextAnalyzer(text_path, stopwords_path, model_path, vector_size, window, min_count)
    text_lis=t.text_preprocess()
    print(text_lis)
    t.model_create()
    near_synonym=t.mostsimilar_infer()
    antonym=t.leastsimilar_infer()
    print("最相关的十个词：")
    for word in near_synonym:
        print(word)
    print("最不相关的十个词：")
    for word in antonym:
        print(word)
    t.model_comparison()
    t.visualization()
        
if __name__=="__main__":
    main()
                
        

