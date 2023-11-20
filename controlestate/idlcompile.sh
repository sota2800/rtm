#!/bin/sh
IDL_PATH=`rtm-config --rtm-idldir`
omniidl -bpython -I$IDL_PATH idl/facedetection.idl idl/select.idl idl/voicerecog.idl idl/selenium.idl 