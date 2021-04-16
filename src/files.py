import json

def readFile(fileName):
    try:
        print(fileName)
        f1=open(fileName,'r')
        print(f1)
        output=json.load(f1)
        f1.close()
        return output
    except:
        return ("Error reading from file")


def writeFile(fileName,data):
    existing_content=[]
    try:
        existing_content=readFile(fileName)
        existing_content.append(data)
    except:
        print("Error reading from file")
    try:
        f2=open(fileName,'w')
        json.dump(existing_content,f2)
        f2.close()
        return ("Written to file")
    except:
        return ("Written to file failed")
