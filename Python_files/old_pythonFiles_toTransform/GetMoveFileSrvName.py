from varsRemote import *

# Create directory
def createDir(sourcePath, dstDir):
    # Check if dst path exists
    if os.path.isdir(dstDir) == False:
        # Create all the dierctories in the given path
        os.makedirs(dstDir); 
    return None

createDir(sourcePath, dstDir)

# Move files from directory to another 
def moveAllFilesinDir(srcDir, dstDir):
    # Check if both the are directories
    if os.path.isdir(srcDir) and os.path.isdir(dstDir) :

        # Iterate over all the files in source directory
        for filePath in glob.glob(srcDir + '/*'):
            if filePath.endswith('.csv') and filePath.startswith('{}_'.format(dstDir)):
                # Move each file to destination Directory
                print(filePath)
                shutil.move(filePath, dstDir);
            else:
                pass
    else:
        print("srcDir & dstDir should be Directories")        

moveAllFilesinDir(srcDir, dstDir)

"""if __name__ == "__main__" :
    moveAllFilesinDir(srcDir, dstDir)"""