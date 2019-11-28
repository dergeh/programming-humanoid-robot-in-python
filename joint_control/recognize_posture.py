'''In this exercise you need to use the learned classifier to recognize current posture of robot

* Tasks:
    1. load learned classifier in `PostureRecognitionAgent.__init__`
    2. recognize current posture in `PostureRecognitionAgent.recognize_posture`

* Hints:
    Let the robot execute different keyframes, and recognize these postures.

'''


from angle_interpolation import AngleInterpolationAgent
from keyframes import hello
import pickle
import numpy as np


class PostureRecognitionAgent(AngleInterpolationAgent):
    def __init__(self, simspark_ip='localhost',
                 simspark_port=3100,
                 teamname='DAInamite',
                 player_id=0,
                 sync_mode=True):
        super(PostureRecognitionAgent, self).__init__(simspark_ip, simspark_port, teamname, player_id, sync_mode)
        self.posture = 'unknown'
        self.posture_classifier = pickle.load(open('robot_pose.pkl'))  # LOAD YOUR CLASSIFIER
        self.postures=['Stand', 'Frog', 'StandInit', 'Belly', 'HeadBack', 'Left', 'Right', 'Crouch', 'Sit', 'Back', 'Knee'] # list of available poses
        self.is_on=True

    def think(self, perception):
        self.posture = self.recognize_posture(perception)
        return super(PostureRecognitionAgent, self).think(perception)

    def recognize_posture(self, perception):
        posture = 'unknown'
        current_state=[] # current joint state verctor representation
        joints=['LHipYawPitch', 'LHipRoll', 'LHipPitch', 'LKneePitch', 'RHipYawPitch', 'RHipRoll', 'RHipPitch', 'RKneePitch'] # list of joints for the state vector
        for joint in joints:
            current_state.append(perception.joint[joint]) # add joint angle value to vector
        current_state.extend(perception.imu) # add current robot angle to vector
        fmt_state=np.asarray(current_state).reshape(1, -1) # reshape vector to fit classfifier format
        posture=self.posture_classifier.predict(fmt_state) # recognize posture
       
        return self.postures[posture[0]]

if __name__ == '__main__':
    agent = PostureRecognitionAgent()
    agent.keyframes = hello()  # CHANGE DIFFERENT KEYFRAMES
    agent.run()
