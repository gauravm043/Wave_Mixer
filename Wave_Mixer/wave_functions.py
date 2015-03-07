import wave,struct
import sys,os


# Returns a tuple (nchannels, sampwidth, framerate, nframes, comptype, compname)

def Amplitude_Scaling(objects,fname,amount):
    
    if not(isinstance(fname, str)):
        # Convert the file type object sent to string type and retrieve the file name
        fname=str(fname)
        fname=fname.split('\'')
        fname=fname[1]
    
    wav_file = wave.open(fname,'r')
    parameters = wav_file.getparams()
    no_frames=wav_file.getnframes()
    print parameters
    myself='top_secret/amplitude'+str(objects)+'.wav'
    new_file = wave.open(myself, 'w')
    new_file.setparams(parameters)
    waveData = wav_file.readframes(parameters[3])
    total_samples= parameters[0]*parameters[3]          # number of channels * number of frames
    data=[]
    var=''
    if parameters[1]==1:     # If the wave data is of 8 bit
        less=-127
        more=127
        var= "%iB" % total_samples
        amp = struct.unpack(var, waveData)
        for i in range(len(amp)):
            data.append(int(amp[i])-128)
            x=data[i]
            if(x*amount>=less and x*amount<= more):
                data[i]=x*amount+128
            elif(x*amount>more):
                data[i]=more+128
            else:
                data[i]=less+128
    else:                   # If it is 16 bit
        less=-32767
        more=32767
        var= "%ih" % total_samples
        amp = struct.unpack(var, waveData)
        for i in range(len(amp)):
            data.append(int(amp[i]))
            x=data[i]
            if(x*amount>=less and x*amount<= more):
                data[i]=x*amount
            elif(x*amount>more):
                data[i]=more
            else:
                data[i]=less
    to_write=struct.pack(var,*data)
    new_file.writeframes(to_write)
    new_file.close()
    return myself
def Time_reversal(objects,fname):
    print fname
    if not(isinstance(fname, str)):
        # Convert the file type object sent to string type and retrieve the file name
        fname=str(fname)
        fname=fname.split('\'')
        fname=fname[1]
    
    wav_file=wave.open(fname,'r')
    parameters=wav_file.getparams()
    print parameters
    total_samples=parameters[0]*parameters[3]
    if parameters[1]==1:
        encode = "%iB" % (total_samples)
    elif parameters[1]==2:
        encode = "%ih" % (total_samples)
    
    wave_data=wav_file.readframes(parameters[3])
    amp=struct.unpack(encode,wave_data)
    data=[]
    if parameters[0]==1:        # If it is mono audio
        for i in range(len(amp)-1,-1,-1):
            data.append(int(amp[i]))
    else:
        left=[]
        right=[]
        for i in range(0,len(amp),2):
            left.append(int(amp[i]))
            if i+1<len(amp):
                right.append(int(amp[i+1]))
        left.reverse()
        right.reverse()
        for i in range(0,len(amp)/2):
            if i<len(left):
                data.append(left[i])
            if i<len(right):
                data.append(right[i])

    to_write=struct.pack(encode,*data)
    myself='top_secret/reverse_file'+str(objects)+'.wav'
    new_file=wave.open(myself,'w')
    new_file.setparams(parameters)
    new_file.writeframes(to_write)
    new_file.close()
    return myself

def Time_Scaling(objects,fname,amount):
    if not(isinstance(fname, str)):
        # Convert the file type object sent to string type and retrieve the file name
        fname=str(fname)
        fname=fname.split('\'')
        fname=fname[1]
    
    encode='' 
    wav_file=wave.open(fname,'r')
    myself='top_secret/time_scaled'+str(objects)+'.wav'
    new_file=wave.open(myself,'w')
    parameters=wav_file.getparams()
    parameters=list(parameters)
    total_samples=parameters[0]*parameters[3]
    if parameters[1]==1:
        encode = "%iB" % (total_samples)
    elif parameters[1]==2:
        encode = "%ih" % (total_samples)
    wave_data=wav_file.readframes(parameters[3])
    amp=struct.unpack(encode,wave_data)
    data=[]
    amp=list(amp)
    gaurav=0
    if parameters[0]==1:
        for i in range(int(len(amp)/amount)):
            if(int(i*amount)>(len(amp)-1)):
                break
            gaurav+=1
            data.append(int(amp[int(i*amount)]))
    else:
        for i in range(0,int(len(amp)/amount),2):
            if(int(i*amount)>(len(amp)-1)):
                break
            gaurav+=1
            data.append(int(amp[int(i*amount)]))
            if(int(i+1)*amount>(len(amp)-1)):
                data.append(0)
            else:
                data.append(int(amp[int((i+1)*amount)]))
    parameters[3]=gaurav
    total_samples=parameters[0]*parameters[3]
    if parameters[1]==1:
        encode = "%iB" % (total_samples)
    elif parameters[1]==2:
        encode = "%ih" % (total_samples)

    parameters=tuple(parameters)

    to_write=struct.pack(encode,*data)
    new_file.setparams(parameters)
    new_file.writeframes(to_write)
    new_file.close()
    return myself

