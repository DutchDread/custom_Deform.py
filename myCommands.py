import maya.OpenMaya as OpenMaya
import maya.cmds as cmds
import random
import pymel.core as pms


"""
Set of functions for maya, for personal use, uses OpenMaya as wrapper.
"""


def getGeoPointPosition(geoObj, space='worldSpace'):
    """
        Takes a selectionlist Object, gives you the vertex positions of the first index in the selectionlist.
    In order to get selectionlist of currently selected objects type:
        selec = OpenMaya.MSelectionList()
        OpenMaya.MGlobal.getActiveSelectionList(selec)

    :param geoObj: selectionList object
    :param space: string, returns coordinates in 'localSpace' or 'worldSpace'

    :return array of vertex positions
    """
    #Create an empty objects/variables to store positions, functionSet and space
    mPoint = OpenMaya.MPointArray()
    mSpace = None
    pointPos = []

    #Get which space it should return the positions in (localSpace/worldSpace)
    if space == 'localSpace':
        mSpace = OpenMaya.MSpace.kObject
    elif space == 'worldSpace':
        mSpace = OpenMaya.MSpace.kWorld

    #Attach a MFnMesh functionSet and get the positions
    DP = OpenMaya.MDagPath()
    geoObj.getDagPath(0,DP)
    mFnSet = OpenMaya.MFnMesh(DP)
    mFnSet.getPoints(mPoint, mSpace)

    #For each vertex/CV of the object
    for x in range(0, mPoint.length()):
        #Append the current vertex position to the list
        pointPos.append([mPoint[x][0], mPoint[x][1], mPoint[x][2]])

    #Return the positions
    return pointPos



def setGeoPointPos(geoObj, positions=[], space='worldSpace'):
    """
    Takes in a selectionList object and an array of vertex positions. Applies the positions to the first object
    in the selectionList.

    :param geoObj: selectionList object
    :param positions: array of vertex locations.
    :param space: string, pushes coordinates in 'localSpace' or 'worldSpace'
    :return: None
    """

    #Create an empty objects/variables to store positions, functionSet and space
    mPoint = OpenMaya.MPointArray()
    mSpace = None
    #Add the list to the MPointArray

    newMesh_array = OpenMaya.MPointArray()
    for vert in positions:
        newMesh_array.append(*vert)


    #Get which space it should return the positions in (localSpace/worldSpace)
    if space == 'localSpace':
        mSpace = OpenMaya.MSpace.kObject
    elif space == 'worldSpace':
        mSpace = OpenMaya.MSpace.kWorld

    #Attach a MFnMesh functionSet and set the positions
    DP = OpenMaya.MDagPath()
    geoObj.getDagPath(0,DP)
    mFnSet = OpenMaya.MFnMesh(DP)
    mFnSet.setPoints(newMesh_array, mSpace)


    #Return the positions
    return None

def getSelect():
    """Returns your current selection.

    :return MSelectList object containing your selection
    """
    selec = OpenMaya.MSelectionList()
    OpenMaya.MGlobal.getActiveSelectionList(selec)
    return selec


def doubleSize(geoList):
    """
    Doubles all floats in an array. Used to test other functions.

    :param :takes an array of vertex locations (a list of lists).

    """
    l = 0
    for p in geoList:
        v = 0
        for i in xrange(len(p)):
            geoList[l][v] *= 2
            v += 1
        l += 1
        print (p)
    return geoList


def getDagPath():
    """
    Returns dagPath of selected object
    """

    selec = OpenMaya.MSelectionList()
    OpenMaya.MGlobal.getActiveSelectionList(selec)
    DP = OpenMaya.MDagPath()
    selec.getDagPath(0, DP)
    print (DP.fullPathName())
    return DP

def viewNotes(string):
    """
    gives a few quick reminders on how to use this library and related functions.
    input a string for reminders on the subject.
    Options are:
    'nodes'

    """
    if string == 'nodes':
        print("""
        To create nodes in cmds: 
        import maya.cmds as cmds
        cmds.createNode('name of the type of node you want to create')
        """)

