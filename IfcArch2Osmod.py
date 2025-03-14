import FreeCAD, FreeCADGui
from PySide import QtGui
from PySide.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLineEdit, QFileDialog
import settings

__Name__ = settings.Name
class ConvertIfcArch2Osmod:
  def Activated(self):
    dialog = FileChooserDialog()
    dialog.exec()

  def GetResources(self):
    return {'Pixmap' : '', 'MenuText': 'ifc2osmod', 'ToolTip': 'Converts IFC file to Openstudio Model(.osm)'} 
       
FreeCADGui.addCommand('ConvertIfcArch2Osmod', ConvertIfcArch2Osmod())

class FileChooserDialog(QDialog):
    def __init__(self):
      super().__init__()
      self.ifc_path = None
      self.osmod_path = None

      self.setWindowTitle("Choose File Paths")
      self.setGeometry(100, 100, 400, 200)

      layout = QVBoxLayout()

      # First file selection
      self.file1_edit = QLineEdit(self)
      self.file1_button = QPushButton("Choose IFC file to convert", self)
      self.file1_button.clicked.connect(self.choose_first_file)

      # Second file selection
      self.file2_edit = QLineEdit(self)
      self.file2_button = QPushButton("Save Osmod file", self)
      self.file2_button.clicked.connect(self.choose_second_file)

      # execute button
      self.exec_button = QPushButton("Convert to osmod", self)
      self.exec_button.clicked.connect(self.convert2osmod)

      layout.addWidget(self.file1_edit)
      layout.addWidget(self.file1_button)
      layout.addWidget(self.file2_edit)
      layout.addWidget(self.file2_button)
      layout.addWidget(self.exec_button)

      self.setLayout(layout)

    def choose_first_file(self):
      file_path, _ = QFileDialog.getOpenFileName(self, "Select First File")
      if file_path:
          self.file1_edit.setText(file_path)
          self.ifc_path = file_path

    def choose_second_file(self):
      file_path, _ = QFileDialog.getSaveFileName(self, "Select Second File")
      if file_path:
          self.file2_edit.setText(file_path)
          self.osmod_path = file_path

    def convert2osmod(self):
      from ifc2osmod import settings, ifcarch2osmod
      ifc_path = str(self.ifc_path)
      osmod_path = str(self.osmod_path)
      opq_constr_path = settings.OSMOD_OPQ_CONSTR_PATH
      smpl_glz_constr_path = settings.OSMOD_SMPL_GLZ_CONSTR_PATH
      ifcarch2osmod.ifcarch2osmod(ifc_path, osmod_path, False, opq_constr_path, smpl_glz_constr_path)
      
      QtGui.QMessageBox.information(None, 
                                    f"Result Window", 
                                    f"Converted:\n {ifc_path}\n to:\n {osmod_path}.")