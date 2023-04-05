import os
import subprocess

limitSizeFile=10000000 # Bytes
quantityLines=20000+1
folderInput='C:/Dario/log-files/logs_ETL'
folderOutput='C:/Dario/log-files/logs_ETL_lastlines'
fileOutputErrors = open(f'{folderOutput}/_Files_with_errors.log', 'w')

def createNewFileLog(fileName):
    fileInputSize=os.path.getsize(f'{folderInput}/{fileName}')
    if fileInputSize > limitSizeFile:
        fileOutputErrors.write(f'File too large > {limitSizeFile} B: "{fileName}" | Size: {fileInputSize} B\n')
        return

    fileInputLinesCount=0
    with open(f'{folderInput}/{fileName}', 'r') as fileInput:
        for line in fileInput:
            fileInputLinesCount+=1
    fileInput.close()

    with open(f'{folderInput}/{fileName}', 'r') as fileInput:
        fileContent=fileInput.readlines()
    fileInput.close()

    fileOutput = open(f'{folderOutput}/{fileName}', 'w')
    print(fileName)
    q=min(quantityLines,fileInputLinesCount)
    for num in range(1,q): 
        fileOutput.write(fileContent[(q-num)*-1])
    fileOutput.close()

def gitCommitPush():
    os.chdir(folderOutput)
    subprocess.run(['git','init'])
    subprocess.run(['git','add','.'])
    subprocess.run(['git','commit','-m','Commit scheduled'])
    subprocess.run(['git','push','-u','origin','master'])

def main():
    os.system ('cls')
    listFiles = os.listdir(folderInput)
    listFilesLog = [fileItem for fileItem in listFiles if os.path.isfile(f'{folderInput}/{fileItem}') and fileItem.endswith(".log")]
    for i in listFilesLog:
        createNewFileLog(i)
    fileOutputErrors.close()
    gitCommitPush()

if __name__ == '__main__':
    main()