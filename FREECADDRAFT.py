import sys 
import subprocess

from datetime import datetime
import FreeCAD
import Draft
import Import
from FreeCAD import Vector
from BOPTools import BOPFeatures




bitList=\
    ["PH0000","PH000","PH00","PH0","PH1","PH2","SL1.0","SL1.5","SL2.0","SL2.5","SL3.0","SL3.5","SL4.0",\
    "T2","T3","T4","T5","T6","T7","T8","T9","T10","T15","T20","P2","P5","P6","H0.7","H0.9","H1. 3","H1.5",\
    "H2.0","H2.5","H3.0","H4.0","Y0.6","Y1.0","Y2.0","Y2.5","Y3.0","SQ0","SQ1.0","SQ2.0","U2.0","U2.6",\
    "U3.0","tri2.0","tri2.3","tri2.5","tri3.0","sim0.8","w1.5","extPH0","extPH2","extSL2.0","extH2.0"]
curStr=iter(bitList)
holeDia=8.3;holeRad=holeDia/2;holeWallThickness=1.5; holeDepth=8;bottomThickness=5; xPadding=3.5; yPadding=xPadding; xBitSpacing=4; yBitSpacing=xBitSpacing;textHoleSep=2
xBitCount=7; yBitCount=8;boxXDist=(holeDia+xBitSpacing)*xBitCount+xPadding*2; boxYDist=(holeDia+yBitSpacing)*yBitCount+yPadding*2;hexMaxRad=3
boxZDist=holeDepth+bottomThickness; holeFilletRad=.6;boxFilletRolad=1.2; textHeight=6; fontSize=6; maxXdist=210;

part=None
solidTexts=[]
holeWallCircles=[]
topPolygons=[]
holeNegativeCircles=[]
shapestrings = []
def extrude(obj,dist, reverse):
    extrudeName=f'{obj.Label}Extrude'
    doc.addObject('Part::Extrusion',extrudeName)
    extrudeObj = doc.getObject(extrudeName)
    extrudeObj.Base = obj
    extrudeObj.DirMode = "Normal"
    extrudeObj.DirLink = None
    extrudeObj.LengthFwd= dist
    extrudeObj.LengthRev = 0.000000000000000
    extrudeObj.Solid = True
    extrudeObj.Reversed = reverse
    extrudeObj.Symmetric = False
    extrudeObj.TaperAngle = 0.000000000000000
    extrudeObj.TaperAngleRev = 0.000000000000000
    # doc.getObject('Extrude').ViewObject.ShapeAppearance=getattr(doc.getObject('Fusion').getLinkedObject(True).ViewObject,'ShapeAppearance',doc.getObject('Extrude').ViewObject.ShapeAppearance)
    # doc.getObject('Extrude').ViewObject.LineColor=getattr(doc.getObject('Fusion').getLinkedObject(True).ViewObject,'LineColor',doc.getObject('Extrude').ViewObject.LineColor)
    # doc.getObject('Extrude').ViewObject.PointColor=getattr(doc.getObject('Fusion').getLinkedObject(True).ViewObject,'PointColor',doc.getObject('Extrude').ViewObject.PointColor)
    obj.Visibility = False
    # obj.Label=extrudeName
    return extrudeObj
def setParent(parent,child):
    parent.addObject(child)
    Gui.activeView().setActiveObject(part.Name, App.activeDocument().Part)
def makeBoundRect(left,top,xDist,yDist):
    rect = Draft.make_rectangle(xDist, yDist, 0)
    rect.Placement.Base = Vector(left,top , 0)
    rect.MakeFace = False
    rect.Label='topRect'
    setParent(parent=part,child=rect)
    return rect
def addCircle(radius,placement,label):
    circle = Draft.make_circle(radius=radius, placement=placement, face=False, support=None)
    circle.Label=label
    setParent(parent=part,child=circle)
    return circle
def addText(text,placement):
    # Gui.Selection.clearSelection()
    # Gui.Selection.addSelection(App.ActiveDocument.Name,)
    ss = Draft.make_shapestring(String=text, FontFile="C:/Windows/Fonts/ariali.ttf", Size=fontSize, Tracking=0.0)
    ss.Justification = u"Top-Left"
    ss.Placement = placement
    ss.Label=f'{bitName}-SS'
    
    ss.AttachmentSupport = None
    Draft.autogroup(ss)
    ss.MakeFace = False
    
    setParent(parent=part,child=ss)
    
    FreeCAD.ActiveDocument.recompute()
    # FreeCAD.getDocument('Unnamed').getObject('ShapeString').Justification = u"Top-Left"
    shapestrings.append(ss)
first=last=rowStart=prevText=None
rightMost=bottomMost=0.0
firsRow=True

doc = FreeCAD.newDocument()
bp = BOPFeatures.BOPFeatures(doc)

### Begin command Std_Part
App.activeDocument().Tip = App.activeDocument().addObject('App::Part','Part')
# App.activeDocument().Part.Label = 'Part'
part=App.activeDocument().Part
# Gui.activeView().setActiveObject('part', App.activeDocument().Part)
App.ActiveDocument.recompute()
### End command Std_Part
### Begin command Std_Workbench
Gui.activateWorkbench("DraftWorkbench")
### End command Std_Workbench
# Gui.runCommand('Draft_ShapeString',0)
App.DraftWorkingPlane.setTop()

