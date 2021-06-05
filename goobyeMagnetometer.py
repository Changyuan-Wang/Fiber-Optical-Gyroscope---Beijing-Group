import u3
import time
import numpy as np
import matplotlib.pyplot as plt
import pickle
from os.path import isfile
import tkinter as tk
from tkinter import filedialog
import sys
import more_itertools as mit
from scipy import interpolate
from skimage.measure import block_reduce


class robot:
    def __init__(self):
        self.labjack = u3.U3()
        
        self.bxycal = 1. /230 #these are used to convert 
        self.bzcal = 1./ 205  #for some reason LSM303 has different gain in z
        
    def close(self):
        self.labjack.close()

    def readAIN_old(self,i):
        ainValue0 = self.labjack.getAIN(0)
        ainValue1 = self.labjack.getAIN(1)
        ainValue2 = self.labjack.getAIN(2)
        ainValue3 = self.labjack.getAIN(3)
        return [ainValue0, ainValue1, ainValue2, ainValue3]
    def readAIN(self,i):
        if i==0 or i==2 or i==3 or i==4:
            return self.labjack.getAIN(i)
    def takeIntensityPoint(self):
        mylj=self.labjack
        mylj.debug=False
        return (time.time(),self.readAIN(0))
    def setDAC0(self,voltage = 0):
        if voltage < 0 or voltage > 5:
            print('output voltage must in range from 0')
     
        DAC0_VALUE = self.labjack.voltageToDACBits(voltage, dacNumber = 0, is16Bits = False)
        self.labjack.getFeedback(u3.DAC0_8(DAC0_VALUE))
    def setDAC1(self,voltage = 0):
        if voltage < 0 or voltage > 5:
            print('output voltage must in range from 0')
    
        DAC1_VALUE = self.labjack.voltageToDACBits(voltage, dacNumber = 1, is16Bits = False)
        self.labjack.getFeedback(u3.DAC1_8(DAC1_VALUE))
    def takeBfieldPoint(self):
        #SCL should be FI07
        #SDA should be FI06
        #pullup resistors neededded
        mylj = self.labjack
        mylj.debug = False
        mylj.configIO(FIOAnalog=0,EIOAnalog=0)
      #  mylj.setFIOState(4,0)
      #  t = mylj.configIO(EnableCounter0 = True,TimerCounterPinOffset = 4)

        LSM303_ADDRESS_MAG   = (0x3C >> 1)  # 0011110x
        LSM303_REGISTER_CRB_REG_M         = 0x01   #to set gain. should be set to 11100000 = 0xE0
        LSM303_REGISTER_MAG_MR_REG_M      = 0x02
        LSM303_REGISTER_MAG_OUT_X_H_M     = 0x03
        response = mylj.i2c(LSM303_ADDRESS_MAG,[LSM303_REGISTER_MAG_MR_REG_M,0x00])
        response = mylj.i2c(LSM303_ADDRESS_MAG,[LSM303_REGISTER_CRB_REG_M,0xE0])
        
        
        response = mylj.i2c(LSM303_ADDRESS_MAG,[LSM303_REGISTER_MAG_OUT_X_H_M], NumI2CBytesToReceive = 6)
        # print(response['I2CBytes'])
        reply = response['I2CBytes'];
        
        t=time.time()
        Bx = mag16(reply[0],reply[1])*self.bxycal
        By = mag16(reply[2],reply[3])*self.bxycal
        Bz = mag16(reply[4],reply[5])*self.bzcal
        
        
        # print(reply)         
        # print(Bx)
        return(t,Bx,By,Bz)
    
def mag16(hibyte,lobyte):
    #a utility to convert LM303 bytes into usable numbers
    
    n = (hibyte << 8) | lobyte
    if n > 32767: 
        n -= 65536
    return n    

def pkSave(variable,filename):
    with open(filename, 'wb') as f:
        pickle.dump(variable, f)
        
def pkSaveNotId(variable,filename):
    if not isfile(filename):
        with open(filename, 'wb') as f:
            pickle.dump(variable, f)
    elif not isfile(filename+'(1)'):
        with open(filename+'(1)', 'wb') as f:
            pickle.dump(variable, f)
    elif not isfile(filename+'(2)'):
        with open(filename+'(2)', 'wb') as f:
            pickle.dump(variable, f)
    elif not isfile(filename+'(3)'):
        with open(filename+'(3)', 'wb') as f:
            pickle.dump(filename, f)     
    elif not isfile(filename+'(4)'):
        with open(filename+'(4)', 'wb') as f:
            pickle.dump(variable, f) 
  
def loadRecord():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    file_path = file_path[:-2]
    with open(file_path+'t', 'rb') as f:
        t=pickle.load(f)
    with open(file_path+'Bx', 'rb') as f:
        Bx=pickle.load(f)
    with open(file_path+'By', 'rb') as f:
        By=pickle.load(f)
    with open(file_path+'Bz', 'rb') as f:
        Bz=pickle.load(f)
    with open(file_path+'I', 'rb') as f:
        I=pickle.load(f)
    return (t,Bx,By,Bz,I)

