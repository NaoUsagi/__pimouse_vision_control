#!/usr/bin/env python
import unittest, rostest
import rosnode, rospy, sys
import time
from pimouse_ros.msg import MotorFreqs
from geometry_msgs.msg import Twist

class VisionTest(unittest.TestCase):
    def get_file_freq(self,lr):
        with open("/dev/rtmotor_raw_"+lr+"0","r") as f:
            s = f.readline().rstrip()
            if s != "":
                return int(s)
            else:
                return 0

    def test_put_freq(self):
        count, l_turn_count,r_turn_count = 0, 0, 0
        start = rospy.Time.now().to_sec()

        prev_lhz, prev_rhz = 0, 0
        while rospy.Time.now().to_sec() - start < 15.0:
            lhz = self.get_file_freq("l")
            rhz = self.get_file_freq("r")

            if lhz == prev_lhz and rhz == prev_rhz:
                continue

            if lhz > rhz: r_turn_count += 1
            if lhz < rhz: l_turn_count += 1

            prev_lhz, prev_rhz = lhz, rhz

            count += 1

        r_turn_rate = 1.0*r_turn_count / count
        l_turn_rate = 1.0*l_turn_count / count

        turn = None
        if r_turn_rate > 0.50 and l_turn_rate < 0.1: turn = "right"
        if l_turn_rate > 0.50 and r_turn_rate < 0.1: turn = "left"
        
        self.assertFalse(turn is None, "direction is not fixed. l:" + str(l_turn_rate) + " r:" + str(r_turn_rate))
        self.assertEqual(sys.argv[1], turn, "wrong direction. l: " + str(l_turn_rate) + " r:" + str(r_turn_rate))

if __name__ == '__main__':
    rospy.init_node('travis_test_face_to_face')
    rostest.rosrun('pimouse_visual_control','travis_test_face_to_face', VisionTest)
