from maya import OpenMaya, OpenMayaMPx
import traceback

class AttrSpec(object):
    def attributetype(self):
        print ("not imp 1")
        raise NotImplementedError()
    def getvalue(self, datahandle):
        print ("not imp 2")
        raise NotImplementedError()
    def setvalue(self, datahandle, value):
        print ("not imp 3")
        raise NotImplementedError()
    def create(self, fnattr, longname, shortname):
        print ("not imp 4")
        raise NotImplementedError()
    def setdefault(self,fnattr, value):
        print ("not imp 5")
        raise NotImplementedError()
    def allow_fields(self):
        return False
    def valuetype(self):
        print ("not imp 6")
        raise NotImplementedError()


class _FloatAttr(AttrSpec):
    def attributetype(self):
        return OpenMaya.MFnNumericAttribute()
    def getvalue(self,datahandle):
        return datahandle.asFloat()
    def setvalue(self, datahandle, value):
        datahandle.setFloat(value)
    def create(self, fnattr, longname, shortname):
        return fnattr.create(longname, shortname, OpenMaya.MFnNumericData.kFloat)
    def setdefault(self, fnattr, value):
        fnattr.setDefault(value)
A_FLOAT = _FloatAttr()

class _StringAttr(AttrSpec):
    def attributetype(self):
        return OpenMaya.MFnTypedAttribute()
    def getvalue(self, datahandle):
        return datahandle.asString()
    def setvalue(self, datahandle, value):
        datahandle.setString(value)
    def create(self, fnattr, longname, shortname):
        return fnattr.create(longname, shortname,
                             OpenMaya.MFnData.kString)
    def setdefault(self, fnattr, value):
        fnattr.setDefault(OpenMaya.MFnStringData().create(value))
A_STRING = _StringAttr()

class _EnumAttr(AttrSpec):
    def attributetype(self):
        return OpenMaya.MFnEnumAttribute()
    def getvalue(self, datahandle):
        return datahandle.asInt()
    def setvalue(self, datahandle, value):
        datahandle.setInt(value)
    def create(self, fnattr, longname, shortname):
        return fnattr.create(longname, shortname)
    def setdefault(self, fnattr, value):
        fnattr.setDefault(value)
    def allow_fields(self):
        return True
A_ENUM = _EnumAttr()

class _ColorAttr(AttrSpec):
    def attributetype(self):
        return OpenMaya.MFnNumericAttribute()
    def getvalue(self, datahandle):
        return datahandle.asFloatVector()
    def setvalue(self, datahandle, value):
        datahandle.setMFloatVector(OpenMaya.MFloatVector(*value))
    def create(self, fnattr, longname, shortname):
        return fnattr.createColor(longname, shortname)
    def setdefault(self, fnattr, value):
        fnattr.setDefault(*value)
A_COLOR = _ColorAttr()

# class _MatrixAttr(AttrSpec):
#     def attributetype(self):
#         return OpenMaya.MFnMatrixAttribute()
#     def getValue(self, datahandle):
#         return datahandle.asMesh()
#     def setValue(self, datahandle, value):
#         raise NotImplementedError()
#     def create(self, fnattr, longname, shortname):      #requires ,om.MFnData.kMesh perhaps?
#         return fnattr.create(longname, shortname)
#
# A_MATRIX = _MatrixAttr()

class _MeshAttr(AttrSpec):
    def attributetype(self):
        return OpenMaya.MFnTypedAttribute()
    def getvalue(self, datahandle):
        return datahandle
    def setvalue(self, datahandle, meshObject):
        return datahandle.setMObject(meshObject)
    def create(self, fnattr, longname, shortname):
        print ("initializing A_MESH.create")
        return fnattr.create(longname, shortname, OpenMaya.MFnData.kMesh)
    def valuetype(self):
        return OpenMaya.MFnData.kMesh

A_MESH = _MeshAttr()                    #variable holding the outcome of _MeshAttr(AttrSpec), which is a function.


class NodeSpec(object):
    def nodebase(self):
        raise NotImplementedError()
    def register(self, fnplugin, typename, typeid, create, init):
        raise NotImplementedError()
    def deregister(self, fnplugin, typeid):
        raise NotImplementedError()

class _DependsNode(NodeSpec):
    def nodebase(self):
        return (OpenMayaMPx.MPxNode,)
    #def _nodetype(self):
        #return OpenMayaMPx.MPxNode.kDependNode
    def register(self, fnplugin, typename, typeid, create, init):
        #fnplugin.registerNode(typename, typeid, create, init, self._nodetype())
        fnplugin.registerNode(typename, typeid, create, init,
                              OpenMayaMPx.MPxNode.kDependNode)
    def deregister(self, fnplugin, typeid):
        fnplugin.deregisterNode(typeid)
NT_DEPENDSNODE = _DependsNode()

