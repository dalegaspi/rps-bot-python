__author__ = 'dalegaspi'

import requests
import random
import base64
import uuid
import sys


baseurl = 'http://10.1.105.226:806/GamePlay.svc'

validweapons = \
    {
        'rock' : { 'conquers' : 'scissors',  'weakness' : 'paper' },
        'paper' : { 'conquers': 'rock', 'weakness' : 'scissors' },
        'scissors' : { 'conquers' : 'paper', 'weakness' : 'rock' }
    }

#me = 'theLoveBot'
#mykey = 'eNoBAgD9%2fzE5AJ0Aaw%3d%3d'

me = 'RyanGoslingBot'
mykey = 'eNoBAgD9%2fzI2AJwAaQ%3d%3d'

#me = 'whoDatBot'
#mykey = 'cGxheWVySWQ9MzA%3d'

#me = '_dont_know_the_scope_of_outsourcing_LOL_bot'
#mykey = 'cGxheWVySWQ9Mzk%3d'

#me = 'donutBot'
#mykey = 'cGxheWVySWQ9MzE%3d'
 

op = 'optimusPrime'
opkey = 'cGxheWVySWQ9MTc2'

#mykey = 'cGxheWVySWQ9MTY0'
#me = 'AJTest21'





def getJsonResponse(url):
    return requests.get(url).json()

def getRandomWeapon():
    return random.choice(validweapons.keys())

def interpretWeapon(c):
    if c == '0':
        return getRandomWeapon()
    elif c.lower() == 'r':
        return 'rock'
    elif c.lower() == 'p':
        return 'paper'
    elif c.lower() == 's':
        return 'scissors'
    else:
        return None

def getKeyFromPlayerId(id):
    # get the key that we create base64 with
    skey = 'playerId={0}'.format(id);
    return base64.encodestring(skey);

def registerPlayer(teamId, name):
    url = '{0}/register/{1}/{2}'.format(baseurl, teamId, name)
    print 'url = {0}'.format(url)
    r = getJsonResponse(url)
    
    pk = r['playerAccessKey']

    return { 'name' : name, 'key' : pk }

def createPhantomPlayer(teamId):
    # our phantom player use GUID
    name = str(uuid.uuid4())

    return registerPlayer(teamId, name)

def joinGame(key, gameId):
    url = '{0}/joinGame/{1}?playerAccessKey={2}'.format(baseurl, gameId, key)
    r = getJsonResponse(url)

    return r

def getWinningWeapon(weapon):
    return validweapons[str(weapon).lower()]['weakness']

def getWeaponConquers(weapon):
    return validweapons[str(weapon).lower()]['conquers']

def getWeaponThatIsNot(weapon):
    # get random weapon that is not the weapon provided
    return random.choice([w for w in validweapons.keys() if (w != str(weapon).lower())])

def getPlayerData(name, plist):
    return next(p for p in plist if (p['name'].lower() == str(name).lower()))

def getAdminKey():
    return getKeyFromPlayerId(0)

def getGlobalPlayerList():
    adminkey = getAdminKey();
    url = '{0}/playerList/?playerAccessKey={1}'.format(baseurl, adminkey)

    r = getJsonResponse(url)

    return r['players']

def getPlayersOnGame(gameId, key=mykey):
    url = '{0}/gamescore/{1}/?playerAccessKey={2}'.format(baseurl, gameId, key)
    r = getJsonResponse(url)

    return r['players']

def getPlayersThatIsNot(gameId, name=me, key=mykey):
    plist = getPlayersOnGame(gameId, key)

    return [p for p in plist if str(p['name']).lower() != str(name).lower()]


def getGameInfo(gameId, key=mykey):
    url = '{0}/gameboard/{1}/?playerAccessKey={2}'.format(baseurl, gameId, key)

    r = getJsonResponse(url)

    return r['game']

def getCell(gameId, row, col, key=mykey):
    board = getGameInfo(gameId, key)
    c = next(c for c in board['gameCells'] if int(c['col']) == int(col) and int(c['row']) == int(row))
    return c

def attackCell(gameId, cell, weapon, key, row=None, col=None):

    if row is not None and col is not None:
        r = row
        c = col
    else:
        r = cell['row']
        c = cell['col']

    url = '{0}/attack/{1}/{2},{3}/{4}?playerAccessKey={5}'.format(baseurl, gameId, c, r, weapon, key)

    rs = getJsonResponse(url)

    #if rs['result'] == 'failure':
    #    print 'attack on [{0}:{1}] results in failure: {2}'.format(r, c, rs['message'])

    return rs

