def file_read(n):
    f = open("Start_Configuration.txt", "r")
    start=[]
    for i in range(n):
        row=[]
        for j in f.readline().strip().split('\t'):
                row.append(j)
        start+=[row]
        row=[]
    #print(start)
    f.close()
    f = open("Goal_Configuration.txt", "r")

    goal=[]
    for i in range(n):
        row=[]
        for j in f.readline().strip().split('\t'):
            row.append(j)
        goal+=[row]
        row=[]
    #print(goal)
    f.close()
    return start,goal

def node(state,gvalue,fvalue,parent,direction):
    firstNode = []
    firstNode.append(state)
    firstNode.append(gvalue)
    firstNode.append(fvalue)
    firstNode.append(parent)
    firstNode.append(direction)
    return firstNode

def hvalue(start,goal):
    """calculate the number of missing tiles"""
    count = 0
    for i in range(0,n):
        for j in range(0,n):
            if (start[i][j] != goal[i][j] and start[i][j] != '-'):
                count+=1
    return count

def manhatton(start,goal):
    """ Calculates total manhatton distance """
    count = 0
    for i in range(0,n):
        for j in range(0,n):
            dist=ds(start[i][j],i,j,goal)
            count=count+dist
    return count

def ds(val,c1,c2,goal):
    dt=0
    for c3 in range(0,n):
        for c4 in range(0,n):
            if(val==goal[c3][c4]):
                dt = abs(c3-c1)+abs(c4-c2)
                return dt

def copy(root):
    temp = []
    for i in root:
        t = []
        for j in i:
            t.append(j)
        temp.append(t)
    return temp

def find(state):
    """find the two positions of the blank spaces """
    count=0
    xy=[]
    for i in range(0,len(state)):
        for j in range(0,len(state)):
            if state[i][j] == '-':
                xy.append(i)
                xy.append(j)
                count+=1
                if (count==2):
                    return xy[0],xy[1],xy[2],xy[3]

def childNode(parentNode):
    #print('p node ' + str(parentNode[0]))
    x1,y1,x2,y2 = find(parentNode[0])  # cordinate of the - tile
    val_list1 = [[x1,y1-1,'right'],[x1,y1+1,'left'],[x1-1,y1,'down'],[x1+1,y1,'up']] # moving direction of - tile
    val_list2 = [[x2,y2-1,'right'],[x2,y2+1,'left'],[x2-1,y2,'down'],[x2+1,y2,'up']]
    children = []
    for val in val_list1:
        child = shuffle(parentNode[0],x1,y1,val[0],val[1])
        if child is not None:
            children.append(node(child,parentNode[1] + 1,0,parentNode,[parentNode[0][val[0]][val[1]],val[2]]))

    for val in val_list2:
        child = shuffle(parentNode[0],x2,y2,val[0],val[1])
        if child is not None:
            children.append(node(child,parentNode[1] + 1,0,parentNode,[parentNode[0][val[0]][val[1]],val[2]]))
    return children

def shuffle(state,x1,y1,x2,y2):
    """ Move the blank space in the given direction and if the position value are out
            of limits the return None """
    if (x2 >= 0 and x2 < len(state) and y2 >= 0 and y2 < len(state) and x2!="-" and y2!="-"):
        new_puzzle = []
        new_puzzle = copy(state)
        temp=new_puzzle[x2][y2]
        new_puzzle[x2][y2] = new_puzzle[x1][y1]
        new_puzzle[x1][y1] = temp
        return new_puzzle
    else:
        return None

def run():
    count = 0

    while True:
        count += 1
        currentNode = opened[0]

        if (hvalue(currentNode[0],goal) == 0):
            outputFile=open("output.txt","a+")
            revNode=currentNode
            moves=[]
            moves1=[]
            while (revNode[3]!=None):
                moves.append(revNode[4])
                revNode=revNode[3]
            moves.reverse()

            for val in moves:
                moves1.append("("+val[0]+","+val[1]+")")
            output = ','.join(moves1)
            outputFile.write(output)
            outputFile.write("\n")
            print (count)
            break

        chilldren = childNode(currentNode)

        for i in chilldren:
            duplicate = False
            i[2] = i[1]+manhatton(i[0],goal)

            for j in closed:
                if(j[0] == i[0]):
                    duplicate = True
                    break
            if(not(duplicate)):
                opened.append(i)
        closed.append(currentNode)
        del opened[0]
        opened.sort(key = lambda x:x[2],reverse=False)


n = int(input('enter the puzzle size'))
start,goal = file_read(n)
print(start)
print(goal)

openNode = node(start,0,0,None,None)

opened = []
closed = []
opened.append(openNode)
run()



