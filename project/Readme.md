## Project assingment
====================

This is Part of the Group Assingment of Group A. The Goal of the Project was to make a Robot play Tic Tak Toe against a human.

The python script presented here is an approach to the movement control of the Robot. 
### Requirements

This project uses the naoqi api make sure you have the module installed on your computer. 

### Usage

Make sure you have a NAO running or a simulted NAO somewhere. Then just execute

 ``` python movement.py --port=9559 --ip="127.0.0.1" --target=1```

 IP and port must be set to fit your robot configuration.
 After executing the script the robot should start moving towards the point given in the commandline and move back to where he came from.


 
## Problems during the development

The plan for the project was to animate a pickup motion for the robot but unfortunaly i wasnt able to do so. I spend a lot of time trying to setup a development environment which i needed a simulated robot for. The presented simspark simulation tool didnt fit my requirements since I wasnt able to connect to the naoqi api. After a lot of searching and trying out different outdated simulationtool i was able to install the up to date version of [webots](https://cyberbotics.com/) but the demo world for the NAO didnt have support for the naoqi api. After many more hours and tryring different solutions presented on the internet i found [naoqisim](https://github.com/cyberbotics/naoqisim) which is a world for  webots where the naoqi api works. Unfortunatly even tho it is better than every other simulation i found its still not stable at all. 

For the pickup motion I would normaly push the real NAO in a position where i want it to be and read the joint positions through the api to modulate a motion in the programm. Due to not being able to get a hands on the robot i tried to do somthing similar in webots. After a lot of tries to get the robot into the desired position i capitulated. Thats why I wasnt able to archive a pickup or drop motin in the program i commented the part where it should have gone.

The pcikup part was impossible to do so i moved onto the movement part and did the best i could but even there the simulation is so unstable, that i wasnt able to really test the movements. I noticed that the walking quality of the robot depended on the camrea angle i used to observe him which i think shouldnt be the case. So I'm not sure if the code i wrote will actually work in the real world.

Lastly the image processing part could not be integraded also due to simulation issues. The cameras of the robot seem to work but i was unable to retrieve pictures from the simulation so i only worked with dummy values.

I'm writing all this to show that i actually did alot more work than the little dumb movement program i wrote put unforutnatly none of my efforts found their way into the final assingment.

