import os,re,sys

#
def listFileList(rootDir):
    for lists in os.listdir(rootDir):
        path = os.path.join(rootDir, lists)
        if os.path.isdir(path):
            listFileList(path)
        else:
            matchobj = re.match(r'^.*\.(m|mm)$', path, re.M|re.I)
            if matchobj:
                iffileViewController(path)

#
def iffileViewController(filename):
    text_file = open(filename, "r")
    for line in text_file:
        matchObj = re.match( r'[-]\s*\((\w+)\)\s*viewDidLoad\s*{?\s*', line, re.M|re.I)
        if matchObj:
            count = len(open(filename,'rU').readlines())
            methodcount = countMethodCount(filename)
            file = os.path.basename(filename)
            out = '%d\t\t%d\t\t%s\t' %(count,methodcount,file)
            print out
            break
    text_file.close()



#
def countMethodCount(filename):
    text_file = open(filename, "r")
    count = 0
    for line in text_file:
        matchObj = re.search( r'[-+]\s*\((\w+)\)\s*(\w+)\s*(:\((.+)\)\s*(\w+))?', line, re.M|re.I)
        if matchObj:
            count = count + 1

    text_file.close()
    return count



if __name__ == '__main__':
    argc = len(sys.argv)
    if argc == 2:
        out = 'lineNum\t\tmethodNum\t\tfileName\t'
        print out
        listFileList(sys.argv[1])
    else:
        print 'input error, please input path like (python count.py ./)'
