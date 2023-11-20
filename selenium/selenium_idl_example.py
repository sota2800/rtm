#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

"""
 @file selenium_idl_example.py
 @brief Python example implementations generated from selenium.idl
 @date $Date$


"""

import omniORB
from omniORB import CORBA, PortableServer
import Library, Library__POA
class datacode:
    def __init__(self,state,recogdata,command,phase):
        self.state=state
        self.recogdata=recogdata
        self.command=command
        self.phase=phase



class seleniumdata_i (Library__POA.seleniumdata):
    """
    @class seleniumdata_i
    Example class implementing IDL interface Library.seleniumdata
    """

    def __init__(self):
        """
        @brief standard constructor
        Initialise member variables here
        """
        self.state="NUM"
        self.recogdata="ぴよ"
        self.command="NUM"
        self.phase="NUM"
        pass

    # Dataset setresult(in string data)
    def setresult(self, data):
        #raise CORBA.NO_IMPLEMENT(0, CORBA.COMPLETED_NO)
        # *** Implement me
        # Must return: result
        data1=datacode(self.state,self.recogdata,self.command,self.phase)
        return data1

    # Dataset search(in Dataset data)
    def search(self, data):
        #raise CORBA.NO_IMPLEMENT(0, CORBA.COMPLETED_NO)
        # *** Implement me
        # Must return: result
        self.state=data.state
        self.recogdata=data.recogdata
        self.command=data.command
        self.phase=data.phase
        return data
    def getdata(self):
        data=datacode(self.state,self.recogdata,self.command,self.phase)
        return data

    # Dataset recom(in Dataset data)
    def recom(self, data):
        #raise CORBA.NO_IMPLEMENT(0, CORBA.COMPLETED_NO)
        # *** Implement me
        # Must return: result
        self.state=data.state
        self.recogdata=data.recogdata
        self.command=data.command
        self.phase=data.phase
        return data

    # Dataset certificate(in Dataset data)
    def certificate(self, data):
        #raise CORBA.NO_IMPLEMENT(0, CORBA.COMPLETED_NO)
        # *** Implement me
        # Must return: result
        self.state=data.state
        self.recogdata=data.recogdata
        self.command=data.command
        self.phase=data.phase
        return data

    # Dataset seleniumadditionalfunction(in Dataset data)
    def seleniumadditionalfunction(self, data):
        raise CORBA.NO_IMPLEMENT(0, CORBA.COMPLETED_NO)
        # *** Implement me
        # Must return: result


if __name__ == "__main__":
    import sys
    
    # Initialise the ORB
    orb = CORBA.ORB_init(sys.argv)
    
    # As an example, we activate an object in the Root POA
    poa = orb.resolve_initial_references("RootPOA")

    # Create an instance of a servant class
    servant = seleniumdata_i()

    # Activate it in the Root POA
    poa.activate_object(servant)

    # Get the object reference to the object
    objref = servant._this()
    
    # Print a stringified IOR for it
    print(orb.object_to_string(objref))

    # Activate the Root POA's manager
    poa._get_the_POAManager().activate()

    # Run the ORB, blocking this thread
    orb.run()

