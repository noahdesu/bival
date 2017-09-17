#!/usr/bin/env python

'''
tools.py
   A storage location for generally applicable methods.
'''

import ConfigParser, StringIO, inspect, os, random, re, string, sys, numbers


#####################
#  BREAKPOINT (bp)  #
#####################
def bp( filename, funcname, msg ) :
  os.system( "rm IR.db" )
  sys.exit( "BREAKPOINT in file " + filename + " at function " + funcname + " :\n>>> " + msg )


############
#  GET ID  #
############
# input nothing
# output random char upper case alphanumeric id of length numChars
def getID( numChars ) :
  return "".join( random.choice('abcdefghijklmnopqrstuvwxyz') for i in range(numChars) )


################
#  GET CONFIG  #
################
def getConfig( settings_path, option, dataType ) :

  print settings_path
  print option
  print dataType

  # ---------------------------------------------- #
  # create config parser instance
  configs = ConfigParser.ConfigParser( )
  section = "DEFAULT"

  # ---------------------------------------------- #
  # read defaults first
  defaults_path    = os.path.abspath( __file__ + "/.." ) + "/defaults.ini" # assume stored in src/
  defaults_ini_str = '[DEFAULT]\n' + open( defaults_path, 'r').read()
  defaults_ini_fp  = StringIO.StringIO( defaults_ini_str )
  configs.readfp( defaults_ini_fp )

  # ---------------------------------------------- #
  # read user-specified settings, if applicable
  if os.path.isfile( settings_path ) : # check if file exists first.
    settings_ini_str = '[DEFAULT]\n' + open( settings_path, 'r').read()
    settings_ini_fp  = StringIO.StringIO( settings_ini_str )
    configs.readfp( settings_ini_fp )

  # ---------------------------------------------- #
  # handle boolean configure types
  if dataType == bool :
    if configs.get( section, option ) == "True"  :
      return True
    else :
      return False

  # ---------------------------------------------- #
  # handle list configure types
  elif dataType == list :

    list_str   = configs.get( section, option )
    list_str   = list_str.translate( None, string.whitespace )  # remove extra spaces and newlines
    list_str   = list_str[1:]                                   # remove leading open bracket
    list_str   = list_str[:-1]                                  # remove trailing close bracket
    list_array = list_str.split( "','" )                        # convert string to array
    clean_array = []
    for x in list_array :
      x = x.replace( "'", "" )                                  # remove straggling apostrophes
      clean_array.append( x )

    return clean_array

  # ---------------------------------------------- #
  # handle int configure types

  elif dataType == int :
    return int( configs.get( section, option ) )

  # ---------------------------------------------- #
  # otherwise treat as a string
  else :
    return configs.get( section, option )


#########
#  EOF  #
#########
