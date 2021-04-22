import sys
import os
import plistlib
import sqlite3
import operator


def findSilverstackInstances():
    if sys.platform != "darwin":
        return "Error: You are not working on an compatible OS. Only MacOS 10.15.7 or higher is supported"
    else:
        pomfortFolder = os.path.expanduser(
            '~/Library/Application Support/Pomfort/')
        try:
            subFolders = os.listdir(pomfortFolder)
        except FileNotFoundError:
            return "Error: Silverstack doesn't appear to be installed on your system"

        instances = []

        for Folder in subFolders:
            if Folder.startswith('Silverstack'):
                instances.append(Folder)

        if len(instances) == 0:
            return False
        else:
            return instances


def getProjectList(instanceKey):
    instance = findSilverstackInstances()[instanceKey]
    pathToInstance = os.path.expanduser(
        '~/Library/Application Support/Pomfort/' + instance + '/')
    projectFolders = os.listdir(pathToInstance)
    list = []

    for project in projectFolders:
        if project.startswith('Project-'):
            path = pathToInstance + project
            file = open(path + '/Project.plist', 'rb')
            plist = plistlib.load(file)
            file.close()
            list.append({
                'id': project.rsplit('-')[1],
                'name': plist['name'],
                'instance': instance,
                'creationDate': plist['creationDate']
            })
    return list


