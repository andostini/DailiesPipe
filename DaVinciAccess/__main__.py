import DaVinciAccess as DaVinci




if __name__ == "__main__":
    print(DaVinci.getProjects())

    #Master/Source/Audi/

    project = DaVinci.Project('TRAINING')
    input()
    print(project.checkConnection())