import FreeCAD, FreeCADGui
from ArchEngUtils import install_packages

class InstallDependencies: 
   def Activated(self):
        install_packages(['ifc2osmod==0.0.7', 'pytz==2025.1'])

   def GetResources(self): 
       return {'Pixmap' : '', 'MenuText': 'InstallDependencies', 'ToolTip': 'Install the required dependencies'} 
       
FreeCADGui.addCommand('InstallDependencies', InstallDependencies())