import os
import subprocess
import sys
import getpass

pyside6_location = os.path.abspath("./_env/_python/Lib/site-packages")
#os.environ['QT_PLUGIN_PATH'] = os.path.join(pyside6_location, "PySide6", "plugins")

if not pyside6_location in sys.path:
    sys.path.append(pyside6_location)

from PySide6 import QtCore
from PySide6 import QtGui
from PySide6 import QtWidgets
import launcher_utils
import shutil


class launcher():
    def __init__(self, project_name, software_name, runas_dev=False):
        super().__init__()
        self.launcher_env = "./_env"
        if software_name=="maya":
            maya_arguments, project_env = self.set_env(project_name, maya_env=f"{self.launcher_env}/_mayaEnv", runas_dev=runas_dev)
            self.maya_launcher(maya_arguments, project_env)


    def set_env(self, project_name, maya_env, runas_dev):
        pt_projects = launcher_utils.pt_proj_info(project_name)
        project_python = pt_projects.get_project_python()
        project_icons = pt_projects.get_project_icon()
        project_coala = pt_projects.get_project_coala()
        project_location = pt_projects.get_project_location()
        project_maya_version = pt_projects.get_project_maya()

        project_env = os.environ.copy()
        # pt_art_tools_path = f"{project_location}/Art/Tools/pt_art_tools"
        pt_art_tools_path = "V:/Panda/Art/Tools/pt_art_tools"  # this should be changed to the upper one after we move coala out from Panda
        #coala_path = f"{pt_art_tools_path}/{project_coala}"
        coala_path = f"{pt_art_tools_path}/{project_coala}"
        python_lib_path = f"{pt_art_tools_path}/WinPython/{project_python}/Lib/site-packages"
        if python_lib_path not in sys.path:
            sys.path.append(python_lib_path)

        project_env["MAYA_SCENES"] = f"{project_location}/Art"
        project_env["PYTHONPATH"] = f"{pt_art_tools_path};{python_lib_path};{coala_path}"
        project_env["MAYA_MODULE_PATH"] = f"{coala_path}/plugins;"
        project_env["MAYA_PLUG_IN_PATH"] = f"{coala_path}/plugins;"

        project_env["PT_Project"] = project_name
        project_env["PT_Tools"] = pt_art_tools_path
        project_env["PT_Coala"] = project_coala

        if runas_dev == True: # add folders to environment
            project_env["PT_Maya"] = "DEV"
            User = getpass.getuser()
            env_folder = f"C:/Users/{User}/Documents/maya"
        else:
            project_env["PT_Maya"] = "Stable"
            # icons folder
            project_env["XBMLANGPATH"] = project_icons
            env_folder = os.path.abspath(maya_env)

        
        maya_exe_path = f"C:/Program Files/Autodesk/MAYA{project_maya_version}/bin/maya.exe"
        maya_arguments = [maya_exe_path]
        project_env["MAYA_APP_DIR"] = f"{os.path.abspath(env_folder)}/"  # Maya projects set from launcher
        #print(f'Running as {project_env["PT_Maya"]}: {project_name}')
        return (maya_arguments, project_env)


    def maya_launcher(self, maya_arguments, project_env):
        subprocess.Popen(maya_arguments, env=project_env)# Doesnt wait after running maya


class pt_luncher_ui(QtWidgets.QWidget):
    icon_loc = "./PtLauncher_icon.png"
    button_size=QtCore.QSize(85, 120)
    launcher_title = "PT Launcher"
    def __init__(self):
        super(pt_luncher_ui, self).__init__(parent=None)
        self.set_ui_default()
        self.create_widget()
        self.create_layout()
        self.create_connection()
        self.pt_projs = launcher_utils.pt_projects()
        self.create_project_buttons()

    def set_ui_default(self):
        self.setStyleSheet("background-color: #1e1e1e;")
        self.setWindowTitle(pt_luncher_ui.launcher_title)
        self.setWindowIcon(QtGui.QIcon(self.icon_loc))
        self.setMinimumWidth(414)
        self.setMaximumWidth(414)
        self.setMinimumHeight(250)
        self.setMaximumHeight(250)

    def create_project_buttons(self):
        row_count,column_count1 = 0, 0
        no_btn_per_row = 4
        for each_proj in self.pt_projs.get_project_list():
            button = self.create_button(each_proj)
            self.button.customContextMenuRequested.connect(lambda pos, btn=button, proj=each_proj: self.show_options(btn, pos, proj))
            self.project_btn_layout.addWidget(button, row_count, column_count1)
            column_count1 += 1
            if column_count1 >= no_btn_per_row:
                row_count += 1
                column_count1 = 0

    def create_widget(self):
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.project_title_layout = QtWidgets.QHBoxLayout()
        self.project_title_layout.setAlignment(QtCore.Qt.AlignLeft)
        self.title = QtWidgets.QLabel("PROJECTS")
        self.title.setFixedHeight(50)
        self.title.setStyleSheet("""font-size: 19px; font-weight: 800; color: #eeeeee; margin-bottom: 5px; letter-spacing: 1px;""")

        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_widget =  QtWidgets.QWidget()
        self.scroll_area.setWidget(self.scroll_widget)

        self.project_btn_layout = QtWidgets.QGridLayout(self.scroll_widget)
        self.project_btn_layout.setAlignment(QtCore.Qt.AlignLeft)
        self.project_btn_layout.setRowStretch(10, 1)

        self.line = QtWidgets.QFrame()
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setStyleSheet("background-color: #787878;")

    def create_button(self, project):
        self.pt_proj_info = launcher_utils.pt_proj_info(project)
        icon_location = f"{self.pt_proj_info.get_project_icon()}/proj_ico.png"
        self.button = QtWidgets.QToolButton()
        self.button.setText(project.upper())
        self.button.setStyleSheet("""font-size: 10px; font-weight: 800; color: #eeeeee; margin-bottom: 5px; letter-spacing: 1px;""")
        if os.path.isfile(icon_location):
            icon = QtGui.QIcon(icon_location)
            self.button.setIcon(icon)
        self.button.setIconSize(pt_luncher_ui.button_size)
        self.button.setFixedSize(pt_luncher_ui.button_size)
        self.button.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.button.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.button.clicked.connect(lambda: self.project_launcher(project))
        return self.button

    def show_options(self, button, pos, project):
        menu = QtWidgets.QMenu(button)
        open_action = menu.addAction("Run as Dev")
        action = menu.exec(button.mapToGlobal(pos))
        if action == open_action:
            self.project_launcher(project, runas_dev=True)

    def create_layout(self):
        self.project_title_layout.addWidget(self.title)

        self.main_layout.addLayout(self.project_title_layout)
        self.main_layout.addWidget(self.line)
        self.main_layout.addWidget(self.scroll_area, 1)

        self.setLayout(self.main_layout)

    def create_connection(self):
        pass

    def project_launcher(self, project, runas_dev=False):
        software_name = "maya"
        launcher(project_name=project, software_name=software_name, runas_dev=runas_dev)
        #self.close()
        pass

    def closeEvent(self, event):
        pass



if __name__=="__main__":
    app=QtWidgets.QApplication(sys.argv)
    launcher_win = pt_luncher_ui()
    launcher_win.show()
    sys.exit(app.exec())
    #pt_proj=launcher_utils.pt_projects()
    #for each_proj in pt_proj.get_project_list():
    #    print(pt_proj.get_project_info(each_proj))
    #launcher_win=pt_luncher_ui()
    #launcher_win.show()