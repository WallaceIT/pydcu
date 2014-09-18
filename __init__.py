import ueye
import time
from time import sleep
import atb
import logging
import numpy as np
import cv2
import ctypes

class Cam():
    def __init__(self):
        self.dict = {}
        self.name = 'UI154xLE-M'
        self.src_id = 1
        self.serial = '' # not sure we need this
    
class Camera_List(list):
    def __init__(self):
        '''dummy file, we just always use the same first camera. needs to be
changed if there may be more than one camera attached'''
        self.append(Cam())



class Control(dict):
    """
    docstring
    """
    def __init__(self,c):
        for key,val in c.items():
            self[key] = val

        self.name = self['name']
        self.atb_name = self['name']
        self.order = self['order']
        self.value = self['value']
        self.default = self['default']
        self.type  = self['type']
        if self.type == 'menu':
            self.menu = self['menu']
            self.min = None
            self.max = None
            self.step = None
        elif self.type == 'bool':
            self.min = 0
            self.max = 1
            self.step = 1
            self.menu=None
        else:
            self.menu=None
            self.step = self['step']
            self.min = self['min']
            self.max = self['max']

        if 'flags' in self:
            self.flags = self['flags']
        else:
            self.flags = "active"


    def get_val(self):
        return self['value']

    def set_val(self,val):
        self.set(self['name'],val)
        self['value'] = val

class Controls(dict):
    """docstring for Controls"""
    def __init__(self, src_id):
        self.src_id = src_id
        control_dict = self.extract_controls()
        for c in control_dict:
            self[c] = Control(control_dict[c])

    def update_from_device(self):
        update_from_device(self)

    def load_defaults(self):
        for c in self.itervalues():
            c.set_val(c.default)

        
    def extract_controls(self):
        controls = {}        
        device_number = 1
        control_order = 0

        control = {}
        control_name = 'fps'
        control['value'] = 30
        control['default'] = 30
        control["type"] = 'range'
        control["name"] = control_name
        control['atb_name'] = control_name
        control["src"] = device_number
        control["order"] = control_order
        control['step'] = 15
        control['min'] = 1
        control['max'] = 600
        controls[control_name] = control
        control_order += 1


        control = {}
        control_name = 'auto exposure'
        control['value'] = False
        control['default'] = False
        control["type"] = 'bool'
        control["name"] = control_name
        control['atb_name'] = control_name
        control["src"] = device_number
        control["order"] = control_order
        control['step'] = None
        control['min'] = None
        control['max'] = None
        controls[control_name] = control
        control_order += 1

        control = {}
        control_name = 'exposure'
        control['value'] = 99.89
        control['default'] = 99.89
        control["type"] = 'range'
        control["name"] = control_name
        control['atb_name'] = control_name
        control["src"] = device_number
        control["order"] = control_order
        control['step'] = .23
        control['min'] = 0.07
        control['max'] = 99.89
        controls[control_name] = control
        control_order += 1

        control = {}
        control_name = 'gain'
        control['value'] = 0
        control['default'] = 0
        control["type"] = 'range'
        control["name"] = control_name
        control['atb_name'] = control_name
        control["src"] = device_number
        control["order"] = control_order
        control['step'] = 1
        control['min'] = 0
        control['max'] = 100
        controls[control_name] = control
        control_order += 1

        control = {}
        control_name = 'contrast'
        control['value'] = 100
        control['default'] = 100
        control["type"] = 'range'
        control["name"] = control_name
        control['atb_name'] = control_name
        control["src"] = device_number
        control["order"] = control_order
        control['step'] = 5
        control['min'] = 0
        control['max'] = 200
        controls[control_name] = control
        control_order += 1

        control = {}
        control_name = 'auto gain'
        control['value'] = False
        control['default'] = False
        control["type"] = 'bool'
        control["name"] = control_name
        control['atb_name'] = control_name
        control["src"] = device_number
        control["order"] = control_order
        control['step'] = None
        control['min'] = None
        control['max'] = None
        controls[control_name] = control
        control_order += 1
        
        # # camera doesn't support auto focus, so this is just a dummy
        # control_name = 'exposure_auto_priority'
        # control["type"] = 'bool'
        # control["name"] = control_name
        # control["src"] = device_number
        # control["order"] = control_order
        # controls[control_name] = control
        # control_order += 1
        
        return controls