def clueSolve(gameid, key, suspect, room, weapon,):

    url = '{0}/clueSolve/{1}/{2}/{3}/{4}/?playerAccessKey={5}'.format(baseurl, gameid, suspect, room, weapon, key)

    print 'attack on {0}'.format(url)
    rs = getJsonResponse(url)

    print 'result for {0}: {1}'.format(url, rs['message'])

    return rs

def doIOwnThisCell(cell, name=me):
    return str(cell['playerName'].lower()) == (name.lower())

def isCellOccupied(cell):
    return cell['isOccupied'];

def invadeCell(gameId, row, col, weapon=getRandomWeapon(), kill=True, tolerance=300, name=me, key=mykey):

    print 'invading cell [{0}:{1}] for game {2}'.format(row, col, gameId)
    # get the cell
    cell = getCell(gameId, row, col, key)

    if weapon is None:
        weapon = getRandomWeapon()

    # get the owner's key
    if isCellOccupied(cell):
        ownercellkey = getKeyFromPlayerId(cell['playerId'])

    # get the players that is not me
    otherplayers = getPlayersThatIsNot(gameId, name, key)

    losingweapon = getWeaponConquers(weapon)

    if not isCellOccupied(cell):
        print 'cell unoccupied...occupying...'
        astat = attackCell(gameId, cell, weapon, key)
    elif not doIOwnThisCell(cell, name):

        # change the cell's weapon using the owner's key to defeat it
        astat = attackCell(gameId, cell, losingweapon, ownercellkey)

        '''
        for now, the mode is that we attack it until the cell count is down to 0
        we might have to update it in such a way that we need to check the cell's
        wincount while in loop
        '''

        # change the bastard's weapon; this is just for safety in case he randomizes it
        astat = attackCell(gameId, cell, losingweapon, ownercellkey)

        for x in range(1, int(cell['winCount']) * 2):
            # attack, bitch!
            astat = attackCell(gameId, cell, weapon, key)
            if astat['gameCell']['playerName'] == name:
                print 'i own this cell [{0}:{1}] now; break'.format(row, col)
                break;
            elif astat['result'] != 'win':
                ownercellkey = getKeyFromPlayerId(astat['gameCell']['playerId']);
                astat = attackCell(gameId, cell, losingweapon, ownercellkey)

            #sys.stdout.write('.')

        #print ''

    if kill:
        #cell = getCell(gameId, row, col, key)

        # if i don't own this cell at this point...wtf
        #if not doIOwnThisCell(cell, name):
        #    return

        for p in otherplayers:
            pk = getKeyFromPlayerId(p['playerId'])

            astat = attackCell(gameId, cell, losingweapon, pk)
            if astat['gameCell']['playerName'] != name:
                print 'a new player owns [{0}:{1}]: {2}; break'.format(row, col, astat['gameCell']['playerName'])
                break

            if astat['result'] != 'loss':
                print 'somebody changed the weapon!'
                astat = attackCell(gameId, cell, weapon, key)

            #sys.stdout.write('.')

    #print ''


def protectCell(gameId, row, col, weapon=getRandomWeapon(), loop=3, tolerance=300, name=me, key=mykey):
    # get the cell
    cell = getCell(gameId, row, col, key)

    if weapon is None:
        weapon = getRandomWeapon()

    # get the players that is not me
    otherplayers = getPlayersThatIsNot(gameId, name, key)

    losingweapon = getWeaponConquers(weapon)

    if doIOwnThisCell(cell, name):
        print 'i own this cell[{0},{1}]; change weapon to {2}'.format(row, col, weapon)
        astat = attackCell(gameId, cell, weapon, key)

        for i in range(1, loop + 1):
            for p in otherplayers:
                pk = getKeyFromPlayerId(p['playerId'])

                astat = attackCell(gameId, cell, losingweapon, pk)

                if astat['result'] == 'failure':
                    print 'failure on [{0}:{1}]: {2}; break'.format(row, col, astat['message'])
                if astat['result'] != 'loss':
                    print 'somebody changed the weapon!'
                    astat = attackCell(gameId, cell, weapon, key)

                sys.stdout.write('.')
                if astat['gameCell']['playerName'] != name:
                    print 'a new player owns [{0}:{1}]: {2}; break'.format(row, col, astat['gameCell']['playerName'])
                    return

            cell = getCell(gameId, row, col, key)

            if (int(cell['winCount']) >= tolerance):
                print 'current winCount is {0}; stopping now'.format(cell['winCount'])
                return
    else:
        print 'i do NOT own this cell[{0},{1}]; skip'.format(row, col)
        return




