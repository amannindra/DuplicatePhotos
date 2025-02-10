from PIL import Image
import os
import hashlib
import shutil
def getFileSize(filePath):
    try:
        image = Image.open(filePath)
        width, height = image.size
        return [width, height]
    except IOError:
        return

def getFilesinFolder(folder):
    hashList = []
    for filename in os.listdir(folder):
        filePath = os.path.join(folder, filename)
        # print(f"filepath: {filePath}")
        if os.path.isfile(filePath):
            size = getFileSize(filePath)
            if size:
                hash = getImageHash(filePath)
                hashList.append([filePath, size, hash])
                # print(f'Image Hash: {getImageHash(filePath)}')   
    return hashList
        
def getImageHash(filePath):
    with open(filePath, 'rb') as f:
        digest = hashlib.file_digest(f, "sha256")
        return digest.hexdigest()



def findDuplicates(hashList, k):
    duplicate = {}
    for i in range(len(hashList)):
        stringVersion = str(hashList[i][k])
        if stringVersion in duplicate:
            duplicate[stringVersion].append(hashList[i][0])
        else:
            duplicate[stringVersion] = [hashList[i][0]]
    return duplicate


# def createFolderForDuplicates(currentFolder, list):
#     os.makedirs(os.path.join(currentFolder, ), exist_ok=True)

#        for filePath1, filePath2 in list:
#         folderName = os.path.dirname(filePath1)
#         os.makedirs(os.path.join(currentFolder, folderName), exist_ok=True)
#         shutil.copy(filePath1, os.path.join(currentFolder, folderName))
#         shutil.copy(filePath2, os.path.join(currentFolder, folderName))
    

def createFoldersForEachDuplicate(currentFolder, duplicates):
    for size in duplicates:
        print(size)
        os.makedirs(os.path.join(currentFolder, size), exist_ok=True)
        for filePath in duplicates[size]:
            shutil.copy(filePath, os.path.join(currentFolder, size))
    
def main():
    currentFolder = os.path.join(os.getcwd(), "photos")
    hash = getFilesinFolder(currentFolder)
    print(hash)
    bySize = findDuplicates(hash, 1)
    byHash = findDuplicates(hash, 2)
    
    print(byHash)

    # if(len(bySize) > 0):
    #     createFoldersForEachDuplicate(currentFolder, bySize)
    # if(len(byHash) > 0):
    #     createFoldersForEachDuplicate(currentFolder, byHash)
    
    
main()