class Camera_Capture(object):
    """docstring for pydcu camera"""
    def __init__(self,cam,size=(640,480),fps=None,timebase=None):
        self.src_id = cam.src_id
        self.serial = cam.serial
        self.name = cam.name
        self.controls = Controls(self.src_id)
        self.timebase = timebase
        self.use_hw_ts = False # revisit, maybe it is supported
                 
        #give camera some time to change settings.
        self.capture = ueye.camera(1)
        self.capture.AllocImageMem(width=size[0],height=size[1],bitpixel=8)
        self.capture.SetImageMem()
        self.capture.SetAOI(x=0, y=0, width=size[0], height=size[1])
        self.capture.SetFrameRate(fps)
        self.capture.SetColorMode()
        self.capture.CaptureVideo()
        self.capture.CopyImageMem()
        self.capture.init_frame = self.capture.data
        self.get_frame = self.capture.read
        self.get_now = time.time() 



    def re_init(self,cam,size=(640,480),fps=30):

        current_size = self.capture.get_size()
        current_fps = self.capture.get_rate()

        self.capture.cleanup()
        self.capture = None
        #recreate the bar with new values
        bar_pos = self.bar._get_position()
        self.bar.destroy()

        self.__init__(cam, current_size, current_fps)


    def re_init_cam_by_src_id(self,requested_id):
        ''' try to re init a camera ''' 
        for cam in Camera_List():
            if cam.src_id == requested_id:
                self.re_init(cam)
                return
        logger.warning("could not reinit capture, src_id not valid anymore")
        return


    def create_atb_bar(self,pos):
        # add uvc camera controls to a separate ATB bar
        size = (200,200)

        self.bar = atb.Bar(name="Camera", label=self.name,
            help="UVC Camera Controls", color=(50,50,50), alpha=100,
            text='light',position=pos,refresh=2., size=size)
        cameras_enum = atb.enum("Capture",dict([(c.name,c.src_id) for c in Camera_List()]) )
        self.bar.add_var("Capture",vtype=cameras_enum,getter=lambda:self.src_id, setter=self.re_init_cam_by_src_id)

        self.bar.add_var('framerate', vtype = atb.enum('framerate',self.capture.rates_menu), getter = lambda:self.capture.current_rate_idx, setter=self.capture.set_rate_idx )
        self.bar.add_var('exposure', vtype=ctypes.c_float, getter = self.capture.get_exposure_time, setter=self.capture.set_exposure_time)
        self.bar.add_var('gain', vtype = ctypes.c_int, getter = self.capture.get_hardware_gain, setter=self.capture.set_hardware_gain)
        self.bar.add_var('contrast', vtype = ctypes.c_int, getter = self.capture.get_contrast, setter=self.capture.set_contrast)
        self.bar.add_var('auto gain', vtype = atb.TW_TYPE_BOOL8, getter = self.capture.getAutoGain, setter=self.capture.setAutoGain )
        self.bar.add_var('auto exposure', vtype = atb.TW_TYPE_BOOL8, getter = self.capture.getAutoExposure, setter=self.capture.setAutoExposure )

        # sorted_controls = [c for c in self.controls.itervalues()]
        # sorted_controls.sort(key=lambda c: c.order)


        # for control in sorted_controls:
        #     name = control.atb_name
        #     if control.type=="bool":
        #         self.bar.add_var(name,vtype=atb.TW_TYPE_BOOL8,getter=control.get_val,setter=control.set_val)
        #     elif control.type=='int':
        #         self.bar.add_var(name,vtype=atb.TW_TYPE_INT32,getter=control.get_val,setter=control.set_val)
        #         self.bar.define(definition='min='+str(control.min),   varname=name)
        #         self.bar.define(definition='max='+str(control.max),   varname=name)
        #         self.bar.define(definition='step='+str(control.step), varname=name)
        #     elif control.type=="menu":
        #         if control.menu is None:
        #             vtype = None
        #         else:
        #             vtype= atb.enum(name,control.menu)
        #         self.bar.add_var(name,vtype=vtype,getter=control.get_val,setter=control.set_val)
        #         if control.menu is None:
        #             self.bar.define(definition='min='+str(control.min),   varname=name)
        #             self.bar.define(definition='max='+str(control.max),   varname=name)
        #             self.bar.define(definition='step='+str(control.step), varname=name)
        #     else:
        #         pass
        #     if control.flags == "inactive":
        #         pass
        #     if control.name == 'exposure_auto_priority':
        #         # the controll should always be off. we set it to 0 on init (see above)
        #         self.bar.define(definition='readonly=1',varname=control.name)

        self.bar.add_button("refresh",self.controls.update_from_device)
        self.bar.add_button("load defaults",self.controls.load_defaults)

        return size

    def close(self):
        self.capture.cleanup()


class CameraCaptureError(Exception):
    """General Exception for this module"""
    def __init__(self, arg):
        super(CameraCaptureError, self).__init__()
        self.arg = arg
