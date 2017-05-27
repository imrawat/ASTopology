# To handle combination producing code(itertools.product(*paths)) from taking too long
MAXIMUM_POSSIBLE_COMBINATIONS_DIRECTED = 1000000

# The maximum number of st-cuts that will be checked 
# any number more than this will force the single node st-cut to be used
# Single node st-cut is preferably the one that is towards the sink/destination.
MAXIMUM_ALLOWED_ST_CUTS_COMBINATIONS_DIRECTED = 1000
