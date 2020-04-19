import cv2
import numpy as np
import time

infinity = 10000000000000000000
height = 200
width = 300

rad = input("Enter the radius of the robot: ")
rad = int(rad)
clearance = input("Enter the clearance for the robot: ")
clearance = int(clearance)
shortest_path = []
blank_image = np.zeros((height, width, 3), np.uint8)

# circle
center_coordinates = (225, 50)
radius = 25
color = (255, 255, 255)
thickness = -1
blank_image = cv2.circle(blank_image, center_coordinates, radius, color, thickness)

maze = {}
inner_dict = {}

height = 200
width = 300


def check(x, y, r, c, c1):
    # Rhombus
    if ((x * (-3 / 5) + y - 55 - r - c < 0) and (x * (3 / 5) + y - 325 - r - c < 0) and (
            x * (-3 / 5) + y - 25 + r + c > 0) and (x * (3 / 5) + y - 295 + r + c > 0)):
        return True

    # polygon - rhombus
    elif x * (7 / 5) + y - 120 > 0 and x * (-6 / 5) + y + 10 - c - r < 0 and x * (6 / 5) + y - 170 - c - r < 0 and x * (
            -7 / 5) + y + 90 + c + r > 0:
        return True

    # polygon - triangle1
    elif y - 15 + c + r > 0 and x * (7 / 5) + y - 120 < 0 and x * (-7 / 5) + y + 20 < 0:
        return True

    # polygon - triangle2
    elif y + 13 * x - 340 + c + r + c1 > 0 and x + y - 100 - r - c < 0 and x * (-7 / 5) + y + 20 > 0:
        return True

    # rectangle -angled
    elif (200 - y) - (1.73) * x + 135 + r + c > 0 and (200 - y) + (0.58) * x - 96.35 - r - c <= 0 and (200 - y) - (
    1.73) * x - 15.54 - r - c <= 0 and (200 - y) + (0.58) * x - 84.81 + r + c >= 0:
        return True

    else:
        return False


def obstaclecheck_circle(x, y, r, c):
    if (((x - 225) ** 2) + ((y - 50) ** 2) < ((25 + r + c) ** 2)):
        return True
    else:
        return False


def obstaclecheck_ellipse(x, y, r, c):
    if (((x - 150) ** 2 / (40 + c + r) ** 2) + ((y - 100) ** 2) / (20 + c + r) ** 2) <= 1:
        return True
    else:
        return False


def obstacle_check(new_i, new_j, r, c, c1):
    if obstaclecheck_circle(new_i, new_j, r, c):
        return True
    elif obstaclecheck_ellipse(new_i, new_j, r, c):
        return True
    elif check(new_i, new_j, r, c, c1):
        return True
    elif ((new_i - r - c < 0) or (new_j - r - c < 0) or (new_i + r + c > width - 1) or (new_j + r + c > height - 1)):
        return True
    else:
        return False


def top_left(i, j, r, c, c2):
    cost = 1.414
    new_i = i - 1
    new_j = j - 1
    if obstaclecheck_circle(new_i, new_j, r, c):
        return None, None, None
    elif obstaclecheck_ellipse(new_i, new_j, r, c):
        return None, None, None
    if check(new_i, new_j, r, c, c2):
        return None, None, None
    elif ((new_i - r - c < 0) or (new_j - r - c < 0) or (new_i + r + c > width - 1) or (new_j + r + c > height - 1)):
        return None, None, None
    else:
        return cost, new_i, new_j


def top(i, j, r, c, c2):
    cost = 1
    new_i = i
    new_j = j - 1
    if obstaclecheck_circle(new_i, new_j, r, c):
        return None, None, None
    elif obstaclecheck_ellipse(new_i, new_j, r, c):
        return None, None, None
    if check(new_i, new_j, r, c, c2):
        return None, None, None
    elif ((new_i - r - c < 0) or (new_j - r - c < 0) or (new_i + r + c > width - 1) or (new_j + r + c > height - 1)):
        return None, None, None
    else:
        return cost, new_i, new_j


def top_right(i, j, r, c, c2):
    cost = 1.414
    new_i = i + 1
    new_j = j - 1
    if obstaclecheck_circle(new_i, new_j, r, c):
        return None, None, None
    elif obstaclecheck_ellipse(new_i, new_j, r, c):
        return None, None, None
    if check(new_i, new_j, r, c, c2):
        return None, None, None
    elif ((new_i - r - c < 0) or (new_j - r - c < 0) or (new_i + r + c > width - 1) or (new_j + r + c > height - 1)):
        return None, None, None
    else:
        return cost, new_i, new_j


def right(i, j, r, c, c2):
    cost = 1
    new_i = i + 1
    new_j = j
    if obstaclecheck_circle(new_i, new_j, r, c):
        return None, None, None
    elif obstaclecheck_ellipse(new_i, new_j, r, c):
        return None, None, None
    if check(new_i, new_j, r, c, c2):
        return None, None, None
    elif ((new_i - r - c < 0) or (new_j - r - c < 0) or (new_i + r + c > width - 1) or (new_j + r + c > height - 1)):
        return None, None, None
    else:
        return cost, new_i, new_j


