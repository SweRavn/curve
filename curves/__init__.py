# -*- coding: utf-8 -*-

def rc():
    """
    Used to sett global settings for Curve
    """
    
    # This is how it is used in matplotlib:
    # rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})

CurvesSettings = {
    'closed': True, # Controls if Curves default to closed or not.
    'verbosity': 0, # 0 - 2 on how verbose Curves should be.
    }

class CurvesException(Exception):
    pass
