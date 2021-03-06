#!/usr/bin/env python
from __future__ import print_function
import roslib
roslib.load_manifest('faa_avi_writer')
import rospy

from faa_msg_and_srv.srv import RecordingCmd


def recording_cmd_proxy(namespace,command,filename,frame_rate):
    srv = '{0}/recording_cmd'.format(namespace)
    proxy = rospy.ServiceProxy(srv,RecordingCmd)
    try:
        resp = proxy(command,filename,frame_rate)
        flag = resp.flag
    except rospy.ServiceException, e:
        flag = False
    return flag

def start_recording(namespace,filename,frame_rate):
    return recording_cmd_proxy(namespace,'start',filename,frame_rate)

def stop_recording(namespace,filename,frame_rate):
    return recording_cmd_proxy(namespace,'stop',filename,frame_rate)


# -----------------------------------------------------------------------------
if __name__ == '__main__':
    import os
    import os.path
    import time
    import faa_introspection


    if 0:
        node = '/maze/image_stitched_labeled/avi_writer'
        filename = os.path.join(os.environ['HOME'], 'test.avi')
        frame_rate = 15.0
        print('starting recording')
        start_recording(node,filename,frame_rate)
        time.sleep(5.0)
        print('stopping recording')
        stop_recording(node,filename,frame_rate)

    if 1:
        # -----------------------------------------------------------------
        # Really need to set different frame rates for the different nodes.
        # -----------------------------------------------------------------
        frame_rate = 15.0
        sleep_dt = 60.0
        avi_writer_nodes = faa_introspection.get_avi_writer_nodes()
        node_filename_list = []
        for node in avi_writer_nodes:
            node_split = node.split('/')
            filename = '{0}.avi'.format('_'.join(node_split[1:]))
            filename = os.path.join(os.environ['HOME'], filename)
            node_filename_list.append((node,filename))

        print('starting recordings: ')
        for node, filename in node_filename_list:
            print('  ', node)
            start_recording(node,filename,frame_rate)
        time.sleep(sleep_dt)

        print()
        print('stopping recordings: ')
        for node, filename in node_filename_list:
            print('  ', node)
            stop_recording(node,filename,frame_rate)







