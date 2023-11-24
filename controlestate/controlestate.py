#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

# <rtc-template block="description">
"""
 @file controlestate.py
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

import facedetection_idl
import select_idl
import voicerecog_idl
import selenium_idl

# Import Service implementation class
# <rtc-template block="service_impl">

# </rtc-template>

# Import Service stub modules
# <rtc-template block="consumer_import">
import Library, Library__POA

import azure.cognitiveservices.speech as speechsdk
speech_config = speechsdk.SpeechConfig(subscription="***********************", region="japanwest")
audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
speech_config.speech_synthesis_voice_name='ja-JP-NanamiNeural'
speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

speech_config.speech_recognition_language="ja-JP"
audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)


# </rtc-template>


# This module's spesification
# <rtc-template block="module_spec">
controlestate_spec = ["implementation_id", "controlestate", 
         "type_name",         "controlestate", 
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
# @class controlestate
# @brief ModuleDescription
# 
# 
# </rtc-template>

class datacode:
    def __init__(self,state,recogdata,command,phase):
        self.state=state
        self.recogdata=recogdata
        self.command=command
        self.phase=phase

class controlestate(OpenRTM_aist.DataFlowComponentBase):
	
    ##
    # @brief constructor
    # @param manager Maneger Object
    # 
    def __init__(self, manager):
        OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

        self._d_controlesota = OpenRTM_aist.instantiateDataType(RTC.TimedString)
        """
        """
        self._controlesotaOut = OpenRTM_aist.OutPort("controlesota", self._d_controlesota)
        self._d_callstaff = OpenRTM_aist.instantiateDataType(RTC.TimedBoolean)
        """
        """
        self._callstaffOut = OpenRTM_aist.OutPort("callstaff", self._d_callstaff)
        self._d_log = OpenRTM_aist.instantiateDataType(RTC.TimedString)
        """
        """
        self._logOut = OpenRTM_aist.OutPort("log", self._d_log)

        """
        """
        self._facedetectionconsumerPort = OpenRTM_aist.CorbaPort("facedetectionconsumer")
        """
        """
        self._selectconusmerPort = OpenRTM_aist.CorbaPort("selectconusmer")
        """
        """
        self._voicerecogconsumerPort = OpenRTM_aist.CorbaPort("voicerecogconsumer")
        """
        """
        self._seleniumconsumerPort = OpenRTM_aist.CorbaPort("seleniumconsumer")

		

        """
        """
        self._libfacedetectionconsumer = OpenRTM_aist.CorbaConsumer(interfaceType=Library.facedetectiondata)
        """
        """
        self._libselectconsumer = OpenRTM_aist.CorbaConsumer(interfaceType=Library.selectdata)
        """
        """
        self._libvoicerecogconsumer = OpenRTM_aist.CorbaConsumer(interfaceType=Library.voicerecogdata)
        """
        """
        self._libseleniumconsumer = OpenRTM_aist.CorbaConsumer(interfaceType=Library.seleniumdata)

        # initialize of configuration-data.
        # <rtc-template block="init_conf_param">
		
        # </rtc-template>
        self.libdata=datacode("STATE_STOP","ぴよ","NUM","DETECTION_1")
        self.start=True


		 
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
		
        # Set OutPort buffers
        self.addOutPort("controlesota",self._controlesotaOut)
        self.addOutPort("callstaff",self._callstaffOut)
        self.addOutPort("log",self._logOut)
		
        # Set service provider to Ports
		
        # Set service consumers to Ports
        self._facedetectionconsumerPort.registerConsumer("facedetectiondata", "Library::facedetectiondata", self._libfacedetectionconsumer)
        self._selectconusmerPort.registerConsumer("selectdata", "Library::selectdata", self._libselectconsumer)
        self._voicerecogconsumerPort.registerConsumer("voicerecogdata", "Library::voicerecogdata", self._libvoicerecogconsumer)
        self._seleniumconsumerPort.registerConsumer("seleniumdata", "Library::seleniumdata", self._libseleniumconsumer)
		
        # Set CORBA Service Ports
        self.addPort(self._facedetectionconsumerPort)
        self.addPort(self._selectconusmerPort)
        self.addPort(self._voicerecogconsumerPort)
        self.addPort(self._seleniumconsumerPort)
		
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
    def onStartup(self, ec_id):
        #起動時にseleniumを起動onstartupに書いててもいいかも

    
        return RTC.RTC_OK
	
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
        time.sleep(10)
        time.sleep(10)

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
	
    ##
    #
    # The execution action that is invoked periodically
    #
    # @param ec_id target ExecutionContext Id
    #
    # @return RTC::ReturnCode_t
    #
    #
    def midfacedetection(self):
        if self.libdata.phase=="DETECTION_1" or self.libdata.phase=="DETECTION_2":
            if self.libdata.phase=="DETECTION_1":
                data="DETECTION_1"
            elif self.libdata.phase=="DETECTION_2":
                data="DETECTION_2"
            facedetectiondata=self.libdata 
            if self.libdata.phase=="DETECTION_1":         
                while(facedetectiondata.phase!="SELECT"):
                    facedetectiondata=datacode("STATE_RUNNING_PROVIDERREAD","ぴよ","NUM",data)
                    facedetectiondata=self.facedetectionconsumer(facedetectiondata)
            elif self.libdata.phase=="DETECTION_2":       
                    facedetectiondata=datacode("STATE_RUNNING_PROVIDERREAD","ぴよ","NUM",data)
                    facedetectiondata=self.facedetectionconsumer(facedetectiondata)
            #self.libdata=facedetectiondata          
        return facedetectiondata
    
    def facedetectionconsumer(self,data):
            temp=self._libfacedetectionconsumer._ptr().facedetection(data)
            print(temp.state)
            time.sleep(1)
            data=self._libfacedetectionconsumer._ptr().setresult("READ")
            while(data.state!="STATE_RUNNING_CONSUMERREAD"):
                data=self._libfacedetectionconsumer._ptr().setresult("READ")
            if data.state!="STATE_STOP" or data.state!="STATE_ERROR":
                data.state="STATE_RUNNING"
            print(data.state,data.phase)
            return data
    
    def selectconsumer(self,data):
            temp=self._libselectconsumer._ptr().select(data)
            print(temp.state)
            time.sleep(1)
            data=self._libselectconsumer._ptr().setresult("READ")
            while(data.state!="STATE_RUNNING_CONSUMERREAD"):
                data=self._libselectconsumer._ptr().setresult("READ")
            if data.state!="STATE_STOP" or data.state!="STATE_ERROR":
                data.state="STATE_RUNNING"
            print(data.state,data.phase)
            return data

    def voicerecogconsumer(self,data):
            temp=self._libvoicerecogconsumer._ptr().voicerecog(data)
            print(temp.state)
            time.sleep(1)
            data=self._libvoicerecogconsumer._ptr().setresult("READ")
            while(data.state!="STATE_RUNNING_CONSUMERREAD"):
                data=self._libvoicerecogconsumer._ptr().setresult("READ")
            print(2,data.state,data.phase)
            if data.state!="STATE_STOP" or data.state!="STATE_ERROR":
                data.state="STATE_RUNNING"
            return data
    def seleniumconsumer(self,data):
            # if data.phase=="SEARCH":
            temp=self._libseleniumconsumer._ptr().search(data)
            # elif data.phase=="RECOM":
            #      temp=self._libseleniumconsumer._ptr().recom(data)
            # elif data.phase=="CERTIFICATE":
            #      temp=self._libseleniumconsumer._ptr().certificate(data)
            print(temp.state)
            time.sleep(1)
            data=self._libseleniumconsumer._ptr().setresult("READ")
            while(data.state!="STATE_RUNNING_CONSUMERREAD"):
                data=self._libseleniumconsumer._ptr().setresult("READ")
            if data.state!="STATE_STOP" or data.state!="STATE_ERROR":
                data.state="STATE_RUNNING"
            print(data.state,data.phase)
            return data

    def onExecute(self, ec_id):

        #seleniumをホームページに戻す
        seleniumdata=datacode("","ぴよ","NUM","RESET_SELENIUM")
        temp=self._libseleniumconsumer._ptr().search(seleniumdata)
        print("RESET_SELENIUM")


        if self.libdata.phase=="DETECTION_1":
            print("----------FACEDETECTION_1_PHASE----------")
            self.libdata=self.midfacedetection()#self.libdata.phaseがDETECTION_1の時とDETECTION_2の時しか動かない

        selectcount=0
        task=""

        #select
        while(selectcount<3):
            if self.libdata.state=="STATE_RUNNING" and (self.libdata.phase=="SELECT" or self.libdata.phase=="AGAIN" or self.libdata.phase=="REPEAT" ):
                print("----------SELECT_PHASE_",selectcount,"----------")
                selectdata=datacode("STATE_RUNNING_PROVIDERREAD","ぴよ","NUM",self.libdata.phase)
                selectdata =self.selectconsumer(selectdata)
                print(selectdata.phase)
                self.libdata=selectdata
         
            if self.libdata.state=="STATE_ERROR":
                break
            elif self.libdata.state=="STATE_RUNNING":
                if self.libdata.phase=="SEARCH":
                    task=self.libdata.phase
                    self._d_log.data="search"
                    self._logOut.write()
                    break
                elif self.libdata.phase=="RECOM":
                    task=self.libdata.phase
                    self._d_log.data="recommendation"
                    self._logOut.write()
                    break
                elif self.libdata.phase=="CERTIFICATE":
                    task=self.libdata.phase
                    self._d_log.data="scertificate"
                    self._logOut.write()
                    break
                elif self.libdata.phase=="ARTICLE":
                    task=self.libdata.phase
                    self._d_log.data="article"
                    self._logOut.write()
                    break
                elif self.libdata.phase=="CALLSTAFF":
                    task=self.libdata.phase
                    break
                elif self.libdata.phase=="DETECTION_1":
                    task=self.libdata.phase
                    self.libdata.phase="DETECTION_1"
                    self.libdata.state="STATE_STOP"
                    break
                if self.libdata.state=="STATE_RUNNING":
                    print("----------FACEDETECTION_2_PHASE----------")
                    temp=self.libdata.phase
                    self.libdata.phase="DETECTION_2"
                    self.libdata=self.midfacedetection()
                    if self.libdata.phase=="STOP":
                        self.libdata.state="STATE_STOP"
                        self.libdata.phase="DETECTION_1"
                        break
                    else:
                        self.libdata.phase=temp  

            selectcount+=1
            if selectcount==2:
                self.libdata.phase="DETECTION_1"
                self.libdata.state="STATE_STOP"
                break
        
        #facedetection
        if self.libdata.state=="STATE_RUNNING":
            print("----------SELECT-VOICERECOG-FACEDETECTION_2_PHASE----------")
            temp=self.libdata.phase
            self.libdata.phase="DETECTION_2"
            self.libdata=self.midfacedetection()
            if self.libdata.phase=="STOP":
                self.libdata.state="STATE_STOP"
                self.libdata.phase="DETECTION_1"
            else:
                self.libdata.phase=temp



        #voicerecog
        if self.libdata.state=="STATE_RUNNING":
            if task=="SEARCH" or task=="RECOM":
                print("----------VOICERECOG_PHASE----------")
                voicerecogdata=datacode("STATE_RUNNING_PROVIDERREAD","ぴよ","NUM",task)
                voicerecogdata=self.voicerecogconsumer(voicerecogdata)
                self.libdata=voicerecogdata

        #facedetection
        if self.libdata.state=="STATE_RUNNING":
            print("----------VOICERECOG_SELENIUM_FACEDETECTION_2_PHASE----------")
            temp=self.libdata.phase
            self.libdata.phase="DETECTION_2"
            self.libdata=self.midfacedetection()
            if self.libdata.phase=="STOP":
                self.libdata.state="STATE_STOP"
                self.libdata.phase="DETECTION_1"
            else:
                self.libdata.phase=temp

        #selenium
        if self.libdata.state=="STATE_RUNNING":
            if task=="SEARCH":
                print("----------SELENIUM_SEARCH_PHASE----------")
                seleniumdata=datacode("STATE_RUNNING_PROVIDERREAD",voicerecogdata.recogdata,"NUM",task)
                seleniumdata=self.seleniumconsumer(seleniumdata)
                self.libdata=seleniumdata
                if self.libdata.phase=="STAY_SEARCH":
                    while(seleniumdata.phase!="AGAIN"):    
                        print("----------SELENIUM_SEARCH_FACEDETECTION_2_PHASE----------")
                        temp=self.libdata.phase
                        self.libdata.phase="DETECTION_2"
                        self.libdata=self.midfacedetection()
                        if self.libdata.phase=="STOP":
                            self.libdata.state="STATE_STOP"
                            self.libdata.phase="DETECTION_1"
                            break
                        self.libdata.phase=temp   
                        seleniumdata=datacode("STATE_RUNNING_PROVIDERREAD","ぴよ","NUM","STAY_SEARCH")
                        seleniumdata=self.seleniumconsumer(seleniumdata)
                    if self.libdata.phase!="DETECTION_1":
                         self.libdata=seleniumdata
                    print(self.libdata.phase) 


            elif task=="RECOM":
                print("----------SELENIUM_RECOM_PHASE----------")
                seleniumdata=datacode("STATE_RUNNING_PROVIDERREAD",voicerecogdata.recogdata,"NUM",task)
                seleniumdata=self.seleniumconsumer(seleniumdata)
                self.libdata=seleniumdata
                if self.libdata.phase=="RECOM_REPEAT":
                    while(seleniumdata.phase!="STAY_SEARCH"):
                         print("----------SELENIUM_RECOM_FACEDETECTION_2_PHASE----------")
                         self.libdata.phase="DETECTION_2"
                         self.libdata=self.midfacedetection()
                         if self.libdata.phase=="STOP":
                            self.libdata.state="STATE_RUNNING_PROVIDERREAD"
                            self.libdata.phase="DETECTION_1" 
                            seleniumdata=self.seleniumconsumer(self.libdata)
                            self.libdata.state="STATE_RUNNING"
                            break 
                         else:
                            seleniumdata.state="STATE_RUNNING_PROVIDERREAD"
                            seleniumdata=self.seleniumconsumer(seleniumdata)
                            print(seleniumdata.phase)
                            self.libdata=seleniumdata                           
                    
                if self.libdata.phase=="STAY_SEARCH":
                    while(seleniumdata.phase!="AGAIN"):    
                        print("----------SELENIUM_SEARCH_FACEDETECTION_2_PHASE----------")
                        self.libdata.phase="DETECTION_2"
                        self.libdata=self.midfacedetection()
                        if self.libdata.phase=="STOP":
                            self.libdata.state="STATE_STOP"
                            self.libdata.phase="DETECTION_1"
                            break   
                        seleniumdata=datacode("STATE_RUNNING_PROVIDERREAD","ぴよ","NUM","STAY_SEARCH")
                        seleniumdata=self.seleniumconsumer(seleniumdata)
                        self.libdata=seleniumdata

            elif task=="CERTIFICATE":
                print("----------SELENIUM_CERTIFICATE_PHASE----------")
                seleniumdata=datacode("STATE_RUNNING_PROVIDERREAD","ぴよ","NUM",task)
                seleniumdata=self.seleniumconsumer(seleniumdata)
                self.libdata=seleniumdata
                self.libdata.state="STATE_RUNNING"


        #callstaff
        if self.libdata.state=="STATE_RUNNING":
            if task=="ARTICLE" or task=="STAFFCALL":
                print("----------CALLSTAFF_PHASE----------")
                self._d_callstaff.data=True
                self._callstaffOut.write()
                time.sleep(5)
                self.libdata.phase="DETECTION_1"
            elif self.libdata.phase=="CALLSTAFF":
                print("----------CALLSTAFF_CERTIFICATE_PHASE----------")
                self._d_callstaff.data=True
                self._callstaffOut.write()
                time.sleep(10)
                self.libdata.phase="DETECTION_1"


        #facedetection
        if self.libdata.state=="STATE_RUNNING":
            print("----------LAST_FACEDETECTION_2_PHASE----------")
            temp=self.libdata.phase
            self.libdata.phase="DETECTION_2"
            self.libdata=self.midfacedetection()
            if self.libdata.phase=="STOP":
                self.libdata.state="STATE_STOP"
                self.libdata.phase="DETECTION_1"
            else:
                self.libdata.phase=temp
        
        print("******",self.libdata.state,self.libdata.phase,"******")

    
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
	



def controlestateInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=controlestate_spec)
    manager.registerFactory(profile,
                            controlestate,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    controlestateInit(manager)

    # create instance_name option for createComponent()
    instance_name = [i for i in sys.argv if "--instance_name=" in i]
    if instance_name:
        args = instance_name[0].replace("--", "?")
    else:
        args = ""
  
    # Create a component
    comp = manager.createComponent("controlestate" + args)

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

