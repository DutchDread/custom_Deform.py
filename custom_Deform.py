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
from maya import OpenMayaMPx
from nodeFactory import (NT_DEPENDSNODE, float_input, float_output, create_node)

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


def register_stressNode(plugin):
    inputnames = ['input', 'scale', 'frames']
    reg, dereg = create_node(NT_DEPENDSNODE, 'circler', 0x60005, [
        float_input('input', 'in'),
        float_input('scale', 'sc', default=10.0),
        float_input('frames', 'fr', default=48.0),
        float_output(
            'outSine', 'so',
            affectors=inputnames,
            transformer=sin),
        float_output(
            'outCosine', 'co',
            affectors=inputnames,
            transformer=cosine),
    ])
    reg(plugin)
    _deregister_funcs.append(dereg)

def _toplugin(mobject):
    return OpenMayaMPx.MFnPlugin(mobject, 'Marcus Reynir', '0,01')

def initializePlugin(mobject):
    plugin = _toplugin(mobject)
    register_stressNode(plugin)

def uninitializePlugin(mobject):
    plugin = _toplugin(mobject)
    for func in _deregister_funcs:
        func(plugin)