def bottom_right(i, j, r, c, c2):
    cost = 1.414
    new_i = i + 1
    new_j = j + 1
    if obstaclecheck_circle(new_i, new_j, r, c):
        return None, None, None
    elif obstaclecheck_ellipse(new_i, new_j, r, c):
        return None, None, None
    if check(new_i, new_j, r, c, c2):
        return None, None, None
    elif ((new_i - r - c < 0 or new_j - r - c < 0 or new_i + r + c > width - 1 or new_j + r + c > height - 1) or (
            new_i + r + c >= 0 and new_i - r - c <= 2 and new_j + r + c >= 1 and new_j - r - c <= 2)):
        return None, None, None
    else:
        return cost, new_i, new_j


def bottom(i, j, r, c, c2):
    cost = 1
    new_i = i
    new_j = j + 1
    if obstaclecheck_circle(new_i, new_j, r, c):
        return None, None, None
    elif obstaclecheck_ellipse(new_i, new_j, r, c):
        return None, None, None
    if check(new_i, new_j, r, c, c2):
        return None, None, None
    elif ((new_i - r - c < 0) or (new_j - r - c < 0) or (new_i + r + c > width - 1) or (new_j + r + c > height - 1)):
        return None, None, None
    else:
        return cost, new_i, new_j


def bottom_left(i, j, r, c, c2):
    cost = 1.414
    new_i = i - 1
    new_j = j + 1
    if obstaclecheck_circle(new_i, new_j, r, c):
        return None, None, None
    elif obstaclecheck_ellipse(new_i, new_j, r, c):
        return None, None, None
    if check(new_i, new_j, r, c, c2):
        return None, None, None
    elif ((new_i - r - c < 0) or (new_j - r - c < 0) or (new_i + r + c > width - 1) or (new_j + r + c > height - 1)):
        return None, None, None
    else:
        return cost, new_i, new_j


def left(i, j, r, c, c2):
    cost = 1
    new_i = i - 1
    new_j = j
    if obstaclecheck_circle(new_i, new_j, r, c):
        return None, None, None
    elif obstaclecheck_ellipse(new_i, new_j, r, c):
        return None, None, None
    if check(new_i, new_j, r, c, c2):
        return None, None, None
    elif ((new_i - r - c < 0) or (new_j - r - c < 0) or (new_i + r + c > width - 1) or (new_j + r + c > height - 1)):
        return None, None, None
    else:
        return cost, new_i, new_j


def function(i, j, r, c, c2):
    weight1, new_i1, new_j1 = top_left(i, j, r, c, c2)
    weight2, new_i2, new_j2 = top(i, j, r, c, c2)
    weight3, new_i3, new_j3 = top_right(i, j, r, c, c2)
    weight4, new_i4, new_j4 = right(i, j, r, c, c2)
    weight5, new_i5, new_j5 = bottom_right(i, j, r, c, c2)
    weight6, new_i6, new_j6 = bottom(i, j, r, c, c2)
    weight7, new_i7, new_j7 = bottom_left(i, j, r, c, c2)
    weight8, new_i8, new_j8 = left(i, j, r, c, c2)

    if (weight1 != None):
        inner_dict[(new_i1, new_j1)] = weight1
        maze[(i, j)] = inner_dict
    if (weight2 != None):
        inner_dict[(new_i2, new_j2)] = weight2
        maze[(i, j)] = inner_dict
    if (weight3 != None):
        inner_dict[(new_i3, new_j3)] = weight3
        maze[(i, j)] = inner_dict
    if (weight4 != None):
        inner_dict[(new_i4, new_j4)] = weight4
        maze[(i, j)] = inner_dict
    if (weight5 != None):
        inner_dict[(new_i5, new_j5)] = weight5
        maze[(i, j)] = inner_dict
    if (weight6 != None):
        inner_dict[(new_i6, new_j6)] = weight6
        maze[(i, j)] = inner_dict
    if (weight7 != None):
        inner_dict[(new_i7, new_j7)] = weight7
        maze[(i, j)] = inner_dict
    if (weight8 != None):
        inner_dict[(new_i8, new_j8)] = weight8
        maze[(i, j)] = inner_dict


