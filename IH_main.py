from IH_helper import *

#testProb = IH_Problem(38000,7,3.9989,512,256)
#testProb.initialize()
#testProb.solve_system(10,True,False,True)
#testProb.saveToFile('Ra38000Pr7alpha3.9989Nx512Nz256_T5.npy')


uArr, vArr, bArr, phiArr, dt = open_fields('Ra38000Pr7alpha3.9989Nx512Nz256_T5.npy')
starting_SS_state = arrsToStateVec(phiArr, bArr)
startingGuess = starting_SS_state
starting_dt = dt
startingProblem = IH_Problem(38000,7,3.9989,512,256)
startingProblem.initialize()
findSteadyState(startingProblem,startingGuess,1.0,1e-2,50,True)
startingProblem.saveToFile('Ra38000Pr7alpha3.9989Nx512Nz256_SS.npy')

#RaVals, NuVals, steady_states = follow_branch(7,3.9989,40500,41500, 500, 512, 256, startingGuess, starting_dt, 1e-2)
