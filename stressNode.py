# Creates custom nodes by making use of custom nodeFactory.py script

# from nodefactory import create_attr, A_FLOAT
# def init():
#     create_attr(Circler, A_FLOAT, 'input', 'in')
#     create_attr(Circler, A_FLOAT, 'scale', 'sc', default=10.0)
#     create_attr(Circler, A_FLOAT, 'frames', 'fr', default=48.0)
#     inputnames = ['input', 'scale', 'frames']
#     create_attr(Circler, A_FLOAT, 'outSine', 'so', inputnames)
#     create_attr(Circler, A_FLOAT, 'outCosine', 'co', inputnames)

import math
from maya import OpenMayaMPx, OpenMaya
from nodeFactory import (NT_DEPENDSNODE, mesh_input, mesh_output, create_node)
import traceback
_deregister_funcs = []

# def floatattr(*args, **kwargs):
#     return create_attrmaker(A_FLOAT, *args, **kwargs)

def make_transformer(mathfunc):
    def inner(input, scale, frames):
        angle = 6.2831853 * (input / frames)
        return mathfunc(angle) * scale
    return inner
sin = make_transformer(math.sin)
cosine = make_transformer(math.cos)


def make_deformer():
    """code for de deformation to be added"""
    def final(base, deformer, blend):
        outputData = base
        try:
            mSpace = OpenMaya.MSpace.kObject

            base_asMesh = OpenMaya.MFnMesh(base.asMesh())
            #get input data as pointarray
            base_mPoint = OpenMaya.MPointArray()
            base_pointPos = []
            try:
                base_asMesh.getPoints(base_mPoint, mSpace)
            except:
                traceback.print_stack()

            print('length: {}'.format(base_mPoint.length()))
            for x in range(0, base_mPoint.length()):
                base_pointPos.append([base_mPoint[x][0], base_mPoint[x][1], base_mPoint[x][2]])

            deformer_asMesh = OpenMaya.MFnMesh(deformer.asMesh())
            deformer_mPoint = OpenMaya.MPointArray()
            deformer_pointPos = []
            deformer_asMesh.getPoints(deformer_mPoint, mSpace)

            for x in range(0, deformer_mPoint.length()):
                deformer_pointPos.append([deformer_mPoint[x][0], deformer_mPoint[x][1], deformer_mPoint[x][2]])

            blend_asMesh = OpenMaya.MFnMesh(blend.asMesh())
            blend_mPoint = OpenMaya.MPointArray()
            blend_pointPos = []
            blend_asMesh.getPoints(blend_mPoint, mSpace)

            for x in range(0, blend_mPoint.length()):
                blend_pointPos.append([blend_mPoint[x][0], blend_mPoint[x][1], blend_mPoint[x][2]])

            #Add our values together
            for p in range(0, len(base_pointPos)):
                base_pointPos[p] = [a + b + c for a, b, c in zip(base_pointPos[p], blend_pointPos[p], deformer_pointPos[p])]

            #Create a new pointarray to hold our new values in
            newMesh_array = OpenMaya.MPointArray()
            for vert in base_pointPos:
                newMesh_array.append(*vert)

            print("about to break?")
            #create meshdata object to set to output value
            dataCreator = OpenMaya.MFnMeshData()
            outputData = dataCreator.create()

            #create mesh instance, set it to operate on it
            meshFn = OpenMaya.MFnMesh()

            meshFn.copy(base.asMesh(), outputData)
            meshFn.setPoints(newMesh_array, mSpace)

            return outputData

        except Exception as e:
            print (str(e))
            traceback.print_stack()
        finally:
            return outputData
    return final

skinDeform = make_deformer()  #I think this is just returning a specific math function that is executed?


def register_stressNode(plugin):
    inputnames = ['base', 'deformed', 'blend']
    reg, dereg = create_node(NT_DEPENDSNODE, 'stressNode', 0x60006, [
        mesh_input('base', 'bs'),
        mesh_input('deformed', 'df'),
        mesh_input('blend', 'bl'),
        mesh_output(
            'outMesh', 'om',
            affectors=inputnames,
            transformer=skinDeform),
    ])
    reg(plugin)
    _deregister_funcs.append(dereg)

def _toplugin(mobject):
    return OpenMayaMPx.MFnPlugin(mobject, 'vendor', 'version')

def initializePlugin(mobject):
    plugin = _toplugin(mobject)
    register_stressNode(plugin)

def uninitializePlugin(mobject):
    plugin = _toplugin(mobject)
    for func in _deregister_funcs:
        func(plugin)                   # Bunch of deregister functions are run with "_toplugin(mobject)" as an argument.
