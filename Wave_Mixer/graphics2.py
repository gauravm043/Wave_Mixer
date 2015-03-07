from Tkinter import *
from wave_functions import *
from audio_functions import *
import record_sound
import os,sys,signal
import Tkinter, Tkconstants, tkFileDialog
import signal
files_1=[]
files_2=[]
files_3=[]
bondiat=[]

class Model(Frame):
    def __init__(self, root,cord_x,cord_y,identifier):
        self.identity=identifier
        self.open_files=[]
        self.amplitude=1
        self.shift=1
        self.scale=1
        self.xx1=0
        self.yy1=0
        self.signal='initiate'
        self.mast = 1
        self.pid=-1
        self.xx1=cord_x
        self.yy1=cord_y
        Frame.__init__(self, root)
        self.Graphics(cord_x,cord_y,root)
        self.mast = Label(root, text="No File Selected!")
        self.mast.pack()
        self.mast.place(bordermode=OUTSIDE,x=self.xx1+10,y=self.yy1+50)

    def askopenfile(self):
        # Defining File Types
        file_opt = options = {}
        options['defaultextension'] = '.wav'
        options['filetypes'] = [('all files', '.wav')]
        options['initialdir'] = './'
        options['initialfile'] = 'myfile.wav'
        options['parent'] = root
        options['title'] = 'Select a file'
        fname=tkFileDialog.askopenfile(mode='r',**file_opt)
        name=fname
        # Change the corresponding Labels
        if not(isinstance(name, str)):
            # Convert the file type object sent to string type and retrieve the file name
            name=str(name)
            name=name.split('\'')
            name=name[1]
            fname=name
            name=name.split('/')
            name=name[-1]

        self.open_files.append(fname)
        give=''
        give=give+name
        self.mast.destroy()
        self.mast = Label(root, text=give)
        self.mast.pack()
        self.mast.place(bordermode=OUTSIDE,x=self.xx1+10,y=self.yy1+50)

        if self.identity ==1:
            files_1.append(fname)
        elif self.identity ==2:
            files_2.append(fname)
        else:
            files_3.append(fname)

        return fname
    def stop(self):
        if self.pid>0:
            os.kill(self.pid,9)
            self.pid=-1
            self.signal='initiate'

    def play(self,objects=0):
        
        if (self.signal=='initiate'):
            self.signal='playing'
            print "new : ",self.pid,self.signal
        
        if (self.pid > 0 and self.signal=='playing'):
            os.kill(self.pid, signal.SIGSTOP)
            self.signal='paused'
            print "new : ",self.pid,self.signal
            return
        elif(self.pid>0 and self.signal=='paused'):
            os.kill(self.pid,signal.SIGCONT)
            self.signal='playing'
            print "new : ",self.pid,self.signal
            return
            
        file_name=''
        if(len(self.open_files)>=1):
            original=self.open_files[len(self.open_files)-1]
            file_name=self.open_files[len(self.open_files)-1]
            if(len(self.open_files)>=1):
                if (float(self.amplitude)!=float(1) and float(self.amplitude)!=float(0.0)):
                    file_name=Amplitude_Scaling(objects,self.open_files[len(self.open_files)-1],float(self.amplitude))
                    self.open_files[0]=file_name
                if float(self.shift) != float(0):
                    file_name=Time_Shifting(objects,self.open_files[len(self.open_files)-1],float(self.shift))
                    self.open_files[0]=file_name
                if (float(self.scale)!=float(0) and float(self.scale)!=float(1)):
                    file_name=Time_Scaling(objects,self.open_files[len(self.open_files)-1],float(self.scale))
                    self.open_files[0]=file_name
                if float(self.reverse.get()) ==float(1):
                    file_name=Time_reversal(objects,self.open_files[len(self.open_files)-1])
                    self.open_files[0]=file_name
            self.open_files[len(self.open_files)-1]=original
            
            if not(isinstance(file_name, str)):
                # Convert the file type object sent to string type and retrieve the file name
                file_name=str(file_name)
                file_name=file_name.split('\'')
                file_name=file_name[1]

        print 'rcecieved' , objects
        if objects==0:
            if file_name!='':
                self.initiate(file_name)
        else:
            bondiat.append(file_name)
            
    def initiate(self,file_name):
        self.pid=os.fork()
        if self.pid==0:
            child=Audio()
            child.play_audio(file_name)
            sys.exit(0)

    def set_amplitude(self,val):
        self.amplitude=val

    def set_timeshift(self,val):
        self.shift=val

    def set_timescale(self,val):
        self.scale=val

    def get_files(self):
        return self.open_files

    def get_amplitude(self):
        return self.amplitude    

    def get_timeshift(self):
        return self.shift

    def get_timescale(self):
        return self.scale

    def get_reverse(self):
        return self.reverse

    def get_mix(self):
        return self.mix

    def get_modulate(self):
        return self.modulate


    def place_text(self,back,item,x1,y1):
        text = Text(root,bg=back)
        text.insert(INSERT,item)
        text.config(state=DISABLED)
        text.pack()
        text.place(bordermode=OUTSIDE, height=30, width=100,x=x1,y=y1)

    def place_slider(self,x1,y1,function):
        w = Scale(root, from_=1, to=5, orient=HORIZONTAL,resolution=0.25,command=function)
        w.pack()
        w.place(bordermode=OUTSIDE, x=x1,y=y1)
    
    def place_slider2(self,x1,y1,function):
        w = Scale(root, from_=-1, to=1, orient=HORIZONTAL,resolution=0.5,command=function)
        w.pack()
        w.place(bordermode=OUTSIDE, x=x1,y=y1)
    
    def place_slider3(self,x1,y1,function):
        w = Scale(root, from_=0, to=8, orient=HORIZONTAL,resolution=0.125,command=function)
        w.pack()
        w.place(bordermode=OUTSIDE, x=x1,y=y1)

    def place_reverse(self,x1,y1,text):
        self.reverse=IntVar()
        C1 = Checkbutton(root, text = text, variable = self.reverse, \
                onvalue = 1, offvalue = 0,justify="left")
        C1.pack()
        C1.place(bordermode=OUTSIDE,x=x1,y=y1)

    def place_modulate(self,x1,y1,text):
        self.modulate=IntVar()
        C1 = Checkbutton(root, text = text, variable = self.modulate, \
                onvalue = 1, offvalue = 0,justify="left")
        C1.pack()
        C1.place(bordermode=OUTSIDE,x=x1,y=y1)

    def place_mix(self,x1,y1,text):
        self.mix=IntVar()
        C1 = Checkbutton(root, text = text, variable = self.mix, \
                onvalue = 1, offvalue = 0,justify="left")
        C1.pack()
        C1.place(bordermode=OUTSIDE,x=x1,y=y1)

    def Graphics(self,cord_x,cord_y,root):
        heading = Label(root, text="WAVE MIXER",font=("Helvetica",20),fg="red")
        heading.pack()
        heading.place(bordermode=OUTSIDE,x=530,y=10)
        
        
        button_opt = {'fill': Tkconstants.BOTH, 'padx': 5, 'pady': 5}
        B=Tkinter.Button(root, text='Select a file', command=self.askopenfile)
        B.pack()
        B.place(bordermode=OUTSIDE, height=30, width=100,x=cord_x+150,y=cord_y+40)
        self.place_slider(cord_x+150,cord_y+80,self.set_amplitude)
        self.place_slider2(cord_x+150,cord_y+150,self.set_timeshift)
        self.place_slider3(cord_x+150,cord_y+220,self.set_timescale)
        self.place_text("yellow","Amplitude",cord_x+10,cord_y+100)
        self.place_text("yellow","Time Shift",cord_x+10,cord_y+170)
        self.place_text("yellow","Time Scaling",cord_x+10,cord_y+240)
        self.place_reverse(cord_x+20,cord_y+300,"Time Reversal")
        self.place_modulate(cord_x+20,cord_y+350,"Select for Modulation")
        self.place_mix(cord_x+20,cord_y+400,"Select For Mixing")

        B=Tkinter.Button(root, text='Play', command=self.play)
        B.pack()
        B.place(bordermode=OUTSIDE, height=30, width=60,x=cord_x+20,y=cord_y+450)

        B=Tkinter.Button(root, text='Stop', command=self.stop)
        B.pack()
        B.place(bordermode=OUTSIDE, height=30, width=60,x=cord_x+90,y=cord_y+450)
        
        

