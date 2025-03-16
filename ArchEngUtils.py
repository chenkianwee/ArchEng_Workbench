import FreeCAD
from PySide import QtGui
import freecad.utils as utils
import addonmanager_utilities as amutils

import settings

__Name__ = settings.Name

def install_packages(packages: list[str]):
    try:
        _encoding = QtGui.QApplication.UnicodeUTF8
        def tr(context, text):
            return QtGui.QApplication.translate(context, text, None, _encoding)
    except AttributeError:
        def tr(context, text):
            return QtGui.QApplication.translate(context, text, None)

    import os
    import sys
    import platform
    import importlib
    try:
        for package in packages:
            psplit = package.split('==')
            pname = psplit[0]
            importlib.import_module(pname)
        QtGui.QMessageBox.information(None, 
                                      tr(__Name__, f"Dependencies Installed"), 
                                      tr(__Name__, f"All dependencies satisfied"))
    except ImportError:
        # figure out what platform OS
        py_exe = utils.get_python_exe()
        if os.path.exists(py_exe) == False:
            FreeCAD.Console.PrintNotification(f"python_exe path does not exist!")

        python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
        system_name = platform.system()
        if system_name == 'Linux':
            if "APPIMAGE" in os.environ:            
                os.environ['PYTHONHOME'] = '/usr'
                os.environ['PYTHONPATH'] = f"/usr/lib/python{python_version}/site-packages"
                command = [py_exe, '-m', 'pip', 'install', '--target', vendor_path]
            else:
                command = [py_exe, '-m', 'pip', 'install']
            
        elif system_name == 'Windows' or system_name == 'Darwin':
            vendor_path = amutils.get_pip_target_directory()
            command = [py_exe, '-m', 'pip', 'install', '--target', vendor_path]
        
        for package in packages:
            command.append(package)

        answer = QtGui.QMessageBox.question(None,
                    tr(__Name__, f"Install Dependencies"),
                    tr(__Name__, f"Install dependencies by executing '{command}'?"))
        if answer == QtGui.QMessageBox.StandardButton.Yes:
            import subprocess
            try:
                result = subprocess.run(
                    command,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    check=True
                )
                FreeCAD.Console.PrintNotification(f"{result.stdout}\n")

            except subprocess.CalledProcessError as e:
                FreeCAD.Console.PrintError(f"Error: {e.stderr}\n")
            except Exception as e:
                FreeCAD.Console.PrintError(f"An unexpected error occurred: {e}\n")

            QtGui.QMessageBox.information(None, 
                                          tr(__Name__, f"Restart FreeCAD"), 
                                          tr(__Name__, f"Please restart FreeCAD for the installation to take effect."))
        else:
            QtGui.QMessageBox.information(None, 
                                          tr(__Name__, f"Dependencies Not Installed"), 
                                          tr(__Name__, f"This command requires {packages} to function. Install {packages} by answering Yes"))
            


        

        