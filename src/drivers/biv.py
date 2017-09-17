#!/usr/bin/env python

'''
biv.py
'''

# **************************************** #


#############
#  IMPORTS  #
#############
# standard python packages
import inspect, os, string, sqlite3, sys, time

# ------------------------------------------------------ #

import utils_biv

# import sibling packages HERE!!!
if not os.path.abspath( __file__ + "/../.." ) in sys.path :
  sys.path.append( os.path.abspath( __file__ + "/../.." ) )

#

# **************************************** #


#########
#  BIV  #
#########
def biv( ) :

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

    # CASE : ini file deteced. Then run entire src model.
    elif ".ini" in arg :
      print "Configure file dedected at '" + sys.argv[1] + "'"
      settings_path = os.path.abspath( sys.argv[1] )
      print "using full path : " + settings_path

      # collapse all source model files into a single program.
      # relation names made unique per source file.
      finalDedPath = collapseSrc( settings_path )

      # pass to orik
      clock_contents_list = utils_biv.getConfig( settings_path, "CLOCK_CONTENTS_LIST", str )
      ORIK_PATH = os.path.abspath( __file__ + "/../../../lib/orik/src/drivers/orik.py" )
      os.system( "rm ./IR.db" )
      os.system( "rm ./tmp.txt" )
      os.system( "python " + ORIK_PATH + " -c 0 -n " + clock_contents_list + " --EOT 2 -f " + finalDedPath + " --evaluator c4" )
      os.system( "rm ./IR.db" )

      flag = True
      break

  # OTHERWISE : no valid input file detected
  if not flag :
    sys.exit( ">> FATAL ERROR : unrecognized input file extension in inputs : " + str( sys.argv ) )


##################
#  COLLAPSE SRC  #
##################
# collapse all bival src files into a single program.
# make relation names unique across ded files.
# ignore files ending with string "_ignore"
def collapseSrc( settings_path ) :

  pathList = getAllPaths()

  allDedLines = []

  # ------------------------------------------- #
  # grab dedalus lines from all valid files.
  #  * parseFile extracts all program lines from
  #    the current file.
  #  * makeUnique ensures all relation names are
  #    unique per dedalus input file.
  for path in pathList :
    lines = parseDedFile( path )
    lines = makeUnique( lines )
    allDedLines.extend( lines )

  # ------------------------------------------- #
  # order define statements first.
  #allDedLines = orderLines( allDedLines )

  # ------------------------------------------- #
  # write the final program to a file.
  finalDedPath = dumpToFile( allDedLines )

  return finalDedPath


##################
#  DUMP TO FILE  #
##################
# save final program to a single file.
def dumpToFile( allDedLines ) :

  print "-----------------------------"
  print "FINAL PROGRAM :"
  print
  for line in allDedLines :
    print line
  print

  final_dump_path = os.path.abspath( os.getcwd() ) + "/final_prog.ded"
  print "DUMPING FINAL PROGRAM TO FILE AT : " + final_dump_path

  fo = open( final_dump_path, "w" )
  for line in allDedLines :
    fo.write( line + "\n" )
  fo.close()

  return final_dump_path


#################
#  MAKE UNIQUE  #
#################
# ensure all relation names are unique for this file, except pre and post.
def makeUnique( lines ) :

  # list of relation names in this program
  # previously assigned unique identifiers.
  previouslyProcessed = []

  # map old relation names to new relation names.
  idMap = {}

  for line in lines :
    line = line.split( "(" )
    relName = line[0]

    if not relName in previouslyProcessed and not relName == "define" and not relName == "pre" and not relName == "post" :
      # append an eight-character id to each relation name.
      newRelName= relName + "_uid" + utils_biv.getID( 8 )
      idMap[ relName ] = newRelName

  # replace subgoal relation names appropriately
  finalLines = []
  for line in lines :
    for relName in idMap :
      line = line.replace( relName, idMap[ relName ] )
    finalLines.append( line )

  return finalLines


####################
#  PARSE DED FILE  #
####################
# extract all dedalus lines from input file.
# return list of all non-comment lines in the file.
def parseDedFile( path ) :

  try :
    program = []

    print
    print "=========================================="
    print " Extracting Dedalus from..." + path

    fo = open( path, "r" )
    for line in fo :
      line = line.rstrip() # need to preserve spaces after "notin" ops.
      line = line.lstrip() # need to preserve spaces after "notin" ops.
      tmp = line.translate( None, string.whitespace )
      if not tmp.startswith( "//" ) and not tmp == "" :
        program.append( line ) # only take non-empty, non-commented lines.
    fo.close()

    # concatenate program into one line
    program = "".join( program )

    # extract complete lines by partitioning the program string
    # over semicolons
    program = program.split( ";" )

    # ignore the last semicolon
    if program[-1] == "" :
      program = program[:-1]

    tmp = []
    for line in program :
      line = line.rstrip()
      line = line + ";"
      tmp.append( line )
    program = tmp

    print " SUCCESSFULLY INPUT PROGRAM :"
    for line in program :
      print "  " + line
    return program

  except IOError :
    utils_biv.bp( __name__, inspect.stack()[0][3], "FATAL ERROR : Could not open file " + filename )
    return None


###################
#  GET ALL PATHS  #
###################
# walking dirs soln from :
# https://stackoverflow.com/questions/1124810/how-can-i-find-path-to-given-file
def getAllPaths() :

  allValidPaths = []

  for root, dirs, files in os.walk( os.path.abspath( __file__ + "/../.." ) ) :
    for name in files :
      if name.endswith( ".ded" ) :
        allValidPaths.append( os.path.abspath(os.path.join(root, name)) )

  if not allValidPaths :
    sys.exit( ">>> FATAL ERROR : no valid paths to bival src files. aborting..." )

  return allValidPaths


##############################
#  MAIN THREAD OF EXECUTION  #
##############################
biv()

#########
#  EOF  #
#########
