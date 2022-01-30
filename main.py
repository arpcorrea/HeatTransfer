from consolidate import *

cwd = os.getcwd()
# All the data from deck.yaml is now in the following deck variable

deck = Deck( cwd + "/OnePlate.yaml" )

problem = Problem(deck)

mesh = Mesher(problem)

model_HT = HeatTransfer(mesh, problem)

# # model_visc =  ViscosityCalculation(problem, mesh)

plots = Plot(problem, mesh, deck)

solves = SolvesTwoPlates( problem,model_HT,mesh, plots)