pid1=[]


back=[]
mod=[]
# Initialising the data directory used for conversions
if os.path.isdir('./top_secret'):
    # Do nothing
    print 'Already Created'
else:
    os.system('mkdir top_secret')


#Initialising parent
root = Tkinter.Tk()
root.minsize(300,300)
root.geometry("1920x1280")
root.title("XtremEqualiser")
#Initialising Waves
wave1=Model(root,80,30,1)
wave2=Model(root,480,30,2)
wave3=Model(root,880,30,3)
        

# Writing functions for recording Sounds
def recording():
    record_sound.record_to_file('demo1.wav')

def play_record():
        x=os.fork()
        pid1.append(x)
        if x==0:
            child=Audio()
            child.play_audio('demo1.wav')
            sys.exit(0)

def stop_it():
    x=pid1[0]
    if x>0:
        os.kill(x,9)
        del pid1[:]

B=Tkinter.Button(root, text='Record', command=recording)
B.pack()
B.place(bordermode=OUTSIDE, height=30, width=80,x=420,y=550)

B=Tkinter.Button(root, text='Play', command=play_record)
B.pack()
B.place(bordermode=OUTSIDE, height=30, width=80,x=500,y=550)

B=Tkinter.Button(root, text='Stop', command=stop_it)
B.pack()
B.place(bordermode=OUTSIDE, height=30, width=80,x=580,y=550)

