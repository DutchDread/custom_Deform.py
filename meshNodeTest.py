#customNode.py

import math, sys
import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx
import random

kPluginNodeTypeName = "asRandomNode"

randomNodeId = OpenMaya.MTypeId(0x87300)

class randomNode(OpenMayaMPx.MPxNode):

    def __init__(self):
            print ("initializing randomnode __init__")
            OpenMayaMPx.MPxNode.__init__(self)
                
    def compute(self, plug, dataBlock):                   
            if ( plug == randomNode.inMesh):                                        # if changed plug is inMesh
                    inputMeshData = dataBlock.inputValue( randomNode.inMesh )      
                    inputAsMesh = OpenMaya.MFnMesh(inputMeshData.asMesh())   
                   
                    mPoint = OpenMaya.MPointArray()
                    mSpace = OpenMaya.MSpace.kObject                    
                    pointPos = [] 
                    inputAsMesh.getPoints(mPoint, mSpace)
                    
                    
                    
                    for x in range(0, mPoint.length()):
                        pointPos.append([mPoint[x][0], mPoint[x][1], mPoint[x][2]])
                    
                    l = 0 
                    for p in pointPos:
                        v = 0
                        for i in xrange(len(p)):
                            pointPos[l][v] *= 2
                            v += 1
                        l += 1
                        
      
                    newMesh_array = OpenMaya.MPointArray()
                    for vert in pointPos:
                        newMesh_array.append(*vert)
                                         
                    #Generate the framework for the outcome mesh.
                    dataCreator = OpenMaya.MFnMeshData()
                    outputData = dataCreator.create()
                    meshFn = OpenMaya.MFnMesh()
                    
                    meshFn.copy(inputMeshData.asMesh(), outputData)
                    
                    meshFn.setPoints(newMesh_array, mSpace)
                    
                    
                    #Set the output mesh
                    outputHandle = dataBlock.outputValue( randomNode.outMesh )
                    outputHandle.setMObject(outputData)
                    
                    #clean the data Block
                    dataBlock.setClean( plug )
                    
            elif plug ==(randomNode.outMesh) :                                      #if plug is outMesh
                  
                    inputMeshData = dataBlock.inputValue( randomNode.inMesh )      
                    inputAsMesh = OpenMaya.MFnMesh(inputMeshData.asMesh())   
                   
                    mPoint = OpenMaya.MPointArray()
                    mSpace = OpenMaya.MSpace.kObject                    
                    pointPos = [] 
                    inputAsMesh.getPoints(mPoint, mSpace)
                    
                    
                    
                    for x in range(0, mPoint.length()):
                        pointPos.append([mPoint[x][0], mPoint[x][1], mPoint[x][2]])
                    
                    l = 0 
                    for p in pointPos:
                        v = 0
                        for i in xrange(len(p)):
                            pointPos[l][v] *= 2
                            v += 1
                        l += 1
                        
      
                    newMesh_array = OpenMaya.MPointArray()
                    for vert in pointPos:
                        newMesh_array.append(*vert)
                                         
                    #Generate the framework for the outcome mesh.
                    dataCreator = OpenMaya.MFnMeshData()
                    outputData = dataCreator.create()
                    meshFn = OpenMaya.MFnMesh()
                    
                    meshFn.copy(inputMeshData.asMesh(), outputData)
                    
                    meshFn.setPoints(newMesh_array, mSpace)
                    
                    
                    #Set the output mesh
                    outputHandle = dataBlock.outputValue( randomNode.outMesh )
                    outputHandle.setMObject(outputData)
                    
                    #clean the data Block
                    dataBlock.setClean( plug )
                                                                                            
            else:
                return OpenMaya.kUnknownParameter
                
def nodeCreator():
        return OpenMayaMPx.asMPxPtr( randomNode() )
        

def nodeInitializer():
        print ('starting node initialiser')
        #define Inputs
        #nAttr = OpenMaya.MFnNumericAttribute()
        #randomNode.inputY = nAttr.create( "inputY", "inY", OpenMaya.MFnNumericData.kFloat, 0.0 )
        #nAttr.setStorable( 1 )
        #nAttr.setWritable( 1 )
        
        
        print ("setting inmesh")
        nAttr = OpenMaya.MFnTypedAttribute()
        randomNode.inMesh = nAttr.create( "inMesh", "in", OpenMaya.MFnData.kMesh)
        nAttr.setStorable( 1 )
        nAttr.setWritable( 1 )
        
        #define Outputs
        
        print ("setting outmesh")
        nAttr = OpenMaya.MFnTypedAttribute()
        randomNode.outMesh = nAttr.create( "outMesh", "out", OpenMaya.MFnData.kMesh)
        nAttr.setStorable( 0 )
        nAttr.setWritable( 0 )
        
        #nAttr = OpenMaya.MFnNumericAttribute()
        #randomNode.outputX = nAttr.create( "outputX", "outX", OpenMaya.MFnNumericData.kFloat, 0.0 )
        #nAttr.setStorable( 0 )
        #nAttr.setWritable( 0 )
        
        
        #Add attributes to the node
        
        print("adding in attributes")
        randomNode.addAttribute( randomNode.inMesh )

        print("adding out attributes") 
        randomNode.addAttribute( randomNode.outMesh )
                
        #Set attibute dependencies/dependencies, determines when something needs to be recomputed
        print("setting affectors")
        randomNode.attributeAffects( randomNode.inMesh, randomNode.outMesh)


def initializePlugin(mobject):
        print ("initializing plugin")
        mplugin = OpenMayaMPx.MFnPlugin( mobject )
        try:
                mplugin.registerNode( kPluginNodeTypeName, randomNodeId, nodeCreator, nodeInitializer )
                print("registernode success")                 
        except:
                sys.stderr.write( "Failed to register node: %s" % kPluginNodeTypeName )
                raise

def uninitializePlugin(mobject):
        mplugin = OpenMayaMPx.MFnPlugin(mobject)
        try:
                mplugin.deregisterNode( randomNodeId)
        except:
                sys.stderr.write( "Failed to deregister node: %s" % kPluginNoseTypeName )
                raise
                
        
                 