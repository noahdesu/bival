
#############
#  IMPORTS  #
#############
import os

# ====================================== #
# build submodules
os.system( "git submodule init" )
os.system( "git submodule update" )

# build PyC4
os.system( "rm -rf ./lib/PyC4/*" )
os.system( "cd ./lib/PyC4/ ; git reset --hard ; git pull origin master ; python setup.py ;" )


# build orik
os.system( "rm -rf ./lib/orik/*" )
os.system( "cd ./lib/orik/ ; git reset --hard ; git pull origin master ; python setup.py ;" )


#########
#  EOF  #
#########
