#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

# <rtc-template block="description">
"""
 @file selenium.py
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

import selenium_idl
from selenium import webdriver
from os.path import join
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import random

# Import Service implementation class
# <rtc-template block="service_impl">
from selenium_idl_example import *

import azure.cognitiveservices.speech as speechsdk
speech_config = speechsdk.SpeechConfig(subscription="***********************", region="japanwest")
audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
speech_config.speech_synthesis_voice_name='ja-JP-NanamiNeural'
speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

speech_config.speech_recognition_language="ja-JP"
audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

# </rtc-template>

# Import Service stub modules
# <rtc-template block="consumer_import">
# </rtc-template>


# This module's spesification
# <rtc-template block="module_spec">
selenium_spec = ["implementation_id", "selenium", 
         "type_name",         "selenium", 
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
# @class selenium
# @brief ModuleDescription
# 
# 
# </rtc-template>
class startselenium:
     def __init__(self,root,driver_path,options,service,driver):
          self.root=root
          self.driver_path=driver_path
          self.options=options
          self.service=service
          self.driver=driver
     
class selenium(OpenRTM_aist.DataFlowComponentBase):
	
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
        self._seleniumproviderPort = OpenRTM_aist.CorbaPort("seleniumprovider")

        """
        """
        self._libseleniumprovider = seleniumdata_i()


        # self.root = join(__file__,"..")
        # self.driver_path=join(self.root, "chromedriver.exe")
        # self.options = webdriver.ChromeOptions()
        # self.options.add_experimental_option("detach", True)
        # self.service = Service(executable_path=self.driver_path) 
        # self.driver = webdriver.Chrome(service=self.service, options=self.options)
		


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
        self._seleniumproviderPort.registerProvider("seleniumdata", "Library::seleniumdata", self._libseleniumprovider)
		
        # Set service consumers to Ports
		
        # Set CORBA Service Ports
        self.addPort(self._seleniumproviderPort)
		
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
        # root = join(__file__,"..")
        # driver_path=join(root, "chromedriver.exe")
        # options = webdriver.ChromeOptions()
        # service = Service(executable_path=driver_path) 
        # driver = webdriver.Chrome(service=service, options=options)
        # driver.get('https://library.konan-u.ac.jp/')
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
        self.selenium_instance=startselenium(join(__file__,".."),join(join(__file__,".."), "chromedriver.exe"),webdriver.ChromeOptions(),
                    Service(executable_path=join(join(__file__,".."), "chromedriver.exe")),
                    webdriver.Chrome(service=Service(executable_path=join(join(__file__,".."), "chromedriver.exe")), options=webdriver.ChromeOptions()))
        self.selenium_instance.options.add_experimental_option("detach", True)
        self.selenium_instance.driver.implicitly_wait(2)
        self.selenium_instance.driver.get('https://library.konan-u.ac.jp/')
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

    def seleniumprovider(self,data):
        temp=self._libseleniumprovider.search(data)
        print(temp.state,temp.phase)
        time.sleep(1)
        data=self._libseleniumprovider.setresult("READ")
        while(data.state!="STATE_RUNNING_PROVIDERREAD"):
            data=self._libseleniumprovider.setresult("READ")
        if data.state!="STATE_STOP" or data.state!="STATE_ERROR":
            data.state="STATE_RUNNING"
        print(data.state,data.phase)
        return data
    

    def onExecute(self, ec_id):
        seleniumdata=self._libseleniumprovider.getdata()
        state=seleniumdata.state
        command=seleniumdata.command
        recogdata=seleniumdata.recogdata
        phase=seleniumdata.phase
        

        if phase=="RESET_SELENIUM":
            self.selenium_instance.driver.get('https://library.konan-u.ac.jp/')
            returndata = datacode("NUM","ぴよ","NUM","NUM")
            seleniumdata=self._libseleniumprovider.search(returndata)
            print("RESET_SELENIUM")

        elif state=="STATE_RUNNING_PROVIDERREAD" and phase=="SEARCH":
            search=self.selenium_instance.driver.find_element(By.XPATH,'//*[@id="topicnav"]/table/tbody/tr/td[3]/a').click()#詳細検索までの移動
            search=self.selenium_instance.driver.find_element(By.XPATH,'//*[@id="DetailedSearch"]/form/div[2]/table/tbody/tr[3]/td/nobr/input[2]').click()
            search=self.selenium_instance.driver.find_element(By.XPATH,'//*[@id="searchForm.keyword"]')
            search.send_keys('{}'.format(recogdata))
            search=self.selenium_instance.driver.find_element(By.XPATH,'//*[@id="DetailedSearch"]/form/div[2]/div/a[1]').click()
            if self.selenium_instance.driver.find_elements(By.XPATH,'//*[@id="DetailedSearch"]/form/table/tbody/tr[1]/td/font/ul/li'):#本がなかった時にTrue値を返す
                    self._d_controlesota.data="speaking"
                    self._controlesotaOut.write()
                    speech_synthesizer.speak_text("すみません見つかりませんでした。")
                    self._d_controlesota.data="neutral"
                    self._controlesotaOut.write()
                    returndata = datacode("STATE_RUNNING_CONSUMERREAD","ぴよ",command,"AGAIN")
                    seleniumdata=self._libseleniumprovider.search(returndata)
                    print(seleniumdata.state,seleniumdata.recogdata,seleniumdata.phase)

            elif self.selenium_instance.driver.find_elements(By.XPATH,'//*[@id="Booklist2"]/div[1]/span[2]'):#検索された本へ移動
                    search=self.selenium_instance.driver.find_element(By.XPATH,'//*[@id="BookListTable"]/table/tbody/tr[3]/td[5]/table[1]/tbody/tr/td/a').click()
                    returndata = datacode("STATE_RUNNING_CONSUMERREAD","ぴよ",command,"STAY_SEARCH")
                    seleniumdata=self._libseleniumprovider.search(returndata)
                    print(seleniumdata.state,seleniumdata.recogdata,seleniumdata.phase)
        elif state=="STATE_RUNNING_PROVIDERREAD" and phase=="STAY_SEARCH":
                time.sleep(10)
                self._d_controlesota.data="question"
                self._controlesotaOut.write()
                speech_synthesizer.speak_text("まだこの画面を見ますか")
                response=speech_recognizer.recognize_once_async().get()
                self._d_controlesota.data="neutral"
                self._controlesotaOut.write()
                if "はい" in response.text or "見ます" in response.text:
                    print(response.text)
                    returndata = datacode("STATE_RUNNING_CONSUMERREAD","ぴよ",command,"STAY_SEARCH")
                    seleniumdata=self._libseleniumprovider.search(returndata)
                    print(seleniumdata.state,seleniumdata.recogdata,seleniumdata.phase)                         
                else:
                    returndata = datacode("STATE_RUNNING_CONSUMERREAD","ぴよ",command,"AGAIN")
                    seleniumdata=self._libseleniumprovider.search(returndata)
                    print(seleniumdata.state,seleniumdata.recogdata,seleniumdata.phase)
                         


        elif state=="STATE_RUNNING_PROVIDERREAD" and phase=="RECOM":
            recommend=self.selenium_instance.driver.find_element(By.XPATH,'//*[@id="topicnav"]/table/tbody/tr/td[3]/a').click()#詳細検索までの移動
            recommend=self.selenium_instance.driver.find_element(By.XPATH,'//*[@id="DetailedSearch"]/form/div[2]/table/tbody/tr[3]/td/nobr/input[2]').click()
            recommend=self.selenium_instance.driver.find_element(By.XPATH,'//*[@id="searchForm.keyword"]')
            recommend.send_keys('{}'.format(recogdata))
            recommend=self.selenium_instance.driver.find_element(By.XPATH,'//*[@id="DetailedSearch"]/form/div[2]/div/a[1]').click()
            if self.selenium_instance.driver.find_elements(By.XPATH,'//*[@id="DetailedSearch"]/form/table/tbody/tr[1]/td/font/ul/li'):#本がなかった時にTrue値を返す
                self._d_controlesota.data="speaking"
                self._controlesotaOut.write()
                speech_synthesizer.speak_text("すみません見つかりませんでした")
                self._d_controlesota.data="neutral"
                self._controlesotaOut.write()
                returndata = datacode("STATE_RUNNING_CONSUMERREAD","ぴよ",command,"AGAIN")
                seleniumdata=self._libseleniumprovider.search(returndata)
                print(seleniumdata.state,seleniumdata.recogdata,seleniumdata.phase)
                
            
            elif self.selenium_instance.driver.find_elements(By.XPATH,'//*[@id="Booklist2"]/div[1]/span[2]'):#おすすめの本があったとき
                recommendtext=self.selenium_instance.driver.find_elements(By.XPATH,'//*[@id="Booklist2"]/div[1]/span[2]')[0].text#何件あるかをstrに変換
                recommendtext1=recommendtext.replace('1件目から','')#（１件目からX件を表示中）のXを取り出してintに格納
                bookcounter=recommendtext1.replace('件を表示中','')
                error=0
                randomexclusion=[]
                def randomf():
                    counter=0 
                    while counter<1:
                        i=random.randint(3,int(bookcounter)+2)
                        if not i in randomexclusion:
                            randomexclusion.append(i)
                            counter=1
                            time.sleep(0.5)
                    recommend=self.selenium_instance.driver.find_element(By.XPATH,'//*[@id="BookListTable"]/table/tbody/tr['+str(i)+']/td[5]/table[1]/tbody/tr/td/a').click()
                    print(i)
                    flag = False
                    for k in range(5,15,1):
                        item = self.selenium_instance.driver.find_element(By.XPATH, '//*[@id="detailTblArea"]/table/tbody/tr[' + str(k) + ']/td[1]')
                        if '書名' in item.text:
                            bookTitleAndAuthors = self.selenium_instance.driver.find_element(By.XPATH, '//*[@id="detailTblArea"]/table/tbody/tr[' + str(k) + ']/td[2]/font/span')
                            flag = True
                            break
                    if flag:
                        items = bookTitleAndAuthors.text.split('/')
                        bookTitle = items[0]
                        self._d_controlesota.data="speaking"
                        self._controlesotaOut.write()
                        speech_synthesizer.speak_text_async(bookTitle + 'をお勧めします。')
                        self._d_controlesota.data="neutral"
                        self._controlesotaOut.write()
                try:
                    randomf()
                except:
                    speech_synthesizer.speak_text("すみません見つかりませんでした")
                    self._d_controlesota.data="neutral"
                    self._controlesotaOut.write()
                    returndata = datacode("STATE_RUNNING_CONSUMERREAD","ぴよ",command,"AGAIN")
                    seleniumdata=self._libseleniumprovider.search(returndata)
                    print(seleniumdata.state,seleniumdata.recogdata,seleniumdata.phase)
                    error=1

                counterE=0
                time.sleep(5)
                while (counterE<int(bookcounter) and error!=1):
                        returndata = datacode("STATE_RUNNING_CONSUMERREAD","ぴよ",command,"RECOM_REPEAT")
                        seleniumdata=self.seleniumprovider(returndata)
                        if seleniumdata.phase=="STOP":
                            break
                        self._d_controlesota.data="question"
                        self._controlesotaOut.write()
                        speech_synthesizer.speak_text("他の本がよろしいですか？")
                        response=speech_recognizer.recognize_once_async().get()
                        self._d_controlesota.data="neutral"
                        self._controlesotaOut.write()
                        if ("はい"in str(response) or "します" in str(response)) and int(bookcounter)!=1:
                            self.selenium_instance.driver.get('https://library.konan-u.ac.jp/')
                            recommend=self.selenium_instance.driver.find_element(By.XPATH,'//*[@id="topicnav"]/table/tbody/tr/td[3]/a').click()#詳細検索までの移動
                            recommend=self.selenium_instance.driver.find_element(By.XPATH,'//*[@id="DetailedSearch"]/form/div[2]/table/tbody/tr[3]/td/nobr/input[2]').click()
                            recommend=self.selenium_instance.driver.find_element(By.XPATH,'//*[@id="searchForm.keyword"]')
                            recommend.send_keys('{}'.format(recogdata))
                            recommend=self.selenium_instance.driver.find_element(By.XPATH,'//*[@id="DetailedSearch"]/form/div[2]/div/a[1]').click()
                            try:
                                randomf()
                            except:
                                speech_synthesizer.speak_text("すみません見つかりませんでした")
                                self._d_controlesota.data="neutral"
                                self._controlesotaOut.write()
                                returndata = datacode("STATE_RUNNING_CONSUMERREAD","ぴよ",command,"AGAIN")
                                seleniumdata=self._libseleniumprovider.search(returndata)
                                print(seleniumdata.state,seleniumdata.recogdata,seleniumdata.phase)
                                break
                            time.sleep(5)
                            counterE+=1
                        else:
                                returndata = datacode("STATE_RUNNING_CONSUMERREAD","ぴよ",command,"STAY_SEARCH")
                                seleniumdata=self._libseleniumprovider.search(returndata)
                                print(seleniumdata.state,seleniumdata.recogdata,seleniumdata.phase)
                                break                     
                        if counterE==int(bookcounter)-1:
                            time.sleep(5)
                            self._d_controlesota.data="question"
                            self._controlesotaOut.write()
                            speech_synthesizer.speak_text("別の本を検索しますか？")
                            response=speech_recognizer.recognize_once_async().get()
                            self._d_controlesota.data="neutral"
                            self._controlesotaOut.write()
                            if "はい"in str(response) or "します" in str(response) or "します" in str(response):
                                self._d_controlesota.data="question"
                                self._controlesotaOut.write()
                                speech_synthesizer.speak_text("すみません見つかりませんでした")
                                self._d_controlesota.data="neutral"
                                self._controlesotaOut.write()
                                returndata = datacode("STATE_RUNNING_CONSUMERREAD","ぴよ",command,"STAY_SEARCH")
                                seleniumdata=self._libseleniumprovider.search(returndata)
                                print(seleniumdata.state,seleniumdata.recogdata,seleniumdata.phase)        
                                break
                            else:
                                returndata = datacode("STATE_RUNNING_CONSUMERREAD","ぴよ",command,"STAY_SEARCH")
                                seleniumdata=self._libseleniumprovider.search(returndata)
                                print(seleniumdata.state,seleniumdata.recogdata,seleniumdata.phase)
                                break  
        elif state=="STATE_RUNNING_PROVIDERREAD" and phase=="CERTIFICATE":
            self._d_controlesota.data="speaking"
            self._controlesotaOut.write()
            speech_synthesizer.speak_text("ライブラリーサーティフィケイトについてですね。これは、成績には現れない力を評価する制度、甲南サーティフィケイトの１つです。図書館情報を活用する技能に優れ、図書館を使いこなして問題を解決する力を有すると評価された学生に、ライブラリーサーティフィケイトを授与します。まずはエントリーをしてください。")
            self._d_controlesota.data="neutral"
            self._controlesotaOut.write()
            self._d_controlesota.data="question"
            self._controlesotaOut.write()
            speech_synthesizer.speak_text("エントリーしますか")
            response=speech_recognizer.recognize_once_async().get()
            self._d_controlesota.data="neutral"
            self._controlesotaOut.write()
            if "はい" in str(response) or "します" in str(response) or "お願い" in str(response):

                self._d_controlesota.data="speaking"
                self._controlesotaOut.write()
                speech_synthesizer.speak_text_async("図書館職員さんをお呼びします。職員さんが来るまでライブラリーサーティフィケイトのホームページを見てお待ちください。")
                self._d_controlesota.data="neutral"
                self._controlesotaOut.write()
                self.selenium_instance.driver.get("https://www.konan-u.ac.jp/lib/?page_id=1583")
                returndata = datacode("STATE_RUNNING_CONSUMERREAD","ぴよ",command,"CALLSTAFF")
                seleniumdata=self._libseleniumprovider.search(returndata)
                print(seleniumdata.state,seleniumdata.recogdata,seleniumdata.phase)
            elif "いいえ" in str(response) or "しません" in str(response):
                self._d_controlesota.data="speaking"
                self._controlesotaOut.write()
                speech_synthesizer.speak_text("わかりました。")
                self._d_controlesota.data="neutral"
                self._controlesotaOut.write()
                returndata = datacode("STATE_RUNNING_CONSUMERREAD","ぴよ",command,"AGAIN")
                seleniumdata=self._libseleniumprovider.search(returndata)
                print(seleniumdata.state,seleniumdata.recogdata,seleniumdata.phase)      


    
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
	



def seleniumInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=selenium_spec)
    manager.registerFactory(profile,
                            selenium,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    seleniumInit(manager)

    # create instance_name option for createComponent()
    instance_name = [i for i in sys.argv if "--instance_name=" in i]
    if instance_name:
        args = instance_name[0].replace("--", "?")
    else:
        args = ""
  
    # Create a component
    comp = manager.createComponent("selenium" + args)

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

