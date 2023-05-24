__author__ = 'dalegaspi'

import gamefuncs
import sys
import getopt



def main(argv):

    # csv file
    csv = None

    # game board id
    game = 0

    # inverted
    inverted = False

    # row
    row = None

    # col
    col = None

    # weapon - None means random
    weapon = None

    try:
        opts, args = getopt.getopt(argv, "ig:d:r:c:w:")
    except:
        print 'attack.py -g <gameId> [-i] [-d <csvfile>] [-r <row>] [-c <col>] [-w <weapon>]'
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-i':
            inverted = True
        elif opt == '-d':
            csv = arg
        elif opt == '-g':
            game = int(arg)
        elif opt == '-r':
            game = int(arg)
        elif opt == '-c':
            game = int(arg)

    print 'game to attack {0}'.format(game)

    if (weapon is not None):
        print 'attack with weapon {0}'.format(weapon)
    else:
        print 'attack with random weapon'
        weapon = gamefuncs.getRandomWeapon()

    if (row is not None and col is not None):
        print 'attack cell [{0}:{1}]'.format(row, col)
        cell = gamefuncs.getCell(game, row, col)
        ar = gamefuncs.attackCell(game, cell, weapon)

    elif (csv is not None):
        print 'attack data will come from {0} inverted {1}'.format(csv, inverted)
    else:
        print 'attack all cells in this board'


if __name__ == "__main__":
    main(sys.argv[1:])