for i,bitName  in enumerate(bitList):
    plm = FreeCAD.Placement()
    plm.Rotation.Q = (0.0, 0.0, 0.0, 1.0)
    checkMakePoly=True

    if first is None:
        checkMakePoly = False
        plm.Base = FreeCAD.Vector(0, 0, 0.0)
        addText(bitName,plm)
        rowStart=shapestrings[-1]
    else:
        prevText = shapestrings[-1]
        bb=prevText.Shape.BoundBox
        plm.Base = FreeCAD.Vector(bb.XMax+xBitSpacing, bb.YMax, 0.0)
        addText(bitName,plm)

        if shapestrings[-1].Shape.BoundBox.XMax-rowStart.Shape.BoundBox.XMin>=maxXdist:
            # go to next row
            firsRow=False
            checkMakePoly=False
            shapestrings[-1].Document.removeObject(shapestrings[-1].Name)
            del shapestrings[-1]
            prevText = rowStart
            bb = prevText.Shape.BoundBox
            plm.Base = FreeCAD.Vector(bb.XMin, bb.YMin - (holeDia + textHoleSep * 2 + yBitSpacing), 0.0)
            addText(bitName,plm)
            rowStart=shapestrings[-1]

            bottomMost = rowStart.Shape.BoundBox.YMin-textHoleSep-holeDia-2*holeWallThickness
        bb=shapestrings[-1].Shape.BoundBox
        rightMost=bb.XMax if bb.XMax>rightMost else rightMost
    plm = FreeCAD.Placement()
    plm.Rotation.Q = (0.0, 0.0, 0.0, 1.0)
    center= shapestrings[-1].Shape.BoundBox.Center
    center.y-=holeRad+textHoleSep+ shapestrings[-1].Shape.BoundBox.YLength
    plm.Base=center
    circle=addCircle(holeRad+holeWallThickness,plm,label=f'{bitName}WallCircle')
    holeWallCircles.append(circle)
    circle=addCircle(holeRad,plm,label=f'{bitName}NegativeCircle')
    holeNegativeCircles.append(circle)
    if checkMakePoly:
        FreeCAD.ActiveDocument.recompute()
        leftMostPrev=holeWallCircles[-2].Shape.BoundBox.XMax
        rightMostCur=holeWallCircles[-1].Shape.BoundBox.XMin
        while rightMostCur-leftMostPrev>=4*hexMaxRad:
            print(f"l: {leftMostPrev} r: {rightMostCur} c: { holeWallCircles[-2].Shape.BoundBox.Center.y} {holeWallCircles[-1].Label}")
            hexMaxPlacement = FreeCAD.Placement()
            hexMaxPlacement.Rotation.Q = (0.0, 0.0, 0.0, 1.0)
            # hexMaxPlacement.Base = FreeCAD.Vector(5, 3, 0.0)
            hexMaxPlacement.Base = FreeCAD.Vector(leftMostPrev+2*hexMaxRad, holeWallCircles[-2].Shape.BoundBox.Center.y, 0.0)
            # hexMaxPlacement.Base = FreeCAD.Vector((rightMostCur-leftMostPrev)/2, holeWallCircles[-1].Shape.BoundBox.Center.y, 0.0)
            hexMax = Draft.make_polygon(6, radius=hexMaxRad, inscribed=False, placement=hexMaxPlacement, face=False, support=None)
            hexMax.Label=f'{bitName}HexMax'
            setParent(parent=part,child=hexMax)
            topPolygons.append(hexMax)
            FreeCAD.ActiveDocument.recompute()
            leftMostPrev=topPolygons[-1].Shape.BoundBox.XMax
            print(f'{bitName}HexMax')

    

            

    if first is None:
        first=shapestrings[0]
fbb=first.Shape.BoundBox
leftMost=fbb.XMin-xPadding
topMost=fbb.YMax+yPadding
rightMost+=xPadding
bottomMost-=yPadding
rectangle=makeBoundRect(leftMost,topMost,rightMost-leftMost,bottomMost-topMost)
namesForTextRectFuse=[]
namesForTextRectFuse=[x.Name for x in shapestrings]
namesForTextRectFuse.extend([x.Name for x in topPolygons])
namesForTextRectFuse.append(rectangle.Name)
textAndRectFuse = bp.make_multi_fuse(namesForTextRectFuse)
textAndRectFuse.Label='textAndRectFuse'
setParent(parent=part,child=textAndRectFuse)
holeWallFuse = bp.make_multi_fuse([x.Name for x in holeWallCircles])
holeWallFuse.Label='holeWallFuse'
setParent(parent=part,child=holeWallFuse)
holeNegativeFuse = bp.make_multi_fuse([x.Name for x in holeNegativeCircles])
holeNegativeFuse.Label='holeNegativeFuse'
textAndRectExtrude=extrude(textAndRectFuse,3,True)
holeWallExtrude=extrude(holeWallFuse,holeDepth+holeWallThickness*2,True)
holeNegativeExtrude=extrude(holeNegativeFuse,holeDepth,True)
setParent(parent=part,child=textAndRectExtrude)
setParent(parent=part,child=holeWallExtrude)
setParent(parent=part,child=holeNegativeExtrude)
rectBitHoleFuse = bp.make_multi_fuse([textAndRectExtrude.Name,holeWallExtrude.Name])
rectBitHoleFuse.Label='rectBitHoleFuse'
topCut = bp.make_cut([rectBitHoleFuse.Name,holeNegativeExtrude.Name])
topCut.Label='topCut'



FreeCAD.ActiveDocument.recompute()

# exportName=f"D:/test{datetime.now().strftime('%d%b%Y-%H%M%S')}.step"

# Import.export(shapestrings, exportName)

# del shapestrings