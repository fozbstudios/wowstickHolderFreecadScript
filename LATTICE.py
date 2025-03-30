import FreeCAD
import Draft
import lattice2Placement
import lattice2ArrayFromShape
import lattice2LinearArray
import lattice2PopulateCopies
import lattice2Executer
import lattice2Base
pl = FreeCAD.Placement()
pl.Rotation.Q = (0.0, 0.0, 0.0, 1.0)
pl.Base = FreeCAD.Vector(-42.508460998535156, -43.09760665893555, 0.0)
rec = Draft.make_rectangle(length=164.30977630615234, height=64.6464614868164, placement=pl, face=False, support=None)
Draft.autogroup(rec)
FreeCAD.ActiveDocument.recompute()
### Begin command Lattice2_Placement_GroupCommand
f = lattice2ArrayFromShape.makeLatticeArrayFromShape(name='ArrayFromShape')
f.ShapeLink = App.ActiveDocument.Rectangle
f.CompoundTraversal = 'Use as a whole'
f.ExposePlacement = True
f.Label = 'Placement from ' + f.ShapeLink.Label
f.TranslateMode = 'child.CenterOfBoundBox'
f.OrientMode = '(none)'
for child in f.ViewObject.Proxy.claimChildren():
    child.ViewObject.hide()
lattice2Executer.executeFeature(f)
Gui.Selection.addSelection(f)
f = None
### End command Lattice2_Placement_GroupCommand
### Begin command Lattice2_Placement_GroupCommand
f = lattice2Placement.makeLatticePlacement(name='Placment')
f.PlacementChoice = 'Custom'
f.Label = 'Custom'
f.Placement.Base = lattice2Base.Autosize.convenientPosition()
f.MarkerSize = lattice2Base.Autosize.convenientMarkerSize()
lattice2Executer.executeFeature(f)
Gui.Selection.addSelection(f)
f = None
### End command Lattice2_Placement_GroupCommand
# App.getDocument("Unnamed").Placment.Placement=App.Placement(App.Vector(0,0,0), App.Rotation(App.Vector(0,0,1),0), App.Vector(0,0,0))
### Begin command Lattice2_LinearArray_GroupCommand
f = lattice2LinearArray.makeLinearArray(name='LinearArray')
f.Link = App.ActiveDocument.Placment
f.GeneratorMode = 'SpanStep'
f.Placement.Base = lattice2Base.Autosize.convenientPosition()
f.SpanEnd = lattice2Base.Autosize.convenientModelSize()
f.Step = lattice2Base.Autosize.convenientMarkerSize()
lattice2Executer.executeFeature(f)
### Begin command Lattice2_LinearArray_GroupCommand
f = lattice2LinearArray.makeLinearArray(name='LinearArray')
f.Link = App.ActiveDocument.Rectangle
f.LinkSubelement = 'Edge3'
f.GeneratorMode = 'SpanStep'
f.Placement.Base = lattice2Base.Autosize.convenientPosition()
f.SpanEnd = lattice2Base.Autosize.convenientModelSize()
f.Step = lattice2Base.Autosize.convenientMarkerSize()
lattice2Executer.executeFeature(f)
Gui.Selection.clearSelection()
Gui.Selection.addSelection(f)
### End command Lattice2_LinearArray_GroupCommand
FreeCAD.getDocument('Unnamed').getObject('LinearArray').Step = 1

FreeCAD.getDocument('Unnamed').getObject('LinearArray').Step = 10

# Gui.Selection.clearSelection()
# Gui.Selection.addSelection('Unnamed','Rectangle','Edge4',-42.5085,-0.503422,0)
### Begin command Lattice2_LinearArray_GroupCommand
f = lattice2LinearArray.makeLinearArray(name='LinearArray')
f.Link = App.ActiveDocument.Rectangle
f.LinkSubelement = 'Edge4'
f.GeneratorMode = 'SpanStep'
f.Placement.Base = lattice2Base.Autosize.convenientPosition()
f.SpanEnd = lattice2Base.Autosize.convenientModelSize()
f.Step = lattice2Base.Autosize.convenientMarkerSize()
lattice2Executer.executeFeature(f)
Gui.Selection.clearSelection()
Gui.Selection.addSelection(f)
### End command Lattice2_LinearArray_GroupCommand
# Gui.Selection.addSelection('Unnamed','LinearArray001')
FreeCAD.getDocument('Unnamed').getObject('LinearArray001').Step = 1

