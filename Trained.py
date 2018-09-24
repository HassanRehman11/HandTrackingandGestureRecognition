from PIL import Image
import numpy as np
from collections import Counter
import os,random,time, csv, cv2
import pandas as pd
class Recog:
    @staticmethod
    def train(filename):
        PATH = os.getcwd()
        img_list = os.listdir("dataSet")
        random.shuffle(img_list)
        total_img =  len(img_list)
        with open(filename,'w',newline='') as f:
            fieldnames = ['label', 'Image']
            thewriter = csv.DictWriter(f,fieldnames=fieldnames)
            thewriter.writeheader()
            for i in range(0,total_img):
                a = img_list[i].split('.')
                label = a[0]
                imgFilename = img_list[i]
                img = Image.open('dataSet/'+imgFilename)
                imgAr = np.array(img)
                imgAr_str = str(imgAr.tolist())
                thewriter.writerow({'label':label, "Image": imgAr_str})

    @staticmethod
    def recognize(image):
        matchedAr = []
        df = pd.read_csv("data.csv")
        length = len(df)
        iar = np.array(image)
        arList = iar.tolist()
        query = str(arList)
        eachQueImg = query.split('],')
        for i in range(0,length):
            label = df.label[i]
            curImg=df.Image[i]
            eachCurImg = curImg.split('],')
            x = 0
            while x<len(eachCurImg):
                if eachCurImg[x]==eachQueImg[x]:
                    matchedAr.append(int(label))
                x+=1
        x = Counter(matchedAr)
        try:
            lala = x.most_common(1)[0][0]
            kala = x.most_common(1)[0][1]
            if kala>150:
                return (lala, kala)
        except:
            pass
x = Recog()
x.train('data.csv')
