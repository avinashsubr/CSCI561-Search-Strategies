from collections import deque

out_file = open("C:\\Users\\Avi\\PycharmProjects\\Assignment1\\output.txt", 'w+')
#out_file = open("output.txt", 'w+')

def breadth_first_search(start_state, goal_state, tree):
    frontier = deque()
    child_parent = {}
    if start_state == goal_state:
        write_to_file(str(start_state) + " " + "0")
        return

    frontier.append(start_state)
    explored = set()

    while frontier:
        node = frontier.popleft()
        explored.add(node)
        if node in tree:
            for dict in tree[node]:
                for child in dict:
                    if child not in frontier and child not in explored:
                        parent = node
                        frontier.append(child)
                        if child not in child_parent:
                            if parent == start_state:
                                child_parent[child] = (parent,0)
                            else:
                                child_parent[child] = (parent, child_parent[parent][1]+1)
                        elif child_parent[child][1] > child_parent[parent][1]:
                            child_parent[child] = (parent, child_parent[parent][1] + 1)
                        if goal_state == child:
                            backtrack(child_parent,start_state,goal_state,child_parent[child][1]+1)
                            return


def depth_first_search(start_state, goal_state, tree):
    frontier = deque()
    if start_state == goal_state:
        write_to_file(str(start_state) + " " + "0")
        return

    child_parent = {}
    frontier.append(start_state)
    explored = set()

    while frontier:
        node = frontier.popleft()
        if goal_state == node:
            backtrack(child_parent,start_state,goal_state,child_parent[goal_state][1]+1)
            return
        explored.add(node)
        if node in tree:
            children = []
            for dict in tree[node]:
                for child in dict:
                    if child not in explored and child not in frontier:
                        parent = node  # local variable for parent
                        children.append(child)
                        if child not in child_parent:
                            if parent == start_state:
                                child_parent[child] = (parent, 0)
                            else:
                                child_parent[child] = (parent,child_parent[parent][1]+1)  #inserting child/parent pair into dictionary
                        elif child_parent[child][1] > child_parent[parent][1]:
                            child_parent[child] = (parent,child_parent[parent][1]+1)
            frontier.extendleft(reversed(children))

def uniform_cost_search(start_state, goal_state, tree):

    openQ = []#[node_cost, state_order, state, path_cost, parent_node_cost]
    state_order = 0
    openQ.append((0,state_order,start_state,0,0))
    state_order += 1
    closedQ = []
    child_parent = {}

    if start_state == goal_state:
        write_to_file(str(start_state) + " " + "0")
        return

    while openQ:
        currTuple = openQ.pop(0)
        currnode = currTuple[2]
        nodecost = currTuple[3] + currTuple[4]

        if currnode == goal_state:
            backtrack(child_parent,start_state,goal_state,nodecost)
            return

        if currnode in tree:
            parent = currnode
            for dict in tree[currnode]:
                for child in dict:
                    if not check_open_queue(child, openQ) and not check_closed_queue(child, closedQ):
                        openQ.append((int(dict[child]) + nodecost,state_order, child, int(dict[child]), nodecost))
                        state_order += 1
                        child_parent[child] = (parent, nodecost)

                    elif check_open_queue(child, openQ):
                        node = getNodeOpenQ(child, openQ)
                        if int(dict[child]) + nodecost < node[0]:
                            openQ = [state for state in openQ if state[2] != node[2]]
                            openQ.append((int(dict[child]) + nodecost, state_order, child, int(dict[child]), nodecost))
                            state_order += 1
                            child_parent[child] = (parent, nodecost)

                    elif check_closed_queue(child, closedQ):
                        node = getNodeClosedQ(child, closedQ)
                        if int(dict[child]) + nodecost < node[1]:
                            closedQ = [i for i in closedQ if i[0] != node[0]]
                            openQ.append((int(dict[child]) + nodecost, state_order, child, int(dict[child]), nodecost))
                            state_order += 1
                            child_parent[child] = (parent, nodecost)
        closedQ.append((currnode, nodecost))
        openQ = sorted(openQ,
                         key=lambda x: (x[0], x[1]))


