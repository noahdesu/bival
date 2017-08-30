
#############
#  IMPORTS  #
#############
import os

# build PyC4
os.system( "git submodule init" )
os.system( "git submodule update" )
os.system( "rm -rf ./lib/PyC4/*" )
os.system( "cd ./lib/PyC4/ ; git reset --hard ; git pull origin master ; python setup.py ;" )


#########
#  EOF  #
#########
