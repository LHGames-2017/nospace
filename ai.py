from flask import Flask, request
from structs import *
import json
import numpy as np
import sys
import random, time
app = Flask(__name__)
dx=0
dy=0

def create_action(action_type, target):
    actionContent = ActionContent(action_type, target.__dict__)
    #print(actionContent)
    return json.dumps(actionContent.__dict__)

def create_move_action(target):
    return create_action("MoveAction", Point(target.X-dx,target.Y-dy))

def create_attack_action(target):
    return create_action("AttackAction", Point(target.X-dx,target.Y-dy))

def create_collect_action(target):
    return create_action("CollectAction", Point(target.X-dx,target.Y-dy))

def create_steal_action(target):
    return create_action("StealAction", Point(target.X-dx,target.Y-dy))

def create_heal_action():
    return create_action("HealAction", "")

def create_purchase_action(item):
    return create_action("PurchaseAction", item)

def deserialize_map(serialized_map):
    """
    Fonction utilitaire pour comprendre la map
    """
    serialized_map = serialized_map[1:]
    rows = serialized_map.split('[')
    column = rows[0].split('{')
    deserialized_map = [[Tile() for x in range(40)] for y in range(40)]
    for i in range(len(rows) - 1):
        column = rows[i + 1].split('{')

        for j in range(len(column) - 1):
            infos = column[j + 1].split(',')
            end_index = infos[2].find('}')
            content = int(infos[0])
            x = int(infos[1])
            y = int(infos[2][:end_index])
            deserialized_map[i][j] = Tile(content, x, y)
    return deserialized_map

#customs
def visual(lines,x,y):
    
    for i in lines:
        line = ''
        for j in i:
            #Empty, Wall, House, Lava, Resource, Shop, Player
            #0      1     2      3     4         5     6
            line+=str(j.Content).replace('None','N').replace('0', ' ').replace('1','#').replace('2','^').replace('3','L').replace('4','$').replace('5','S').replace('6','o')
        print(line)

def distance(p1, p2):
    return math.ceil(math.sqrt((p2[0]-p1[0])**2+(p2[1]-p1[1])**2))

'''
def searchg(x,y,grid,target, at):
    if grid[x][y] == target:
        at.append([x,y]) #found
        return True
    elif grid[x][y] == 1 or grid[x][y] == 3:
        return False #wall or lava
    elif grid[x][y] == 9:
        return False #been here
    
    at.append([x,y])
    grid[x][y] == 9
    
    if ((x<len(grid)-1 and search(x+1,y,grid,target, at))
        or (y > 0 and search(x, y-1,grid,target, at))
        or (x > 0 and search(x-1,y,grid,target, at))
        or (y < len(grid)-1 and search(x, y+1,grid,target, at))):
        return True
    return False
'''
def search_next(me, target,m,dx,dy):
    x=me.Position.X
    y=me.Position.Y
    if m[x-dx][y-dy].Content==4:
        return create_move_action(Point(x+dx,y+dy))
    neighbors = [[x+1,y],[x-1,y],[x,y+1],[x,y]]
    tNeighbors = []
    for neighbor in neighbors:
        tNeighbors.append([distance([x,y],[target.X, target.Y]),neighbor])
    sortedNeighbors=sorted(tNeighbors, key=lambda x:x[0])
    for n in sortedNeighbors:
        #print(target.__dict__)
        #print(x,y)
        #print('----------',n,'--------')
            #Empty, Wall, House, Lava, Resource, Shop, Player
            #0      1     2      3     4         5     6
        tile = m[n[1][0]-dx][n[1][1]-dy]
        #print(tile.__dict__)
        content = tile.Content
        point = Point(n[1][0],n[1][1])
        if content==0 or content==2 or content==5:
            return create_move_action(point)
        elif content==1 or content == 6:
            #print('attack',point)
            return create_attack_action(point)
        else:# content==3:
            #print('skip')
            continue
        
def route(start, end, at, best=[]):
    best.append(end)
    for i in range(len(at)-1,-1,-1):
        if compare(at[i], best[-1]):
            best.append(at[i])
    best=best[::-1]
    return best

