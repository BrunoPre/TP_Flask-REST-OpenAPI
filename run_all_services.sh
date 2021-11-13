#!/bin/bash

source ~/archdist/bin/activate

python movie.py &
python booking.py &
python showtime.py &
python user.py &

echo 'All services are running'

while True; do

done

exit 0
