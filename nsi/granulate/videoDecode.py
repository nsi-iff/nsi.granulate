#! /bin/env python
import os
import sys
import StringIO
import gtk
import pygst
import gst
from PIL import Image

class VideoDecode(object):
    '''
    Extracts frames from a video file.  
    '''
    def __init__(self, videoFile):
        '''
        videoFile is the media input file
        '''
        self._create_pipeline(videoFile)
        self._configure_message_handling()
    
    def _create_pipeline(self, videoFile):
        '''
        Creates a pipeline in the form:
        -------------------------------------------
        | filesrc | decodebin | jpegenc | appsink |
        -------------------------------------------   
        '''
        self.pipeline = gst.parse_launch(('filesrc location=%s ! decodebin ! videorate ! video/x-raw-yuv,framerate=30/1 ! jpegenc ! appsink name=sink max-buffers=100 sync=False')%videoFile)
        self.pipeline.set_state(gst.STATE_PLAYING)
        self.sink = self.pipeline.get_by_name('sink')
        
    def _configure_message_handling(self):
        '''
        Registers callback for receiving bus messages
        ''' 
        bus = self.pipeline.get_bus()
        bus.add_signal_watch()
        bus.connect('message', self._on_message)
    
    def sliceVideoBlock(self, sizeBlock = 1,frameA = None, frameB = None):
        '''
        Runs the extracting
        '''
        listImage = []
        if frameA and frameB:
            listImg.append(frameA)
            listImg.append(frameB)
        frameId = 0
        while frameId < sizeBlock:
            self.sink.set_property('max-buffers',100)
            self.frameBuffer = self.sink.emit('pull-buffer')           
            if self.frameBuffer is None:
                break    
            frame = Image.open(StringIO.StringIO(self.frameBuffer.data))
            listImage.append(frame)
            frameId += 1
        return listImage        
    
    def _on_message(self, bus, message):
        '''
        Callback for message processing
        '''
        if message.type == gst.MESSAGE_EOS:
            self.pipeline.set_state(gst.STATE_NULL)
            gtk.main_quit()
        if message.type == gst.MESSAGE_ERROR:
            err, debug = message.parse_error()
            print "Error: %s" % err, debug
            self.player.set_state(gst.STATE_NULL)
