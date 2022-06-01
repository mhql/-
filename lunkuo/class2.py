import math
import cv2
import os
import matplotlib.pyplot as pl
import numpy as np
from dxfwrite import DXFEngine as dxf


def two_line_intersection(line1_point1:list,line1_point2:list,line2_point1:list,line2_point2:list):
    k1=(line1_point1[1]-line1_point2[1])/(line1_point1[0]-line1_point2[0])
    b1=line1_point1[1]-k1*line1_point1[0]
    k2=(line2_point1[1]-line2_point2[1])/(line2_point1[0]-line2_point2[0])
    b2=line2_point1[1]-k2*line2_point1[0]
    x=int((b2-b1)/(k1-k2))
    y=int(k1*x+b1)
    return [x,y]


def jiajiao(point1,point2,point3):
    cross_product=(point1[0]-point2[0])*(point3[0]-point2[0])+(point1[1]-point2[1])*(point3[1]-point2[1])
    ji=two_point_distance(point1,point2)*two_point_distance(point3,point2)
    angle=math.acos(cross_product/ji)/np.pi*180
    return angle


def test(img):
    cv2.namedWindow("a",cv2.WINDOW_FREERATIO)
    cv2.imshow("a",img)
    cv2.moveWindow("a",1000,300)
    cv2.waitKey(0)

def two_point_distance(point1,point2):
    return np.sqrt((point1[1]-point2[1])**2+(point1[0]-point2[0])**2)

def show_line(img,k,b):
    h,w=img.shape[:2]
    point=[]
    b=int(b)
    x=0
    y=0
    while x!=w:
        if int(k*x+b)==y:
            point.append(x)
            point.append(y)
        x+=1
    while y!=h:
        if int(k*x+b)==y:
            point.append(x)
            point.append(y)
        y+=1
    while x!=0:
        if int(k*x+b)==y:
            point.append(x)
            point.append(y)
        x-=1
    while y!=0:
        if int(k*x+b)==y:
            point.append(x)
            point.append(y)
        y-=1
'''
    if len(point)==4:
        pass

    else:
        print("有{}个点".format(len(point)))
'''

