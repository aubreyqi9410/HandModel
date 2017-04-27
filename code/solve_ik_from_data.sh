# Bash Scripts that takes two syncronized files (DataGlove and VICON) and solves IK
#gloveDir="$HOME/Downloads/manipulation_trials/test/finger1/"
gloveDir="$HOME/Klampt/DataGlove/resources/test/"
viconDir="$HOME/Klampt/VICON/data/"
objDir="$HOME/Klampt/HandModel/data/"
glovefn="finger2_A.configs"
viconfn="finger2.csv"
objfn="finger2.csv"
frameIdx=1262
python solve_ik_from_data.py $gloveDir$glovefn $viconDir$viconfn $objDir$objfn $frameIdx
