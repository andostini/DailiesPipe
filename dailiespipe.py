import SilverstackAccess as Silverstack
import json 
import time
import DaVinciAccess as DaVinci

instances = Silverstack.findSilverstackInstances()

if instances == False:
    print("Error: No compatible Silverstack Instance has been found installed on your System")
    exit()

print("""Welcome to DailiesPipe. This tool is developed to synchronize your Silverstack Library to DaVinci in realtime. 
Your current version of DailiesPipe is v0.1 and is tested with Silverstack (Lab) 7.3.1 and Resolve Studio 17.1. Check for updates under fabian-decker.de/dailiespipe.

Not sure what to do? Check out the manual under fabian-decker.de/dailiespipe

STEP 1: Choose your Silverstack instance to sync from""")



i = 0
while i < len(instances):
    print("[{}] - {}".format(i, instances[i]))
    i += 1

print("Type the number of the silverstack instance that you want to sync from")
UserInstance = input()


instanceFound = False
while instanceFound == False:
    try: 
        ProjectList = Silverstack.getProjectList(int(UserInstance))
    except: 
        print("Error: choose a number from the list above. Go to website for help")
        UserInstance = input()
    else:
        instanceFound = True
        ProjectList = Silverstack.getProjectList(int(UserInstance))


i = 0
while i < len(ProjectList):
    print("[{}] - {} - {}".format(i, ProjectList[i]['name'],ProjectList[i]['id']))
    i += 1

print("Type the number of the silverstack project that you want to sync from")
UserProject = input()
Project = False

projectFound = False
while projectFound == False:
    try: 
        Project = Silverstack.Project(ProjectList[int(UserProject)])
    except:
        print("Error: choose a number from the list above. Go to website for help")
        UserProject = input()
    else:
        projectFound = True


print('STEP 2: Lets choose the DaVinci Project that you want to sync to.')

davinciprojects = DaVinci.getProjects()
i = 0
while i < len(davinciprojects):
    print("[{}] - {}".format(i, davinciprojects[i]))
    i += 1

UserDaVinciProject = input()
projectFound = False


while projectFound == False:
    try:
        DaVinciProject = DaVinci.Project(DaVinci.getProjects()[int(UserDaVinciProject)])
    except Exception as e:
        print("Error: choose a number from the list above. Go to website for help")
        print(e)
        UserDaVinciProject = input()
    else:
        projectFound = True

Project.fetchLibrary()
Project.fetchFolderStructure()


def SyncToDavinci(SilFolders, DaFolder, TopLevel):
    #peeeew
    #SilFolders refers to the Silverstack Folder tree, DaFolder refers to the Folder in Davinci will relate to the Silverstack Root Folder, given as an DaVinci Folder Object
    
    if TopLevel:
        Project.fetchLibrary()
        Project.fetchFolderStructure()
    
    if DaVinciProject.checkConnection():
        if TopLevel:
             print('Syncing...')

        for Folder in SilFolders:
            if Folder["type"] == 'folder':
                #Create complement in Resolve
                DaSubFolder = DaVinci.getSubfolderByName(DaFolder, Folder['name'])
                if  DaSubFolder == None:
                    DaVinciProject.CreateFolder(DaFolder, Folder['name'])
                    DaSubFolder = DaVinci.getSubfolderByName(DaFolder, Folder['name'])

                if len(Folder['subFolders']) > 0:
                    SyncToDavinci(Folder['subFolders'], DaSubFolder, False)

            elif Folder["type"] == 'bin':
                DaSubFolder = DaVinci.getSubfolderByName(DaFolder, Folder['name'])
                if  DaSubFolder == None:
                    if Project.MediaBinOffloaded(Folder["PK"]):
                        Bin = DaVinciProject.CreateFolder(DaFolder, Folder['name'])
                        Items = Project.FetchBinItems(Folder)
                        DaVinciProject.AddToMediaPool(Items)
                        
    else:
        print('You have closed your associated DaVinci Project. Close this window, open the project in DaVinci and restart this script')
        exit()

    if TopLevel:
        time.sleep(5)   
        SyncToDavinci(Project.FolderStructure, DaVinciProject.getSourceFolder(), True)


SyncToDavinci(Project.FolderStructure, DaVinciProject.getSourceFolder(), True)




f = open("test.json", "w")
f.write(json.dumps(Project.FolderStructure))
f.close()




