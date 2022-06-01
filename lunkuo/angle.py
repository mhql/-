# coding=utf-8
import cv2
import os
import numpy as np
import class2

#从main函数开始

accuary=1 #精准度，手动调节。建议1到5.越高速度越慢
flag=0

def bright(img,c,gamma):
    blank=np.zeros(img.shape,dtype=np.uint8)
    img=cv2.addWeighted(img,c,blank,1-c,gamma)
    return img

def draw_location(img):
    filename=os.listdir("picture")#读取模板文件名
    fit=[0]#匹配度
    zuobiao=[0,0,0,0]
    max=[]
    name=[]
    for i in filename:
        tel=cv2.imread(("picture/"+i),0)
        p=i[0:-4].split(",")#去除后缀名
        for i in range(accuary+1):
            scale=1-0.2*i/accuary #缩放比例
            try:
                tel=cv2.resize(tel,None,None,scale,scale,cv2.INTER_AREA)#调整模板大小。为原图一倍到0.64倍之间
                res=cv2.matchTemplate(img,tel,cv2.TM_CCOEFF_NORMED)
                minv,maxv,minl,maxl=cv2.minMaxLoc(res)#maxv为最大匹配度，maxl为匹配坐标
                if maxv>fit[0]:
                    fit[0]=maxv
                    max=maxl
                    for i in range(len(p)):
                        zuobiao[i]=round(int(p[i])*scale)
                        name=p
            except:
                continue
    print(name)
    class2.picture_process.all_point[2][0]=max[0]+int(zuobiao[2])
    class2.picture_process.all_point[2][1]=max[1]+int(zuobiao[3])
    class2.picture_process.all_point[3][0]=max[0]+int(zuobiao[0])
    class2.picture_process.all_point[3][1]=max[1]+int(zuobiao[1])

def move(event,x,y,p,f):
    cishu=0
    global flag
    if event==cv2.EVENT_LBUTTONDOWN:
        for i in class2.picture_process.all_point:
            if (abs(i[0]-x)<10 and abs(i[1]-y)<10):
                class2.picture_process.xuan_zhong=cishu
                flag=1
            cishu+=1
        cishu=0
    if event==cv2.EVENT_RBUTTONDOWN:
        if flag==1:
            i=class2.picture_process.xuan_zhong
            class2.picture_process.all_point[i]=[x,y]
            flag=0
            class2.picture_process.xuan_zhong=-1

def mid_point(point1,point2):
    point=[0,0]
    point[0]=(point1[0]+point2[0])//2
    point[1]=(point1[1]+point2[1])//2
    return point


def main():
    cap=cv2.VideoCapture("8.mp4")#输入读取视频名称。读取摄像头为0
    ret,f=cap.read()
    height=f.shape[0]#获得视频大小
    width=f.shape[1]
    plt=np.array([[width*0.33,height*0.04],[width*0.7,height]],dtype=np.int32)#调整框的大小。第一个点矩阵左上角坐标，第二个右下角坐标
    cv2.namedWindow("window",cv2.WINDOW_KEEPRATIO)
    cv2.setMouseCallback("window",move)#鼠标相应事件，用于暂停移动点位
    while 1:
        state=np.load("state.npy")#读取state内容决定是否暂停或翻转
        if cap.isOpened and state[0]: 
            state=np.load("state.npy")
            ret,f=cap.read()
            if(state[2]):
                f=cv2.flip(f,1)
            frame=f.copy()
            process_frame=bright(frame,1.8,30)#增加亮度
            process_frame=cv2.cvtColor(process_frame,cv2.COLOR_BGR2GRAY)
            
            
            process_frame=class2.picture_process.background_off(process_frame,plt )#去背景
            draw_location(process_frame)#模板匹配函数
            process_frame=class2.picture_process.count_point(process_frame)#找点主函数
            
            
            
            cv2.rectangle(frame,plt[0],plt[1],(100,210,20),2)#画绿框
            class2.picture_process.draw_point(frame,class2.picture_process.all_point)#标出每个点
            class2.picture_process.line(frame)#连线

            #cv2.imshow("window",frame)  
            if(not state[1]):
                while(not state[1]):
                    cv2.imshow("window",frame)
                    class2.picture_process.save(process_frame)
                    frame=f.copy()
                    cv2.rectangle(frame,plt[0],plt[1],(100,210,20),2)
                    class2.picture_process.draw_point(frame,class2.picture_process.all_point)
                    yi_liu_suan_si()
                    class2.picture_process.line(frame)
                    state=np.load("state.npy")
                    cv2.waitKey(10)
            else:
                cv2.imshow("window",frame)
                cv2.waitKey(10)
        else:
            cv2.waitKey(50)
            cv2.destroyAllWindows()

def yi_liu_suan_si():

    
    p=class2.picture_process.all_point
    p[5]=class2.two_line_intersection(p[0],p[1],[(p[0][0]+p[3][0])//2,(p[0][1]+p[3][1])//2],p[2])
    p[4][0]=int((p[6][0]-p[7][0])*0.4+p[7][0])
    p[4][1]=int((p[6][1]-p[7][1])*0.4+p[7][1])





main()