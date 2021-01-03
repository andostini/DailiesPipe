import AccessSilverstack as Silverstack
import subprocess

instances = Silverstack.findSilverstackInstances()


projects = Silverstack.getProjectList(0)


project = Silverstack.Project(projects[0])

project.fetchLibrary()
project.fetchFolderStructure()
#subprocess.call(('open', project.getCurrentBestClip(88)))

"""
{
    'name': 'B002C005_201219_15257', 
    'scene': '3', 
    'shot': '1', 
    'take': '5', 
    'camera': None, 
    'files': [
        {
            'relativePath': '/B002_15257/B002C005_201219_15257.cine', 
            'fileSize': 9787416628, 
            'fileType': 'cine', 
            'Volume': {
                'label': 'B002_15257', 
                'mountPath': '/Volumes/B002_15257', 
                'playbackPriority': 2
            }
        }, 
        {
            'relativePath': '/20201219_Pro7_PetProtect/OCN/SD01_(PART_1)_2020-12-19/B_Cam/B002_15257/B002_15257/B002C005_201219_15257.cine', 
            'fileSize': 9787416628, 
            'fileType': 'cine', 
            'Volume': {
                'label': 'PetProtect1', 
                'mountPath': '/Volumes/PetProtect1', 
                'playbackPriority': 2
                }
            }, 
        {
            'relativePath': '/20201219_Pro7_PetProtect/OCN/SD01_(PART_1)_2020-12-19/B_Cam/B002_15257/B002_15257/B002C005_201219_15257.cine', 
            'fileSize': 9787416628, 
            'fileType': 'cine', 
            'Volume': 
                {'label': 'PetProtect2', 
                'mountPath': '/Volumes/PetProtect2', 
                'playbackPriority': 2
            }
        }, 
        {
            'relativePath': '/20201219_Pro7_PetProtect/OCN/SD01_(PART_1)_2020-12-19/B_Cam/B002_15257/B002_15257/B002C005_201219_15257.cine', 
            'fileSize': 9787416628, 
            'fileType': 'cine', 
            'Volume': {
                'label': 'PromiseR412', 
                'mountPath': '/Volumes/PromiseR412', 
                'playbackPriority': 3
            }
        }, 
        {
            'relativePath': '/20201219_Pro7_PetProtect/OCN/SD01_(PART_1)_2020-12-31/SD01_(PART_1)/B002_15257/B002_15257/B002C005_201219_15257.cine', 
            'fileSize': 9787416628, 
            'fileType': 'cine', 
            'Volume': {
                'label': 'PetProtect5', 
                'mountPath': '/Volumes/PetProtect5', 
                'playbackPriority': 2}
        }
    ]
}
"""