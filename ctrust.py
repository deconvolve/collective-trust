import random, statistics, names, time
from pyvis.network import Network
# from multiprocessing import Pool
# import matplotlib.pyplot as plt

# Note N is actually N_bar and M is used to represent the function 2^M

class Voter:
    intrinsic_vote = 1
    def __init__(self, id):
        self.trustee_edges = {}
        self.trustor_edges = {}
        self.id = id
        # self.name = names.get_full_name() # Adds 7s computation time with population = 4000
    def nominate(self, trustees, N):
        for trustee in trustees:
            assert trustee != self, "A voter has nominated themselves"
            e = Edge(self, trustee, 0.5/N)
            trustee.trustor_edges[self.id] = e
            self.trustee_edges[trustee.id] = e
    def transitive_distribution(self, recursion_depth, distribution=-1):
        recursion_depth -= 1
        if recursion_depth < 1: # Limit recursion depth
            return
        if distribution == -1: # Root node
            distribution = 0
            for e in self.trustor_edges.values():
                distribution += e.get_nominative()
            distribution /= (len(self.trustee_edges)*4) # distributing a quarter of the root's nominated trust vote among the 2nd-level trustees
        else: # Recursive case
            distribution /= (len(self.trustee_edges)*2) # distributing half of the previous distribution among the trustees
        for e in self.trustee_edges.values():
            e.add_distributive(distribution)
            e.other(self).transitive_distribution(recursion_depth, distribution) # Recurse
    def get_vote_data(self, edge_data):
        for e in self.trustor_edges.values():
             edge_data.append((e.trustor.id, e.trustee.id, e.get_weight()))
        return 

class Edge:
    def __init__(self, trustor, trustee, weight):
        self.trustor = trustor
        self.trustee = trustee
        self.nominative = weight
        self.distributive = 0.0
    def get_nominative(self):
        return self.nominative
    def add_distributive(self, weight):
        self.distributive += weight
    def get_weight(self):
        return self.nominative + self.distributive
    def other(self, notOther):
        if self.trustee == notOther:
            assert notOther != self.trustor, "Failed to assert: %s != %s" % (notOther, self.trustor)
            return self.trustor
        else:
            assert notOther == self.trustor
            return self.trustee

def InstantiatePopuplation(population, measure=False):
    st = time.time()
    voters = []
    for i in range(population):
        voters.append(Voter(i))
    et = time.time()
    if measure:
        t = 1000*(et-st)
        print("Instantiation time: %d ms" % t)
    return voters

def PerformNominations(voters, mean_trustees, sdev_trustees, measure=False):
    st = time.time()
    for voter in voters:
        # Pick a random number of trustees >=1
        n = -1
        while n<0.5: # This truncates the normal distribution at 1
            n = random.gauss(mean_trustees, sdev_trustees) # not thread safe
        # print(n)
        n_trustees = round(n)
        # print(n_trustees)
        # Randomly choose k voters as trustees
        trustees = random.choices(voters, k=n_trustees)
        while voter in trustees: # Make sure the voter doesn't nominate themselves
            trustees = random.choices(voters, k=n_trustees)
        voter.nominate(trustees, n_trustees)
    et = time.time()
    if measure:
        t = 1000*(et-st)
        print("Nomination time: %d ms" % t)
    return

def PerformTD(voters, recursion_depth=2, measure=False):
    # Perform transitive distribution
    st = time.time()
    # with Pool() as pool:
    for voter in voters:
        voter.transitive_distribution(recursion_depth)
        # pool.close()
    et = time.time()
    if measure:
        t = 1000*(et-st)
        print("Transitive distribution time: %d ms" % t)
    return

def AnalyseData(voters, measure=False):
    # Data analysis
    st = time.time()
    gross_weights = []
    nominated_trusts = []
    transitive_trusts = []
    for voter in voters:
        gross_weights.append(voter.vote_weight())
        nominated_trusts.append(voter.nominated_trust)
        transitive_trusts.append(voter.transitive_trust)
    mean_nominated_trust = statistics.mean(nominated_trusts)
    sdev_nominated_trust = statistics.stdev(nominated_trusts)
    median_nominated_trust = statistics.median(nominated_trusts)
    mean_transitive_trust = statistics.mean(transitive_trusts)
    sdev_transitive_trust = statistics.stdev(transitive_trusts)
    median_transitive_trust = statistics.median(transitive_trusts)
    mean_gross_weight = statistics.mean(gross_weights)
    sdev_gross_weight = statistics.stdev(gross_weights)
    median_gross_weight = statistics.median(gross_weights)
    # print("Nominated trusts:")
    # print(nominated_trusts)
    # print("Transitive trusts:")
    # print(transitive_trusts)
    # print("Gross weights:")
    # print(gross_weights)
    # print("Mean nominated trust: %.5f (should be 1)" % mean_nominated_trust)
    # print("Standard deviation of nominated trust: %.5f" % sdev_nominated_trust)
    # print("Median nominated trust: %.5f" % mean_nominated_trust)
    # print("Mean transitive trust: %.5f (should be 1)" % mean_transitive_trust)
    # print("Standard deviation of transitive trust: %.5f" % sdev_transitive_trust)
    # print("Median transitive trust: %.5f" % mean_transitive_trust)
    print("Mean gross weight: %.5f (should be 3)" % mean_gross_weight)
    print("Standard deviation of gross weight: %.5f" % sdev_gross_weight)
    print("Median gross weight: %.5f" % mean_gross_weight)
    winner = None
    winner_gross_weight = 0
    for voter in voters:
        gross_weight = voter.vote_weight()
        if gross_weight > winner_gross_weight:
            winner_gross_weight = gross_weight
            winner = voter
    print("The elected winner is %s, with %f votes" % (names.get_full_name(), winner_gross_weight))
    # n_bins = 50
    # fig, ax = plt.subplots()
    # ax.hist(gross_weights, bins=n_bins)
    # fig.show()
    et = time.time()
    if measure:
        t = 1000*(et-st)
        print("Data analysis time: %d ms" % t)
    return

def VisualiseData(voters, measure=False):
    st = time.time()
    network = Network(height="750px", width="100%", bgcolor="#222222", font_color="white")
    # set the physics layout of the network
    network.barnes_hut()

    edge_data = []
    for voter in voters:
        voter.get_vote_data(edge_data)

    for data in edge_data:
                network.add_node(data[0], data[0], title=data[0])
                network.add_node(data[1], data[1], title=data[1])
                network.add_edge(data[0], data[1], value=data[2])

    neighbor_map = network.get_adj_list()

    # add neighbor data to node hover data
    for node in network.nodes:
                    node["title"] += " Neighbors:<br>" + "<br>".join(str(neighbor_map[node["id"]]))
                    node["value"] = len(neighbor_map[node["id"]])

    network.show("voter_network.html")
    et = time.time()
    if measure:
        t = 1000*(et-st)
        print("Data visualisation time: %d ms" % t)
    return