class Project:
    def __init__(self, project):
        self.projectName = project['name']
        self.id = project['id']
        self.instance = project['instance']
        self.pathToInstance = os.path.expanduser(
            '~/Library/Application Support/Pomfort/' + self.instance + '/')
        self.pathToProject = os.path.expanduser(
            '~/Library/Application Support/Pomfort/' + self.instance + '/Project-' + self.id)
        self.Volumes = None
        self.Library = None
        self.FolderStructure = None

    def fetchVolumes(self):
        # GET ALL VOLUMES on open project. Seperate function which will be called less often then the fetchVolume function
        try:
            conn = sqlite3.connect(self.pathToProject + '/Silverstack.psdb')
            c = conn.cursor()
        except:
            return 'Error: Could not connect to Project Database.'

        c.execute(
            'SELECT * FROM ZVOLUME ORDER BY ZPLAYBACKPRIORITY DESC, ZLABEL ASC')
        results = c.fetchall()
        conn.close()

        list = []
        for result in results:
            list.append({
                'label': result[14],
                'priority': result[8],
                'freeCapacity': result[5],
                'totalCapacity': result[9],
                'mountPath': result[15]
            })
        self.Volumes = list
        return True

    def getVolume(self, PK):
        try:
            conn = sqlite3.connect(self.pathToProject + '/Silverstack.psdb')
            c = conn.cursor()
        except:
            return 'Error: Could not connect to Project Database.'

        c.execute(
            'SELECT ZPLAYBACKPRIORITY, ZLABEL, ZMOUNTPATH FROM ZVOLUME WHERE Z_PK=?', (PK,))
        result = c.fetchone()
        conn.close()

        return {
            'label': result[1],
            'mountPath': result[2],
            'playbackPriority': result[0]
        }

    def getCurrentBestClip(self, Owner):
        # Gets the file from the highest priority Volume (sorts alphabetically if identical prority), checks wether online (if not goes to next Volume) and returns its complete Path
        # Index is Index of Clip in self.Library

        clip = self.getClipFromLibrary(Owner)
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
                'relativePath': file[5],
                'fileSize': file[1],
                'fileType': file[4],
                'volumeLabel': Volume['label'],
                'volumeMountPath': Volume['mountPath'],
                'volumePlaybackPriority': Volume['playbackPriority']
            })

        return list

    def getClipFromLibrary(self, Owner):
        # get specific clip from Library by Owner
        if self.Library == None:
            return False

        for clip in self.Library:
            if clip['PK'] == Owner:
                return clip
        else:
            return False

    def MediaBinOffloaded(self, PK):
        # Checks if a bin's offload job is completed
        try:
            conn = sqlite3.connect(self.pathToProject + '/Silverstack.psdb')
            c = conn.cursor()
        except:
            return 'Error: Could not connect to Project Database.'

        c.execute('SELECT ZMEDIABININFO FROM ZFOLDER WHERE Z_PK = ?', (PK, ))
        mediabininfo = c.fetchone()[0]

        c.execute(
            'SELECT ZOFFLOADJOB FROM ZMEDIABININFO WHERE Z_PK = ?', (mediabininfo, ))
        offloadjob = c.fetchone()[0]

        c.execute(
            'SELECT ZSTATEIDENTIFIER FROM ZACTIVITYJOB WHERE Z_PK = ?', (offloadjob, ))
        try:
            identifier = c.fetchone()[0]
        except:
            return False
        else:
            if identifier == "com.pomfort.workState.finishedSuccessfully":
                return True
            else:
                return False

        print("OFFLOADHJOB:", offloadjob)
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
                'name': Owner[15],
                'PK': Owner[0],
                'ENT': Owner[1],
                'scene': Owner[16],
                'shot': Owner[17],
                'take': Owner[18],
                'camera': Owner[19],
                'files': self.fetchFiles(Owner[0])
            })

        self.Library = list

    def getJobs(self):
        try:
            conn = sqlite3.connect(self.pathToProject + '/Silverstack.psdb')
            c = conn.cursor()
        except:
            return 'Error: Could not connect to Project Database.'

        c.execute('SELECT Z_PK,Z_ENT, Z_OPT, ZSOURCEMEDIABININFO, ZSOURCEPATH1, ZPROGRESS, ZSTARTDATE, ZTIMEELAPSED, ZJOBQUEUENAME, ZNAME, ZSTATEIDENTIFIER FROM ZACTIVITYJOB')
        Jobs = c.fetchall()
        c.close()

        list = []

        for Job in Jobs:
            list.append({
                "name": Job[9],
                "progress": Job[5],
                "startdarte": Job[6],
                "state": Job[10],
                "jobquename": Job[8],
            })

        return list

    def fetchFolderStructure(self):
        try:
            conn = sqlite3.connect(self.pathToProject + '/Silverstack.psdb')
            c = conn.cursor()
        except:
            return 'Error: Could not connect to Project Database.'

        c.execute('SELECT Z_PK FROM ZFOLDER WHERE ZFOLDERTYPE = ?', (20014,))
        RootPK = c.fetchone()[0]

        c.execute(
            'SELECT Z_PK, ZFOLDERTYPE, ZSORTINDEX, ZMEDIABININFO, ZPARENT, ZNAME FROM ZFOLDER ORDER BY ZSORTINDEX')
        Folders = c.fetchall()

        def findFolderType(typeNumber):
            if typeNumber == 20004:
                return "folder"
            elif typeNumber == 20005:
                return "bin"
            else:
                return "Unknown"

        def findItems(folderPK):
            c.execute(
                'SELECT ZOFFLOADJOB FROM ZMEDIABININFO WHERE ZFOLDER = ?', (folderPK,))
            offloadjob = c.fetchone()[0]

            c.execute(
                'SELECT ZSOURCERESOURCE FROM ZACTIVITYTASK WHERE ZJOB = ?', (offloadjob,))
            tasks = c.fetchall()

            for task in tasks:
                c.execute(
                    'SELECT ZOWNER FROM ZFILERESOURCE WHERE Z_PK = ?', (task[0],))
                Owner = c.fetchone()[0]
                Path = self.getCurrentBestClip(Owner)

            return'Cool'

        def findSubFolder(parentPK):
            list = []
            for Folder in Folders:

                if Folder[4] == parentPK:
                    # Adding Subfolder to tree

                    subfolder = {
                        'PK': Folder[0],
                        'name': Folder[5],
                        'type': findFolderType(Folder[1]),
                        'sortIndex': Folder[2],
                        'parent': Folder[4],
                        'subFolders': None
                    }

                    if subfolder['type'] == 'folder':
                        subfolder['subFolders'] = findSubFolder(Folder[0])

                    list.append(subfolder)

            list.sort(key=operator.itemgetter('sortIndex'))
            return list

        Tree = findSubFolder(RootPK)
        self.FolderStructure = Tree

        c.close()

        return True

    def FetchBinItems(self,Folder):
        try:
            conn = sqlite3.connect(self.pathToProject + '/Silverstack.psdb')
            c = conn.cursor()
        except:
            return 'Error: Could not connect to Project Database.'

        c.execute(
            'SELECT ZOFFLOADJOB FROM ZMEDIABININFO WHERE ZFOLDER = ?', (Folder['PK'],))
        offloadjob = c.fetchone()[0]

        c.execute(
            'SELECT ZSOURCERESOURCE FROM ZACTIVITYTASK WHERE ZJOB = ?', (offloadjob,))
        tasks = c.fetchall()

        items = []

        for task in tasks:
            c.execute('SELECT ZOWNER FROM ZFILERESOURCE WHERE Z_PK = ?', (task[0],))
            Owner = c.fetchone()[0]
            Path = self.getCurrentBestClip(Owner)
            items.append(Path)

        return items