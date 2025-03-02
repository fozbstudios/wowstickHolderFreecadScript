from pickle import TRUE
import re
from PyQt5.QtCore import left
import cadquery as cq
from cadquery.cq import( Workplane)
from cadquery.occ_impl import shapes
from cadquery.occ_impl import geom
from cadquery.selectors import* 
from cadquery_massembly import MAssembly, Mate
from jupyter_cadquery.cadquery.cad_objects import Edges
from jupyter_cadquery.utils import rotate
from jupyter_cadquery.viewer.client import show, show_object
from sqlalchemy.sql.expression import true
#Avoid clean error
cq.occ_impl.shapes.Shape.clean = lambda x: x


bitList=\
    ["PH0000","PH000","PH00","PH0","PH1","PH2","SL1.0","SL1.5","SL2.0","SL2.5","SL3.0","SL3.5","SL4.0",\
    "T2","T3","T4","T5","T6","T7","T8","T9","T10","T15","T20","P2","P5","P6","H0.7","H0.9","H1. 3","H1.5",\
    "H2.0","H2.5","H3.0","H4.0","Y0.6","Y1.0","Y2.0","Y2.5","Y3.0","SQ0","SQ1.0","SQ2.0","U2.0","U2.6",\
    "U3.0","tri2.0","tri2.3","tri2.5","tri3.0","sim0.8","w1.5","extPH0","extPH2","extSL2.0","extH2.0"]
curStr=iter(bitList)
holeDia=8.3;holeDepth=8;bottomThickness=5; xPadding=3.5; yPadding=xPadding; xBitSpacing=4; yBitSpacing=xBitSpacing;textHoleSep=2
xBitCount=7; yBitCount=8;boxXDist=(holeDia+xBitSpacing)*xBitCount+xPadding*2; boxYDist=(holeDia+yBitSpacing)*yBitCount+yPadding*2
boxZDist=holeDepth+bottomThickness; holeFilletRad=.6;boxFilletRolad=1.2; textHeight=6; fontSize=6


solidTexts=[]
first=last=None
wp=cq.Workplane()
for i in bitList:
    solid=cq.Compound.makeText(i,fontSize,textHeight,halign="left",valign="top")
    solidTexts.append(solid)
    solidTexts.sort(key=lambda x: x.BoundingBox().xlen,reverse=True)
    
curX=count=0
rowMax=-xBitSpacing # so when we check cout==zero it the loop it cancels out
for i in solidTexts:
    if count == 0:
        curX=rowMax+xBitSpacing
        curY= holeDia+textHoleSep #? maybe +text hole sep
    aboveOrigin=i.BoundingBox().ylen/2
    i=i.move(cq.Location(cq.Vector(curX,curY+aboveOrigin+10,0)))
    # sBBox=globalizeBoundingBox(i)
    sBBox=i.BoundingBox()
    # i.move(cq.Location(cq.Vector(100,50,20)))
    # sBBox=i.BoundingBox()
    
    rowMax=max(rowMax,sBBox.xmax)
    holePos=i.CenterOfBoundBox()-cq.Vector(0,sBBox.ymin-textHoleSep,holeDepth/2)
    holeCut=cq.Solid.makeCylinder(holeDia/2,height=holeDepth,pnt=holePos)
    curY=sBBox.ymax+textHoleSep
    if  not first:
        fb=i.BoundingBox()
        first=[fb.xmin,fb.ymin,fb.zmin]
    wp.add(i)
    wp.add(holeCut)
    count+=1
    if count == yBitCount:
        count=0
cq.exporters.export(wp,"text.amf")