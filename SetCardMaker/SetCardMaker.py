#Author- SAF_RRK
#Description- creates 3d models of SET card game based on user input parameters. Made for VR Set game. 

from turtle import shape
import adsk.core, adsk.fusion, adsk.cam, traceback

handlers = []

class ShapeOptions():
    """
    List of the shape options
    """
    def __init__(self):
        pass

    Circle = 0
    Diamond = 1
    Snake = 2
    Oval = 3


class FillingOptions():
    """
    List of the filling options
    """
    def __init__(self):
        pass

    Empty = 0
    Striped = 1
    Full = 2

#base card parameters (some are user inputs)
CardLength = 8.89                                                               #card length [cm]|| advanced user input 
CardRatio = 5 / 7                                                               #card length to width ratio [num]|| advanced user input
CardWidth = 8.89 * CardRatio                                                    #card width [cm]
CardEdgeCurve = CardLength * ( 16 / 88.9 )                                      #card edge fillet amount [cm]
CardHeightMultiplier = 1                                                        #card height multiplier [num] || advanced user input 
CardHeight = CardLength * ( 15 / 88.9 ) * CardHeightMultiplier                  #card height [cm]

#base shape parameters                                                             
ShapeAmount = 3                                                                 #shape amount [num] || regular user input
Shape = ShapeOptions.Oval                                                       #shape || regular user input
shapeHeightRatio = 0.3                                                          #ratio between shape extrusion height to card height [num] || advanced user input
shapeHeight = CardHeight * shapeHeightRatio                                     #shape extrusion height [cm]

#circle parameters 
circleLength = 2                                                                #circle diameter [cm] || **TESTING**                     

#diamond parameters
diamondWidth = 4                                                                #diamond shape width [cm] || advanced user input
diamondRatio = 0.475                                                            #diamond height to width ratio [num] || advanced user input
diamondHeight = diamondRatio * diamondWidth                                     #diamond height [cm]

#oval parameters
ovalWidth = 3.7                                                                 #ellipse width [cm] || advanced user input
ovalRatio = 0.4864                                                              #ellipse height to width ratio [num] || advanced user input
ovalHeight = ovalRatio * ovalWidth                                              #ellipse height [cm]

#snake parameters
snakeWidth = 4                                                                  #snake width [cm] || advanced user input
snakeConst = snakeWidth / 40                                                    #snake size ratio [num]
snakePoints = [(6.654, 0, 0), (7.815, 0, -6.858), (6.021, 0, -14.245), (0, 0, -19.153), (-3.689, 0, -20), (-8.543, 0, -18.731), (-8.174, 0, -14.667), (-5.958, 0, -10.974), (-5.113, 0, -6.33), (-6.654, 0, 0), (-7.815, 0, 6.858), (-6.021, 0, 14.245), (0, 0, 19.153), (3.689, 0, 20), (8.543, 0, 18.731), (8.174, 0, 14.667), (5.958, 0, 10.974), (5.113, 0, 6.33), (6.654, 0, 0)]     #basic snake point list as found in testing

#filling parameters
filling = FillingOptions.Full                                                   #filling - regular user input


#function to get the shape center points on the cards, depending on the shape amount. 
def GetCenterPoints (shapeAmount):
    cPoints = []
    for i in range(1, shapeAmount + 1) :
        zPos = ((CardLength / (shapeAmount + 1)) * i) - (CardLength / 2)
        cPoints.append(adsk.core.Point3D.create(0, zPos, 0))
    return cPoints


#function to draw a certain shape around a center point
def DrawShape (center, shape, sketchCurves, ui):
    
    #sketch objects
    sketchCircles = sketchCurves.sketchCircles
    sketchLines = sketchCurves.sketchLines
    sketchArcs = sketchCurves.sketchArcs
    
    #draw circle  (for testing)
    if (shape is ShapeOptions.Circle):
        circle = sketchCircles.addByCenterRadius(center, circleLength / 2)
        
    #draw diamond
    elif (shape is ShapeOptions.Diamond):
        diamondCorners = [adsk.core.Point3D.create(center.x + (diamondWidth / 2), center.y, center.z), adsk.core.Point3D.create(center.x - (diamondWidth / 2), center.y, center.z), adsk.core.Point3D.create(center.x, center.y + (diamondHeight / 2), center.z), adsk.core.Point3D.create(center.x, center.y - (diamondHeight / 2), center.z)]                                                     #right, left, top, bottom
        diamond = [sketchLines.addByTwoPoints(diamondCorners[0], diamondCorners[2]), sketchLines.addByTwoPoints(diamondCorners[0], diamondCorners[3]), sketchLines.addByTwoPoints(diamondCorners[1], diamondCorners[2]), sketchLines.addByTwoPoints(diamondCorners[1], diamondCorners[3])]
        
    #draw ellipse
    elif (shape is ShapeOptions.Oval):
        arcRight = sketchArcs.addByThreePoints(adsk.core.Point3D.create(center.x + (ovalWidth / 2) - (ovalHeight / 2), center.y - (ovalHeight / 2), center.z), adsk.core.Point3D.create(center.x + (ovalWidth / 2), center.y, center.z), adsk.core.Point3D.create(center.x + (ovalWidth / 2) - (ovalHeight / 2), center.y + (ovalHeight / 2), center.z))        #draw right arc
        arcLeft = sketchArcs.addByThreePoints(adsk.core.Point3D.create(center.x - (ovalWidth / 2) + (ovalHeight / 2), center.y - (ovalHeight / 2), center.z), adsk.core.Point3D.create(center.x - (ovalWidth / 2), center.y, center.z), adsk.core.Point3D.create(center.x - (ovalWidth / 2) + (ovalHeight / 2), center.y + (ovalHeight / 2), center.z))         #draw left arc
        lineTop = sketchLines.addByTwoPoints(adsk.core.Point3D.create(center.x + (ovalWidth / 2) - (ovalHeight / 2), center.y + (ovalHeight / 2), center.z), adsk.core.Point3D.create(center.x - (ovalWidth / 2) + (ovalHeight / 2), center.y + (ovalHeight / 2), center.z))                                                                                    #draw top line
        lineBottom = sketchLines.addByTwoPoints(adsk.core.Point3D.create(center.x + (ovalWidth / 2) - (ovalHeight / 2), center.y - (ovalHeight / 2), center.z), adsk.core.Point3D.create(center.x - (ovalWidth / 2) + (ovalHeight / 2), center.y - (ovalHeight / 2), center.z))                                                                                 #draw bottom line

    #draw snake
    elif (shape is ShapeOptions.Snake):
        points = adsk.core.ObjectCollection.create()
        for p in snakePoints: 
            points.add(adsk.core.Point3D.create(center.x + p[2] * snakeConst, center.y + p[0] * snakeConst, center.z + p[1] * snakeConst))       #wrong order for some reason switched for some reason
        
        spline = sketchCurves.sketchFittedSplines.add(points)
        
    
