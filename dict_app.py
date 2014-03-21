# -*- coding:Utf-8 -*-

class Glob:
    """Namespace for global variables"""

    dbName = "facerec"          # name of the database
    user = "root"               # user name
    passwd = ""                 # password
    host = "127.0.0.1"          # name or IP address of the server

    # Structure of the database
    dicoT ={"friends":[('id', "k"),
                       ('id_fb', "i"),
                       ('name', 255)]}

