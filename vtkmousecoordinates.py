# -*- coding: utf-8 -*-
"""
Example of getting the x, y, z mouse click coordinates in vtk

@author: Roger Woodman
"""
 
import vtk
 
class MyInteractorStyle(vtk.vtkInteractorStyleTrackballCamera):
    """
    Creates a new vtkInteractorStyle which prints the x, y, z mouse click
    coordinate when the user clicks on the volume.
    """
    
    def __init__(self, interactor, renderer):
        
        # Create reference to interactor and renderer
        self.interactor = interactor
        self.renderer = renderer
        
        # Add event observers to left mouse click events
        self.AddObserver('LeftButtonPressEvent', self.leftButtonPressEvent)
        self.AddObserver('LeftButtonReleaseEvent', self.leftButtonReleaseEvent)

    def leftButtonPressEvent(self, obj, event):
        """
        Left button pressed. Display x, y, z coordinates
        """
        # Get mouse coordinates on screen
        screenX, screenY = self.interactor.GetEventPosition()

        # Translate mouse coordinates on screen to coordinates on the volume
        self.interactor.GetPicker().Pick(screenX, screenY, 0, self.renderer)
        picked = self.interactor.GetPicker()
        x, y, z = picked.GetPickPosition()

        # Print coordinate details
        print("Coordinates on screen (x, y): %s, %s" % (screenX, screenY))
        print("Coordinates on volume (x, y, z): %s, %s, %s" % (round(x, 2,), round(y, 2), round(z, 2)))

        # Send event to main handler function
        self.OnLeftButtonDown()
        return
 
    def leftButtonReleaseEvent(self,obj,event):
        """
        Left button released.
        * This is here as a reminder
        """
        # Send event to main handler function
        self.OnLeftButtonUp()
        return
 
if __name__ == '__main__': 
    
    # Create sphere
    source = vtk.vtkSphereSource()
    source.SetCenter(0, 0, 0)
    source.SetRadius(1)
    source.Update()
    
    # Create mapper object
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(source.GetOutputPort())
    
    # Create actor
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
     
    # Create renderer
    renderer = vtk.vtkRenderer()
    renderer.SetBackground(1, 1, 1)
    renderer.AddActor(actor)
    
    # Create render window
    renderWindow = vtk.vtkRenderWindow()
    renderWindow.AddRenderer(renderer)
     
    # Create interactor
    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(renderWindow)
    interactor.SetInteractorStyle(MyInteractorStyle(interactor, renderer))
    
    # Start interactor     
    interactor.Initialize()
    interactor.Start()
    