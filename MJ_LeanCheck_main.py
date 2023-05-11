import PoseModule as pm
import cv2
from tkinter import *
from PIL import Image, ImageTk
from tkinter import filedialog

win=Tk()
win.title("MJ Lean Check")
win.geometry("1280x720+0+0")
win.state("zoomed")
#bg is background color,fg is foreground color/text color
frame_1 = Frame(win, width=1920, height=1080, bg='#ffffff').place(x=0, y=0)#frame height,width,bg=white,place 0,0 means at the top left corner
widget = Label(win, text="Pose Analyzer", font=("Arial", 36, ("bold")), bg="#00fdc0", fg="#000000").pack(pady=10) #lable is used to display text,pack is used to display the text in the window

w = 820
h = 480

cap = cv2.VideoCapture(0)

label1 = Label(win, width=w, height=h)
label1.place(x=600, y=100)#right top corner of the label
    
close_bttn = Button(win,text = "Exit",width=7, height=2, bg = "#ff0000", fg = "#000000", font=("Calibri", 20,"bold"), command = win.destroy).place(x=1200, y=600)#win.destroy means exit the window when the button is clicked

status_label = Label(win, text="Status: ", font=("Arial", 25, "underline bold"), fg="#000000").place(x=30, y=130) #initializing the label
status_txt = StringVar()#strigvar is used to display the text in the label
status_txt_label = Label(win, textvariable=status_txt, font=("Arial", 25, "underline bold"),  fg="#0000fe").place(x=160, y=130)#displaying the text in the label

angle_label = Label(win, text="Angle: ", font=("Arial", 25, "underline bold"), fg="#000000").place(x=30, y=200)
angle_txt = StringVar()
angle_txt_label = Label(win, textvariable=angle_txt, fg = "#0000fe", font=("Arial", 25, "underline bold")).place(x=140, y=200)

side_label = Label(win, text="Side: ", font=("Arial", 25, "underline bold"), fg="#000000").place(x=30, y=270)
side_txt = StringVar()
side_txt_label = Label(win, textvariable=side_txt, fg = "#0000fe", font=("Arial", 25, "underline bold")).place(x=120, y=270)


# For uploading Videos
def video_upload():
    'here we are using global variable because we are using the variable in another function, filedialog is tkinter module and askopenfilename is used to open the file. the file types are given in list to provide user the option to open any file of this file'
    global video_input,cap
    video_input = filedialog.askopenfilename(filetypes=[("Video Files (*.mp4)","*.mp4"),("Image Files (*.jpg)","*.jpg"),("Image Files (*.png)","*.png"),("Image Files (*.gif)","*.gif")])
    if video_input=="": #if the user does not select any file then the webcam will open 
        cap.set(cv2.CAP_PROP_POS_FRAMES)
    else:    
        cap = cv2.VideoCapture(video_input)

# For Live feed
def cam_live():
    global video_input,cap
    video_input = 0
    cap = cv2.VideoCapture(video_input)

# _________________Live Button ____________________________

live_btn = Button(win, height = 1, width=8,font=("Calibri", 20, "bold"),  text="Live", fg="#114488", bg="#77FFD0", command=cam_live)
live_btn.place(x=200,y=600)

# _________________upload Button___________________________

upload_btn = Button(win, height = 1, width=8,text="upload",font=("Calibri", 20, "bold"), fg="#114488", bg='#77FFD0', command=video_upload)
upload_btn.place(x=600,y=600)

#__________________Pose Detection__________________________

detector = pm.PoseDetector()
paused=False

def toggle_pause():
    global paused
    paused=not paused
                        
play_btn = Button(win,text="Play",width=10,height=2,bg="#00ff00",fg="#000000",font=("Calibri",20,"bold"),command=toggle_pause)
                        


while True:
    success, img = cap.read() #for example succes has value true and img has the image like data in form of array of pixelsi-e numpy.ndarray
    if success:
        img=cv2.flip(img, 1)#flip is used to flip the image, 1 means flip horizontally
        img=cv2.resize(img,(w,h))#resize is used to resize the image
        img=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = detector.findPose(img) #this function is defined in PoseModule.py
        lmList=detector.findPosition(img)#this function is defined in PoseModule.py,lmlist==landmarks_list

        if len(lmList) != 0:#means that a pose is detected
            if lmList[24][3] > lmList[23][3]:#specifies left side is detected
            ##____________________Left side____________________##
                alpha,beta,gamma=detector.findAngle(img, 11,23,25,27, side="left")
                side_txt.set("Left")
                
            elif lmList[24][3] < lmList[23][3]:#specifies right side is detected
            ##____________________Right side___________________##
                alpha,beta,gamma=detector.findAngle(img, 12,24,26,28, side="right")
                side_txt.set("Right")

            ## Angle Accuracy Determination
            if 170<=beta<=190:
                if 170<=gamma<=190:
                    if 35<=alpha<=55:
                        status_txt.set("Ideal")
                        play_btn.place(x=40,y=400)
                        paused=True
                        
                    elif 55<alpha<=70:
                        status_txt.set("close to ideal")
                    elif alpha<35:
                        status_txt.set("Too Much Bent")
                    else:
                        status_txt.set("totally wrong")
                else:
                    status_txt.set("Straight Your Legs")
                    alpha='--'
            else:
                status_txt.set("Straight Your Back")
                alpha='--'
            if type(alpha)==float:
                angle_txt.set(str(round(alpha))+'°')
            else:
                angle_txt.set(alpha)

        image = Image.fromarray(img)
        finalImage = ImageTk.PhotoImage(image)
        label1.configure(image=finalImage)
        label1.image = finalImage
        while paused==True:
            win.update()
            cv2.waitKey(0)
            
            

    else:
        cap.set(cv2.CAP_PROP_POS_FRAMES,0)
    play_btn.place_forget()
    win.update()    