#function for getting user input **TEST**
def GetUserInputs (ui, design):
    # Get the CommandDefinitions collection.
    cmdDefs = ui.commandDefinitions

    # Create a button command definition.
    buttonSample = cmdDefs.addButtonDefinition('SampleScriptButtonId', 'Python Sample Button', 'Sample button tooltip')
        
    # Connect to the command created event.
    sampleCommandCreated = SampleCommandCreatedEventHandler()
    buttonSample.commandCreated.add(sampleCommandCreated)
    handlers.append(sampleCommandCreated)
        
    # Execute the command.
    buttonSample.execute()
        
    # Keep the script running.
    adsk.autoTerminate(False)    


#function for extruding shapes on card
def ExtrudeShapes (extrusions, sketch, ui):
    sketchShapes = sketch.profiles                                                              #get sketch shapes
    
    distance = adsk.core.ValueInput.createByReal(shapeHeight)                                   #set extrude height
    
    #extrude shapes on card
    for shapeIndex in range(1, sketchShapes.count):
        
        
        extrusions.addSimple(sketchShapes.item(shapeIndex), distance, adsk.fusion.FeatureOperations.JoinFeatureOperation)   #extrude command
        
    
#function for executing the shape filling    
def FillShapes (filling, ui):
    
    #1 - make sketch 
    #2 - get outer lines
    #3 - make offset
    
    if (filling is FillingOptions.Empty):
        

#run the program
def run(context):
    ui = None

    try:
        
        app = adsk.core.Application.get()
        ui  = app.userInterface
        design = adsk.fusion.Design.cast(app.activeProduct)
        rootComp = design.rootComponent
        xyPlane = rootComp.xYConstructionPlane
        xzPlane = rootComp.xZConstructionPlane
        yzPlane = rootComp.yZConstructionPlane
        originPoint = adsk.core.Point3D.create(0,0,0)

        #GetUserInputs(ui, design)

        
        #create new card component:
        CardOcc = rootComp.occurrences.addNewComponent(adsk.core.Matrix3D.create())
        CardComp = CardOcc.component
        CardComp.name = 'Card'


        #setup card component features:
        cardSketches = CardComp.sketches
        cardExtrudes = CardComp.features.extrudeFeatures


        #create base sketch:
        baseSketch = cardSketches.add(xzPlane)
        sketchLines = baseSketch.sketchCurves.sketchLines
        

        #create base rectangle:
        baseRectangle = sketchLines.addCenterPointRectangle(originPoint, adsk.core.Point3D.create(CardWidth / 2, CardLength / 2, 0))


        #fillet base edges:
        baseRectangle.item(0)
        baseRecArcs = baseSketch.sketchCurves.sketchArcs
        for i in range(4):
            baseRecArcs.addFillet(baseRectangle.item(i), baseRectangle.item(i).endSketchPoint.geometry, baseRectangle.item((i + 1) % 4), baseRectangle.item((i + 1) % 4).startSketchPoint.geometry, CardEdgeCurve)


        #extrude base sketch:
        baseProfile = baseSketch.profiles.item(0)
        CardExtrudeHeight = adsk.core.ValueInput.createByReal(CardHeight)
        cardExtrudes.addSimple(baseProfile, CardExtrudeHeight, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)

        #select face to draw sketch:
        cardBody = CardComp.bRepBodies[0]
        cardFaces = cardBody.faces
        shapesFace = max(cardFaces, key=(lambda f: f.centroid.y))

        #pointOnCardFace = adsk.core.Point3D.create(0, CardHeight, 0)
        #cardFace = CardComp.findBRepUsingPoint(pointOnCardFace, adsk.fusion.BRepEntityTypes.BRepFaceEntityType)


        #draw sketch on selected face:
        shapesSketch = cardSketches.add(shapesFace)


        #get shape center points on sketch:
        ShapesSktCrvs = shapesSketch.sketchCurves   
        shapesSktPts = shapesSketch.sketchPoints
        shapeCenters = GetCenterPoints(ShapeAmount)
        
        #draw center points and corresponding shapes on sketch
        for i in range(len(shapeCenters)):
            #ui.messageBox(format(shapeCenters[i]))
            shapesSktPts.add(shapeCenters[i])
            DrawShape(shapeCenters[i], Shape, ShapesSktCrvs, ui)

        #extrude card shapes using ExtrudeShapes() function:
        ExtrudeShapes(cardExtrudes, shapesSketch, ui)
        
        #success message
        ui.messageBox(format('Success bitch'))
        
        
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


