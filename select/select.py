#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

# <rtc-template block="description">
"""
 @file select.py
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

import select_idl

# Import Service implementation class
# <rtc-template block="service_impl">
from select_idl_example import *

import azure.cognitiveservices.speech as speechsdk
speech_config = speechsdk.SpeechConfig(subscription="***********************", region="japanwest")
audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
speech_config.speech_synthesis_voice_name='ja-JP-NanamiNeural'
speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

speech_config.speech_recognition_language="ja-JP"
audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)


class datacode:
    def __init__(self,state,recogdata,command,phase):
        self.state=state
        self.recogdata=recogdata
        self.command=command
        self.phase=phase

# </rtc-template>

# Import Service stub modules
# <rtc-template block="consumer_import">
# </rtc-template>


# This module's spesification
# <rtc-template block="module_spec">
select_spec = ["implementation_id", "select", 
         "type_name",         "select", 
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
# @class select
# @brief ModuleDescription
# 
# 
# </rtc-template>
class select(OpenRTM_aist.DataFlowComponentBase):
	
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

        """
        """
        self._selectproviderPort = OpenRTM_aist.CorbaPort("selectprovider")

        """
        """
        self._selectprovider = selectdata_i()
		


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
		
        # Set OutPort buffers
        self.addOutPort("controlesota",self._controlesotaOut)
		
        # Set service provider to Ports
        self._selectproviderPort.registerProvider("selectdata", "Library::selectdata", self._selectprovider)
		
        # Set service consumers to Ports
		
        # Set CORBA Service Ports
        self.addPort(self._selectproviderPort)
		
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
    #def onActivated(self, ec_id):
    #
    #    return RTC.RTC_OK
	
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
    def onExecute(self, ec_id):
        selectdata=self._selectprovider.getdata()
        state=selectdata.state
        recogdata=selectdata.recogdata
        command=selectdata.command
        phase=selectdata.phase
        response=""
        

        if state=="STATE_RUNNING_PROVIDERREAD" and (phase=="SELECT" or phase =="AGAIN" or phase=="REPEAT"):
            if phase=="SELECT":
                self._d_controlesota.data="hello"
                self._controlesotaOut.write()
                speech_synthesizer.speak_text("こんにちは")
                self._d_controlesota.data="neutral"
                self._controlesotaOut.write()
                
            if phase=="AGAIN":
                speech_synthesizer.speak_text("他にご用件はありますか？")
                self._d_controlesota.data="question"
                self._controlesotaOut.write()
                response=speech_recognizer.recognize_once_async().get()
                print(response.text)
                if "ないです" in response.text or "ありません" in response.text or "いいえ" in response.text:
                    speech_synthesizer.speak_text("ご利用ありがとうございました")
                    self._d_controlesota.data="hello"
                    self._controlesotaOut.write()
                    time.sleep(2)
                    self._d_controlesota.data="neutral"
                    self._controlesotaOut.write()
                    phase="DETECTION_1"
                elif "はい" in response.text or "あります" in response.text:
                    phase="SELECT"
                elif "検索" in response.text or "おすすめ" in response.text or "お勧め" in response.text or "サーティフィケート" in response.text or "スタッフ" in response.text or "文献" in response.text or "調べて" in response.text:
                    phase="PASS"
            if phase=="SELECT" or phase=="REPEAT":
                speech_synthesizer.speak_text("ご用件は何でしょうか")
                self._d_controlesota.data="listening"
                self._controlesotaOut.write()
                response=speech_recognizer.recognize_once_async().get()
                self._d_controlesota.data="neutral"
                self._controlesotaOut.write()
                print(response.text)
            if "検索"in str(response):
                returndata = datacode("STATE_RUNNING_CONSUMERREAD",recogdata,command,"SEARCH")
                selectdata=self._selectprovider.select(returndata)
                print(selectdata.state,selectdata.recogdata)
            elif "お勧め" in str(response) or "おすすめ" in str(response):
                returndata =datacode("STATE_RUNNING_CONSUMERREAD",recogdata,command,"RECOM")
                selectdata=self._selectprovider.select(returndata)
            elif "サーティフィケート" in str(response):
                returndata =datacode("STATE_RUNNING_CONSUMERREAD",recogdata,command,"CERTIFICATE")
                selectdata=self._selectprovider.select(returndata)
            elif "スタッフ" in str(response):
                self._d_controlesota.data="speaking"
                self._controlesotaOut.write()
                speech_synthesizer.speak_text("図書館職員さんをお呼びします。少々お待ちください")
                self._d_controlesota.data="neutral"
                self._controlesotaOut.write()
                returndata =datacode("STATE_RUNNING_CONSUMERREAD",recogdata,command,"STAFFCALL")
                selectdata=self._selectprovider.select(returndata)
            elif "文献"in str(response):
                self._d_controlesota.data="speaking"
                self._controlesotaOut.write()
                speech_synthesizer.speak_text("文献の受け取りですね。図書館職員さんをお呼びします。少々お待ちください。")
                self._d_controlesota.data="neutral"
                self._controlesotaOut.write()
                returndata = datacode("STATE_RUNNING_CONSUMERREAD",recogdata,command,"ARTICLE")
                selectdata=self._selectprovider.select(returndata)
            elif phase=="DETECTION_1":
                returndata =datacode("STATE_RUNNING_CONSUMERREAD",recogdata,command,"DETECTION_1")
                selectdata=self._selectprovider.select(returndata)
                print(selectdata.state,selectdata.recogdata)
            else:
                returndata =datacode("STATE_RUNNING_CONSUMERREAD",recogdata,command,"REPEAT")
                selectdata=self._selectprovider.select(returndata)
                print(selectdata.state,selectdata.recogdata)
        if phase=="DETECTION_1":
            returndata =datacode("STATE_RUNNING_CONSUMERREAD",recogdata,command,"DETECTION_1")
            selectdata=self._selectprovider.select(returndata)
            print(selectdata.state,selectdata.recogdata)

    
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
	



def selectInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=select_spec)
    manager.registerFactory(profile,
                            select,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    selectInit(manager)

    # create instance_name option for createComponent()
    instance_name = [i for i in sys.argv if "--instance_name=" in i]
    if instance_name:
        args = instance_name[0].replace("--", "?")
    else:
        args = ""
  
    # Create a component
    comp = manager.createComponent("select" + args)

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