# aimAtFirst.py

import maya.cmds as cmds

selectionList = cmds.ls( orderedSelection=True )

if len( selectionList ) >= 2:

    print 'Selected items: %s' % ( selectionList )

    targetName = selectionList[0]

    selectionList.remove( targetName )

    for objectName in selectionList:

        print 'Constaining %s towards %s' % ( objectName, targetName )

        cmds.aimConstraint( targetName, objectName, aimVector=[0, 1, 0] )

else:

    print 'Please select two or more objects.'

#========================================================================================================
""" starts using maya.cmds from here"""
# aimAtFirst.py

def aimAtFirst():
    """
    puts an aim constraint on all selected objects save the first, aims them all at the first.
    """
    selectionList = cmds.ls( orderedSelection=True )

    if len( selectionList ) >= 2:

        print 'Selected items: %s' % ( selectionList )

        targetName = selectionList[0]

        selectionList.remove( targetName )

        for objectName in selectionList:

            print ('Constraining {} towards {}'.format( objectName, targetName ))

            cmds.aimConstraint( targetName, objectName, aimVector=[0, 1, 0] )

    else:

        print ('Please select two or more objects.')


# randomInstances.py
def createRandomInstance(number=10, x = 10, y = 10, z = 10, scale = [1.0, 1.0], randomOrient = False):
    """
    Creates a bunch of randomly distrubuted copies of selection.

    :param number: the amount of copies wanted (default: 10)
    :param x: Maximum movement in x, default 10
    :param y: Maximum movement in y, default 10
    :param z: Maximum movement in z, default 10
    :param scale: Maximum scale multiplier [low,high], default [1.0, 1.0]
    :param randomOrient: set to true to randomize orientation. Default false


    """
    random.seed( 1234 )

    result = cmds.ls( orderedSelection=True )

    print ('Copying: {}'.format(result))

    transformName = result[0]

    instanceGroupName = cmds.group( empty=True, name=transformName + '_instance_grp#' )

    for i in range( 0, number):

        instanceResult = cmds.instance( transformName, name=transformName + '_instance#' )

        cmds.parent( instanceResult, instanceGroupName )


        xvar = random.uniform( -x, x )
        yvar = random.uniform( -y, y )
        zvar = random.uniform( -z, z )

        cmds.move(xvar, yvar, zvar, instanceResult )

        xRot = 0
        yRot = 0
        zRot = 0

        if randomOrient == True:
            xRot = random.uniform( 0, 360 )
            yRot = random.uniform( 0, 360 )
            zRot = random.uniform( 0, 360 )

        cmds.rotate(xRot, yRot, zRot, instanceResult )

        scalingFactor = random.uniform( scale[0], scale[1])

        cmds.scale(scalingFactor, scalingFactor, scalingFactor, instanceResult )

    cmds.hide( transformName )

    cmds.xform( instanceGroupName, centerPivots=True )


class masterUI:
    """
    creates a UI class, opens a UI to execute some commands.

    """


    def __init__(self):
        if cmds.window('master_UI', exists = True):
            cmds.deleteUI('master_UI')

        self.myWin = cmds.window('master_UI', width=200)
        cmds.columnLayout(adjustableColumn=True)
        cmds.text(label = 'selected objects')
        itemList = cmds.ls(selection = True)
        cmds.textScrollList('itemList', append=itemList)
        self.createButton("on/off", self.toggleButton)
        self.createButton("Create instances", 'createRandomInstance()')
        self.cmds.separator(h =20,style='none')
        self.cmds.text(label = 'testing12')
        self.cmds.textField('pStatementInput')                 #creates an input field
        self.createPrintFunction()
        self.cmds.showWindow()

    def createPrintFunction(self):
        cmds.button('type statement', command = self.printFunction)

    def createButton(self, label, method):
        cmds.button(label = label, command = method)

    def printFunction(*args):
        pStatement = cmds.textField('pStatementInput', q = True, text = True)
        print (pStatement)

    def toggleButton(*arg):
        print 'jeej'
