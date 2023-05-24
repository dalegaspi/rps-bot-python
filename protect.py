__author__ = 'dalegaspi'

import gamefuncs
import sys
import getopt
import multiprocessing


def main(argv):

    # csv file
    csv = None

    # game board id
    game = 0

    # inverted
    inverted = False

    # multiprocess
    multiprocess = False

    # row
    row = None

    # col
    col = None

    # weapon
    weapon = None

    # loop
    loop = 3

    try:
        opts, args = getopt.getopt(argv, "mg:d:r:c:w:l:")
    except:
        print 'protect.py -g <gameId> [-m] [-d <csvfile] [-r <row>] [-c <col>] [-w <weapon>] [-l <loop>]'
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
        elif opt == '-w':
            weapon = arg
        elif opt == '-l':
            loop = int(arg)

    print 'game to protect {0}'.format(game)

    if (weapon is not None):
        print 'protect with weapon {0}'.format(weapon)
    else:
        print 'protect with random weapon'

    if (row is not None and col is not None):
        print 'protect cell [{0}:{1}]'.format(row, col)

        gamefuncs.protectCell(game, row, col, weapon, loop)

    if (csv is not None):
        print 'protect data will come from {0}'.format(csv)
        pool = multiprocessing.Pool()

        if multiprocess:
            print 'multi-processing enabled'

        for row, l in enumerate([line.strip() for line in open(csv)]):
            for col, c in enumerate([char for char in l.split(',')]):
                weapon = gamefuncs.interpretWeapon(c)
                if (weapon is not None):
                    if multiprocess:
                        pool.apply_async(gamefuncs.protectCell, args=(game, row, col, weapon, loop))
                    else:
                        gamefuncs.protectCell(game, row, col, weapon=weapon, loop=loop)

        if multiprocess:
            pool.close()
            pool.join()

    else:
        print 'protect all cells in this board'

        ginfo = gamefuncs.getGameInfo(game)

        pool = multiprocessing.Pool(16)
        if multiprocess:
            print 'multi-processing enabled'

        for row in xrange(0, int(ginfo['rows'])):
            for col in xrange (0, int(ginfo['cols'])):
                if multiprocess:
                    pool.apply_async(gamefuncs.protectCell, args=(game, row, col, weapon, loop))
                else:
                    gamefuncs.protectCell(game, row, col, weapon, loop)

        if multiprocess:
            pool.close()
            pool.join()


if __name__ == "__main__":
    main(sys.argv[1:])