class picture_process (object):
    xuan_zhong=-1
    center=[0,0]
    universal_counter=[]
    perimeter,t=0,0
    all_point=np.zeros((8,2),dtype=int)

    @classmethod
    def save(self,img):
        state=np.load("state.npy")
        if state[3]==0:
            return
        c=picture_process.universal_counter
        
        draw=dxf.drawing("lunkuo.dxf")
        for i in c[picture_process.t]:
            draw.add(dxf.point((i[0][0],i[0][1])))
        draw.save()
        img2=picture_process.sobel(img) 
        k=np.ones((2,2),np.uint8)
        r,img2=cv2.threshold(img2,40,255,cv2.THRESH_BINARY)
        img2=cv2.erode(img2,k)
        counters,h=cv2.findContours(img2,cv2.RETR_EXTERNAL ,cv2.CHAIN_APPROX_NONE)
        a=np.zeros(img.shape,np.uint8)
        cv2.drawContours(a,counters,-1,(255,255,255),1)
       
        draw2=dxf.drawing("lunkuo2.dxf")
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                if a.item(i,j)!=0:
                    draw2.add(dxf.point((i,j)))
        draw2.save()
        state[3]=0
        np.save("state.npy",state)
        

    @classmethod
    def draw_point(self,img,all_point):
        k=[7,7]
        for i in all_point:
            if (i[0]==0 and i[1]==0):
                pass
            else:
                cv2.circle(img,(i[0],i[1]),4,(0,0,255),-1)
        if picture_process.xuan_zhong!=-1:
            zuobiao=picture_process.all_point[picture_process.xuan_zhong]
            cv2.rectangle(img,zuobiao-k,zuobiao+k,(100,210,25),2)

    
        
    @classmethod
    def scharr(self,img):
        schx=cv2.Scharr(img,cv2.CV_64F,1,0)
        schy=cv2.Scharr(img,cv2.CV_64F,0,1)
        schx=cv2.convertScaleAbs(schx)
        schy=cv2.convertScaleAbs(schy)
        sch=cv2.addWeighted(schx,0.5,schy,0.5,0)
        return sch


    @classmethod
    def approximate_counter(self,xishu ):
        perimeter=xishu*picture_process.perimeter
        return cv2.approxPolyDP(picture_process.universal_counter[picture_process.t],perimeter,True)

    @classmethod
    def file(self): 
        files= os.listdir("picture")
        files.sort()
        for i in range(len(files)):
            files[i]="picture/"+files[i]
        return files
        
        
    @classmethod
    def sobel(self,img):
        #img=cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
        sobx=cv2.Sobel(img,cv2.CV_64F ,1,0,ksize=3)
        sobx=cv2.convertScaleAbs(sobx)
        soby=cv2.Sobel(img,cv2.CV_64F ,0,1,ksize=3)
        soby=cv2.convertScaleAbs(soby)
        img=cv2.addWeighted(sobx,0.5,soby,0.5,0)
        return img

    @classmethod
    def background_off(self,img,plt):
        #将方框外像素清空
        zeros = np.full(img.shape,255,dtype=np.uint8)
        cv2.rectangle(zeros,plt[0],plt[1],(0,0,0),-1)
        img2=cv2.add(zeros,img)
        #hist=cv2.calcHist([img2],[0],None,[256],[0,256])
        #print(np.array(hist,dtype=np.uint8))
        #pl.hist(img2.ravel(),128)
        #pl.show()
        
        return img2

    @classmethod
    def count_point(self,img):
        picture_process.universal_counter=picture_process.find_counter(img)#找轮廓函数，返回轮廓

        picture_process.max_perimeter()#寻找最大轮廓，即脚部轮廓

        picture_process.find_first_point(img)#寻找0点

        picture_process.find_second_point(img)#寻找1点

        picture_process.find_f_point(img,0.77)#剩下点



        #return all_point
        return img


    @classmethod
    def find_counter(self,img):
        r,img=cv2.threshold(img,251,255,cv2.THRESH_BINARY_INV)#二值化
        counters,h=cv2.findContours(img,cv2.RETR_EXTERNAL ,cv2.CHAIN_APPROX_NONE)
        return counters

    @classmethod
    def max_perimeter(self):
        counter=picture_process.universal_counter
        t=0
        perimter=0
        first=np.array(counter,dtype=object).shape
        for i in range(first[0]):
            p=cv2.arcLength(counter[i],True)
            if p > perimter:
                perimter=p
                t=i
        picture_process.perimeter=perimter
        picture_process.t=t
        

    @classmethod
    def find_first_point(self,img):
        h=img.shape[0]
        rec_counter=picture_process.approximate_counter(0.008)#用多边形近似轮廓
        flat_counter=list(rec_counter.ravel())
        i=1
        while len(flat_counter)>i:
            if(flat_counter[i]>0.7*h):
                del flat_counter[i]
                del flat_counter[i-1]
            else:
                i+=2
        i=flat_counter.index(max(flat_counter[::2]))#定位x最大值坐标
        picture_process.all_point[0][0]=flat_counter[i]
        picture_process.all_point[0][1]=flat_counter[i+1]-6

    @classmethod
    def find_second_point(self,img):
        
        first_point=picture_process.all_point[0].copy()
        height,width=img.shape[:2]
        a=np.zeros(img.shape[:2],np.uint8)
        copyimg=cv2.drawContours(a,picture_process.universal_counter[picture_process.t],-1,(255,255,255),1)
        if (first_point[1]<int(height*0.6) and int(width*0.3)<first_point[0] ):#0点坐标正常则裁剪
            copyimg=copyimg[first_point[1]:int(height*0.6),int(width*0.3):first_point[0]]   

        flag=0
        for i in range(copyimg.shape[1]):
            for j in range(copyimg.shape[0]):
                if copyimg.item(j,i)!=0:
                    if flag:
                        x=int(width*0.3)+i
                        y=first_point[1]+j
                        picture_process.all_point[1][0]=x
                        picture_process.all_point[1][1]=y
                        return 0
                    else:
                        flag=1
                        break

    @classmethod
    def line(self,img):
        p=picture_process.all_point#顺序是 b g r 
        cv2.line(img,p[4],p[5],(0,0,255),2)
        cv2.line(img,p[5],p[2],(0,0,255),2)
        cv2.line(img,p[0],p[1],(0,0,255),2)
        cv2.line(img,p[2],p[0],(0,0,255),2)
        cv2.line(img,p[3],p[0],(0,0,255),2)
        cv2.line(img,p[3],p[2],(0,0,255),2)
        cv2.line(img,p[7],p[6],(0,0,255),2)
        cv2.line(img,(int(p[5][0]+0.4*(p[5][0]-p[4][0])),int(p[5][1]+0.4*(p[5][1]-p[4][1]))),p[5],(0,0,255),2)
        angle=jiajiao(p[2],p[5],p[4])
        cv2.putText(img,"angle1={:.2f}".format((180-angle)),(700,400),cv2.FONT_HERSHEY_COMPLEX,1.3,(0,0,255),2)#显示角度


    @classmethod
    def find_f_point(self,img,beta): 
        
        jiao_dian=[]
        counters=picture_process.universal_counter
        k=(picture_process.all_point[0][1]-picture_process.all_point[1][1])/(picture_process.all_point[0][0]-picture_process.all_point[1][0])#计算01直线斜率
        b=int(picture_process.all_point[0][1]-k*picture_process.all_point[0][0])
        alpha=two_point_distance(picture_process.all_point[0],picture_process.all_point[1])#得到01线段长度
        show_line(img,k,b+beta*alpha)#直线平移计算交点
        for i in counters[picture_process.t]:
            if int(k*i[0][0]+b+beta*alpha)==i[0][1] :
                jiao_dian.append(i[0][0])
                jiao_dian.append(i[0][1])

        if len (jiao_dian)==4:#刚好有两个交点（6和7）时计算4点

            picture_process.all_point[4][0]=int((jiao_dian[0]-jiao_dian[2])*0.4+jiao_dian[2])
            picture_process.all_point[4][1]=int((jiao_dian[1]-jiao_dian[3])*0.4+jiao_dian[3])
            picture_process.all_point[6]=[jiao_dian[0],jiao_dian[1]]
            picture_process.all_point[7]=[jiao_dian[2],jiao_dian[3]]
            g_point=two_line_intersection(picture_process.all_point[0],picture_process.all_point[1],picture_process.all_point[2],[(picture_process.all_point[0][0]+picture_process.all_point[3][0])//2,(picture_process.all_point[0][1]+picture_process.all_point[3][1])//2])#计算5点
            picture_process.all_point[5]=g_point

