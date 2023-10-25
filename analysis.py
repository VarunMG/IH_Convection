import numpy as np
import matplotlib.pyplot as plt


###### functions to open various files and extract data
def openFields(file_name):
    with open(file_name,'rb') as load_file:
        uFromFile = np.load(load_file)
        vFromFile = np.load(load_file)
        bFromFile = np.load(load_file)
        phiFromFile = np.load(load_file)
        dt = np.load(load_file)
    return uFromFile, vFromFile, bFromFile, phiFromFile, dt

def openFields_timemarcher(file_name):
    with open(file_name,'rb') as load_file:
        time = np.load(load_file)
        bFromFile = np.load(load_file)
        uFromFile = np.load(load_file)
        vFromFile = np.load(load_file)
    return time, uFromFile, vFromFile, bFromFile

def openNuData(file_name):
    with open(file_name,'rb') as load_file:
        tVals = np.load(load_file)
        NuVals = np.load(load_file)
    return tVals, NuVals

def openVertMeans(file_name):
    with open(file_name,'rb') as load_file:
        vertMeans = np.load(load_file)
    return vertMeans

## functions for coordinate arrays
def makeChebPoints(N):
    points = np.zeros(N)
    points[0] = 1
    points[-1] = -1
    for i in range(1,N-1):
        points[i] = np.cos(((2*i-1)/(2*(N-2)))*np.pi)
    points = np.flip(points)
    return points

def makexPoints(alpha,N):
    return np.linspace(-1*np.pi/alpha,np.pi/alpha,N,endpoint=False)

def makeCoordArrs(alpha,Nx,Nz):
    xArr = makexPoints(alpha,Nx)
    zArr = makeChebPoints(Nz)
    return xArr, zArr

##functions to calculate spectra
def takeYAverage(verticalSlice,yVals):
    N = len(verticalSlice)
    avg = (1/2)*np.trapz(verticalSlice,yVals)
    return avg

def calcMeans(array,yVals,Nx):
    result = np.zeros(Nx)
    for i in range(Nx):
        result[i] = takeYAverage(array[:,i],yVals)
    return result
    
def calcWaveNums(alpha,Nx):
    kNums = np.zeros(Nx)
    for i in range(int(Nx/2)):
        kNums[i] = i
    for i in range(int(Nx/2),Nx):
        kNums[i] = i-Nx
    kVals = alpha*kNums
    return kVals

def calcSpectra(uArr,vArr,bArr,yVals,alpha,Nx):
    uMeans = calcMeans(uArr.T,yVals,Nx)
    vMeans = calcMeans(vArr.T,yVals,Nx)
    bMeans = calcMeans(bArr.T,yVals,Nx)
    
    ufft = np.fft.fft(uMeans)/Nx
    vfft = np.fft.fft(vMeans)/Nx
    bfft = np.fft.fft(bMeans)/Nx
    
    numShells = int(Nx/2)+1
    
    e_spectra = np.zeros(numShells)
    b_spectra = np.zeros(numShells)
    e_spectra[0] = 0.5*np.abs(ufft[0])**2 + 0.5*np.abs(vfft[0])**2
    b_spectra[0] = 0.5*np.abs(bfft[0])**2
    for i in range(1,numShells):
        e_spectra[i] = np.abs(ufft[i])**2 + np.abs(vfft[i])**2
        b_spectra[i] = np.abs(bfft[i])**2
    e_spectra = (2*np.pi/alpha)*e_spectra
    b_spectra = (2*np.pi/alpha)*b_spectra
    shells = np.arange(0,numShells)
    return shells, e_spectra, b_spectra


