'''In this exercise you need to put all code together to make the robot be able to stand up by its own.

* Task:
    complete the `StandingUpAgent.standing_up` function, e.g. call keyframe motion corresponds to current posture

'''


from recognize_posture import PostureRecognitionAgent
from keyframes import hello, leftBellyToStand, rightBackToStand, leftBackToStand


class StandingUpAgent(PostureRecognitionAgent):
    def think(self, perception):
        self.standing_up()
        return super(StandingUpAgent, self).think(perception)

    def standing_up(self):
        posture = self.posture
        # only update keyframe if the agent is in on mode and no other keyframe is being executed
        if self.is_on and self.t0==-1 :
            self.posture = self.recognize_posture(self.perception) # regonize posture
            # select keyframe based on the posture
            if posture=='Belly':
                self.keyframes=leftBellyToStand()
            elif posture=='Back' or posture=='Left' or posture=='HeadBack':
                self.keyframes=leftBackToStand()
            elif posture=='Right' or posture=='Sit':
                self.keyframes=rightBackToStand()
            elif posture=='Stand' or posture =='StandInit':
                self.keyframes=([],[],[])



class TestStandingUpAgent(StandingUpAgent):
    '''this agent turns off all motor to falls down in fixed cycles
    '''
    def __init__(self, simspark_ip='localhost',
                 simspark_port=3100,
                 teamname='DAInamite',
                 player_id=0,
                 sync_mode=True):
        super(TestStandingUpAgent, self).__init__(simspark_ip, simspark_port, teamname, player_id, sync_mode)
        self.stiffness_on_off_time = 0
        self.stiffness_on_cycle = 10  # in seconds
        self.stiffness_off_cycle = 3  # in seconds

    def think(self, perception):
        action = super(TestStandingUpAgent, self).think(perception)
        time_now = perception.time
        if time_now - self.stiffness_on_off_time < self.stiffness_off_cycle:
            action.stiffness = {j: 0 for j in self.joint_names}  # turn off joints
            self.is_on=False # set agent to inactive
        else:
            action.stiffness = {j: 1 for j in self.joint_names}  # turn on joints
            self.is_on=True # set agent back to active mode
        if time_now - self.stiffness_on_off_time > self.stiffness_on_cycle + self.stiffness_off_cycle:
            self.stiffness_on_off_time = time_now

        return action


if __name__ == '__main__':
    agent = TestStandingUpAgent()
    agent.run()
