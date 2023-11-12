from IH_helper import *
from steady_state_helper import *

def longRun(Ra,Pr,alpha,Nx,Nz,T,fileName=None):
    testProb = IH_Problem(Ra,Pr,alpha,Nx,Nz)
    testProb.initialize()
    testProb.solve_system(T,True,False,True)
    if fileName is None:
        fileName = 'Ra' + str(Ra) + 'Pr' + str(Pr) + 'alpha' + str(alpha) + 'Nx' + str(Nx) + 'Nz' + str(Nz) + '_T'+str(T)+'.npy'
    testProb.saveToFile(fileName)

def getSteady(Ra,Pr,alpha,Nx,Nz,T,tol,guessFile,steadyStateFile):
    uArr, vArr, bArr, phiArr, dt = open_fields(guessFile)
    starting_SS_state = arrsToStateVec(phiArr, bArr)
    startingGuess = starting_SS_state
    starting_dt = dt
    startingProblem = IH_Problem(Ra,Pr,alpha,Nx,Nz)
    startingProblem.initialize()
    findSteadyState(startingProblem,startingGuess,T,tol,50,True)
    startingProblem.saveToFile(steadyStateFile)


def branchFollow(Pr,alpha,Ra_start,num_steps,Ra_step, Nx, Nz,startFile, T,tol):
    uArr, vArr, bArr, phiArr, dt = open_fields(startFile)
    starting_SS_state = arrsToStateVec(phiArr, bArr)
    startingGuess = starting_SS_state
    starting_dt = dt
    RaVals, NuVals = follow_branch(Pr,alpha,Ra_start,num_steps,Ra_step, Nx, Nz, startingGuess, starting_dt, T,tol)
    return RaVals, NuVals


####################
### for long run ###
####################

#Ra = 38000
#Pr = 7
#alpha = 3.9989
#Nx = 128
#Nz = 100
#T = 50

#longRun(Ra,Pr,alpha,Nx,Nz,T)

#########################################
### For finding a single steady state ###
#########################################

#Ra = 38100
#Pr = 7
#alpha=3.9989
#Nx=128
#Nz=100
#T=0.1
#guessFile = 'Ra38000Pr7alpha3.9989Nx128Nz100_T50.npy'
#steadyFile = 'Ra38100Pr7alpha3.9989Nx60Nz100_SS.npy'

#getSteady(Ra,Pr,alpha,Nx,Nz,T,1e-6,guessFile, steadyFile)

##############################
### For following a branch ###
##############################

Pr = 7
alpha = 3.9989
Ra_start = 183368
num_steps = 20
Ra_step = 1.001
Nx = 128
Nz = 100
startFile = 'Ra183368.0Pr7alpha3.9989Nx128Nz100_SS.npy'
T = 0.1
tol = 1e-6

RaVals, NuVals = branchFollow(Pr, alpha, Ra_start, num_steps, Ra_step, Nx,Nz,startFile,T,tol)

