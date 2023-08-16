import ctrust

# Simulation Parameters
population = 400
mean_trustees = 2.5
sdev_trustees = 1
recursion_depth = 3
voters = []
# Edge data for network visualisation
edge_data = []

if __name__ == '__main__':

    voters = ctrust.InstantiatePopuplation(population, True)

    ctrust.PerformNominations(voters, mean_trustees, sdev_trustees, True)

    ctrust.PerformTD(voters, recursion_depth, True)

    ctrust.VisualiseData(voters, True)

    ctrust.AnalyseData(voters, True)