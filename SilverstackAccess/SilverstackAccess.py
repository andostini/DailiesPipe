import sys
import os
import plistlib
import sqlite3
import operator

def findSilverstackInstances():
    if sys.platform != "darwin":
        return "Error: You are not working on an compatible OS. Only MacOS 10.15.7 or higher is supported"
    else:
        pomfortFolder = os.path.expanduser('~/Library/Application Support/Pomfort/')
        try: 
            subFolders = os.listdir(pomfortFolder)
        except FileNotFoundError:
            return "Error: Silverstack doesn't appear to be installed on your system"
        
        instances = []
        
        for Folder in subFolders:
            if Folder.startswith('Silverstack'):
                instances.append(Folder)

        if len(instances) == 0:
            return "Error: No compatible Silverstack Instance has been found installed on your System"
        else:
            return instances



def getProjectList(instanceKey):
    instance = findSilverstackInstances()[instanceKey]
    pathToInstance = os.path.expanduser('~/Library/Application Support/Pomfort/' + instance + '/')
    projectFolders = os.listdir(pathToInstance)
    list = []
    
    for project in projectFolders:
        if project.startswith('Project-'):
            path = pathToInstance + project
            file = open(path + '/Project.plist', 'rb')
            plist = plistlib.load(file)
            file.close()
            list.append({
                'id' : project.rsplit('-')[1],
                'name' : plist['name'],
                'instance' : instance,
                'creationDate' : plist['creationDate']
            })
    return list
    
    
    
    
class Project:
    def __init__(self, project):
        self.projectName = project['name']
        self.id = project['id']
        self.instance = project['instance']
        self.pathToInstance = os.path.expanduser('~/Library/Application Support/Pomfort/' + self.instance + '/')
        self.pathToProject = os.path.expanduser('~/Library/Application Support/Pomfort/' + self.instance + '/Project-' + self.id)
        self.Volumes = None
        self.Library = None
        self.FolderStructure = None

    def fetchVolumes(self):
        #GET ALL VOLUMES on open project. Seperate function which will be called less often then the fetchVolume function
        try: 
            conn = sqlite3.connect(self.pathToProject + '/Silverstack.psdb')
            c = conn.cursor()
        except:
            return 'Error: Could not connect to Project Database.'

        c.execute('SELECT * FROM ZVOLUME ORDER BY ZPLAYBACKPRIORITY DESC, ZLABEL ASC')
        results = c.fetchall()
        conn.close()

        list = []
        for result in results:
            list.append({
                'label' : result[14],
                'priority' : result[8],
                'freeCapacity' : result[5],
                'totalCapacity' : result[9],
                'mountPath' : result[15]
            })
        self.Volumes = list
        return True

    def getVolume(self, PK):
        try: 
            conn = sqlite3.connect(self.pathToProject + '/Silverstack.psdb')
            c = conn.cursor()
        except:
            return 'Error: Could not connect to Project Database.'

        c.execute('SELECT ZPLAYBACKPRIORITY, ZLABEL, ZMOUNTPATH FROM ZVOLUME WHERE Z_PK=?', (PK,))
        result = c.fetchone()
        conn.close()

        return {
            'label': result[1],
            'mountPath' : result[2],
            'playbackPriority' : result[0]
        }

    def getCurrentBestClip(self, Owner):
        #Gets the file from the highest priority Volume (sorts alphabetically if identical prority), checks wether online (if not goes to next Volume) and returns its complete Path
        #Index is Index of Clip in self.Library

        clip = self.ClipFromLibrary(Owner)
        files = clip['files']

        files.sort(key=operator.itemgetter('volumePlaybackPriority'))
        files.reverse()
        val = ""
        for file in files:
            fullPath = file['volumeMountPath'] + file['relativePath']
            if os.path.isfile(fullPath):
                val = fullPath
                break
        else:
            val = False

        return val


    def fetchFiles(self, Owner):
        try: 
            conn = sqlite3.connect(self.pathToProject + '/Silverstack.psdb')
            c = conn.cursor()
        except:
            return 'Error: Could not connect to Project Database.'
        c.execute('SELECT Z_PK, ZFILESIZE, ZOWNER, ZVOLUME, ZFILETYPE, ZRELATIVEPATH FROM ZFILERESOURCE WHERE ZOWNER = ?', (str(Owner),))
        files = c.fetchall()
        list = []

        for file in files:
            Volume = self.getVolume(file[3])
            list.append({
                'relativePath' : file[5],
                'fileSize' : file[1],
                'fileType': file[4],
                'volumeLabel' : Volume['label'],
                'volumeMountPath': Volume['mountPath'],
                'volumePlaybackPriority' : Volume['playbackPriority']
            })

        return list

    def getClipFromLibrary(self, Owner):
        #get specific clip from Library by Owner
        if self.Library == None:
            return False

        for clip in self.Library:
            if clip['PK'] == Owner:
                return clip
        else:
            return False



    def fetchLibrary(self):
        try: 
            conn = sqlite3.connect(self.pathToProject + '/Silverstack.psdb')
            c = conn.cursor()
        except:
            return 'Error: Could not connect to Project Database.'

        c.execute('SELECT Z_PK,Z_ENT, ZMETADATA, ZUSERINFO, ZRECORDERINFO, ZTIMECODERANGE, ZPIXELHEIGHT, ZPIXELWIDTH, ZWHITEPOINTKELVIN, ZCREATIONDATE, ZSHOOTINGDATE, ZASA, ZDURATION, ZFPS, ZCODEC, ZNAME, ZSCENE, ZSHOT, ZTAKE, ZCAMERA, ZCOLORSPACE, ZIDENTIFIER FROM ZRESOURCEOWNER')
        Owners = c.fetchall()
        c.close()

        list = []

        for Owner in Owners:
            list.append({
                'name' : Owner[15],
                'PK' : Owner[0],
                'ENT' : Owner[1],
                'scene' : Owner[16],
                'shot' : Owner[17],
                'take' : Owner[18],
                'camera' : Owner[19],
                'files' : self.fetchFiles(Owner[0])
            })
        
        self.Library = list

    def fetchFolderStructure(self):
        try: 
            conn = sqlite3.connect(self.pathToProject + '/Silverstack.psdb')
            c = conn.cursor()
        except:
            return 'Error: Could not connect to Project Database.'

        c.execute('SELECT Z_PK FROM ZFOLDER WHERE ZFOLDERTYPE = ?', (20014,))
        RootPK = c.fetchone()[0]

        c.execute('SELECT Z_PK, ZFOLDERTYPE, ZSORTINDEX, ZMEDIABININFO, ZPARENT, ZNAME FROM ZFOLDER')
        Folders = c.fetchall()
        def findSubFolder(parentPK):
            list = []
            for Folder in Folders:
                if Folder[4] == parentPK:
                    list.append({
                        'PK' : Folder[0],
                        'name' : Folder[5],
                        'type' : Folder[1],
                        'sortIndex' : Folder[2],
                        'parent' : Folder[4],
                        'subFolders' : findSubFolder(Folder[0])
                    })
            list.sort(key=operator.itemgetter('sortIndex'))
            return list

        c.close()

