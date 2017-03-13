import urllib.request
import re
import os
import csv

topnum = 1;

#获取网页源代码
def getHtml(url):
    page = urllib.request.urlopen(url);
    html = page.read();
    return html;

#通过正则表达式获取该网页下的每部电影的title
def getName(html):
    nameList = re.findall(r'<span.*?class="title">(.*?)</span>', html, re.S);
    global topnum
    newNameList = [];
    for index,item in enumerate(nameList):
        if item.find("&nbsp") == -1:#通过检测&gt;或者&nbsp;这种HTML转义符，只保留第一个标题
            newNameList.append("Top " + str(topnum) + " " + item);
            topnum += 1;
    return newNameList;

#通过正则表达式获取该网页下的每部电影的introduction
def getInfo(html):
    infoList = re.findall(r'<span.*?class="inq">(.*?)</span>', html, re.S);
    return infoList;

#通过正则表达式获取该网页下的每部电影的rating_num
def getScore(html):
    scoreList = re.findall(r'<span.*?class="rating_num".*?property="v:average">(.*?)</span>', html, re.S);
    return scoreList;

#通过正则表达式获取该网页下的每部电影的img
def getImg(html):
    imgList = re.findall(r'<img.*?alt=.*?src="(https.*?)".*?class.*?>', html, re.S);
    return imgList;

#初始化数据列表
namesUrl=[]
scoresUrl=[]
infosUrl=[]
imgsUrl=[]

#实现翻页,每页25个
for page in range(0,250,25):
    url = "https://movie.douban.com/top250?start={}".format(page)
    html = getHtml(url).decode("UTF-8");
    namesUrl.extend(getName(html));
    scoresUrl.extend(getScore(html));
    infosUrl.extend(getInfo(html));
    imgsUrl.extend(getImg(html));

#将获得的信息进行打印，并存給列表allinfo，方便存储
allInfo = [];
if len(namesUrl) == len(scoresUrl) == len(imgsUrl):
    length = len(namesUrl);
    for i in range(0,length):
        print(namesUrl[i]+" , score = "+scoresUrl[i]+" ,\n imgUrl="+imgsUrl[i]);
        tmp = [];
        tmp.append(namesUrl[i]);
        tmp.append(scoresUrl[i]);
        tmp.append(imgsUrl[i]);
        allInfo.append(tmp);

#print(allInfo);
#将获得的数据进行存储
def save_to_csv(list_tmp):
    with open('D:/movie.csv','w+',newline='') as fp:
        a = csv.writer(fp,delimiter=',');
        a.writerow(['name','score','imgurl']);
        a.writerows(list_tmp);

save_to_csv(allInfo);
