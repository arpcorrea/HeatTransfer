from consolidate import *

cwd = os.getcwd()
# All the data from deck.yaml is now in the following deck variable

deck = Deck( cwd + "/twoplates.yaml" )

problem = TwoPlates(deck)

local_mesh = LocalMesher(problem)

global_mesh = Mesher(local_mesh)

model_HT = HeatTransfer(global_mesh, problem)

# model_visc =  ViscosityCalculation(problem, mesh)

plots = Plot(problem, global_mesh, deck)

solves = SolvesTwoPlates( problem, model_HT, global_mesh, plots)