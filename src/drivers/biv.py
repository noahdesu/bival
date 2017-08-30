#!/usr/bin/env python

'''
driver.py
'''

# **************************************** #


#############
#  IMPORTS  #
#############
# standard python packages
import inspect, os, sqlite3, sys, time

# ------------------------------------------------------ #
# import python lib packages HERE!!!
if not os.path.abspath( __file__ + "/../../../lib/PyC4/src/drivers/" ) in sys.path :
  sys.path.append( os.path.abspath( __file__ + "/../../../lib/PyC4/src/drivers/" ) )

import pyc4

# import sibling packages HERE!!!
if not os.path.abspath( __file__ + "/../.." ) in sys.path :
  sys.path.append( os.path.abspath( __file__ + "/../.." ) )

#

# **************************************** #


############
#  DRIVER  #
############
def biv() :

  pyc4.pyc4( sys.argv )



#########
#  EOF  #
#########
