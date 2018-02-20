# This doesn't make sense yet 
#The units for rate should be 
# occupancy = rate * number of occupants * area
occupancy = list(map(lambda x:area*number_of_occupants*x, occupancy_per_m2))