def Time_Shifting(objects,fname,amount):
    if not(isinstance(fname, str)):
        # Convert the file type object sent to string type and retrieve the file name
        fname=str(fname)
        fname=fname.split('\'')
        fname=fname[1]
    
    wav_file=wave.open(fname,'r')
    myself='top_secret/time_shifted'+str(objects)+'.wav'
    new_file=wave.open(myself,'w')
    parameters=wav_file.getparams()
    print parameters
    total_samples=parameters[0]*parameters[3]
    if parameters[1]==1:
        encode = "%iB" % (total_samples)
    elif parameters[1]==2:
        encode = "%ih" % (total_samples)
    wave_data=wav_file.readframes(parameters[3])
    amp=struct.unpack(encode,wave_data)
    data=[]
    new_frames=0
    extra_frames=int(parameters[2]*amount)
    print "extra : ",extra_frames,"original :",parameters[3]
    if extra_frames>0:
        for i in range(0,extra_frames):
            if parameters[1]==2:
                data.append(0)
                if parameters[0]==2:                    # extra sound if stereo channel
                    data.append(0)
            if parameters[1]==1:
                data.append(128)
                if parameters[0]==2:                    # extra sound if stereo channel
                    data.append(128)
        for i in range(0,len(amp)):
            data.append(int(amp[i]))
        new_frames=parameters[3]+extra_frames
    else:
        for i in range(abs(extra_frames)*parameters[0],len(amp)):
            data.append(int(amp[i]))
        new_frames=parameters[3]-abs(extra_frames)

    
    total_samples=parameters[0]*new_frames
    if parameters[1]==1:
        encode = "%iB" % (total_samples)
    elif parameters[1]==2:
        encode = "%ih" % (total_samples)
    print len(data)
    to_write=struct.pack(encode,*data)
    new_parameters=(parameters[0],parameters[1],parameters[2],new_frames,parameters[4],parameters[5])
    new_file.setparams(new_parameters)
    new_file.writeframes(to_write)
    new_file.close()
    return myself

def Mixing(objects,fname1,fname2):
    wav_file1=wave.open(fname1,'r')
    wav_file2=wave.open(fname2,'r')
    parameters1=wav_file1.getparams()
    parameters2=wav_file2.getparams()
    print parameters1
    print parameters2
    nframes=0
    # Checking whether they are compatible for mixing or not
    if parameters1[0]==parameters2[0] and parameters1[1]==parameters2[1] and parameters1[2]==parameters2[2]:
        nframes=max(parameters1[3],parameters2[3])
        total_samples=parameters1[3]*parameters1[0]
        encode1=''
        encode2=''
        encode=''
        x=int(parameters1[0]*nframes)
        
        if parameters1[1]==1:
            encode1 = "%iB" % (total_samples)
            encode = "%iB" % (x)
        if parameters1[1]==2:
            encode = "%ih" % (x)
            encode1 = "%ih" % (total_samples)
        
        total_samples=parameters2[3]*parameters2[0]
        if parameters2[1]==1:
            encode2 = "%iB" % (total_samples)
        if parameters2[1]==2:
            encode2 = "%ih" % (total_samples)
        wave_data1=wav_file1.readframes(parameters1[3])
        amp1=struct.unpack(encode1,wave_data1)
        amp1=list(amp1)

        wave_data2=wav_file2.readframes(parameters2[3])
        amp2=struct.unpack(encode2,wave_data2)
        amp2=list(amp2)

        data=[]
        length=max(len(amp1),len(amp2))
        for i in range(length):
            temp=0
            if parameters1[1]==2:       # Mixing for 16 bit files
                if i < len(amp1) and i < len(amp2):
                    temp=amp1[i]+amp2[i]
                elif i < len(amp1):
                    temp=amp1[i]+0
                else:
                    temp=amp2[i]+0
               # print temp 
                if(temp>=-32767 and temp<=32767):
                    data.append(int(temp))
                elif(temp>32767):
                    data.append(int(32767))
                else:
                    data.append(int(-32767))
                
                
            elif parameters1[1]==1:
                if i < len(amp1) and i < len(amp2):
                    temp=(amp1[i]+amp2[i]) -128 -128
                elif i < len(amp1):
                    temp=amp1[i]-128
                else:
                    temp=amp2[i]-128
               # print temp 
                if(temp>=-127 and temp<=127):
                    data.append(int(temp)+128)
                elif(temp>255):
                    data.append(int(255))
                else:
                    data.append(int(0))

        wav_file1.close()
        wav_file2.close()
        myself='top_secret/mix'+str(objects)+'.wav'
        new_file=wave.open(myself,'w')
        print len(data)
        new_parameters=(parameters1[0],parameters1[1],parameters1[2],nframes,parameters1[4],parameters1[5])
        print new_parameters
        
        new_file.setparams(new_parameters)
        to_write=struct.pack(encode,*data)
        
        new_file.writeframes(to_write)
        new_file.close()
    else:
        return 'NONE'
    return myself