mod_mix=[]
mod_bond=[]
mod_mix.append(0)
mod_bond.append(0)
def Mix():
    if len(back) > 0 and mod_mix[0]==1:
        x=back[0]
        os.kill(x,signal.SIGSTOP)
        mod_mix[0]=0
        return
    elif len(back) > 0 and mod_mix[0]==0:
        x=back[0]
        os.kill(x,signal.SIGCONT)
        mod_mix[0]=1
        return

    wave1.play(1)
    wave2.play(2)
    wave3.play(3)
    l1=wave1.get_files()
    l2=wave2.get_files()
    l3=wave3.get_files()
    m1=int(wave1.mix.get())
    m2=int(wave2.mix.get())
    m3=int(wave3.mix.get())
    play=0
    length=len(bondiat)
    if (m1==1 and m2==1 and m3==1 and len(l3)>=1 and len(l1)>=1 and len(l2)>=1):
        play=1
        f=Mixing(1,bondiat[0],bondiat[1])
        if f!='NONE':
            f2=Mixing(1,f,bondiat[2])
        f=f2
    elif (m1==1 and m2==1 and len(l1)>=1 and len(l2)>=1):
        play=1
        # Remember to make wave functions in a class
        f=Mixing(1,bondiat[0],bondiat[1])
    elif (m2==1 and m3==1 and len(l2)>=1 and len(l3)>=1):
        play=1
        # Remember to make wave functions in a class
        f=Mixing(1,bondiat[0],bondiat[1])
    elif (m1==1 and m3==1 and len(l1)>=1 and len(l3)>=1):
        play=1
        # Remember to make wave functions in a class
        f=Mixing(1,bondiat[0],bondiat[1])
    
    if play==1 and f!='NONE':
        mod_mix[0]=1
        pid=os.fork()
        if pid>0:
            back.append(pid)
        if pid==0:
            child=Audio()
            child.play_audio(f)
            sys.exit(0)
    print bondiat
    del bondiat[ : ]

def Modulation():
    if len(mod) > 0 and mod_bond[0]==1:
        x=mod[0]
        os.kill(x,signal.SIGSTOP)
        mod_bond[0]=0
        return
    elif len(mod) > 0 and mod_bond[0]==0:
        x=mod[0]
        os.kill(x,signal.SIGCONT)
        mod_bond[0]=1
        return
    wave1.play(1)
    wave2.play(2)
    wave3.play(3)
    l1=wave1.get_files()
    l2=wave2.get_files()
    l3=wave3.get_files()
    m1=int(wave1.modulate.get())
    m2=int(wave2.modulate.get())
    m3=int(wave3.modulate.get())
    play=0
    f=''
    if (m1==1 and m2==1 and m3==1 and len(l3)>=1 and len(l1)>=1 and len(l2)>=1):
        play=1
        f=Modulate(1,bondiat[0],bondiat[1])
        if f!='NONE':
            f2=Modulate(1,f,bondiat[2])
        f=f2
    elif (m1==1 and m2==1 and len(l1)>=1 and len(l2)>=1):
        play=1
        # Remember to make wave functions in a class
        f=Modulate(1,bondiat[0],bondiat[1])
    elif (m2==1 and m3==1 and len(l2)>=1 and len(l3)>=1):
        play=1
        # Remember to make wave functions in a class
        f=Modulate(1,bondiat[0],bondiat[1])
    elif (m1==1 and m3==1 and len(l1)>=1 and len(l3)>=1):
        play=1
        # Remember to make wave functions in a class
        f=Modulate(1,bondiat[0],bondiat[1])
    if f!='NONE':
        if play==1:
            mod_bond[0]=1
            pid=os.fork()
            if pid>0:
                mod.append(pid)
            if pid==0:
                child=Audio()
                child.play_audio(f)
                sys.exit(0)
    print bondiat
    del bondiat[ : ]

def Stop_Mix():
        os.kill(back[len(back)-1], signal.SIGSTOP)
        del back[:]
        mod_mix[0]=-1


def Stop_Modulate():
        os.kill(mod[len(mod)-1], signal.SIGSTOP)
        del mod[:]
        mod_bond[0]=-1

B=Tkinter.Button(root, text='Mix and Play', command=Mix)
B.pack()
B.place(bordermode=OUTSIDE, height=30, width=100,x=150,y=550)

B=Tkinter.Button(root, text='Stop', command=Stop_Mix)
B.pack()
B.place(bordermode=OUTSIDE, height=30, width=100,x=250,y=550)

B=Tkinter.Button(root, text='Modulate and Play', command=Modulation)
B.pack()
B.place(bordermode=OUTSIDE, height=30, width=150,x=750,y=550)

B=Tkinter.Button(root, text='Stop', command=Stop_Modulate)
B.pack()
B.place(bordermode=OUTSIDE, height=30, width=100,x=900,y=550)


root.mainloop()


#Developing Functionalities
