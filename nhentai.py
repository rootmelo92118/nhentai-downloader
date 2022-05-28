from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
from im2pdf import union
import os, requests
import ssl, threading, time
ssl._create_default_https_context = ssl._create_unverified_context

dictionary1 = {}
dictionary2 = {}

def downloader(name,num,url,fileType):
    try:
        global dictionary1
        image = urlopen(url)
        comic = open(name+"_"+str(num+1)+"."+fileType,"wb")
        comic.write(image.read())
        comic.close()
        dictionary1[num] = name+"_"+str(num+1)+"."+fileType
        print(dictionary1)
    except:
        downloader(name,num,url,fileType)


    
def urlproc(num,url):
    datap = requests.get(url+"/" + str(num))
    pagep = bs(datap.text, "html.parser")
    global dictionary2
    dictionary2[num] = str(pagep.find("section", id="image-container").find("a").find("img")["src"])

url = input("Document URL : ")
data = requests.get(url+"/1")
page = bs(data.text, "html.parser")
if url[-1] == "/":
    name = url.split("/")[-2]
else:
    name = url.split("/")[-1]
source = []
filelist = []
Th1 = []
Th2 = []
last = int(str(page.find("a", class_="last")["href"]).split("/")[-2])
print("get1")

for i in range(1,last+1):
    print(i)
    T = threading.Thread(target=urlproc,args=(i,url,))
    Th2.append(T)
for i in range(0,len(Th2)):
    print("thread start "+str(i))
    Th2[i].start()
    time.sleep(0.4)
for i in range(0,len(Th2)):
    print("thread join "+str(i))
    Th2[i].join()
for i in range(1,last+1):
    source.append(dictionary2[i])
print(source)

for i in range(0,len(source)):
    try:
        FT = source[i].split(".")[-1]
        T = threading.Thread(target=downloader, args=(name,i,source[i],FT,))
        T.start()
        Th1.append(T)
    except Exception as e:
        print(e)

print(dictionary1)

for i in Th1:
    i.join()

for i in range(0, len(source)):
    try:
        filelist.append(dictionary1[i])
        print(dictionary1[i])
    except Exception as e:
        print(e)

union(filelist, name+".pdf")
for u in range(0, len(filelist)):
    os.remove(filelist[u])
