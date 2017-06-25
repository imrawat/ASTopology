# To handle combination producing code(itertools.product(*paths)) from taking too long
MAXIMUM_POSSIBLE_COMBINATIONS_DIRECTED = 1000000

# The maximum number of st-cuts that will be checked 
# any number more than this will force the single node st-cut to be used
# Single node st-cut is preferably the one that is towards the sink/destination.
MAXIMUM_ALLOWED_ST_CUTS_COMBINATIONS_DIRECTED = 1000

# python find_cut_directed.py -c IL -m 1 -s N -H 2
'''
Node characteristic that can be used in heuristic weight
'''
CUSTOMER_DEGREE = 'customer_degree'
PROVIDER_DEGREE = 'provider_degree'
PEER_DEGREE = 'peer_degree'
CUSTOMER_CONE_SIZE = 'customer_cone_size'
ALPHA_CENTRALITY = 'alpha_centrality'
BETWEENNESS_CENTRALITY = 'betweenness_centrality'
KATZ_CENTRALITY = 'katz_centrality'
UNITY = 'unity'

PATH_FREQUENCY = 'path_frequency'
CAPACITY = 'capacity'
HEURISTIC_WEIGHT = 'heuristic_weight'



'''
Various heuristic of node characteristic combinations that can be applied
'''
class HEURISTIC:
	CUSTOMER_DEGREE = 1
	PROVIDER_DEGREE = 2
	PEER_DEGREE = 3
	CUSTOMER_CONE_SIZE = 4
	KATZ_CENTRALITY = 5
	BETWEENNESS_CENTRALITY = 6
	PATH_FREQUENCY = 7
	UNITY = 8