def compare(a,b):
    if (a[0]==b[0]) and (abs(a[1]-b[1])==1):
        return True
    elif (a[1]==b[1]) and (abs(a[0]-b[0])==1):
        return True
    else:
        return False
    
def arr2action(c,d):
    if c[0]==d[0]:
        if c[1]<d[1]:
            return create_move_action(Point(x+1,y))
        else:
            return create_move_action(Point(x-1,y))
    elif c[0]<d[0]:
        return create_move_action(Point(x,y-1))
    else:
        return create_move_action(Point(x,y+1))

def findTargets(mapmatrix, me):
    resources = []
    enemyhouses = []
    shops = []
    for row in mapmatrix:
        for tile in row:
            if tile.Content==4:
                resources.append(tile)
            elif tile.Content==2 and tile.Content!=me.HouseLocation:
                enemyhouses.append(tile)
            elif tile.Content==5:
                shops.append(tile)
            else:
                continue
    return [resources, enemyhouses, shops]

def decide(me, closestEnemies, targets, grid):
    try:
        distEn = closestEnemy[0][0]
        enemy = closestEnemy[0][1]
    except:
        distEn=0
        enemy = []
    distTarget = targets[0][0]
    target = targets[0][1]
    best=[]
    at=[]
    
    if distEn==1:
        #print('------1-------')
        return create_attack_action(Point(enemy.X,enemy.Y))
    elif distTarget==1 and target.Content==2:
        #print('------2-------')
        return create_collect_action(Point(target.X,target.Y))
    elif distTarget==0 and target.Content==4:
        #print('------3-------')
        return create_collect_action(Point(target.X,target.Y))
    else:
        #print('------4-------')
        #t = random.choice([1,0])
        #u = (t+1)%2
        #return create_move_action(Point(me.Position.X+t,me.Position.Y+u))
        return search_next(me, target, grid)
def bot():
    """
    Main de votre bot.
    """
    map_json = request.form["map"]

    # Player info

    encoded_map = map_json.encode()
    map_json = json.loads(encoded_map)
    p = map_json["Player"]
    pos = p["Position"]
    x = pos["X"]
    y = pos["Y"]
    
    house = p["HouseLocation"]
    player = Player(p["Health"], p["MaxHealth"], Point(x,y),
                    Point(house["X"], house["Y"]),
                    p["CarriedResources"], p["CarryingCapacity"])

    # Map
    serialized_map = map_json["CustomSerializedMap"]
    deserialized_map=deserialize_map(serialized_map)
    transposed=np.transpose(deserialized_map)
    
    
    targets = findTargets(deserialized_map, player)
    visual(transposed[::-1],x,y)
    otherPlayers = []
    '''
    #print(map_json)
    for player_dict in map_json["OtherPlayers"]:
        #print(player_dict)
        for player_name in player_dict.keys():
            player_info = player_dict[player_name]
            #print('---------')
            #print(player_info)
            #print('---------')
            p_pos = player_info["Position"]
            player_info = PlayerInfo(player_info["Health"],
                                     player_info["MaxHealth"],
                                     Point(p_pos["X"], p_pos["Y"]))

            otherPlayers.append({player_name: player_info })
    '''
    # return decision
    #targets = 
    tTargets = []
    for target in targets[0]:#+targets[1]:
        tTargets.append([distance([x,y],[target.X,target.Y]),target])
    sortedTargets = sorted(tTargets, key=lambda x:x[0])
    
    
    tEnemies = []
    for enemy in otherPlayers:
        tEnemies.append([distance([x,y],[enemy.X,enemy.Y]),enemy])
    sortedEnemies = sorted(tEnemies, key=lambda x:x[0])
    dx,dy=0,0
    for i,line in enumerate(deserialized_map):
        for j,tile in enumerate(line):
            if tile.X==x and tile.Y==y:
                dx = x-i
                dy = y-j
    #return decide(player, sortedEnemies, sortedTargets, deserialized_map)
    
    return search_next(player, sortedTargets[0][1], deserialized_map,dx,dy)
    
    
    
@app.route("/", methods=["POST"])
def reponse():
    """
    Point d'entree appelle par le GameServer
    """
    sys.stdout.flush()
    return bot()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
