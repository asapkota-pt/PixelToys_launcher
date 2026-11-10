import os
import subprocess
import json
import sys
import getpass

import LauncherUtils

class PtDccEnv():
    """ Class to define and return environment for each DCC platform"""
    def __init__(self, project_name, env, runas_dev):
        self.project_name = project_name
        self.env = env
        self.runas_dev = runas_dev
        self.maya_env = self.get_maya_env
        self.blender_env = self.get_blender_env
        self.houdini_env = self.get_houdini_env
        self.unity_env = self.get_unity_env
        self.unreal_env = self.get_unreal_env

    @property
    def get_maya_env(self):
        pt_projects = LauncherUtils.PtProjInfo(self.project_name)
        project_python = pt_projects.get_project_python()
        project_icons = pt_projects.get_project_icon()
        project_coala = pt_projects.get_project_coala()
        project_location = pt_projects.get_project_location()
        project_maya_version = pt_projects.get_project_maya()

        project_env = os.environ.copy()
        # pt_art_tools_path = f"{project_location}/Art/Tools/pt_art_tools"
        pt_art_tools_path = "V:/Panda/Art/Tools/pt_art_tools"  # this should be changed to the upper one after we move coala out from Panda
        # coala_path = f"{pt_art_tools_path}/{project_coala}"
        coala_path = f"{pt_art_tools_path}/{project_coala}"
        python_lib_path = f"{pt_art_tools_path}/WinPython/{project_python}/Lib/site-packages"
        if python_lib_path not in sys.path:
            sys.path.append(python_lib_path)

        project_env["MAYA_SCENES"] = f"{project_location}/Art"
        project_env["PYTHONPATH"] = f"{pt_art_tools_path};{python_lib_path};{coala_path}"
        project_env["MAYA_MODULE_PATH"] = f"{coala_path}/plugins;"
        project_env["MAYA_PLUG_IN_PATH"] = f"{coala_path}/plugins;"

        project_env["PT_Project"] = self.project_name
        project_env["PT_Tools"] = pt_art_tools_path
        project_env["PT_Coala"] = project_coala

        if self.runas_dev == True:  # add folders to environment
            project_env["PT_Maya"] = "DEV"
            User = getpass.getuser()
            env_folder = f"C:/Users/{User}/Documents/maya"
        else:
            project_env["PT_Maya"] = "Stable"
            # icons folder
            project_env["XBMLANGPATH"] = project_icons
            env_folder = os.path.abspath(self.env)

        maya_exe_path = f"C:/Program Files/Autodesk/MAYA{project_maya_version}/bin/maya.exe"
        maya_arguments = [maya_exe_path]
        project_env["MAYA_APP_DIR"] = f"{os.path.abspath(env_folder)}/"  # Maya projects set from launcher
        # print(f'Running as {project_env["PT_Maya"]}: {project_name}')
        return (maya_arguments, project_env)

    @property
    def get_blender_env(self):
        return (None, None)

    @property
    def get_houdini_env(self):
        return (None, None)

    @property
    def get_unity_env(self):
        return (None, None)

    @property
    def get_unreal_env(self):
        return (None, None)


if __name__ == "__main__":
    test = get_env("Panda", "maya", True)
    print(test.maya_env)
    print(test.blender_env)