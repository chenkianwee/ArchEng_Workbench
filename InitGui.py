class ArchEngWorkbench(Workbench): 
    MenuText = "ArchEng"
    def Initialize(self):
        import IfcArch2Osmod, InstallDep # assuming Scripts.py is your module
        self.list = ['ConvertIfcArch2Osmod', 'InstallDependencies'] # That list must contain command names, that can be defined in Scripts.py
        self.appendToolbar("ArchEng",self.list) 
        
Gui.addWorkbench(ArchEngWorkbench())