def a_star(start_state, goal_state, tree, sunday_tree):

    openQ = []#[node_cost, state_order, state, path_cost, parent_node_cost]
    state_order = 0
    openQ.append((sunday_tree[start_state],state_order,start_state,0,0))
    state_order += 1
    closedQ = []
    child_parent = {}

    if start_state == goal_state:
        write_to_file(str(start_state) + " " + "0")
        return

    while openQ:

        currTuple = openQ.pop(0)
        currnode = currTuple[2]
        nodecost = currTuple[3] + currTuple[4]

        if currnode == goal_state:
            backtrack(child_parent,start_state,goal_state,nodecost)
            return

        if currnode in tree:
            for dict in tree[currnode]:
                for child in dict:
                    if not check_open_queue(child,openQ) and not check_closed_queue(child,closedQ):
                        openQ.append((int(dict[child]) + nodecost + int(sunday_tree[child]), state_order, child, int(dict[child]), nodecost))
                        state_order += 1
                        child_parent[child] = (currnode, nodecost)

                    elif check_open_queue(child,openQ):
                        node = getNodeOpenQ(child,openQ)
                        if int(dict[child]) + nodecost + int(sunday_tree[child]) < node[0]:
                            openQ = [i for i in openQ if i[2] != node[2]]
                            openQ.append((int(dict[child]) + nodecost + int(sunday_tree[child]), state_order, child, int(dict[child]), nodecost))
                            state_order += 1
                            child_parent[child] = (currnode, nodecost)

                    elif check_closed_queue(child,closedQ):
                        node = getNodeClosedQ(child,closedQ)
                        if int(dict[child]) + nodecost < node[1]:
                            closedQ = [i for i in closedQ if i[0] != node[0]]
                            openQ.append((int(dict[child]) + nodecost + int(sunday_tree[child]), state_order, child, int(dict[child]), nodecost))
                            state_order += 1
                            child_parent[child] = (currnode, nodecost)
        closedQ.append((currnode, nodecost))
        openQ = sorted(openQ,
                         key=lambda x: (x[0], x[1]))

def write_to_file(str):
    out_file.write(str + '\n')

def check_open_queue(child,queue):
    for item in queue:
        if item[2] == child:
            return True
    return False

def check_closed_queue(child,queue):
    for item in queue:
        if item[0] == child:
            return True
    return False

def getNodeClosedQ(child, closedQ):
	for node in closedQ:
		if node[0] == child:
			return node

def getNodeOpenQ(child, openQ):
	for node in openQ:
		if node[2] == child:
			return node

def backtrack(child_parent,start_state,goal_state,path_cost):
    solution = []
    solution.append((goal_state,path_cost))
    while goal_state is not start_state:
        solution.append((child_parent[goal_state][0],child_parent[goal_state][1]))
        goal_state = child_parent[goal_state][0]
    for entry in reversed(solution):
        write_to_file(entry[0] + " " + str(entry[1]))

with open("E:\\Education\\USC\\Fall 2016\\CSCI561 AI\\Assignments\\HW1\\input.txt", 'r') as f:
#with open("input.txt", 'r') as f:
    algo = f.readline().replace("\n", "")
    start_state = f.readline().replace("\n", "")
    goal_state = f.readline().replace("\n", "")
    traffic_lines_num = int(f.readline())

    tree = {}
    count = 0
    while count < traffic_lines_num:
        line = f.readline()
        splitLine = line.split()
        if splitLine[0] in tree:
            tree[splitLine[0]].append({splitLine[1]:splitLine[2]})
        else:
            tree[splitLine[0]] = [{splitLine[1]:splitLine[2]}]
        count += 1

    if algo == "BFS":
        breadth_first_search(start_state, goal_state, tree)

    elif algo == "DFS":
        depth_first_search(start_state, goal_state, tree)

    elif algo == "UCS":
        uniform_cost_search(start_state, goal_state, tree)

    elif algo == "A*":
        sunday_traffic_lines_num = int(f.readline())
        sunday_tree = {}
        count = 0;
        while count < sunday_traffic_lines_num:
            line = f.readline()
            splitLine = line.split()
            sunday_tree[splitLine[0]] = splitLine[1]
            count += 1
        a_star(start_state, goal_state, tree, sunday_tree)

    out_file.close()