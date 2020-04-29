# -*- encoding: UTF-8 -*-

import math
import argparse
from naoqi import ALProxy

class RouteGenerator:


    fieldCoordinates=[]
    def __init__(self, fieldCoordinates):
        self.fieldCoordinates=fieldCoordinates

    # pre definded routes to certain points on the field 
    routes={1:[3,1],2:[3,2],3:[3],4:[3,4],5:[3,5],6:[3,5,6],7:[3,5,7],8:[3,5,8],9:[3,5,9],10:[3,5,9,10], 11:[3,5,9,11],12:[3,1,13,12],13:[3,1,13],14:[3,1,14],15:[3,1,15],16:[3,1,16]}
    
    #mapping function to add theta value to tuple to fit api requirement
    def add_theta(self,point):
            w_point=point
            w_point.append(0)
            return w_point

    # takes a target point on the field and generates a route based on the given model 
    def generateRoute(self,target):
        #get the control point chain to the target
        abstract_route=self.routes[target]
        raw_route=[]
        #map the chain to coordinates
        for i in abstract_route:
            raw_route.append(self.fieldCoordinates[i])
        start=[raw_route[0][1],raw_route[0][0]]
        concrete_route=[start]

        # map the coordinates to relative coordinates based on the previous control point
        for i in range(1,len(raw_route)):
            dx=raw_route[i][0]-raw_route[i-1][0]
            dy=raw_route[i][1]-raw_route[i-1][1]
            concrete_route.append([dy,dx])
        
        # add theta value to all tuples and return them
        return map(self.add_theta,concrete_route)

    # same as the route generation but with an inversed control point chain
    def generateHomeRoute(self,target):
        abstract_route=self.routes[target][::-1]
        abstract_route.append(0)
        raw_route=[]
        for i in abstract_route:
            raw_route.append(self.fieldCoordinates[i])
        start=[raw_route[0][1],raw_route[0][0]]
        concrete_route=[start]
        for i in range(1,len(raw_route)):
            dx=raw_route[i][0]-raw_route[i-1][0]
            dy=raw_route[i][1]-raw_route[i-1][1]
            concrete_route.append([dy,dx])
        

        return map(self.add_theta,concrete_route)
        


def main(robotIP, PORT=9559, target):
    motionProxy  = ALProxy("ALMotion", robotIP, PORT)
    postureProxy = ALProxy("ALRobotPosture", robotIP, PORT)

    # Wake up robot
    motionProxy.wakeUp()

    # Send robot to Pose Init
    postureProxy.goToPosture("StandInit", 0.5)

    #model the dummy playing field control points
    field=[]
    field.append([0,0])
    field.append([-2,1.5])
    field.append([-1,1.5])
    field.append([0,1.5])
    field.append([1,1.5])
    field.append([2,1.5])
    field.append([2,2.5])
    field.append([2,3.5])
    field.append([2,4.5])
    field.append([2,5.5])
    field.append([1,5.5])
    field.append([0,5.5])
    field.append([-1,5.5])
    field.append([-2,5.5])
    field.append([-2,4.5])
    field.append([-2,3.5])
    field.append([-2,2.5])
    field.append([0,3.5])

    #spot where the robot should move to based on the game logic module
    desired_spot=target

    # initialize the generator with the coordinates
    rGenerator=RouteGenerator(field)

    #generate the rout to the desired field
    control_points=rGenerator.generateRoute(desired_spot)

    #pickup motion would happen here 

    # disable the arms so the robot doesnt drop the object while walking
    motionProxy.setMoveArmsEnabled(False, False)

    # move to desired field
    motionProxy.moveTo(control_points) 

    # enable armrs to drop the object
    motionProxy.setMoveArmsEnabled(True, True) 

    # drop motion would go here

    #generate the rout back to the home position
    control_points=rGenerator.generateHomeRoute(desired_spot)

    #walk home 
    motionProxy.moveTo(control_points)


    # Go to rest position and await new event
    motionProxy.rest()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="127.0.0.1",
                        help="Robot ip address")
    parser.add_argument("--port", type=int, default=9559,
                        help="Robot port number")
    parser.add_argument("--target", type=int, default=1, help="target position between 1 and 16 where the robot should drop the object")
    args = parser.parse_args()
    main(args.ip, args.port, args.target)


        