"""
Data recorder with variable output length.
"""
 
if array_length!=None and x!=None:
    recL.append(x)
else:
    recL = []

recorded_result = recL[len(recL)-array_length:]
