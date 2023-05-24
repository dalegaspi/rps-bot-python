__author__ = 'dalegaspi'


__author__ = 'dalegaspi'

import gamefuncs
import sys
import getopt
import multiprocessing


def main(argv):

    # game board id
    game = 0

    # row
    row = None

    # col
    col = None

    try:
        opts, args = getopt.getopt(argv, "g:r:c:")
    except:
        print 'bomb.py -g <gameId> -r <row> -c <col>'
        sys.exit(2)

    for opt, arg in opts:

        if opt == '-g':
            game = int(arg)
        elif opt == '-r':
            row = int(arg)
        elif opt == '-c':
            col = int(arg)

    # get one bomb
    try:
        plist = gamefuncs.getPlayersOnGame(game)

        firstPlayerWithBomb =  next(p for p in plist if int(p['bombs']) > 0)
        print 'player with bomb: {0}'.format(firstPlayerWithBomb['name'])
        firstPlayerKeyWithBomb = gamefuncs.getKeyFromPlayerId(int(firstPlayerWithBomb['playerId']))

        astat = gamefuncs.attackCell(game, None, 'bomb', firstPlayerKeyWithBomb, row, col)

        print 'bomb result = {0}'.format(astat['result'])
    except:
        print 'no bombs available.  sad panda is sad.'


if __name__ == "__main__":
    main(sys.argv[1:])