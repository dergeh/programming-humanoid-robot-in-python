'''In this exercise you need to implement inverse kinematics for NAO's legs

* Tasks:
    1. solve inverse kinematics for NAO's legs by using analytical or numerical method.
       You may need documentation of NAO's leg:
       http://doc.aldebaran.com/2-1/family/nao_h21/joints_h21.html
       http://doc.aldebaran.com/2-1/family/nao_h21/links_h21.html
    2. use the results of inverse kinematics to control NAO's legs (in InverseKinematicsAgent.set_transforms)
       and test your inverse kinematics implementation.
'''


from forward_kinematics import ForwardKinematicsAgent
from numpy.matlib import identity
from scipy.optimize import fmin
import numpy as np
from numpy import sin, cos, pi, matrix, random, linalg, asarray
from math import atan2



class InverseKinematicsAgent(ForwardKinematicsAgent):
    def inverse_kinematics(self, effector_name, transform):
        '''solve the inverse kinematics

        :param str effector_name: name of end effector, e.g. LLeg, RLeg
        :param transform: 4x4 transform matrix
        :return: list of joint angles
        '''
        joint_angles = []
        # YOUR CODE HERE
        chain= self.chains[effector_name]
        N= len(chain)-1
        T0=self.local_trans(0,0,0,0)
        def error_func(theta, target):
                self.forward_kinematics(T0, l, theta)
                print(self.transforms)
                Te = np.matrix([from_trans(Ts[-1])]).T
                e = target - Te
                return linalg.norm(e)

        theta = random.random(N)

        x_e, y_e, z_e, theta_e= from_trans(transform)
        target = matrix([[x_e, y_e, z_e, theta_e]]).T
        func = lambda t: error_func(t, target)
        print( fmin(func, theta))

        return joint_angles

    def set_transforms(self, effector_name, transform):
        '''solve the inverse kinematics and control joints use the results
        '''
        # YOUR CODE HERE
        joint_angles=self.inverse_kinematics(effector_name,transform)
        print(joint_angles)
        self.keyframes = ([], [], [])  # the result joint angles have to fill in
    # brauch noch fallunterscheidung x y z
    def from_trans(m):
        '''get x, y, z, theta from transform matrix'''
        return [m[0, -1], m[1, -1],m[2, -1], atan2(m[1, 0], m[0, 0])]

if __name__ == '__main__':
    agent = InverseKinematicsAgent()
    # test inverse kinematics
    T = identity(4)
    T[-1, 1] = 0.05
    T[-1, 2] = 0.26
    print(T)
    agent.set_transforms('LLeg', T)
    agent.run()
