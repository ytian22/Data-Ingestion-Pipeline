from flask import Flask, request #import main Flask class and request objectfrom process_Jay2 import extract_json # import function from process.py
import os
import sys
import glob
import json


app = Flask(__name__) #create the Flask app


def extract_json(json_line):
    """
    This function processes 1 line of json and output extracted name and age info

    :param json_line: one blob/line of json file
    :return: extracted name and age
    """
    flag = 0
    name, age = '', ''
    try:
        a_dict = json.loads(json_line)
        # check present
        name, age = a_dict['name'], a_dict['prop']['age']
    except Exception as e:
        print('having error load json line: %s' % e)
        flag = 1

    # check non-empty
    if name == '' or age == '': flag = 1

    # check age
    if isinstance(age, int)==0: flag=1
    elif age<0: flag=1

    return '%s\t%s' % (name, age), flag


def check_existing_file(path, prefix, filename):
    '''
    This function removes every file that satisfies the pattern,
    '''
    for f in glob.glob('%s/%s/%s*.txt' % (path,prefix,filename.split('.')[0])): # remove file according to pattern
        os.remove(f)
    for f in glob.glob('%s/%s/%s*.log' % (path,prefix,filename.split('.')[0])): # remove file according to pattern
        os.remove(f)


@app.route('/',methods=['POST']) # change the method on the route to accept only POST requests
def processing_json():
    '''
    Use to receive & process json format POST request and write to file,
    '''
    
    # get raw string & write to txt
    raw = request.data.decode('utf-8').strip()   # one JSON blob
    with open("%s/%s/Raw.txt"%(path,prefix), "a") as f1:
        f1.write(raw+'\n')
        print('Successfully write in Raw.txt!')

    # process json & write to txt
    
    name_age, flag = extract_json(raw)
    if flag == 0: 
        with open("%s/%s/proc.txt"%(path,prefix), "a") as f2:
            f2.write(name_age+'\n')   # to make sure each record in a line
        print('Successfully write in proc.txt')
    
    return 'Done!'


if __name__ == '__main__':
    prefix = sys.argv[1]

    # should change
    path='/srv/runme'

    # check existing file and remove
    check_existing_file(path,prefix,'Raw.txt')
    check_existing_file(path,prefix,'proc.txt')

    # need to change port
    app.run(host='0.0.0.0', port=8080)