FreeCAD.getDocument('Unnamed').getObject('LinearArray001').Step = 10

# Gui.Selection.addSelection('Unnamed','LinearArray')
### Begin command Lattice2_PopulateCopiesGroupCommand
f = lattice2PopulateCopies.makeLatticePopulateCopies(name='Populate')
f.Object = App.ActiveDocument.LinearArray001
f.PlacementsTo = App.ActiveDocument.LinearArray
f.Referencing = 'Origin'
f.Label = 'Populate LinearArray with LinearArray001'
lattice2Executer.executeFeature(f)
f.Object.ViewObject.hide()
f.PlacementsTo.ViewObject.hide()
Gui.Selection.addSelection(f)
f = None
FreeCAD.getDocument('Unnamed').getObject('Populate').Placement = App.Placement(App.Vector(-1,0,0),App.Rotation(App.Vector(0,0,1),0))
FreeCAD.getDocument('Unnamed').getObject('Populate').Placement = App.Placement(App.Vector(-10,0,0),App.Rotation(App.Vector(0,0,1),0))
FreeCAD.getDocument('Unnamed').getObject('Populate').Placement = App.Placement(App.Vector(-100,0,0),App.Rotation(App.Vector(0,0,1),0))
FreeCAD.getDocument('Unnamed').getObject('Populate').Placement = App.Placement(App.Vector(-10,0,0),App.Rotation(App.Vector(0,0,1),0))
FreeCAD.getDocument('Unnamed').getObject('Populate').Placement = App.Placement(App.Vector(-100,0,0),App.Rotation(App.Vector(0,0,1),0))
FreeCAD.getDocument('Unnamed').getObject('Populate').Placement = App.Placement(App.Vector(-10,0,0),App.Rotation(App.Vector(0,0,1),0))
FreeCAD.getDocument('Unnamed').getObject('Populate').Placement = App.Placement(App.Vector(-1,0,0),App.Rotation(App.Vector(0,0,1),0))
FreeCAD.getDocument('Unnamed').getObject('Populate').Placement = App.Placement(App.Vector(-5,0,0),App.Rotation(App.Vector(0,0,1),0))
FreeCAD.getDocument('Unnamed').getObject('Populate').Placement = App.Placement(App.Vector(-50,0,0),App.Rotation(App.Vector(0,0,1),0))

pl = FreeCAD.Placement()
pl.Rotation.Q = (0.0, 0.0, 0.0, 1.0)
pl.Base = FreeCAD.Vector(-24.8907527923584, -15.723710060119629, 0.0)
pol = Draft.make_polygon(6, radius=2.0, inscribed=True, placement=pl, face=False, support=None)
Draft.autogroup(pol)
FreeCAD.ActiveDocument.recompute()
### Begin command Lattice2_PopulateCopiesGroupCommand
f = lattice2PopulateCopies.makeLatticePopulateCopies(name='Populate')
f.Object = App.ActiveDocument.Polygon
f.PlacementsTo = App.ActiveDocument.Populate
f.Referencing = 'Origin'
f.Label = 'Populate Populate LinearArray with LinearArray001 with Polygon'
lattice2Executer.executeFeature(f)
Gui.Selection.addSelection(f)
f = None
Draft.move([FreeCAD.ActiveDocument.Populate001], FreeCAD.Vector(-10.303340911865234, -15.974515914916992, 0.0), copy=False)
FreeCAD.ActiveDocument.recompute()
App.activeDocument().addObject("Part::Compound","Compound")
App.activeDocument().Compound.Links = [App.activeDocument().Populate002,App.activeDocument().Rectangle,]
App.ActiveDocument.recompute()
App.getDocument('Unnamed').addObject('Part::Extrusion','Extrude')
f = App.getDocument('Unnamed').getObject('Extrude')
f.Base = App.getDocument('Unnamed').getObject('Compound')
f.DirMode = "Normal"
f.DirLink = None
f.LengthFwd = 10.000000000000000
f.LengthRev = 0.000000000000000
f.Solid = True
f.Reversed = False
f.Symmetric = False
f.TaperAngle = 0.000000000000000
f.TaperAngleRev = 0.000000000000000
App.getDocument('Unnamed').getObject('Compound').Visibility = False
App.ActiveDocument.recompute()