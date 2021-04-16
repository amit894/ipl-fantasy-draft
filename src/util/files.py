def readFile(self,fileName):
    try:
        f1=open('../resources/owners/'+fileName+'.json','r')
        output=json.load(f1)
        f1.close()
        return output
    except:
        f1.close()
        return ("Error reading from file")


def writeFile(self,fileName,data):
    existing_content=[]
    try:
        existing_content=readFile()
        existing_content.append(data)
    except:
        print("Error reading from file")
    try:
        f2=open('../resources/owners/'+fileName+'.json','w')
        json.dump(existing_content,f2)
        f2.close()
        return ("Written to file")
    except:
        f2.close()
        return ("Written to file failed")