def Modulate(objects,fname1,fname2):
    wav_file1=wave.open(fname1,'r')
    wav_file2=wave.open(fname2,'r')
    myself='top_secret/modulate'+str(objects)+'.wav'
    new_file=wave.open(myself,'w')
    parameters1=wav_file1.getparams()
    parameters2=wav_file2.getparams()
    print "parameters    :",parameters1
    print "parameters    :",parameters2
    nframes=0
    # Checking whether they are compatible for mixing or not
    if parameters1[0]==parameters2[0] and parameters1[1]==parameters2[1] and parameters1[2]==parameters2[2]:
        nframes=max(parameters1[3],parameters2[3])
        total_samples=parameters1[3]*parameters1[0]
        encode1=''
        encode2=''
        encode=''
        x=int(parameters1[0]*nframes)
        
        if parameters1[1]==1:
            encode1 = "%iB" % (total_samples)
            encode = "%iB" % (x)
        if parameters1[1]==2:
            encode = "%ih" % (x)
            encode1 = "%ih" % (total_samples)
        
        total_samples=parameters2[3]*parameters2[0]
        if parameters2[1]==1:
            encode2 = "%iB" % (total_samples)
        if parameters2[1]==2:
            encode2 = "%ih" % (total_samples)
        wave_data1=wav_file1.readframes(parameters1[3])
        amp1=struct.unpack(encode1,wave_data1)
        amp1=list(amp1)

        wave_data2=wav_file2.readframes(parameters2[3])
        amp2=struct.unpack(encode2,wave_data2)
        amp2=list(amp2)

        data=[]
        length=max(len(amp1),len(amp2))
        for i in range(length):
            temp=0
            if parameters1[1]==2:       # Mixing for 16 bit files
                if i < len(amp1) and i < len(amp2):
                    temp=amp1[i]*amp2[i]
                elif i < len(amp1):
                    temp=amp1[i]+0
                else:
                    temp=amp2[i]+0
               # print temp 
                if(temp>=-32767 and temp<=32767):
                    data.append(int(temp))
                elif(temp>32767):
                    data.append(int(32767))
                else:
                    data.append(int(-32767))
                
                
            elif parameters1[1]==1:
                if i < len(amp1) and i < len(amp2):
                    temp=((amp1[i]-128)*(amp2[i] - 128))
                elif i < len(amp1):
                    temp=amp1[i]-128
                else:
                    temp=amp2[i]-128
               # print temp 
                if(temp>=-127 and temp<=127):
                    data.append(int(temp)+128)
                elif(temp>255):
                    data.append(int(255))
                else:
                    data.append(int(0))

        wav_file1.close()
        wav_file2.close()
        print len(data)
        new_parameters=(parameters1[0],parameters1[1],parameters1[2],nframes,parameters1[4],parameters1[5])
        print new_parameters
        
        new_file.setparams(new_parameters)
        to_write=struct.pack(encode,*data)
        
        new_file.writeframes(to_write)
        new_file.close()
    else:
        return 'NONE'
    return myself



#Amplitude_Scaling('ckh.wav',3)
#Time_reversal('Battle.wav')
#Time_Scaling('ckh.wav',2)
#Time_Shifting('Battle.wav',10)
#Mixing('got.wav','bella.wav')

#Amplitude_Scaling('ckh.wav',3)
#Time_reversal('Battle.wav')
#Time_Scaling('ckh.wav',2)
#Time_Shifting('Battle.wav',10)
#Mixing('got.wav','bella.wav')
#Modulate('got.wav','bella.wav')
#Mixing('got.wav','bella.wav')