def RunNPlot(N=100,sleep=0.1):
    Robot=robot()
    Robot.setDAC0(1.2)
    t,Bx,By,Bz,t,I=np.zeros((N,)),np.zeros((N,)),np.zeros((N,)),np.zeros((N,)),np.zeros((N,)),np.zeros((N,))
    
    # to avoid 冷启动
    print("wait 0.5 second")
    Robot.takeBfieldPoint()
    time.sleep(0.5)
    
    startTime=time.time()
    for i in range(N):
        t[i],Bx[i],By[i],Bz[i]=Robot.takeBfieldPoint()
        I[i]=Robot.takeIntensityPoint()[1]
        print('t=%.3f,Bx=%.3f,By=%.3f,Bz=%.3f'%(t[i],Bx[i],By[i],Bz[i]))
        print('t=%.3f,I=%.3f\n'%(t[i],I[i]))
        time.sleep(sleep)
    t=t-startTime

    Robot.close()
    
    fmtTime=(time.strftime("%Y%m%d_%H%M%S",time.localtime()))
    pkSaveNotId(t, './/history//%s_t'%fmtTime)
    pkSaveNotId(Bx, './/history//%s_Bx'%fmtTime)
    pkSaveNotId(By, './/history//%s_By'%fmtTime)
    pkSaveNotId(Bz, './/history//%s_Bz'%fmtTime)
    pkSaveNotId(t, './/history//%s_t_I'%fmtTime)
    pkSaveNotId(I, './/history//%s_I'%fmtTime)
    
    return (t,Bx,By,Bz,I)

def ChooseOneMethod(new_trail=True,load=False,counts=200,sleep=0.1):
    if new_trail+load==1:
        if new_trail==True:
            global Robot
            Robot=robot()
            t,Bx,By,Bz,I=RunNPlot(counts,sleep)
        if load==True:
            t,Bx,By,Bz,I=loadRecord()
    return t,Bx,By,Bz,I
        



t,Bx,By,Bz,I=ChooseOneMethod(new_trail=False,load=True,counts=350,sleep=0.1)

cont_t=np.linspace(0,t.max(),5000)
By2, Bz2 = By-By.mean(), Bz-Bz.mean()
B=np.sqrt(Bx**2+By**2+Bz**2)
D=np.arctan(By2/Bz2)*180/np.pi
D=np.arctan(By2/Bz2)*180/np.pi
difference=0
condition_minus=(np.diff(D)>50)
condition_plus=(np.diff(D)<-50)
for i in range(len(D)-1):
    if condition_minus[i]==True:
        difference-=180
    if condition_plus[i]==True:
        difference+=180
    D[i+1]=D[i+1]+difference

# a=block_reduce(np.squeeze(np.dstack((t,D))),(30,1),func=np.mean)[:-1,:]
# linear=interpolate.interp1d(a[:,0],a[:,1],kind='linear',fill_value='extrapolate')
# quad=interpolate.interp1d(a[:,0],a[:,1],kind='quadratic',fill_value='extrapolate')

omega=np.diff(D)/np.diff(t)
tavg=t[:-1]+1/2*np.diff(t)
cont_tavg=np.linspace(0,tavg.max(),5000)


a=block_reduce(np.squeeze(np.dstack((tavg,omega))),(30,1),func=np.mean)[:-1,:]
linear_omega=interpolate.interp1d(a[:,0],a[:,1],kind='linear',fill_value='extrapolate')
quad_omega=interpolate.interp1d(a[:,0],a[:,1],kind='quadratic',fill_value='extrapolate')

b=block_reduce(np.squeeze(np.dstack((t,I))),(30,1),func=np.mean)[:-1,:]
linear_I=interpolate.interp1d(b[:,0],b[:,1],kind='linear',fill_value='extrapolate')
quad_I=interpolate.interp1d(b[:,0],b[:,1],kind='quadratic',fill_value='extrapolate')

c=block_reduce((np.squeeze(np.dstack((
    linear_I(cont_t),linear_omega(cont_t))))),(30,1),func=np.mean)[:-1,:]
linear_omega_I=interpolate.interp1d(c[:,0],c[:,1],kind='linear',
                                    bounds_error=False,fill_value=np.NaN)
quad_omega_I=interpolate.interp1d(b[:,0],b[:,1],kind='quadratic',
                                  bounds_error=False,fill_value=np.NaN)

# sys.exit()
# DofT=(np.squeeze(np.dstack((t,D)))[:-1,:])[np.diff(D)<50,:]

# dD = np.diff(D)
# dt=np.diff(t)
# tAvg=t[:-1]+0.5*dt
# convinient_t_avg=t[:-1]
# omegaOfT=np.squeeze(np.dstack((convinient_t_avg,dD/dt)))
# mask=(omegaOfT[:,1]>360)^(omegaOfT[:,1]<-360) # the part you don't want
# omegaOfT=omegaOfT[~mask,:]
# omegaOfT_reduced=block_reduce(omegaOfT, (7,1),np.mean,
#                               cval=np.mean(omegaOfT))[:-1,:]

    
# derivativeD[(derivativeD>360)^(derivativeD<-360)]=np.NaN
# derivativeD=derivativeD[(derivativeD<360)&(derivativeD>-360)]
# AvgDerivativeD=np.array([sum(x)/len(x) for x in mit.chunked(derivativeD,3)])
# AvgTime=np.array([sum(x)/len(x) for x in mit.chunked(derivativeD,3)])

