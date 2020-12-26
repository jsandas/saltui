import struct

"""
Credit to Mike Lowe github ActiveState/code for the original work of parsing the lastlog database
https://github.com/ActiveState/code/blob/3b27230f418b714bc9a0f897cb8ea189c3515e99/recipes/Python/496768_Last_Login_Record_Extraction/recipe-496768.py
http://code.activestate.com/recipes/496768-last-login-record-extraction/

Currently only works in python2.  Something to do with the encoding of the data from
the data.
"""
def getrecord(file,uid, preserve = False):
    """
    Returns [int(unix_time),string(device),string(host)] from the lastlog formated file object, 
    set preserve = True to preserve your position within the file
    """
    last_log_format = '=L32s256s'
    position = file.tell()
    recordsize = struct.calcsize(last_log_format)
    file.seek(recordsize*uid)
    data = file.read(recordsize)
    if preserve:
        file.seek(position)
    try:
        returnlist =  list(struct.unpack(last_log_format,data))
        returnlist[1] = returnlist[1].replace('\x00','')
        returnlist[2] = returnlist[2].replace('\x00','')
        return returnlist
    except:
        return False

#if __name__ == '__main__':
def lastlog():
    try:
        import sys
        import pwd
        import time
    except:
        return 'Unsupported OS'

    try:
        llfile = open("/var/log/lastlog",'r')
    except:
      #print('Unable to open /var/log/lastlog')
      return 'Unable to find or open the file: /var/log/lastlog'

    last_log = {}
    last_log['users'] = {}
    for user in pwd.getpwall():
        username = user[0]
        last_log['users'][username] = {}
        record = getrecord(llfile,user[2])
        if record and record[0] > 0:
            #data = '%16s\t\t%s\t%s' % (user[0],time.ctime(record[0]),record[2])
            #print(data)
            last_log['users'][username]['last_login'] = time.ctime(record[0])
            last_log['users'][username]['client_ip'] = record[2]
        elif record:
            #data = '%16s\t\tNever logged in' % (user[0],)
            #print(data)
            last_log['users'][username]['last_login'] = 'Never'
            last_log['users'][username]['client_ip'] = 'N/A'
        else:
            pass
    llfile.close()
    return(last_log)
