import AccessSilverstack as Silverstack
import subprocess





if __name__ == "__main__":
    instances = Silverstack.findSilverstackInstances()
    projects = Silverstack.getProjectList(0)
    
    project = Silverstack.Project(projects[0])
    project.fetchLibrary()

    