##plotting functions
def plotFields(xArr,zArr, uArr,vArr,bArr):
    X,Z = np.meshgrid(xArr, zArr)
    
    ##just for coolness, cmap='coolwarm' also looks alright
        
    fig, axs = plt.subplots(2, 2)
    p1 = axs[0,0].pcolormesh(X.T,Z.T,bArr,cmap='seismic')
    axs[0,0].quiver(X.T,Z.T,uArr,vArr)
    fig.colorbar(p1,ax=axs[0,0])
    
    p2 = axs[0,1].pcolormesh(X.T,Z.T,bArr,cmap='seismic')
    fig.colorbar(p2,ax=axs[0,1])
    
    p3 = axs[1,0].contourf(X.T,Z.T,bArr,cmap='seismic')
    fig.colorbar(p3,ax=axs[1,0])
    
    #p4 = axs[1,1].plot(self.tVals,self.NuVals)
    #axs[1,1].set_title('Nusselt vs. Time')
    # p4 = axs[1,1].contourf(X.T,Z.T,np.linalg.norm(uArr,axis=0),cmap='BrBG')
    # fig.colorbar(p4,ax=axs[1,1])
    
    #plt.suptitle(title)

def plotNuData(tVals,NuVals):
    dNudt = np.gradient(NuVals,tVals)
    
    figs, axs = plt.subplots(2,1)
    p1 = axs[0].plot(tVals,NuVals)
    p2 = axs[1].plot(NuVals,dNudt)


def plotVertMeans(tVals, zVals, vertMeans):
    T,Z = np.meshgrid(tVals,zVals)
    plt.pcolormesh(T,Z,vertMeans.T,cmap='seismic')
    plt.colorbar()
    

time, uArr, vArr, bArr = openFields_timemarcher('fluidData0.66377.npy')
#tValsFine, NuValsFine  = openNuData('/Users/gudibanda/Desktop/Research/IH_Convection_local/Ra300000Pr7alpha3.9989Nx512Nz512_NuData.npy')
#tValsCoarse, NuValsCoarse = openNuData('/Users/gudibanda/Desktop/Research/IH_Convection_local/Ra300000Pr7alpha3.9989Nz512Nx256_T10_NuData.npy')

#tValsFine, NuValsFine = openNuData('/Users/gudibanda/Desktop/Research/IH_Convection_local/Ra700000Pr7alpha3.9989Nx512Nz256_T10_NuData.npy')

#uFromFile, vFromFile, bFromFile, phiFromFile, dt = openFields('/Users/gudibanda/Desktop/Research/IH_Convection_local/Ra38000Pr7alpha3.9989Nx512Nz256_T5.npy')

#tVals, NuVals = openNuData('/Users/gudibanda/Desktop/Research/IH_Convection_local/Ra700000Pr7alpha3.9989Nx512Nz512_T20_NuData.npy')
#uArr, vArr, bArr, phiArr, dt = openFields('Ra38000Pr7alpha3.9989Nx512Nz256_T5.npy')
vertMeans = openVertMeans('Ra10000000Pr7alpha3.9989Nx512Nz256_T10_vertMeans.npy')
tVals, NuVals = openNuData('/Users/gudibanda/Desktop/Research/IH_Convection_local/Ra10000000Pr7alpha3.9989Nx512Nz256_T10_NuData.npy')

tValsCoarse, NuValsCoarse = openNuData('Ra700000Pr7alpha3.9989Nx128Nz64_T0.5_NuData.npy')

Nx = 512
Nz = 256
alpha = 3.9989
xArr, zArr = makeCoordArrs(alpha,Nx,Nz)

plotFields(xArr,zArr,uArr.T,vArr.T,bArr.T)

#plotNuData(tValsFine,NuValsFine)
#plotNuData(tValsCoarse,NuValsCoarse)

plotNuData(tVals,NuVals)

plotVertMeans(tVals, zArr, vertMeans)

# X,Z = np.meshgrid(xArr,zArr)
# plt.figure()
# plt.pcolormesh(X,Z,vArr.T,cmap='seismic')
# plt.colorbar()

shells, e_spectra, b_spectra = calcSpectra(uArr,vArr,bArr, zArr,alpha,Nx)

plt.figure()
plt.plot(shells,e_spectra,label='velocity spectra')
plt.plot(shells,b_spectra,label='thermal spectra')
plt.legend()