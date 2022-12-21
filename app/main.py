import sys
from central.main import mainCentral
from rooms.main import mainRoom

if sys.argv[1] == 'S':
    mainCentral(sys.argv[2])

elif sys.argv[1] == 'R':
    mainRoom(sys.argv[2], sys.argv[3])
