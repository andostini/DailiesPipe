# DailiesPipeCLI
This is a 3rd Party CLI Tool to realtime sync your Silverstack Library to a DaVinci Studio Project. Developed in my freetime. Use at own risk.
This is version 0.1alpha and is tested with DaVinci 17.1.1 Build 9 and Silverstack and Silverstack Lab 7.3.1


## Quick Start Guide
### Prerequisites
- This script only works with the paid version of DaVinci Resolve Studio. A version for the free Lite version might be possible in future
- You need to enable external scripting in DaVinci. Go to 'DaVinci Resolve' -> 'Preferences' (Cmd + ,) -> 'General' and switch 'External scripting usage' to 'Local'.
- Download the .zip file from the Download folder above and extract it to somewhere on your computer. 
- Find the file named 'Python' within the folder and right-click open it (only works with right click open). Close the window when it says 'Process completed'
- Find the file named 'dailiespipe' within the folder and right-click open it (has to be right click opened only the first time you start it.)

### Start syncing
- Open Silverstack and DaVinci and create the projects that you want to associate. Existing projects can be used of course.
- Start the 'dailiespipe' executable
- Every new version of Silverstack will create a new Silverstack instance. Silverstack Lab will create its own instances. In the first step of the script you have to choose the instance in which you have created your project in. 
- It will now list all the projects in your chosen instance. If you can't find your Silverstack project here, close the terminal window and reopen the 'dailiespipe' executable and try another instance.
- In the last step the script will let you choose a DaVinci Project. Important: your project must be found in the root of the project manager
- Your projects will now be synced as long as you have the terminal window running in the background or until you close DaVinci.

### Things you should now
- This is a one way road. Your Silverstack project will not be manipulated or edited in any way. It will be just read out.
- Should your script crash, usually indicated with a Traceback, please take a screenshot and mail it to me or post it as an issue on Github describing the circumstances
- Only new folders will be imported into DaVinci. If your folder already exists in DaVinci but is empty it will not be touched

## Roadmap / Future features
- History (fast restart of former project links)
- Restart from beginning command
- Create Timeline for every reel
- Auto sync audio at input
- Auto apply Lut / Node Tree to clips
- Auto generate render job with specified render preset

## DaVinciAccess Documentation:

### getProjects()
Returns a list of all projects in the root folder of the project manager.

### getSubfolderNames(Folder)
Returns a list of all subfolder names of a given folder as an array of strings

### getSubfolderByName(Folder, Name)
Checks wether a a subfolder with a given name exists within the given folder object. Returns folder as object or None.


## SilverstacAccess Documentation:
### findSilverstackInstance()
To find all instances of Silverstack, SilverstackLab currently and once installed. Note: This tool is not compatible to all versions of Silverstack. Returns an array with the names of all instances, e.g.: ['Silverstack6', 'Silverstack7', 'SilverstackLab7'] 
Currently supported: Silverstack7

### getProjectList(instanceKey)
Finds all projects from a specific instance and retrieves first informations about the projects, e.g. their names and creation date. Returns array of dicts, with each dict beeing a project and its information.

### Project Class (project)
You can turn a project dict returned from getProjectList() into a Project class. With it's initialization it will store all basic information, but no Clips and Folders from your Silverstack project

#### fetchVolumes()
Retrieves all Volumes used in your Silverstack project

#### fetchFolderStructure()
Retrieves all folders, media bins, etc. and their child elements from your Silverstack project tree. Returns as an array of dicts.

#### fetchLibrary()
Retrieves all your clips from your media library, containing all their meta data and files. All clips have a unique Id called Owner. This is determined by Pomfort developers. Returns array of dicts

#### getClipFromLibrary(Owner)
Retrieves one clip with a specific Owner ID from your media library, containing all it's meta data and files. Returns dict. 

#### getCurrentBestClip(Owner)
Takes a specific Owner ID, looks wether its available in the library and gives one file which is best for usage. Takes into account the Playback Priority set in Silverstack software and wether the file is online.
Returns the file's path as a string or False, if no file is online. 

#### getJobs()
Returns all the job history of Silverstack as an array of objects with name, progress and state.

#### FetchBinItems(Folder)
Fetches all the items of a bin and returns only its path to its current best clip.



## Changelog
### v0.1 - 2021/01/03 



