#版本1
import asyncio
import requests
import re
import time
from lxml import etree
import librosa
#import nest_asyncio
#nest_asyncio.apply()

class VoaCrawler:
    def __init__(self):
        self.base_url='https://www.51voa.com'
        self.dir_name="C:\\Users\\范春\\Desktop\\大二下\\数据分析\\result_13th\\"
    
    async def get_links(self,page_num):
        links=[]
        url = f'{self.base_url}/VOA_Standard_{page_num}.html'
        response=await asyncio.to_thread(requests.get,url)
        html=etree.HTML(response.text)
        for j in range(0,50):
            links = links+html.xpath('//*[@id="righter"]/div[3]/ul/li[%s]/a/@href'%str(j))
        return links

    async def get_mp3_links(self,link):
        url=self.base_url+link
        response=await asyncio.to_thread(requests.get,url)
        mp3_links=re.findall(r'https://.+?\.mp3',response.text)
        if mp3_links:
            return mp3_links[0]
        else:
            return None
    
    async def download_mp3(self,mp3_link):
        mp3_response=await asyncio.to_thread(requests.get, mp3_link)
        mp3_stream=mp3_response.content
        fname=mp3_link[mp3_link.rfind('/')+1:]
        with open(self.dir_name+fname,'wb')as f:
            f.write(mp3_stream)
        return fname
    
    async def speech_rate(self,fname):
        y,sr=await asyncio.to_thread(librosa.load, self.dir_name+fname, sr=None)
        onsets=librosa.onset.onset_detect(y=y,sr=sr,units="time",hop_length=128,backtrack=False)
        number_of_words=len(onsets)
        duration=len(y)/sr
        words_per_second=number_of_words/duration
        print(fname,':',words_per_second)

    async def main(self):
        links = await self.get_links(3)
        mp3_links = []
        fnames = []
        tasks = []
        for link in links:
            tasks.append(asyncio.create_task(self.get_mp3_links(link)))
        mp3_links = await asyncio.gather(*tasks)
        mp3_links = [link for link in mp3_links if link]
        tasks = []
        for mp3_link in mp3_links:
            tasks.append(asyncio.create_task(self.download_mp3(mp3_link)))
        fnames = await asyncio.gather(*tasks)
        fnames=[fname for fname in fnames if fname]
        tasks=[]
        for fname in fnames:
            tasks.append(asyncio.create_task(self.speech_rate(fname)))
        await asyncio.gather(*tasks)
        
    
if __name__ == "__main__":
    #loop=asyncio.get_event_loop()
    #tasks=[asyncio.create_task(mp3_links(3))]
    VC=VoaCrawler()
    start=time.time()
    asyncio.run(VC.main())
    #loop.run_until_complete(asyncio.wait(tasks))
    end=time.time()
    print(end-start)
    
#版本2
import asyncio
import requests
import aiohttp
import aiofiles
import re
import time
from lxml import etree

class VoaCrawler:
    def __init__(self):
        self.base_url='https://www.51voa.com'
        self.dir_name="C:\\Users\\范春\\Desktop\\大二下\\数据分析\\result_13th\\"
    
    async def get_links(self,page_num):
        links=[]
        url = f'{self.base_url}/VOA_Standard_{page_num}.html'
        response=await asyncio.to_thread(requests.get,url)
        html=etree.HTML(response.text)
        for j in range(0,50):
            links = links+html.xpath('//*[@id="righter"]/div[3]/ul/li[%s]/a/@href'%str(j))
        return links

    async def get_mp3_links(self,link):
        url=self.base_url+link
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                html=await response.text()
                mp3_links=re.findall(r'https://.+?\.mp3',html)
                if mp3_links:
                    return mp3_links[0]
                else:
                    return None
    
    async def download_mp3(self,mp3_link):
        async with aiohttp.ClientSession() as session:
            async with session.get(mp3_link) as response:
                mp3_stream=await response.read()
                fname=mp3_link[mp3_link.rfind('/')+1:]
                async with aiofiles.open(self.dir_name+fname,'wb') as f:
                    f.write(mp3_stream)
                return fname
            
    async def main(self):
        links = await self.get_links(3)
        mp3_links = []
        tasks = []
        for link in links:
            tasks.append(asyncio.create_task(self.get_mp3_links(link)))
        mp3_links = await asyncio.gather(*tasks)
        mp3_links = [link for link in mp3_links if link]
        tasks = []
        for mp3_link in mp3_links:
            tasks.append(asyncio.create_task(self.download_mp3(mp3_link)))
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    VC=VoaCrawler()
    start=time.time()
    asyncio.run(VC.main())
    end=time.time()
    print(end-start)
