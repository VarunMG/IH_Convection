from IH_helper import *

#testProb = IH_Problem(38000,7,3.9989,128,64)
#testProb.initialize()
#testProb.solve_system(30,True,False,True)
#testProb.saveToFile('Ra38000Pr7alpha3.9989Nx64Nz64_T5.npy')


uArr, vArr, bArr, phiArr, dt = open_fields('Ra38001Pr7alpha3.9989Nx128Nz64_SS.npy')
starting_SS_state = arrsToStateVec(phiArr, bArr)
startingGuess = starting_SS_state
starting_dt = dt
#startingProblem = IH_Problem(38002,7,3.9989,128,64)
#startingProblem.initialize()
#findSteadyState(startingProblem,startingGuess,0.5,1e-2,50,True)
#startingProblem.saveToFile('Ra38002Pr7alpha3.9989Nx128Nz64_SS.npy')

RaVals, NuVals, steady_states = follow_branch(7,3.9989,38003,38100, 1, 128, 64, startingGuess, starting_dt, 1e-2)
print(RaVals, NuVals)