def dijkstra(maze, start, goal):
    dist_from_start = {}
    parent_node = {}
    explored_path = []
    Allnodes = maze
    infinity = 1000000000
    shortest_path = []
    for node in Allnodes:
        dist_from_start[node] = infinity
    dist_from_start[start] = 0
    flag = 0

    while (Allnodes and (flag != 1)):
        minNode = None
        for node in Allnodes:
            if minNode is None:
                minNode = node
            elif dist_from_start[node] < dist_from_start[minNode]:
                minNode = node
                x = minNode[0]
                y = minNode[1]
                v = goal[0]
                w = goal[1]
                if minNode != goal:
                    explored_path.append(minNode)

                else:
                    flag = 1

        for childNode, cost in maze[minNode].items():
            if cost + dist_from_start[minNode] < dist_from_start[childNode]:
                dist_from_start[childNode] = cost + dist_from_start[minNode]
                parent_node[childNode] = minNode
        del Allnodes[minNode]
    #         Allnodes.pop(minNode)
    cv2.destroyAllWindows()
    print("\n")
    print("Time taken for exploring nodes and calculating the shortest path")
    print("--- %s seconds ---" % (time.time() - start_time))
    for path in explored_path:
        x = path[0]
        y = path[1]
        cv2.circle(blank_image, (x, y), 1, (255, 0, 0), -1)
        #         blank_image[y,x] = (0,0,255)
        cv2.namedWindow('T', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('T', 1000, 500)
        cv2.imshow("T", blank_image)
        cv2.waitKey(1)

    currentNode = goal
    while currentNode != start:
        try:
            shortest_path.insert(0, currentNode)
            currentNode = parent_node[currentNode]
        except KeyError:
            print('shortest_path not reachable')
            break
    shortest_path.insert(0, start)
    if dist_from_start[goal] != infinity:
        print("\n")
        print('Shortest distance is ' + str(dist_from_start[goal]))
        print("\n")
        # print('And the shortest_path is ' + str(shortest_path))
        for path in shortest_path:
            x = path[0]
            y = path[1]
            blank_image[y, x] = (0, 255, 0)
            cv2.namedWindow('T', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('T', 1000, 500)
            cv2.imshow("T", blank_image)
            cv2.waitKey(50)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return shortest_path


for x in range(200):
    for y in range(300):
        j = x;
        i = 200 - y
        if obstacle_check(y, x, rad, clearance, 40):
            blank_image[x, y] = (150, 150, 150)
        if obstacle_check(y, x, 0, 0, 0):
            blank_image[x, y] = (255, 255, 255)

print("Enter 1 to select the Goal and Start point by clicking on the image")
print("Enter 2 to manually enter the Goal and Start Node")
i = input("Enter your choice: ")
i = int(i)

if (i == 1):
    m = 0
    a = []


    def draw_circle(event, x, y, flags, param):
        global m
        global mouseX, mouseY
        if event == cv2.EVENT_FLAG_LBUTTON:
            cv2.circle(blank_image, (x, y), 5, (255, 0, 0), -1)
            a.append(x)
            a.append(y)
            mouseX, mouseY = x, y
            if len(a) > 2:
                cv2.circle(blank_image, (a[2], a[3]), 5, (255, 0, 0), -1)
            print("coordinates of the start and goal node = ")
            print(mouseX, 200 - mouseY)
            m = m + 1


    cv2.namedWindow('image')
    cv2.setMouseCallback('image', draw_circle)

    while (1):
        cv2.imshow('image', blank_image)
        k = cv2.waitKey(20) & 0xFF
        if k == 27 or m == 2:
            cv2.waitKey(1000)
            cv2.destroyAllWindows()
            break
    cv2.circle(blank_image, (a[2], a[3]), 2, (255, 0, 0), -1)
    w = a[0]
    x = a[1]
    y = a[2]
    z = a[3]
    c2 = 40
    if obstacle_check(w, x, rad, clearance, c2):
        print(" Start point - Obstacles detected or the points are out of the maze")
        exit()
    elif obstacle_check(y, z, rad, clearance, c2):
        print(" Goal point - Obstacles detected or the points are out of the maze")
        exit()
    else:
        print("\n")
        print("***********Wait till the path gets generated - max wait time -180 seconds**********")
        for i in range(width):
            for j in range(height):
                inner_dict = {}
                function(i, j, rad, clearance, c2)
        start_time = time.time()
        short_path = dijkstra(maze, (w, x), (y, z))

if (i == 2):
    w = input("Enter x coordinates for the Start point : ")
    x = input("Enter y coordinates for the Start point : ")
    y = input("Enter x coordinates for the Goal point : ")
    z = input("Enter x coordinates for the Goal point : ")

    w = int(w)
    x = int(x)
    x = 200 - x
    y = int(y)
    z = int(z)
    z = 200 - z

    c2 = 40
    if obstacle_check(w, x, rad, clearance, c2):
        print(" Start point - Obstacles detected or the points are out of the maze")
        exit()
    elif obstacle_check(y, z, rad, clearance, c2):
        print(" Goal point - Obstacles detected or the points are out of the maze")
        exit()
    else:
        print("\n")
        print("***********Wait till the path gets generated - max wait time -120 seconds**********")
        for i in range(width):
            for j in range(height):
                inner_dict = {}
                function(i, j, rad, clearance, c2)
        start_time = time.time()
        short_path = dijkstra(maze, (w, x), (y, z))
        print("--- %s seconds ---" % (time.time() - start_time))