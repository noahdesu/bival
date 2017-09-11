#!/usr/bin/env python

'''
biv.py
'''

# **************************************** #


#############
#  IMPORTS  #
#############
# standard python packages
import inspect, os, sqlite3, sys, time

# ------------------------------------------------------ #
# import python lib packages HERE!!!

# import sibling packages HERE!!!
if not os.path.abspath( __file__ + "/../.." ) in sys.path :
  sys.path.append( os.path.abspath( __file__ + "/../.." ) )

#

# **************************************** #


#########
#  BIV  #
#########
def biv() :

  flag = False
  for arg in sys.argv :

    # CASE : overlog detected
    if ".olg" in arg :
      print "Overlog input file dedected at '" + sys.argv[1] + "'"
      print "  => running PyC4 evaluator..."

      if not os.path.abspath( __file__ + "/../../../lib/PyC4/src/drivers/" ) in sys.path :
        sys.path.append( os.path.abspath( __file__ + "/../../../lib/PyC4/src/drivers/" ) )
      import pyc4

      pyc4.pyc4( sys.argv )
      flag = True
      break

    # CASE : dedalus detected
    elif ".ded" in arg :
      print "Dedalus input file dedected at '" + sys.argv[1] + "'"
      print "  => running orik..."
      
      if not os.path.abspath( __file__ + "/../../../lib/orik/src/drivers/" ) in sys.path :
        sys.path.append( os.path.abspath( __file__ + "/../../../lib/orik/src/drivers/" ) )
      import orik

      orik.orik( )
      flag = True
      break

  # OTHERWISE : no valid input file detected
  if not flag :
    sys.exit( ">> FATAL ERROR : unrecognized input file extension in inputs : " + str( sys.argv ) )


##############################
#  MAIN THREAD OF EXECUTION  #
##############################
print "shit"
biv()

#########
#  EOF  #
#########
