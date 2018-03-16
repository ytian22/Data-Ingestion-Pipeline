import subprocess
import sys
import os
from datetime import datetime

def rotate_log(path, prefix, filename):
    '''
    This process change the file name to a suffixed version, as log rotation does

    :param when: 'S' -> second, 'M' -> minute
    :param path: path of file that needs to be rotated
    :param prefix: prefix
    :param filename: Raw.txt or proc.txt
    '''
    # file name of the file to be rotated
    file='%s/%s/%s'%(path,prefix,filename)
    print(file)

    # get the time as a unique combination
    now = datetime.now()
    date=now.date()
    H=now.hour
    M=now.minute
    S=now.second

    # new & unique file name give to it
    suffix = "%s-%s-%s-%s"%(date,H,M,S)
    result_file = '%s/%s/%s'%(path,prefix,('-'+suffix+'.').join(filename.split('.')))

    # use command line to rename file to achieve rotation
    if os.path.isfile(file):
        subprocess.call(['mv %s %s'%(file,result_file)],shell=True)


if __name__ == '__main__':
    # should change for test or homework
    path ='/srv/runme'

    prefix = sys.argv[1]
    rotate_log(path, prefix, 'Raw.txt')
    rotate_log(path, prefix, 'proc.txt')