import numpy as np
import tkinter as tk

class Set_window:
    state=np.array([1,1,0,0])
    whether_open=True
    whether_continue=True
    reverse=0
    lk=0

    @classmethod
    def conti(self):
        Set_window.state[1]=1
        np.save("state.npy",Set_window.state)

    @classmethod
    def reverse(self):
        Set_window.state[2]=not Set_window.state[2]
        np.save("state.npy",Set_window.state)
    

    @classmethod
    def camera_open(self):
        Set_window.state[0]=1
        np.save("state.npy",Set_window.state)
        
    @classmethod
    def pause(self):
        Set_window.state[1]=0
        Set_window.state[3]=1
        np.save("state.npy",Set_window.state)

    @classmethod
    def close_all(self):
        Set_window.state[0]=0
        np.save("state.npy",Set_window.state)

    def __init__(self):

        window=tk.Tk()
        window.title("图像识别")
        window.geometry("250x400")
        #hide_window()#隐藏窗口

        button_1_camera_open=tk.Button(window,text="open",width=10,height=1,command=Set_window.camera_open)
        button_1_camera_open.place(relx=0.3,rely=0.05)

        button_2_close=tk.Button(window,text="close",width=10,height=1,command=Set_window.close_all)
        button_2_close.place(relx=0.3,rely=0.2)

        button_3_reverse=tk.Button(window,text="reverse",width=10,height=1,command=Set_window.reverse)
        button_3_reverse.place(relx=0.3,rely=0.35)

        button_4_pause=tk.Button(window,text="pause",width=10,height=1,command=Set_window.pause)
        button_4_pause.place(relx=0.3,rely=0.5)

        button_5_continue=tk.Button(window,text="continue",width=10,height=1,command=Set_window.conti)
        button_5_continue.place(relx=0.3,rely=0.65)

        

        window.mainloop()

    

win=Set_window()


