'''In this exercise you need to implement an angle interploation function which makes NAO executes keyframe motion

* Tasks:
    1. complete the code in `AngleInterpolationAgent.angle_interpolation`,
       you are free to use splines interploation or Bezier interploation,
       but the keyframes provided are for Bezier curves, you can simply ignore some data for splines interploation,
       please refer data format below for details.
    2. try different keyframes from `keyframes` folder

* Keyframe data format:
    keyframe := (names, times, keys)
    names := [str, ...]  # list of joint names
    times := [[float, float, ...], [float, float, ...], ...]
    # times is a matrix of floats: Each line corresponding to a joint, and column element to a key.
    keys := [[float, [int, float, float], [int, float, float]], ...]
    # keys is a list of angles in radians or an array of arrays each containing [float angle, Handle1, Handle2],
    # where Handle is [int InterpolationType, float dTime, float dAngle] describing the handle offsets relative
    # to the angle and time of the point. The first Bezier param describes the handle that controls the curve
    # preceding the point, the second describes the curve following the point.
'''


from pid import PIDAgent
from keyframes import hello, leftBellyToStand, wipe_forehead, leftBackToStand


class AngleInterpolationAgent(PIDAgent):
    def __init__(self, simspark_ip='localhost',
                 simspark_port=3100,
                 teamname='DAInamite',
                 player_id=0,
                 sync_mode=True):
        super(AngleInterpolationAgent, self).__init__(simspark_ip, simspark_port, teamname, player_id, sync_mode)
        self.keyframes = ([], [], [])
        self.t0=0 # starting time of the agent gotten from simspark

    def think(self, perception):
        target_joints = self.angle_interpolation(self.keyframes, perception)
        self.target_joints.update(target_joints)
        return super(AngleInterpolationAgent, self).think(perception)

    def angle_interpolation(self, keyframes, perception):
        target_joints = {}
        names, times, keys = keyframes
        
        # iterates over the joint names to interpolate the value for the given joint
        for i in range(0,len(names)):
                time_index=0
                #time since the agent started
                time_rel=self.perception.time-self.t0

                #bool for termination if time limit is reached
                end=False

                # iterates over all times to determine timeframe we are in
                for it in range (0, len(times[i])):
                    
                    if times[i][it] > time_rel:
                        time_index=it
                        break
                    if it==len(times[i])-1:
                        target_joints[names[i]]=keys[i][it][0]
                        end=True
                # if end of times array is reached robot halts at last given position
                if end:
                    continue
                # if index 0 start with 0,0 as position and 0.3333,0 as control point 1 to avoid index faults
                if time_index==0:
                    p0=(0,0)
                    p1=(0.3333,0)

                # else get pervious position
                else:
                    p0=(0,keys[i][time_index-1][0])
                    p1=(keys[i][time_index-1][2][1],keys[i][time_index-1][2][2]) # control point 1 
               
                # set point for bezier interpolation
                p2=(1+keys[i][time_index][1][1],keys[i][time_index][1][2]) # control point 2
                p3=(1,keys[i][time_index][0]) # destination

                # normalize time so t gets between 0 and 1
                lower=0
                if time_index!=0:
                    lower=times[i][time_index-1]
                upper=times[i][time_index]
                t=(time_rel-lower)/(upper-lower)

                # cubic bezier
                n_p0=tuple(x*((1-t)**3) for x in p0)
                n_p1=tuple(x*3*t*((1-t)**2) for x in p1 )
                n_p2=tuple(x*3*(1-t)*(t**2) for x in p2) 
                n_p3=tuple(x*(t**3) for x in p3 )
                b=(n_p0[0]+n_p1[0]+n_p2[0]+n_p3[0], n_p0[1]+n_p1[1]+n_p2[1]+n_p3[1])  
                #if names[i]=="HeadYaw": #for testing the bezier curves writes the interpolated points to a csv file 
                #    b_t=(b[0]*(upper-lower)+lower)
                #    test=open("yawTest.csv", "a")
                #    test.write("%f,%f\n"%(b_t,b[1]))
                #add interpolated value to target_joint dicct
                target_joints[names[i]]=b[1]
                
       
        return target_joints

if __name__ == '__main__':
    agent = AngleInterpolationAgent()
    agent.keyframes = hello() # CHANGE DIFFERENT KEYFRAMES
    agent.t0=agent.perception.time # set starting time to get relative time in interpolation
    agent.run()