# near=interpolate.interp1d(omegaOfT[:,0],omegaOfT[:,1],
#                        kind='nearest',fill_value='extrapolate')
# quad=interpolate.interp1d(omegaOfT[:,0],omegaOfT[:,1],
#                        kind='quadratic',fill_value='extrapolate')
# cubic=interpolate.interp1d(omegaOfT[:,0],omegaOfT[:,1],
#                        kind='cubic',fill_value='extrapolate')
# slin=interpolate.interp1d(omegaOfT[:,0],omegaOfT[:,1],
#                        kind='slinear',fill_value='extrapolate')




# 1. (Bx,By,Bz)-t
plt.figure()
plt.title('Magnetic Field')
plt.plot(t,Bx,'.',label = 'Bx')
plt.plot(t,By,'.',label = 'By')
plt.plot(t,Bz,'.',label = 'Bz')
plt.ylim(-1.5,1.5)
plt.xlabel('time, seconds')
plt.ylabel('field, Gauss')
plt.draw()
plt.legend()

# 2. D-t
plt.figure()
plt.title('Heading')
plt.plot(t,D,'.',label='heading')
plt.xlabel('time, seconds')
plt.ylabel('heading, degree')
plt.draw()
plt.legend()

# 3. omega-t
plt.figure()
plt.title('Angular Velocity')
plt.plot(tavg,omega,'.',label='angular velocity')
plt.plot(cont_tavg,linear_omega(cont_tavg),label='linear interpolation of binned data')
plt.xlabel('time, seconds')
plt.ylabel(r'$\omega$, $deg \cdot s^{-1}$')
plt.draw()
plt.legend()

# 4. I-t
plt.figure()
plt.title('Voltage of Photodiode')
plt.plot(t,I,'.',label = 'Voltage')
plt.plot(cont_t,linear_I(cont_t),label='linear interpolation of binned data')
plt.xlabel('Time, seconds')
plt.ylabel(r'Voltage, V')
plt.draw()
plt.legend()

# 5. omega-I
plt.figure()
plt.title('Calibration Function')
cont_I=np.linspace(1.1,1.3,5000)
plt.xlim(1.1,1.3)
plt.ylim(-260,260)
plt.plot(cont_I,linear_omega_I(cont_I),label='calibration function')
plt.xlabel(r'Voltage, V')
plt.ylabel(r'$\omega$, $deg \cdot s^{-1}$')
plt.draw()
plt.legend()


sys.exit()

# vector B (normalized)
plt.figure()
plt.plot(t,By2,'.',label = 'By2')
plt.plot(t,Bz2,'.',label = 'Bz2')
plt.ylim(-1.5,1.5)
plt.xlabel('time, seconds')
plt.ylabel('field, Gauss')
plt.draw()
plt.legend()

# # heading old (normalized)
# plt.figure()
# plt.plot(t,D,'.',label = 'Heading(from normalized B data)')
# plt.xlabel('time, seconds')
# plt.ylabel('heading, degree')
# plt.draw()
# plt.legend()

# # derivative of heading old (normalized)
# plt.figure()
# plt.plot(omegaOfT[:,0],omegaOfT[:,1],
#          '.',label = r'$\omega(t)$')
# # plt.ylim(np.percentile(omegaOfT[:,1],0),np.percentile(omegaOfT[:,1],92))
# # dense_t=np.linspace(0, omegaOfT[:,0].max(),5000)
# # plt.plot(dense_t,slin(dense_t),label='slinear')
# plt.xlabel('time, seconds')
# plt.ylabel(r'angular velocity, $deg \cdot s^{-1}$')
# plt.draw()
# plt.legend()

# # derivative of heading old (normalized,reduced)
# plt.figure()
# plt.plot(omegaOfT_reduced[:,0],omegaOfT_reduced[:,1],
#          '.',label = r'$\omega(t)$_reduced')
# plt.xlabel('time, seconds')
# plt.ylabel(r'angular velocity, $deg \cdot s^{-1}$')
# plt.draw()
# plt.legend()

# module B
plt.figure()

plt.ylim(0,1.5)
plt.plot(t,B,label='B')
plt.xlabel('time, seconds')
plt.ylabel('field, Gauss')
plt.legend()

# Voltage
fig=plt.figure()
ax = fig.add_subplot()
line1,=ax.plot(t,I,'.',label = 'Intensity')
ax.set_xlabel('Time, seconds')
ax.set_ylabel(r'Intensity, $J \cdot s^{-1} \cdot m^{-2}$')
# plt.ylim(0.2,0.7)
plt.draw()
ax.legend()


D=block_reduce(D, (2,),np.mean,cval=np.mean(D))

plt.figure()
plt.plot(-np.diff(D),'-x')