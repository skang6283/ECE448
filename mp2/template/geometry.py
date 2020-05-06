# geometry.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Jongdeog Lee (jlee700@illinois.edu) on 09/12/2018

"""
This file contains geometry functions that relate with Part1 in MP2.
"""

import math
import numpy as np
from const import *

def computeCoordinate(start, length, angle):
    """Compute the end cooridinate based on the given start position, length and angle.

        Args:
            start (tuple): base of the arm link. (x-coordinate, y-coordinate)
            length (int): length of the arm link
            angle (int): degree of the arm link from x-axis to couter-clockwise

        Return:
            End position (int,int):of the arm link, (x-coordinate, y-coordinate)
    """


    x = int(math.cos(math.radians(angle))*length)
    y = int(math.sin(math.radians(angle))*length)

    return (start[0]+x, start[1]-y)

def doesArmTouchObjects(armPosDist, objects, isGoal=False):
    """Determine whether the given arm links touch any obstacle or goal

        Args:
            armPosDist (list): start and end position and padding distance of all arm links [(start, end, distance)]
            objects (list): x-, y- coordinate and radius of object (obstacles or goals) [(x, y, r)]
            isGoal (bool): True if the object is a goal and False if the object is an obstacle.
                           When the object is an obstacle, consider padding distance.
                           When the object is a goal, no need to consider padding distance.
        Return:
            True if touched. False if not.
    """


    for object in objects:
        goalx = object[0]   #goal x
        goaly = object[1]   #goal y

        r = object[2]       #goal r

        for link in armPosDist:

            start = link[0]     #start
            #print("start",start)

            end = link[1]       #end
            #print("end",end)

            if isGoal:
                padding = 0   #padding dist
            else:
                padding = link[2]

            r =object[2] + padding
            startx = start[0] - goalx   #shift startx
            starty = goaly - start[1]   #shift starty

            endx = end[0] - goalx       #shift endx
            endy = goaly - end[1]       #shift endy

            dx = endx - startx
            dy = endy - starty
            dr = math.sqrt(dx**2+dy**2)         #link length
            D = startx*endy - endx*starty

            discriminant = r**2 * dr**2 - D**2
            start_to_goal = math.sqrt(startx**2 + starty**2)
            tip_to_goal = math.sqrt(endx**2 + endy**2)


            endv_x = endx - startx
            endv_y = starty - endy

            goalv_x = 0 - startx
            goalv_y = starty - 0

            dot_product = endv_x * goalv_x + endv_y * goalv_y

            # print(dot_product)

            if discriminant >= 0 and start_to_goal <= dr and dot_product >= 0 :
                return True
            if discriminant >= 0 and (tip_to_goal <= r or start_to_goal <=r) :
                return True


    return False

def doesArmTipTouchGoals(armEnd, goals):
    """Determine whether the given arm tip touch goals

        Args:
            armEnd (tuple): the arm tip position, (x-coordinate, y-coordinate)
            goals (list): x-, y- coordinate and radius of goals [(x, y, r)]. There can be more than one goal.
        Return:
            True if arm tick touches any goal. False if not.
    """
    for goal in goals:
        dist = math.sqrt((goal[0]-armEnd[0])*(goal[0]-armEnd[0]) + (goal[1]-armEnd[1])*(goal[1]-armEnd[1]))
        if dist <= goal[2]:
            return True
    return False


def isArmWithinWindow(armPos, window):
    """Determine whether the given arm stays in the window

        Args:
            armPos (list): start and end positions of all arm links [(start, end)]
            window (tuple): (width, height) of the window

        Return:
            True if all parts are in the window. False if not.
    """
    for arm in armPos:
        start = arm[0]
        end = arm[1]
        if start[0] > window[0]:
            return False
        elif start[1] > window[1]:
            return False
        elif end[0] > window[0]:
            return False
        elif end[1] > window[1]:
            return False
        elif start[0] < 0:
            return False
        elif start[1] < 0:
            return False
        elif end[0] < 0:
            return False
        elif end[1] < 0:
            return False


    return True


if __name__ == '__main__':
    computeCoordinateParameters = [((150, 190),100,20), ((150, 190),100,40), ((150, 190),100,60), ((150, 190),100,160)]
    resultComputeCoordinate = [(243, 156), (226, 126), (200, 104), (57, 156)]
    testRestuls = [computeCoordinate(start, length, angle) for start, length, angle in computeCoordinateParameters]
    assert testRestuls == resultComputeCoordinate

    testArmPosDists = [((100,100), (135, 110), 4), ((135, 110), (150, 150), 5)]
    testObstacles = [[(120, 100, 5)], [(110, 110, 20)], [(160, 160, 5)], [(130, 105, 10)]]
    resultDoesArmTouchObjects = [
        True, True, False, True, False, True, False, True,
        False, True, False, True, False, False, False, True
    ]

    testResults = []
    for testArmPosDist in testArmPosDists:
        for testObstacle in testObstacles:
            testResults.append(doesArmTouchObjects([testArmPosDist], testObstacle))
            # print(testObstacle)
            # print(testArmPosDist)
            # print(doesArmTouchObjects([testArmPosDist], testObstacle))

    print("\n")
    for testArmPosDist in testArmPosDists:
        for testObstacle in testObstacles:
            testResults.append(doesArmTouchObjects([testArmPosDist], testObstacle, isGoal=True))
            # print(testObstacle)
            # print(testArmPosDist)
            # print(doesArmTouchObjects([testArmPosDist], testObstacle, isGoal=True))

    assert resultDoesArmTouchObjects == testResults

    testArmEnds = [(100, 100), (95, 95), (90, 90)]
    testGoal = [(100, 100, 10)]
    resultDoesArmTouchGoals = [True, True, False]

    testResults = [doesArmTipTouchGoals(testArmEnd, testGoal) for testArmEnd in testArmEnds]
    assert resultDoesArmTouchGoals == testResults

    testArmPoss = [((100,100), (135, 110)), ((135, 110), (150, 150))]
    testWindows = [(160, 130), (130, 170), (200, 200)]
    resultIsArmWithinWindow = [True, False, True, False, False, True]
    testResults = []
    for testArmPos in testArmPoss:
        for testWindow in testWindows:
            testResults.append(isArmWithinWindow([testArmPos], testWindow))
    assert resultIsArmWithinWindow == testResults

    print("Test passed\n")
