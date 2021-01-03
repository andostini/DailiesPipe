# SilverstackAccess
This is a 3rd party tool reveal a an API for Pomfort's Silverstack and SilverstackLab to make use of its Media Library, ingested media and meta data. 
This module is not published on Pypi.

## Basic Functions:
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

## Changelog
### v0.1 - 2021/01/03 



