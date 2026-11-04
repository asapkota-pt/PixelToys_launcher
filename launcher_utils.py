import os
import subprocess
import json

class get_project_data_object:
    """ Class to Read projects_info json file and return necessary information"""
    def __init__(self):
        self._project_info_json = "./PT_projects_info.json"
        self.project_list = self.get_project_list
        self.project_info = self.get_info_from_json

    @property
    def get_info_from_json(self):
        all_proj_data=""
        with open(self._project_info_json) as f:
            all_proj_data = json.load(f)

        if all_proj_data=="":
            return (False)
        else:
            return(all_proj_data)

    @property
    def get_project_list(self):
        pt_project_list = (x for x in self.get_info_from_json)
        return (list(pt_project_list))



class pt_projects():
    """Class for recieving list of Projects to populate Launcher UI"""
    def __init__(self):
        self.project_data = get_project_data_object()

    def get_project_list(self):
        return(self.project_data.project_list)

    def get_project_info(self):
        return (self.project_data.project_info)



class pt_proj_info:
    """Class to get each Project detailed information"""
    def __init__(self, project_name):
        super().__init__()
        self.project = project_name
        self._pt_projects = pt_projects()

        self._pt_project_list = self._pt_projects.get_project_list()
        self.project_data = None
        self.initialize()

    def initialize(self):
        if self.project in self._pt_project_list:
            self.project_data = self._pt_projects.get_project_info()

    @property
    def get_project_info(self):
        return(all_proj_data[self.project])

    def get_project_location(self):
        data=self.project_data[self.project]
        return(f"{data['project_location']}/{self.project}")

    def get_project_icon(self):
        data=self.project_data[self.project]
        return(f"{self.get_project_location()}/_info/_ico")

    def get_project_python(self):
        data=self.project_data[self.project]
        return(data['python'])

    def get_project_coala(self):
        data=self.project_data[self.project]
        return(data['coala_version'])

    def get_project_maya(self):
        data=self.project_data[self.project]
        return(data['maya_version'])

    def get_project_prefs(self):
        data=self.project_data[self.project]
        return(f"{self.get_project_location()}/_info/_mayaDocs")


if __name__ == "__main__":
    proj_list = pt_projects().get_project_list()
    print(proj_list)
    proj_data = pt_proj_info(proj_list[0])
    print(proj_data.get_project_location())
    print(proj_data.get_project_prefs())
    #for each_proj in proj_data.get_project_list():
    #    print (proj_data.get_project_info(each_proj))
