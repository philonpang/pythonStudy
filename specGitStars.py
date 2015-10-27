import os, re, sys, json

import ssl
import requests.packages.urllib3.util.ssl_
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL'

#count file output
outCountFile = 'outCount.xls'
lastopenfile = ''

#if count fix num
iscountvalid = 0
outPutNum = 2

#specific index
global fromIndex

#index
count = 0

#match the star text
def matchStarText(text):
    find = 0
    searchObj = re.search( r'.*stargazers">.*', text, re.M|re.I)
    if searchObj:
        find = 1
    return find

#match the star text
def matchForkText(text):
    find = 0
    searchObj = re.search( r'.*class="social-count">.*', text, re.M|re.I)
    if searchObj:
        find = 1
    return find

#drop the special char in line nums
def formatNumber(text):
    text = text.strip()
    text = text.replace(',','')
    return text



#open spec file read git url
def openAndReadGitUrl(path,count):
    json_file = open(path, "r")
    json_data = json.load(json_file)
    gitname = json_data["name"]
    giturl = 'none'
    if 'git' in json_data["source"]:
        giturl = json_data["source"]["git"]

    print ("%s\t%s" %(gitname,giturl))
    if giturl != 'none' and giturl.startswith('http'):
        gitsummary = 'none'
        if 'summary' in json_data:
            gitsummary = json_data['summary'].replace('\n','')
        gitDescription = 'none'
        if 'description' in json_data:
            gitDescription = json_data['description'].replace('\n','')
        gitstar = '-'
        gitfork = '-'

        try:
            fp = requests.get(giturl,timeout=15)
            if fp.status_code == requests.codes.ok:
                match = 0
                for line in fp.iter_lines():
                    line = line.decode('utf-8')
                    if match == 1:
                        gitstar =  formatNumber(line)
                        match = 0
                    if match == 2:
                        gitfork = formatNumber(line)
                        break


                    if matchStarText(line) == 1:
                        match = 1
                    if matchForkText(line) == 1:
                        match = 2
                out = '%d\t%s\t\t%s\t\t%s\t\t%s\t\t%s\t\t%s\n' %(count,gitname,gitstar,gitfork,giturl,gitsummary,gitDescription)
                out = out.encode('ascii', 'ignore')
                print (out.decode('utf-8'))
                file = open(outCountFile,'a')
                out = out.decode('utf-8')
                file.write(out)
        except requests.exceptions.HTTPError as e:
            print ("ERROR:%s" %(e))
        except requests.exceptions.Timeout as e:
            print ("ERROR:%s" %(e))
        except requests.exceptions.RequestException as e:
            print ("ERROR:%s" %(e))




# print all spec file
def listFileList(rootDir):
    global lastopenfile, count
    for file in os.listdir(rootDir):
        if iscountvalid and count >= outPutNum:
            break
        path = os.path.join(rootDir, file)
        if os.path.isdir(path):
            dirs = os.listdir(path)
            newpath = os.path.join(path, dirs[len(dirs)-1])
            if os.path.isdir(newpath):
                listFileList(newpath)
        else:
            if (count+1) >= fromIndex:
                openAndReadGitUrl(path, count+1)
            else:
                print ("index %d was jumped...fromIndex is %d" %(count+1,fromIndex))
            count += 1



if __name__ == '__main__':
    argc = len(sys.argv)
    if argc == 2:
        if os.path.exists(outCountFile):
            os.remove(outCountFile)
        fromIndex = 1
        listFileList(sys.argv[1])
    else:
        if argc == 3:
            fromIndex = int(sys.argv[2])
            listFileList(sys.argv[1])
        else:
            print ('input error, please input path like (python specGitStars.py ~/.cocoapods/repos/master/Specs)')
