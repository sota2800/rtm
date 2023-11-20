#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

# <rtc-template block="description">
"""
 @file camera.py
 @brief ModuleDescription
 @date $Date$


"""
# </rtc-template>

import sys
import time
sys.path.append(".")

# Import RTM module
import RTC
import OpenRTM_aist
import cv2
import pyrealsense2 as rs
import numpy as np
import mediapipe as mp
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

# realsenseから顔までの距離のうち, 人がSotaと話そうとしていると判定される範囲の上限値および下限値. 単位はセンチメートル.
DISTANCE_MIN = 10 # 0cmは稀に検出されることがあるため含まない方がよい.
DISTANCE_MAX = 100



# Import Service implementation class
# <rtc-template block="service_impl">

# </rtc-template>

# Import Service stub modules
# <rtc-template block="consumer_import">
# </rtc-template>


# This module's spesification
# <rtc-template block="module_spec">
camera_spec = ["implementation_id", "camera", 
         "type_name",         "camera", 
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
# @class camera
# @brief ModuleDescription
# 
# 
# </rtc-template>
class camera(OpenRTM_aist.DataFlowComponentBase):
	
    ##
    # @brief constructor
    # @param manager Maneger Object
    # 
    def __init__(self, manager):
        OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

        self._d_camera = OpenRTM_aist.instantiateDataType(RTC.CameraImage)
        """
        """
        self._cameraOut = OpenRTM_aist.OutPort("camera", self._d_camera)
        self._d_distance = OpenRTM_aist.instantiateDataType(RTC.TimedFloat)
        """
        """
        self._distanceOut = OpenRTM_aist.OutPort("distance", self._d_distance)
        """
        
         - Name:  conf_width
         - DefaultValue: 640
        """
        self._conf_width = [640]
        """
        
         - Name:  conf_height
         - DefaultValue: 480
        """
        self._conf_height = [480]
        """
        
         - Name:  conf_bpp
         - DefaultValue: 24
        """
        self._conf_bpp = [24]


		


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
        self.bindParameter("Width", self._conf_width, "640")
        self.bindParameter("Height", self._conf_height, "480")
        self.bindParameter("Bits_Per_Pixel", self._conf_bpp, "24")
        # Bind variables and configuration variable
		
        # Set InPort buffers
		
        # Set OutPort buffers
        self.addOutPort("camera",self._cameraOut)
        self.addOutPort("distance",self._distanceOut)
		
        # Set service provider to Ports
		
        # Set service consumers to Ports
		
        # Set CORBA Service Ports
		
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

        self._d_camera.height = self._conf_height[0]#コンフィグレーションのパラメーターをCameraImage型の変数に格納（self._d_変数名.メンバ名）
        self._d_camera.width = self._conf_width[0]#コンフィグレーションのパラーメータのアクセスself._変数名
        self._d_camera.bpp = self._conf_bpp[0]#ビット深度グレースケール8bit カラー24bit
        #self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self._d_camera.height)#カメラから取得する画像サイズの設定コンフィグレーションからサイズ640,480
        #self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self._d_camera.width)
    
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
        # pipeline = rs.pipeline()
        # config = rs.config()
        # config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
        # pipeline.start(config)

        # pipelinedepth=rs.pipeline()
        # configdepth = rs.config()
        # configdepth.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        # pipelinedepth.start(configdepth)
        # #ret, frame = self.cap.read()
        # while True:
        #     time.sleep(0.1)
        #     frames = pipeline.wait_for_frames()
        #     color_frame = frames.get_color_frame()

        #     framesdepth = pipelinedepth.wait_for_frames()
        #     depth_frame = framesdepth.get_depth_frame()

        #     # 距離を測定する
        #     distance = depth_frame.get_distance(320, 240)
        #     if not color_frame:
        #         continue
        # Create a pipeline
        # Create a pipeline

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
                    x = int(results.detections[0].location_data.relative_keypoints[3].x * ciWidth)
                    y = int(results.detections[0].location_data.relative_keypoints[3].y * ciHeight)
                    distance = aligned_depth_frame.get_distance(x,y)
                    distance = int(distance * 100)
                    self._d_distance.data=distance
                    print(distance)
                    self._distanceOut.write()
            img = np.array(color_frame.get_data())
            self._d_camera.format = 'png'
            self._d_camera.pixels = img.tobytes()#numpy配列からbyte配列へ
            #self._d_camera.pixels=img
            #print(self._d_camera.pixels)
            self._cameraOut.write()

    
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
	



def cameraInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=camera_spec)
    manager.registerFactory(profile,
                            camera,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    cameraInit(manager)

    # create instance_name option for createComponent()
    instance_name = [i for i in sys.argv if "--instance_name=" in i]
    if instance_name:
        args = instance_name[0].replace("--", "?")
    else:
        args = ""
  
    # Create a component
    comp = manager.createComponent("camera" + args)

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

