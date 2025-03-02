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
xBitCount=7; yBitCount=8;boxXDist=(holeDia+xBitSpacing)*xBitCount+xPadding*2; boxYDist=(holeDia+yBitSpacing)*yBitCount+yPadding*2
boxZDist=holeDepth+bottomThickness; holeFilletRad=.6;boxFilletRolad=1.2; textHeight=6; fontSize=6; maxXdist=210;

part=None
solidTexts=[]
holeWallCircles=[]
holeNegativeCircles=[]
shapestrings = []
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

    if first is None:
        plm.Base = FreeCAD.Vector(0, 0, 0.0)
        addText(bitName,plm)
        rowStart=shapestrings[-1]
    else:
        prevText = shapestrings[-1]
        bb=prevText.Shape.BoundBox
        plm.Base = FreeCAD.Vector(bb.XMax+xBitSpacing, bb.YMax, 0.0)
        addText(bitName,plm)

        if shapestrings[-1].Shape.BoundBox.XMax-rowStart.Shape.BoundBox.XMin>=maxXdist:
            shapestrings[-1].Document.removeObject(shapestrings[-1].Name)
            del shapestrings[-1]
            prevText = rowStart
            bb = prevText.Shape.BoundBox
            plm.Base = FreeCAD.Vector(bb.XMin, bb.YMin - (holeDia + textHoleSep * 2 + yBitSpacing), 0.0)
            addText(bitName,plm)
            rowStart=shapestrings[-1]
            bottomMost = rowStart.Shape.BoundBox.YMin-textHoleSep-holeDia
            
        bb=shapestrings[-1].Shape.BoundBox
    plm = FreeCAD.Placement()
    plm.Rotation.Q = (0.0, 0.0, 0.0, 1.0)
    center= shapestrings[-1].Shape.BoundBox.Center
    center.y-=holeRad+textHoleSep+ shapestrings[-1].Shape.BoundBox.YLength
    plm.Base=center
    circle=addCircle(holeRad+holeWallThickness,plm,label=f'{bitName}WallCircle')
    holeWallCircles.append(circle)
    circle=addCircle(holeRad,plm,label=f'{bitName}NegativeCircle')
    holeNegativeCircles.append(circle)    
      

            

    if first is None:
        first=shapestrings[0]
fbb=first.Shape.BoundBox
leftMost=fbb.XMin-xPadding
topMost=fbb.YMax+yPadding
print(f'r{rightMost} l{leftMost} t{topMost} b{bottomMost}')
rightMost+=xPadding
bottomMost-=yPadding
rectangle=makeBoundRect(leftMost,topMost,rightMost-leftMost,bottomMost-topMost)
namesForFuse=[x.Name for x in shapestrings]
namesForFuse.append(rectangle.Name)
textAndRectFuse = bp.make_multi_fuse(namesForFuse)
textAndRectFuse.Label='textAndRectFuse'
setParent(parent=part,child=textAndRectFuse)
holeWallFuse = bp.make_multi_fuse([x.Name for x in holeWallCircles])
holeWallFuse.Label='holeWallFuse'
setParent(parent=part,child=holeWallFuse)
holeNegativeFuse = bp.make_multi_fuse([x.Name for x in holeNegativeCircles])
holeNegativeFuse.Label='holeNegativeFuse'

setParent(parent=part,child=holeNegativeFuse)



FreeCAD.ActiveDocument.recompute()

exportName=f"D:/test{datetime.now().strftime('%d%b%Y-%H%M%S')}.step"

Import.export(shapestrings, exportName)

del shapestrings