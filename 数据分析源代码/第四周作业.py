import datetime
import jieba
import pickle
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation


def sort_doc(file_path):
    '''
    文档分类
    ：param file_path:分档路径
    : return:分类结果
    '''
    data_by_time={}
    with open(file_path,"r",encoding="utf-8") as f:
        for line in f:
            fields=line.strip().split('\t')
            text=fields[1]
            time_str=fields[2]
            
            time=datetime.datetime.strptime(time_str, "%a %b %d %H:%M:%S %z %Y").date()
            if time in data_by_time:
                data_by_time.get(time).append(text)
            else:
                data_by_time.setdefault(time,[]).append(text)
            
        return data_by_time

def get_dic_len(data_dic):
    print(len(list(data_dic.keys())))
    
    
def get_stoplist():
    '''
    获得停用词表
    ：return:停用词表
    '''
    jieba.load_userdict(r"C:\\Users\\范春\\Desktop\\大二下\\数据分析\\stoplist.txt")
    with open("C:\\Users\\范春\\Desktop\\大二下\\数据分析\\stoplist.txt",'r',encoding="utf-8") as M:
        #用splitlines函数将读取的每一行作为一个元素存入列表stoplist
        stoplist=M.read().splitlines()
    return stoplist

def word_process(sentence,stopwords):
    '''
    数据预处理
    ：param sentence:句子
    ：param stopwords:停用词表
    ：return：空格连接字符串
    '''
    #使用jieba对文本进行分词操作，并去除符号
    words=[word for word in jieba.cut(sentence) if word.isalnum()]
    #print(words,'\n')
    for word in words:
        if word in stopwords:
            words.remove(word)
        
    result=' '.join(words)
    return result

def word_result(data_dic):
    '''
    处理数据
    :param data_dic:按天划分的数据字典
    :return:处理后的字符串列表 
    '''
    data_lis=[]
    stoplist=get_stoplist()
    for k in data_dic:
        result=word_process(" ".join(data_dic[k]),stoplist)
        data_lis.append(result)
    
    return data_lis

def matrix_fre(data_lis):
    '''
    词频矩阵，构建主题模型，主题概率分布，序列化保存
    ：param data_lis:字符串列表
    : return :词频矩阵
    '''
    vectorizer=CountVectorizer() #创建词袋数据结构
    matrix=vectorizer.fit_transform(data_lis) #将文本转换成词频矩阵
    
    k=3
     #使用LatentDirichletAllocation构建主题模型
    lda = LatentDirichletAllocation(n_components=k)
    lda.fit(matrix)
    
    #输出每个主题对应的词语
    feature_names = vectorizer.get_feature_names()
    for i,topic in enumerate(lda.components_):
        print(f"Topic {i}:")
        top_words=[feature_names[j] for j in topic.argsort()[:-6:-1]]
        print(top_words)
    
    #输出每篇文档的主题概率分布    
    for i in range(len(data_lis)):
        print(f"Document {i}:")
        print(lda.transform(matrix[i]))
    
    #利用pickle进行序列化保存
    pickle.dump((lda,matrix,vectorizer),open("C:\\Users\\范春\\Desktop\\大二下\\数据分析\\lda_model.pkl",'wb'))
    
    return matrix
    
def pplt(matrix):
    '''
    计算困惑度绘制elbow图确定主题数量
    : param matrix:词频矩阵
    '''
    perplexity_scores=[]
    k_range=range(1,6)
    for k in k_range:
        lda = LatentDirichletAllocation(n_components=k)
        lda.fit(matrix)
        perplexity_scores.append(lda.perplexity(matrix))
    plt.plot(k_range,perplexity_scores,'-o')
    plt.xlabel("Number of topics")
    plt.ylabel("Perplexity")
    plt.show()
    

def main():
    data_dic=sort_doc("E:\weibo.txt")
    for k,v in data_dic.items():
        print(k,':',v,'\n')
    get_dic_len(data_dic)
    data_lis=word_result(data_dic)
    matrix=matrix_fre(data_lis)
    print(matrix)
    pplt(matrix)
    
if __name__=='__main__':
    main()
    
            
    