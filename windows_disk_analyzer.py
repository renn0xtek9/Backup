import re
import subprocess

def ConvertPathToCygwinPath(path):
    drive=path.split(':')[0]
    pathunderdrive=re.sub('\\\\','/',path.split(':')[1])
    cygpath=str('/cygdrive/{}{}'.format(drive.lower(),pathunderdrive))
    return cygpath

class WindowsDiskAnalyzer:
    def __init__(self):
        self.content=[""]
        pass

    def __AnalyzeDisks(self):
        sp=subprocess.Popen(["wmic",'logicaldisk','get','volumename,name'],
            stdout=subprocess.PIPE,bufsize=1)
        out,err=sp.communicate()
        out=out.decode('ascii').rsplit('\r\r\n')
        sp.wait()
        return out

    def getDictionnaryOfKeyAndDrive(self,content=[""]):
        if content==[""]:
            content=self.__AnalyzeDisks()
        ret=dict()
        for line in content:
            #print(line)
            line=line.rsplit('\n')[0]
            if ':' in line :
                drivepath=str(line.split(':')[0]+':')
                label=line.split(':')[1]
                label=re.sub('^ *','',label)
                label=re.sub(' *$','',label)
             #   print("{} {}".format(drivepath,label))
                if len(label)>0:
                    ret[label]=drivepath
        return ret