# def create_attr(nodeclass, attrspec, ln, san, affectors=(), default=None):
#     attr = attrspec.attributetype() #1
#     plug = attrspec.create(attr, ln, sn) #2
#
#     if default is not None:
#         attrspec.setdefault(attr, default)
#
#     isinput = not bool(affectors)
#     attr.setWritable(isinput)
#     attr.setStorable(isinput)
#
#     nodeclass.addAttribute(plug)
#     setattr(nodeclass, ln, sn, plug)
#
#     for affectedby in affectors:
#         inattrobj = getattr(nodeclass, affectedby)
#         nodeclass.attributeAffects(inattrobj, attrobj)

class _TransformNode(NodeSpec):
    xform_typeid = OpenMaya.MTypeId(0x60080)
    class TransformMatrix(OpenMayaMPx.MPxTransformationMatrix):
        pass
    def nodebase(self):
        return (OpenMayaMPx.MPxTransform,)
    def _make_node_matrix(self):
        return OpenMayaMPx.asMPxPtr(TransformMatrix())
    def register(self, fnplugin, typename, typeid, create, init):
        fnplugin.registerTransform(
            typename, typeid, create, init,
            self._make_node_matrix, self.xform_typeid)
    def deregister(self, fnplugin, typeid):
        fnplugin.deregisterNode(typeid)
NT_TRANSFORMNODE = _TransformNode()

def create_attrmaker(attrspec, ln, sn, affectors=(), default=None, transformer=None, fields=()):
    print ("attrspec: {}".format(str(attrspec)))
    if not attrspec.allow_fields() and fields:
        raise RuntimeError('Fields not allowed for {}'.format(attrspec))


    def createattr(nodeclass):
        fnattr = attrspec.attributetype()
        print ("initializing attr creation")
        attrobj = attrspec.create(fnattr, ln, sn )

        for name, value in fields:
            fnattr.addField(name,value)

        if default is not None:
            attrspec.setdefault(fnattr, default)

        isinput = not bool(affectors)
        fnattr.setWritable(isinput)
        fnattr.setStorable(isinput)
        if not isinput and transformer is None:
            raise RuntimeError('must specify transformer.')

        nodeclass.addAttribute(attrobj)
        setattr(nodeclass, ln, attrobj)

        for affectedby in affectors:
            inputplug = getattr(nodeclass, affectedby)
            nodeclass.attributeAffects(inputplug, attrobj)

        return ln, attrspec, transformer, affectors
    return createattr

def float_input(ln, sn, **kwargs):
    return create_attrmaker(A_FLOAT, ln, sn, **kwargs)

def float_output(ln, sn, **kwargs):
    return create_attrmaker(A_FLOAT, ln, sn, **kwargs)

def mesh_input(ln, sn, **kwargs):
    print ("initializing mesh input")
    try:
        return create_attrmaker(A_MESH, ln, sn, **kwargs)
    except:
        traceback.print_stack()

def mesh_output(ln, sn, **kwargs):
    try:
        return create_attrmaker(A_MESH, ln,sn, **kwargs)
    except:
        traceback.print_stack()

def create_node(nodespec, name, typeid, attrmakers):
    print ("initializing create node")
    attr_to_spec = {}
    outattr_to_xformdata = {}

    def compute(mnode, plug, datablock):
        try:
            attrname = plug.name().split('.')[-1]               #holds attribute long name as key: Spec as attribute
            xformdata = outattr_to_xformdata.get(attrname)      #outattribute long name as key, [transformer, affectors]
                                                                # as tuple
        except:
            traceback.print_stack()

        try:
            if xformdata is None:
                return OpenMaya.MStatus.kUnknownParameter       # this is not gonna work, outdated, switch to exception
        except:
            traceback.print_stack()

        try:
            xformer, affectors = xformdata
            invals = []
            for inname in affectors:
                inplug = getattr(nodetype, inname)
                indata = datablock.inputValue(inplug)
                try:
                    inval = attr_to_spec[inname].getvalue(indata)
                except Exception as e:
                    print(e)
                    traceback.print_stack()
                invals.append(inval)
        except:
            traceback.print_stack()

        try:
            outval = xformer(*invals)
            outhandle = datablock.outputValue(plug)

        except:
            traceback.print_stack()

        try:
            attr_to_spec[attrname].setvalue(outhandle, outval)
            datablock.setClean(plug)
        except Exception as e:
            print (e)
            print(attr_to_spec[attrname].setvalue(outhandle, outval))
            traceback.print_stack()

    methods = {'compute': compute}
    nodetype = type(name, nodespec.nodebase(), methods)

    mtypeid = OpenMaya.MTypeId(typeid)
    def creator():
        return OpenMayaMPx.asMPxPtr(nodetype())
    def init():
        for makeattr in attrmakers:
            ln, attrspec, xformer, affectors = makeattr(nodetype)
            attr_to_spec[ln] = attrspec
            if xformer is not None:
                outattr_to_xformdata[ln] = xformer, affectors

    def register(plugin):
        nodespec.register(plugin, name, mtypeid, creator, init)
    def deregister(plugin):
        nodespec.deregister(plugin, mtypeid)
    return register, deregister
