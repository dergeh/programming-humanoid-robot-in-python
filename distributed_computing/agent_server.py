'''In this file you need to implement remote procedure call (RPC) server

* There are different RPC libraries for python, such as xmlrpclib, json-rpc. You are free to choose.
* The following functions have to be implemented and exported:
 * get_angle
 * set_angle
 * get_posture
 * execute_keyframes
 * get_transform
 * set_transform
* You can test RPC server with ipython before implementing agent_client.py
'''

# add PYTHONPATH
import os
import sys
import time
sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'kinematics'))

from inverse_kinematics import InverseKinematicsAgent
#from jsonrpcserver import methods
from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple

from jsonrpc import JSONRPCResponseManager, dispatcher

class ServerAgent(InverseKinematicsAgent):
    '''ServerAgent provides RPC service

    '''

    

    @Request.application
    def application(self, request):
        # expose methods in the dispatcher
        dispatcher["get_angle"]=self.get_angle
        dispatcher["set_angle"]=self.set_angle
        dispatcher["get_posture"]=self.get_posture
        dispatcher["execute_keyframes"]=self.execute_keyframes
        dispatcher["get_transform"]=self.get_transform
        dispatcher["set_transform"]=self.set_transform
        dispatcher["ping"]= self.ping
        response = JSONRPCResponseManager.handle(
            request.data, dispatcher)
        return Response(response.json, mimetype='application/json')

    
    def get_angle(self, joint_name):
        '''get sensor value of given joint'''

        return self.perception.joint[joint_name]

   
    def ping(self, msg):
        return 'pong'+msg

    def set_angle(self, joint_name, angle):
        '''set target angle of joint for PID controller
        '''
        self.target_joints[joint_name]=angle
        
    def get_posture(self):
        '''return current posture of robot'''
        return self.posture

    def execute_keyframes(self, keyframes):
        '''excute keyframes, note this function is blocking call,
        e.g. return until keyframes are executed
        '''
        self.keyframes=keyframes
        while (self.t0!=-1):
            time.sleep(0.1)
        return

    def get_transform(self, name):
        '''get transform with given name
        '''
        return self.transforms[name]

    def set_transform(self, effector_name, transform):
        '''solve the inverse kinematics and control joints use the results
        '''
        self.set_transforms(effector_name,transform)


if __name__ == '__main__':
    agent = ServerAgent()
    #start server
    run_simple('localhost', 4000, agent.application)
    agent.run()

