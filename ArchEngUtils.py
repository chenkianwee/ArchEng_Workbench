from PySide import QtGui

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
        cmdlist = ['pip', 'install']
        for package in packages:
            cmdlist.append(package)
        cmdlist.append('--user')
        answer = QtGui.QMessageBox.question(None,
                    tr(__Name__, f"Install Dependencies"),
                    tr(__Name__, f"Install {cmdlist} by executing pip?"))
        if answer == QtGui.QMessageBox.StandardButton.Yes:
            import subprocess
            proc = subprocess.Popen(cmdlist, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = proc.communicate()
            print(out.decode())
            print(err.decode())
            QtGui.QMessageBox.information(None, 
                                          tr(__Name__, f"Restart FreeCAD"), 
                                          tr(__Name__, f"Please restart FreeCAD for the installation to take effect."))
        else:
            QtGui.QMessageBox.information(None, 
                                          tr(__Name__, f"Dependencies Not Installed"), 
                                          tr(__Name__, f"This command requires {packages} to function. Install {packages} by answering Yes"))