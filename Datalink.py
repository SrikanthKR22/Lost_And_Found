'''#|/////////////////////////////////////////////////////////////////////////////////|[<START>]|\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\|#'''

#|\-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~|[<IMPORTS>]|-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~/|#

import mysql.connector as datawind
from mysql.connector import Error
import password

#|\-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~|[<FUNCTIONS>]|-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~/|#

config_data = {
    'host' : 'localhost',
    'user' : 'root',
    'passwd' : password.password,
    'database' : 'Lost_Found'
}

datalink = None
def get_connection():
    global datalink
    if datalink is None or not datalink.is_connected():
        try:
            datalink = datawind.connect(**config_data)
            print("\n||||[Connection Secured! Datalink Active!]||||\n")
        except Error as e:
            print("Cannot Connect To Datalink", e)
            datalink = None
    return datalink

def get_cursor(dictionary = False):
    datalink = get_connection()
    if datalink:
        return datalink.cursor(dictionary=dictionary)
    return None

def commit():
    datalink = get_connection()
    if datalink:
        datalink.commit()

def disconnect_datalink():
    global datalink
    if datalink and datalink.is_connected():
        datalink.close()
        print("Disconnected From Datalink Successfully!")

"""#|//////////////////////////////////////////////////////////////////////////////////|[<-END->]|\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\|#"""