__author__ = 'dalegaspi'

import gamefuncs
import sys
import getopt
import multiprocessing
import random


def main(argv):

    # csv file
    csv = None

    # game board id
    game = 0

    # inverted
    multiprocess = False

    # row
    row = None

    # col
    col = None

    # weapon - None means random
    weapon = None

    kill = False

    randomattack = False

    try:
        opts, args = getopt.getopt(argv, "kmg:d:r:c:w:n")
    except:
        print 'invade.py -g <gameId> [-k] [-m] [-d <csvfile>] [-r <row>] [-c <col>] [-w <weapon>] [-n]'
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-m':
            multiprocess = True
        elif opt == '-d':
            csv = arg
        elif opt == '-g':
            game = int(arg)
        elif opt == '-r':
            row = int(arg)
        elif opt == '-c':
            col = int(arg)
        elif opt == '-k':
            kill = True
        elif opt == '-w':
            weapon = arg
        elif opt == '-n':
            randomattack  = True

    print 'game to invade {0}'.format(game)

    if (weapon is not None):
        print 'invade with weapon {0}'.format(weapon)
    else:
        print 'invade with random weapon'

    if (row is not None and col is not None):
        print 'invade cell [{0}:{1}]'.format(row, col)

        gamefuncs.invadeCell(game, row, col, weapon=weapon)

    elif (csv is not None):
        print 'invade data will come from {0}'.format(csv)

        pool = multiprocessing.Pool()
        if multiprocess:
            print 'multi-processing enabled'


        for row, l in enumerate([line.strip() for line in open(csv)]):
            for col, c in enumerate([char for char in l.split(',')]):
                weapon = gamefuncs.interpretWeapon(c)
                if (weapon is not None):
                    if multiprocess:
                        pool.apply_async(gamefuncs.invadeCell, args=(game, row, col, weapon, kill))
                    else:
                        gamefuncs.invadeCell(game, row, col, weapon=weapon)

        if multiprocess:
            pool.close()
            pool.join()
    else:
        print 'invade all cells in this board'
        ginfo = gamefuncs.getGameInfo(game)

        pool = multiprocessing.Pool(32)
        if multiprocess:
            print 'multi-processing enabled'

        invadefunc = pool.apply_async if multiprocess else apply

        rows = range(0, int(ginfo['rows']))
        cols = range(0, int(ginfo['cols']))

        if randomattack:
            random.shuffle(rows)
            random.shuffle(cols)

        matrix = [(r, c) for c in cols for r in rows]

        if randomattack:
            random.shuffle(matrix)

        for cell in matrix:
            invadefunc(gamefuncs.invadeCell, (game, cell[0], cell[1], weapon, kill))

        if multiprocess:
            pool.close()
            pool.join()

if __name__ == "__main__":
    main(sys.argv[1:])
