#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

# <rtc-template block="description">
"""
 @file facedetection.py
 @brief ModuleDescription
 @date $Date$


"""
# </rtc-template>

import sys
import time
sys.path.append(".")
import cv2

# Import RTM module
import RTC
import OpenRTM_aist

import facedetection_idl

# Import Service implementation class
# <rtc-template block="service_impl">
from facedetection_idl_example import *

# Madiapipe
import cv2
import numpy
import numpy as np
import pyrealsense2 as rs
import mediapipe as mp
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils
DUR =3
DISTANCE_MIN =10
DISTANCE_MAX = 100

# </rtc-template>

# Import Service stub modules
# <rtc-template block="consumer_import">
# </rtc-template>


# This module's spesification
# <rtc-template block="module_spec">
facedetection_spec = ["implementation_id", "facedetection", 
         "type_name",         "facedetection", 
         "description",       "ModuleDescription", 
         "version",           "1.0.0", 
         "vendor",            "VenderName", 
         "category",          "Category", 
         "activity_type",     "STATIC", 
         "max_instance",      "1", 
         "language",          "Python", 
         "lang_type",         "SCRIPT",
         ""]
# </rtc-template>

# <rtc-template block="component_description">
##
# @class facedetection
# @brief ModuleDescription
# 
# 
# </rtc-template>
class facedetection(OpenRTM_aist.DataFlowComponentBase):
	
    ##
    # @brief constructor
    # @param manager Maneger Object
    # 
    def __init__(self, manager):
        OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

        self._d_detection = OpenRTM_aist.instantiateDataType(RTC.CameraImage)
        """
        """
        self._detectionIn = OpenRTM_aist.InPort("detection", self._d_detection)
        self._d_distance = OpenRTM_aist.instantiateDataType(RTC.TimedFloat)
        """
        """
        self._distanceIn = OpenRTM_aist.InPort("distance", self._d_distance)
        self._d_controlesota = OpenRTM_aist.instantiateDataType(RTC.TimedString)
        """
        """
        self._controlesotaOut = OpenRTM_aist.OutPort("controlesota", self._d_controlesota)

        """
        """
        self._facedetectionconsumerPort = OpenRTM_aist.CorbaPort("facedetectionconsumer")

        """
        """
        self._libfacedetectionprovider = facedetectiondata_i()
		


        # initialize of configuration-data.
        # <rtc-template block="init_conf_param">
		
        # </rtc-template>


		 
    ##
    #
    # The initialize action (on CREATED->ALIVE transition)
    # 
    # @return RTC::ReturnCode_t
    # 
    #
    def onInitialize(self):
        # Bind variables and configuration variable
		
        # Set InPort buffers
        self.addInPort("detection",self._detectionIn)
        self.addInPort("distance",self._distanceIn)
		
        # Set OutPort buffers
        self.addOutPort("controlesota",self._controlesotaOut)
		
        # Set service provider to Ports
        self._facedetectionconsumerPort.registerProvider("facedetectiondata", "Library::facedetectiondata", self._libfacedetectionprovider)
		
        # Set service consumers to Ports
		
        # Set CORBA Service Ports
        self.addPort(self._facedetectionconsumerPort)
		
        return RTC.RTC_OK
	
    ###
    ## 
    ## The finalize action (on ALIVE->END transition)
    ## 
    ## @return RTC::ReturnCode_t
    #
    ## 
    #def onFinalize(self):
    #

    #    return RTC.RTC_OK
	
    ###
    ##
    ## The startup action when ExecutionContext startup
    ## 
    ## @param ec_id target ExecutionContext Id
    ##
    ## @return RTC::ReturnCode_t
    ##
    ##
    #def onStartup(self, ec_id):
    #
    #    return RTC.RTC_OK
	
    ###
    ##
    ## The shutdown action when ExecutionContext stop
    ##
    ## @param ec_id target ExecutionContext Id
    ##
    ## @return RTC::ReturnCode_t
    ##
    ##
    #def onShutdown(self, ec_id):
    #
    #    return RTC.RTC_OK
	
    ###
    ##
    ## The activated action (Active state entry action)
    ##
    ## @param ec_id target ExecutionContext Id
    ## 
    ## @return RTC::ReturnCode_t
    ##
    ##
    def onActivated(self, ec_id):

        self.starttime = 0
        self.starttime2 = 0
        self.pipeline = rs.pipeline()

        # Create a config and configure the pipeline to stream
        #  different resolutions of color and depth streams
        config = rs.config()

        # Get device product line for setting a supporting resolution
        pipeline_wrapper = rs.pipeline_wrapper(self.pipeline)
        pipeline_profile = config.resolve(pipeline_wrapper)
        device = pipeline_profile.get_device()
        device_product_line = str(device.get_info(rs.camera_info.product_line))

        found_rgb = False
        for s in device.sensors:
            if s.get_info(rs.camera_info.name) == 'RGB Camera':
                found_rgb = True
                break
        if not found_rgb:
            print("The demo requires Depth camera with Color sensor")
            exit(0)

        config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

        if device_product_line == 'L500':
            config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
        else:
            config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

        # Start streaming
        profile = self.pipeline.start(config)

        # Getting the depth sensor's depth scale (see rs-align example for explanation)
        depth_sensor = profile.get_device().first_depth_sensor()
        depth_scale = depth_sensor.get_depth_scale()
        print("Depth Scale is: " , depth_scale)

        # We will be removing the background of objects more than
        #  clipping_distance_in_meters meters away
        clipping_distance_in_meters = 1 #1 meter
        clipping_distance = clipping_distance_in_meters / depth_scale

        # Create an align object
        # rs.align allows us to perform alignment of depth frames to others frames
        # The "align_to" is the stream type to which we plan to align depth frames.
        align_to = rs.stream.color
        self.align = rs.align(align_to)
    
        return RTC.RTC_OK
	
    ###
    ##
    ## The deactivated action (Active state exit action)
    ##
    ## @param ec_id target ExecutionContext Id
    ##
    ## @return RTC::ReturnCode_t
    ##
    ##
    #def onDeactivated(self, ec_id):
    #
    #    return RTC.RTC_OK
	
    ###
    ##
    ## The execution action that is invoked periodically
    ##
    ## @param ec_id target ExecutionContext Id
    ##
    ## @return RTC::ReturnCode_t
    ##
    ##
    def onExecute(self, ec_id):
        facedetectiondata=self._libfacedetectionprovider.getdata()
        state=facedetectiondata.state
        command=facedetectiondata.command
        phase=facedetectiondata.phase
        if state=="STATE_RUNNING_PROVIDERREAD" and phase=="DETECTION_1":
            startwindow=True

            flag_system = True

            # Streaming loop
            while True:
            # Get frameset of color and depth
                frames = self.pipeline.wait_for_frames()
                # frames.get_depth_frame() is a 640x360 depth image

                # Align the depth frame to color frame
                aligned_frames = self.align.process(frames)

                # Get aligned frames
                aligned_depth_frame = aligned_frames.get_depth_frame() # aligned_depth_frame is a 640x480 depth image
                color_frame = aligned_frames.get_color_frame()

                # Validate that both frames are valid
                if not aligned_depth_frame or not color_frame:
                    continue

                depth_image = np.asanyarray(aligned_depth_frame.get_data())
                color_image = np.asanyarray(color_frame.get_data())
                ciHeight, ciWidth, ciColors = color_image.shape
                with mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5) as face_detection:
                    
                    color_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)
                    
                    results = face_detection.process(color_image)

                    color_image = cv2.cvtColor(color_image, cv2.COLOR_RGB2BGR)
                    

                    # ↓ 下記のif文に関する説明 ↓
                    # 顔の6点の座標は予測してとれており, カメラの範囲自体は0<= x,y <=1.0, 例えば左耳のみが範囲外になっても顔は認識され, その際左耳の座標はx=1.04~やx=-0.4~などの予測値が取得される. 
                    # results.detections[0].location_data.relative_keypointsのlenは顔が認識されている場合に限り常に6である. 
                    # 恐らく3点以上ないと顔検知せず, 6点全てのプロットができない. depth_imageの範囲外に鼻の座標があるから, x,yの予測値が取得できていてもdistanceを計算できず,
                    # out of range value for argument "x"のエラーになる. 以下は鼻の座標がdepth_imageおよびcolor_imageの外に出るときにx,yを用いてdistanceを計算させないための条件である.
                    
                    # 顔が認識され, かつ鼻の点がカメラ範囲より0.1(results.detectionsにおける座標. 範囲は幅も高さも0.0~1.0)だけ内側にある場合
                    if (results.detections)\
                        and (0.1 <= results.detections[0].location_data.relative_keypoints[2].x and results.detections[0].location_data.relative_keypoints[2].x <= 0.9)\
                        and (0.1 <= results.detections[0].location_data.relative_keypoints[2].y and results.detections[0].location_data.relative_keypoints[2].y <= 0.9):

                        # リストresults.detections[0]にはbounding_boxが最大のものについてのデータが格納されている.
                        # このデータの中から右目[0],左目[1],鼻[2],口[3],右耳[4],左耳[5]の6つの点のうち鼻の点の座標を取得する. 
                        # 以下の計算で座標になる. (x,y)の単位はピクセルであるからint型でなければならない.
                        ciWidth=640
                        ciHeight=480
                        x = int(results.detections[0].location_data.relative_keypoints[3].x * ciWidth)
                        y = int(results.detections[0].location_data.relative_keypoints[3].y * ciHeight)
                        distance = aligned_depth_frame.get_distance(x,y)
                        distance = int(distance * 100)


                            # ターミナルに3桁スペース埋め(右詰め)で(x, y), 4桁スペース埋め(右詰め)でdistanceを表示する.
                            #print('\r(x, y) = ({: 3}, {: 3})   distance = {: 4} cm'.format(x,y,distance), end='')

                            # color_imageにアノテーションを描画.
                        for detection in results.detections:
                            mp_drawing.draw_detection(color_image, detection)
    
                        # realsenseから顔までの距離が人がSotaと話そうとしていると判定される範囲内にある場合
                        if 0 <= distance and distance <= 100:


                            # starttime=0とプログラム先頭で初期化されているが, そのままであればstarttimeを現在時刻に更新.
                            if self.starttime == 0:
                                self.starttime = time.time()
                    
                            # カメラが顔を認識する時間が十分経過した場合
                            elif self.starttime+3 <= time.time():  # DUR=3:カメラが人の顔を認識する時間長
                                cv2.waitKey(1)
                                cv2.destroyWindow('MediaPipe Face Detection') # カメラ画像のウィンドウを閉じる
                                cv2.waitKey(1) 
                                self.starttime = 0

                                returndata = datacode("STATE_RUNNING_CONSUMERREAD","ぴよ",command,"SELECT")
                                facedetectiondata=self._libfacedetectionprovider.facedetection(returndata)
                                print(facedetectiondata.state,facedetectiondata.recogdata,facedetectiondata.phase)
                                startwindow=False
                                break
                            
                    else:
                        self.starttime = 0 # starttime = 0 に再初期化
                        
                        print('\r          Face is not detected.           ', end='') # 顔が認識されなかったことをターミナルに表示する.
                        # returndata = datacode("STATE_RUNNING_CONSUMERREAD","ぴよ",command,"FACEDETECTION_REPEAT")
                        # facedetectiondata=self._libfacedetectionprovider.facedetection(returndata)
                        # print(facedetectiondata.state,facedetectiondata.recogdata,facedetectiondata.phase)
                        
                        # アノテーション描画済みのcolor_imageをセルフィービュー用に左右反転してウィンドウ上に表示.
                    if startwindow:
                        cv2.startWindowThread()
                        cv2.imshow('MediaPipe Face Detection', cv2.flip(color_image, 1))
                        key = cv2.waitKey(1)
                        # escキーかqを押してセルフィービューウィンドウを閉じ, 終了する.
                        if key & 0xFF == ord('q') or key == 27:
                            cv2.destroyAllWindows()

        elif state=="STATE_RUNNING_PROVIDERREAD" and phase=="DETECTION_2":
            startwindow2=True
            startwindow=True

            flag_system = True

            # Streaming loop
            while True:
            # Get frameset of color and depth
                frames = self.pipeline.wait_for_frames()
                # frames.get_depth_frame() is a 640x360 depth image

                # Align the depth frame to color frame
                aligned_frames = self.align.process(frames)

                # Get aligned frames
                aligned_depth_frame = aligned_frames.get_depth_frame() # aligned_depth_frame is a 640x480 depth image
                color_frame = aligned_frames.get_color_frame()

                # Validate that both frames are valid
                if not aligned_depth_frame or not color_frame:
                    continue

                depth_image = np.asanyarray(aligned_depth_frame.get_data())
                color_image = np.asanyarray(color_frame.get_data())
                ciHeight, ciWidth, ciColors = color_image.shape
                with mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5) as face_detection:
                    
                    color_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)
                    
                    results = face_detection.process(color_image)

                    color_image = cv2.cvtColor(color_image, cv2.COLOR_RGB2BGR)

                with mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5) as face_detection:
                    
                    color_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)
                    
                    results = face_detection.process(color_image)

                    color_image = cv2.cvtColor(color_image, cv2.COLOR_RGB2BGR)
                    

                    # ↓ 下記のif文に関する説明 ↓
                    # 顔の6点の座標は予測してとれており, カメラの範囲自体は0<= x,y <=1.0, 例えば左耳のみが範囲外になっても顔は認識され, その際左耳の座標はx=1.04~やx=-0.4~などの予測値が取得される. 
                    # results.detections[0].location_data.relative_keypointsのlenは顔が認識されている場合に限り常に6である. 
                    # 恐らく3点以上ないと顔検知せず, 6点全てのプロットができない. depth_imageの範囲外に鼻の座標があるから, x,yの予測値が取得できていてもdistanceを計算できず,
                    # out of range value for argument "x"のエラーになる. 以下は鼻の座標がdepth_imageおよびcolor_imageの外に出るときにx,yを用いてdistanceを計算させないための条件である.
                    
                    # 顔が認識され, かつ鼻の点がカメラ範囲より0.1(results.detectionsにおける座標. 範囲は幅も高さも0.0~1.0)だけ内側にある場合
                    if (results.detections)\
                        and (0.1 <= results.detections[0].location_data.relative_keypoints[2].x and results.detections[0].location_data.relative_keypoints[2].x <= 0.9)\
                        and (0.1 <= results.detections[0].location_data.relative_keypoints[2].y and results.detections[0].location_data.relative_keypoints[2].y <= 0.9):

                        # リストresults.detections[0]にはbounding_boxが最大のものについてのデータが格納されている.
                        # このデータの中から右目[0],左目[1],鼻[2],口[3],右耳[4],左耳[5]の6つの点のうち鼻の点の座標を取得する. 
                        # 以下の計算で座標になる. (x,y)の単位はピクセルであるからint型でなければならない.
                        ciWidth=640
                        ciHeight=480
                        x = int(results.detections[0].location_data.relative_keypoints[3].x * ciWidth)
                        y = int(results.detections[0].location_data.relative_keypoints[3].y * ciHeight)
                        distance = aligned_depth_frame.get_distance(x,y)
                        distance = int(distance * 100)

                            # ターミナルに3桁スペース埋め(右詰め)で(x, y), 4桁スペース埋め(右詰め)でdistanceを表示する.
                            #print('\r(x, y) = ({: 3}, {: 3})   distance = {: 4} cm'.format(x,y,distance), end='')

                            # color_imageにアノテーションを描画.
                        for detection in results.detections:
                            mp_drawing.draw_detection(color_image, detection)
    
                        # realsenseから顔までの距離が人がSotaと話そうとしていると判定される範囲内にある場合
                        if 0 <= distance and distance <= 100:


                            # starttime=0とプログラム先頭で初期化されているが, そのままであればstarttimeを現在時刻に更新.
                            if self.starttime2 == 0:
                                self.starttime2 = time.time()
                    
                            # カメラが顔を認識する時間が十分経過した場合
                            elif self.starttime2+1 <= time.time():  # DUR=3:カメラが人の顔を認識する時間長
                                cv2.waitKey(1)
                                cv2.destroyWindow('MediaPipe Face Detection') # カメラ画像のウィンドウを閉じる
                                cv2.waitKey(1) 
                                self.starttime2 = 0

                                returndata = datacode("STATE_RUNNING_CONSUMERREAD","ぴよ",command,"SELECT")
                                facedetectiondata=self._libfacedetectionprovider.facedetection(returndata)
                                print(facedetectiondata.state,facedetectiondata.recogdata,facedetectiondata.phase)
                                startwindow2=False
                                break
                                
                    else:
                        self.starttime2 = 0 # starttime = 0 に再初期化
                        
                        print('\r          Face is not detected.           ', end='') # 顔が認識されなかったことをターミナルに表示する.
                        returndata = datacode("STATE_RUNNING_CONSUMERREAD","ぴよ",command,"STOP")
                        facedetectiondata=self._libfacedetectionprovider.facedetection(returndata)
                        print(facedetectiondata.state,facedetectiondata.recogdata,facedetectiondata.phase)
                        break
                    if startwindow2:
                        cv2.startWindowThread()
                        cv2.imshow('MediaPipe Face Detection', cv2.flip(color_image, 1))
                        key = cv2.waitKey(1)
                        # escキーかqを押してセルフィービューウィンドウを閉じ, 終了する.
                        if key & 0xFF == ord('q') or key == 27:
                            cv2.destroyAllWindows()

            

    
        return RTC.RTC_OK
	
    ###
    ##
    ## The aborting action when main logic error occurred.
    ##
    ## @param ec_id target ExecutionContext Id
    ##
    ## @return RTC::ReturnCode_t
    ##
    ##
    #def onAborting(self, ec_id):
    #
    #    return RTC.RTC_OK
	
    ###
    ##
    ## The error action in ERROR state
    ##
    ## @param ec_id target ExecutionContext Id
    ##
    ## @return RTC::ReturnCode_t
    ##
    ##
    #def onError(self, ec_id):
    #
    #    return RTC.RTC_OK
	
    ###
    ##
    ## The reset action that is invoked resetting
    ##
    ## @param ec_id target ExecutionContext Id
    ##
    ## @return RTC::ReturnCode_t
    ##
    ##
    #def onReset(self, ec_id):
    #
    #    return RTC.RTC_OK
	
    ###
    ##
    ## The state update action that is invoked after onExecute() action
    ##
    ## @param ec_id target ExecutionContext Id
    ##
    ## @return RTC::ReturnCode_t
    ##

    ##
    #def onStateUpdate(self, ec_id):
    #
    #    return RTC.RTC_OK
	
    ###
    ##
    ## The action that is invoked when execution context's rate is changed
    ##
    ## @param ec_id target ExecutionContext Id
    ##
    ## @return RTC::ReturnCode_t
    ##
    ##
    #def onRateChanged(self, ec_id):
    #
    #    return RTC.RTC_OK
	



def facedetectionInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=facedetection_spec)
    manager.registerFactory(profile,
                            facedetection,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    facedetectionInit(manager)

    # create instance_name option for createComponent()
    instance_name = [i for i in sys.argv if "--instance_name=" in i]
    if instance_name:
        args = instance_name[0].replace("--", "?")
    else:
        args = ""
  
    # Create a component
    comp = manager.createComponent("facedetection" + args)

def main():
    # remove --instance_name= option
    argv = [i for i in sys.argv if not "--instance_name=" in i]
    # Initialize manager
    mgr = OpenRTM_aist.Manager.init(sys.argv)
    mgr.setModuleInitProc(MyModuleInit)
    mgr.activateManager()
    mgr.runManager()

if __name__ == "__main__":
    main()

