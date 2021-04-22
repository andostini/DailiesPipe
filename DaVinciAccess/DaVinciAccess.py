from DaVinciAccess.python_get_resolve import GetResolve


resolve = GetResolve()
try: 
    projectManager = resolve.GetProjectManager()
except:
    print('You must open DaVinci first')
    exit()
mediaStorage = resolve.GetMediaStorage()
projectManager.GotoRootFolder()

def getProjects():
    return projectManager.GetProjectListInCurrentFolder()

def getSubfolderNames(Folders):
    Folders = Folders.GetSubFolderList()
    list = []
    for Folder in Folders:
        list.append(Folder.GetName())
    return list

def getSubfolderByName(Folder, name):
    subFolders = Folder.GetSubFolderList()

    if subFolders != None:
        for subFolder in subFolders:
            if subFolder.GetName() == name:
                return subFolder
    
    return None



class Project:
    def __init__(self, projectName):
        self.projectName = projectName
        self.project = projectManager.LoadProject(projectName)
        self.mediaPool = self.project.GetMediaPool()
        self.RootFolder = self.mediaPool.GetRootFolder()

        subFolders = getSubfolderNames(self.RootFolder)
        if 'Source' not in subFolders:
            self.mediaPool.AddSubFolder(self.RootFolder, 'Source')

        if 'Timelines' not in subFolders:
            self.mediaPool.AddSubFolder(self.RootFolder, 'Timelines')

        self.SourceFolder = getSubfolderByName(self.RootFolder, 'Source')
        self.TimelineFolder = getSubfolderByName(self.RootFolder, 'Timeline')

    def GetName(self):
        return self.project.GetName()

    def checkConnection(self):
        #Check if project has been changed in the meantime
        try: 
            test = resolve.GetProjectManager()
        except:
            return False
        else:
            if self.projectName == projectManager.GetCurrentProject().GetName():
                return True
            else:
                return False

    def getSourceFolder(self):
        return self.SourceFolder

    def CreateFolder(self, Parent, Name):
        return self.mediaPool.AddSubFolder(Parent, Name)

    def AddToMediaPool(self, Items):
        if self.checkConnection():
            return mediaStorage.AddItemListToMediaPool(Items)
