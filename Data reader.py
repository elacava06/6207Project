import xlrd
#sets up 'sheet' to be the spreadsheet of raw data
book = xlrd.open_workbook('RawData.xlsx')
sheets = book.sheets()
sheet = sheets[0]

'''
Used to convert the timestamp for a data point into a 'graph ID'
which tells which timestep graph the data point belongs to (since
there is a separate graph representation for each of the 5667
timesteps)

Input is a float of a timestamp value

Outputs an integer representing the corresponding graph ID number
'''
def findGraphID(timestamp):
    rawGraphID = (((timestamp - 41581.7508) * 1000000)/5.7869246879)
    graphID = int(round(rawGraphID))
    return graphID

'''
Used to break up the different timesteps into unique "graphs" (there
ends up being 5667 of them) and to put the values from the
corresponding rows of data in the excel file into the appropriate
"graph"

Outputs a dictionary with the timestep as the key and a list of rows
as the corresponding value. Each row is also a list of values of that row
and essentially represents a player on the field during that timestep.
The 4 values per row are [timestamp, playerID, xLocation, yLocation).
'''
def createPlayerLocationsByGraphID():
    playerLocationsByGraphID = {}
    #hardcoded 62750 because this is the size of the trimmed dataset
    # that I am using
    for x in range(62570):
        graphID = findGraphID(sheet.cell_value(x,0))
        if graphID in playerLocationsByGraphID:
            playerLocationsByGraphID[graphID].append(sheet.row_values(x))
        else:
            playerLocationsByGraphID[graphID] = [sheet.row_values(x)]
    return playerLocationsByGraphID

'''
Used to organize data about each individual timestep graph in two
ways, by player ID number and by graph ID number

Outputs a tuple of two dictionaries, (playerInfoByGraphID,
playerInfoByPlayerID). playerInfoByGraphID is a dictionary with
an integer graph ID as the key and a list of Player Info tuples
as the value. There is one Player Info tuple for every player on
the field during the timestep corresponding to the graph ID.
playerInfoByPlayerID is a dictionary with an integer player ID as
the key and a list of Player Info tuples as the value. There is
one Player Info tuple for every timestep during which the player
was on the field. The Player Info tuples are of the form (PlayerID,
numPlayersOnField, distancesToPlayers, totalDistance,
closenessCentrality).
'''
def createInfoByID():
    playerLocationsByGraphID = createPlayerLocationsByGraphID()
    playerInfoByGraphID = {}
    playerInfoByPlayerID = {}
    #hardcoded 1-15 because these are the player IDs in the dataset
    for playerID in range(1,16):
        playerInfoByPlayerID[playerID] = []
    #hardcoded 5667 because this is the observed number of unique timesteps
    for graphID in range(5667):
        playerLocations = playerLocationsByGraphID[graphID]
        numPlayersOnField = len(playerLocations)
        distanceInfoOfPlayers = []
        for i in playerLocations:
            iTimestamp = i[0]
            iPlayerID = i[1]
            iXLocation = i[2]
            iYLocation = i[3]
            distancesToPlayers = []
            totalDistance = 0
            for j in playerLocations:
                jTimestamp = j[0]
                jPlayerID = j[1]
                jXLocation = j[2]
                jYLocation = j[3]
                distance = (((iXLocation - jXLocation)**2) + ((iYLocation - jYLocation)**2))**(0.5)
                distancesToPlayers.append(distance)
                totalDistance += distance
            closenessCentrality = (numPlayersOnField/totalDistance)
            playerInfo = (iPlayerID, numPlayersOnField, distancesToPlayers, totalDistance, closenessCentrality)
            distanceInfoOfPlayers.append(playerInfo)
            playerInfoByPlayerID[iPlayerID].append(playerInfo)
        playerInfoByGraphID[graphID] = distanceInfoOfPlayers
    return (playerInfoByGraphID, playerInfoByPlayerID)

'''
Used to compute the average closeness centrality of the players
over the course of the game.

Input is a dictionary with an integer player ID as the key and a
list of Player Info tuples as the value. There is one Player Info
tuple for every timestep during which the player was on the field.
The Player Info tuples are of the form (PlayerID, numPlayersOnField,
distancesToPlayers, totalDistance, closenessCentrality).

Output is a dictionary with an integer player ID as the key and a
float representing the average closeness centrality of that player
over the course of the game as the value.
'''
def getAverageClosenessCentralities(playerInfoByPlayerID):
    averageCentralityByPlayerID = {}
    for playerID in playerInfoByPlayerID:
        totalCentrality = 0
        for timestepData in playerInfoByPlayerID[playerID]:
            totalCentrality += timestepData[4]
        if len(playerInfoByPlayerID[playerID]) != 0:
            averageCentrality = totalCentrality/len(playerInfoByPlayerID[playerID])
            averageCentralityByPlayerID[playerID] = averageCentrality
    return averageCentralityByPlayerID

###MAIN WORKSPACE###


infoByID = createInfoByID()
averageClosenessCentralities = getAverageClosenessCentralities(infoByID[1])
print averageClosenessCentralities


###MAIN WORKSPACE###
    


