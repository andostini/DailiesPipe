import SilverstackAccess as Silverstack
import subprocess





if __name__ == "__main__":
    instances = Silverstack.findSilverstackInstances()
    projects = Silverstack.getProjectList(0)
    
    project = Silverstack.Project(projects[3])
    project.fetchLibrary()

    project.fetchFolderStructure()
    