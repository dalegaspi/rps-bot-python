__author__ = 'dalegaspi'

import gamefuncs
import sys
import getopt
import multiprocessing

def blacklist(game, playerid, limit):
    key = gamefuncs.getKeyFromPlayerId(playerid)

    print 'playerId {0} increase error by {1}'.format(playerid, limit)
    for i in range(0, limit):
        # attack with an illegal weapon
        if i % 10 == 0:
            gamefuncs.attackCell(game, None, gamefuncs.getRandomWeapon(), key, 0, 0)
        
	gamefuncs.attackCell(game, None, 'bullshit', key, 0, 0)

    print 'playerId {0} is now blacklisted'.format(playerid)


def main(argv):

    # game board id
    game = 0

    # multiprocess
    multiprocess = False

    # all?
    all = False

    # whitelist
    whitelist = []

    # limit
    limit = 100

    try:
        opts, args = getopt.getopt(argv, "mag:l:c:")
    except:
        print 'blacklist.py -g <gameId> [-m] [-l <pidcsv>]'
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-m':
            multiprocess = True
        elif opt == '-a':
            all = True
        elif opt == '-g':
            game = int(arg)
        elif opt == '-l':
            whitelist = [int(p) for p in str(arg).split(',')]
        elif opt == '-c':
            limit = int(arg)


    print 'game to blacklist {0}'.format(game)

    ginfo = gamefuncs.getGameInfo(game)

    if (all):
        blist = [int(p['playerId']) for p in ginfo['players'] if int(p['playerId']) not in whitelist]
    else:
        blist = whitelist

    pool = multiprocessing.Pool(16)
    if multiprocess:
        print 'multi-processing enabled'

    for p in blist:
        if multiprocess:
            pool.apply_async(blacklist, args=(game, p, limit))
        else:
            blacklist(game, p, limit)

    if multiprocess:
        pool.close()
        pool.join()


if __name__ == "__main__":
    main(sys.argv[1:])
