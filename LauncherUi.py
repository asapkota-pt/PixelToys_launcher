import os
import subprocess
import sys

pyside6_location = os.path.abspath("./_env/_python/Lib/site-packages")
#os.environ['QT_PLUGIN_PATH'] = os.path.join(pyside6_location, "PySide6", "plugins")

if not pyside6_location in sys.path:
    sys.path.append(pyside6_location)

import LauncherUtils
import LauncherEnv

from PySide6 import QtCore
from PySide6 import QtGui
from PySide6 import QtWidgets

class Launcher():
    """Class to  recieve environment from launcher_env and run defined DCC software """
    def __init__(self, project_name, software_name, runas_dev=False):
        super().__init__()
        self.pt_launcher_env = "./_env"
        self.project_name = project_name
        self.dcc_name = software_name
        self.runas_dev = runas_dev
        self.setup_launch()

    def setup_launch(self):
        pt_environment = LauncherEnv.PtDccEnv(self.project_name, env=f"{self.pt_launcher_env}/_mayaEnv", runas_dev=self.runas_dev)
        arguments, project_env = None, None
        if self.dcc_name == "maya":
            arguments, project_env = pt_environment.maya_env

        if arguments == None or project_env == None:
            raise ValueError("No environment is set for the launch")

        self.launch_dcc(arguments, project_env)

    def launch_dcc(self, arguments, project_env):
        #Launching DCC
        subprocess.Popen(arguments, env=project_env)# Doesnt wait after running maya



class PtLuncherUi(QtWidgets.QWidget):
    """ Class for Launcher UI """
    icon_loc = "./PtLauncher_icon.png"
    button_size=QtCore.QSize(85, 120)
    launcher_title = "PT Launcher"
    def __init__(self):
        super(PtLuncherUi, self).__init__(parent=None)
        self.set_ui_default()
        self.create_widget()
        self.create_layout()
        self.create_connection()
        self.pt_projs = LauncherUtils.PtProjects()
        self.create_project_buttons()

    def set_ui_default(self):
        self.setStyleSheet("background-color: #1e1e1e;")
        self.setWindowTitle(PtLuncherUi.launcher_title)
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
        self.pt_proj_info = LauncherUtils.PtProjInfo(project)
        icon_location = f"{self.pt_proj_info.get_project_icon()}/proj_ico.png"
        self.button = QtWidgets.QToolButton()
        self.button.setText(project.upper())
        self.button.setStyleSheet("""font-size: 10px; font-weight: 800; color: #eeeeee; margin-bottom: 5px; letter-spacing: 1px;""")
        if os.path.isfile(icon_location):
            icon = QtGui.QIcon(icon_location)
            self.button.setIcon(icon)
        self.button.setIconSize(PtLuncherUi.button_size)
        self.button.setFixedSize(PtLuncherUi.button_size)
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
        Launcher(project_name=project, software_name=software_name, runas_dev=runas_dev)
        #self.close()
        pass

    def closeEvent(self, event):
        pass



if __name__=="__main__":
    app=QtWidgets.QApplication(sys.argv)
    launcher_win = PtLuncherUi()
    launcher_win.show()
    sys.exit(app.exec())