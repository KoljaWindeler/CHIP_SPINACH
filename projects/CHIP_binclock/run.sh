locationOfScript=$(dirname "$(readlink -e "$0")")
cd $locationOfScript
screen -S "mylittlescreen" -d -m
screen -r "mylittlescreen" -X stuff 'python3 bin_clock.py&\n'
