
# transform.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Jongdeog Lee (jlee700@illinois.edu) on 09/12/2018

"""
This file contains the transform function that converts the robot arm map
to the maze.
"""
import copy
from arm import Arm
from maze import Maze
from search import *
from geometry import *
from const import *
from util import *

def transformToMaze(arm, goals, obstacles, window, granularity):
    """This function transforms the given 2D map to the maze in MP1.

        Args:
            arm (Arm): arm instance
            goals (list): [(x, y, r)] of goals
            obstacles (list): [(x, y, r)] of obstacles
            window (tuple): (width, height) of the window
            granularity (int): unit of increasing/decreasing degree for angles

        Return:
            Maze: the maze instance generated based on input arguments.

    """
    start_tmp = arm.getArmAngle()               #alpha beta
    armLimit = arm.getArmLimit()            #[(min,max), (min,max)]




    alpha_max = armLimit[0][1]
    alpha_min = armLimit[0][0]
    beta_max = armLimit[1][1]
    beta_min = armLimit[1][0]

    num_rows = int((alpha_max - alpha_min)/granularity) + 1
    num_cols = int((beta_max - beta_min)/granularity) + 1
    #print(num_rows, num_cols)

    map = []
    col= []
    for x in range(num_rows):
        col=[]
        for y in range(num_cols):
            col.append(SPACE_CHAR)
        map.append(col)

    theta_x = alpha_min
    theta_y = beta_min
    offsets = (theta_x,theta_y)

    start = angleToIdx(start_tmp,offsets,granularity)
    alpha_start = start[0]
    beta_start = start[1]
    start = idxToAngle(start,offsets,granularity)
    alpha_start = start[0]
    beta_start = start[1]

    while theta_x <= alpha_max:
        #print("theta_x:", theta_x)
        while theta_y <= beta_max:
            #print("theta_y:",theta_y)
            armAngle = (theta_x,theta_y)
            arm.setArmAngle(armAngle)

            coordinate = angleToIdx(armAngle,offsets,granularity)
            # if (doesArmTipTouchGoals(arm.getEnd(),goals)):
            #     print True
            print(coordinate[0]+1,coordinate[1]+1,doesArmTouchObjects(arm.getArmPosDist(), goals, True),doesArmTouchObjects(arm.getArmPosDist(), obstacles, False),doesArmTipTouchGoals(arm.getEnd(),goals))

            if theta_x == alpha_start and theta_y == beta_start:
                map[coordinate[0]][coordinate[1]] = START_CHAR
            elif doesArmTouchObjects(arm.getArmPosDist(), obstacles, False) and not doesArmTipTouchGoals(arm.getEnd(),goals):
                map[coordinate[0]][coordinate[1]] = WALL_CHAR
            elif doesArmTouchObjects(arm.getArmPosDist(), goals, True) and doesArmTipTouchGoals(arm.getEnd(),goals):
                map[coordinate[0]][coordinate[1]] = OBJECTIVE_CHAR
            elif not isArmWithinWindow(arm.getArmPos(),window):
                map[coordinate[0]][coordinate[1]] = WALL_CHAR
            # else:
            #     map[coordinate[0]][coordinate[1]] = SPACE_CHAR
            theta_y +=granularity

        theta_y = beta_min
        theta_x +=granularity
    #print(offsets)
    #print(alpha_start,beta_start)
    #print("outof loop")
    maze = Maze(map,offsets,granularity)
    #print("done")
    return maze
