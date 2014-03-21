# -*- coding:Utf-8 -*-

import facebook
import urllib
import MySQLdb, sys
from dict_app import *
import cv

oauth_access_token='CHANGE THIS TO YOUR ACCESS TOKEN'
graph = facebook.GraphAPI(oauth_access_token)
friends = graph.get_connections("me", "friends")

class GestionBD:
    """Mise en place et interfaçage d'une base de données MySQL"""
    def __init__(self, dbName, user, passwd, host, port =3306):
        "Établissement de la connexion - Création du curseur"
        try:
            self.baseDonn = MySQLdb.connect(db =dbName,
                  user =user, passwd =passwd, host =host, port =port)
        except Exception, err:
            print 'La connexion avec la base de données a échoué :\n'\
                  'Erreur détectée :\n%s' % err
            self.echec =1
        else:    
            self.cursor = self.baseDonn.cursor()   # création du curseur
            self.echec =0

    def creerTables(self, dicTables):
        "Création des tables décrites dans le dictionnaire <dicTables>."
        for table in dicTables:            # parcours des clés du dictionn.
            req = "CREATE TABLE %s (" % table
            pk =''
            for descr in dicTables[table]:
                nomChamp = descr[0]        # libellé du champ à créer
                tch = descr[1]             # type de champ à créer
                if tch =='i':
                    typeChamp ='INTEGER'
                elif tch =='k':
                    # champ 'clé primaire' (incrémenté automatiquement)
                    typeChamp ='INTEGER AUTO_INCREMENT'   
                    pk = nomChamp
                else:
                    typeChamp ='VARCHAR(%s)' % tch                
                req = req + "%s %s, " % (nomChamp, typeChamp)
            if pk == '':
                req = req[:-2] + ")"
            else:
                req = req + "CONSTRAINT %s_pk PRIMARY KEY(%s))" % (pk, pk)
            self.executerReq(req)

    def supprimerTables(self, dicTables):
        "Suppression de toutes les tables décrites dans <dicTables>"
        for table in dicTables.keys():
            req ="DROP TABLE %s" % table
            self.executerReq(req) 
        self.commit()                       # transfert -> disque

    def executerReq(self, req):
        "Exécution de la requête <req>, avec détection d'erreur éventuelle"
        try:
            self.cursor.execute(req)
        except Exception, err:
            # afficher la requête et le message d'erreur système :
            print "Requête SQL incorrecte :\n%s\nErreur détectée :\n%s"\
                   % (req, err)
            return 0
        else:
            return 1

    def resultatReq(self):
        "renvoie le résultat de la requête précédente (un tuple de tuples)"
        return self.cursor.fetchall()

    def commit(self):
        if self.baseDonn:
            self.baseDonn.commit()         # transfert curseur -> disque        

    def close(self):
        if self.baseDonn:
            self.baseDonn.close()



bd = GestionBD(Glob.dbName, Glob.user, Glob.passwd, Glob.host)
if bd.echec:
    sys.exit()

table = "friends"
champs = "(id_fb, name)"

haar=cv.Load('haarcascade_frontalface_default.xml')

# go over the images of the friends
for friend in friends["data"]:
    print friend[u'name'], friend[u'id']
    # retrieve image file and store in tree
    urllib.urlretrieve ("https://graph.facebook.com/"+friend[u'id']+"/picture?width=200&height=200",
                        "images/photo/"+friend[u'id']+".jpg")
    id_fb = friend[u'id'].decode('utf8')
    name = MySQLdb.escape_string(friend[u'name'].decode('utf8'))
    valeurs = "("+id_fb+",'"+name+"')"
    req ="INSERT INTO %s %s VALUES %s" % (table, champs, valeurs)
    bd.commit()
    bd.executerReq(req)
    
    image = cv.LoadImage("images/photo/"+friend[u'id']+".jpg")
    storage = cv.CreateMemStorage()
    detected = cv.HaarDetectObjects(image, haar, storage, 1.1, 2,
                                cv.CV_HAAR_DO_CANNY_PRUNING, (10,10))
    if detected:
        c = 0
        for face in detected:
            center = (face[0][0]+face[0][2]/2,
                      face[0][1]+face[0][3]/2)
            rows = face[0][3]
            cols = face[0][2]
            dst = cv.CreateMat(rows, cols, cv.CV_8UC3);
            cv.GetRectSubPix(image, dst, center)
            cv.SaveImage('images/face/'+friend[u'id']+"_"+str(c)+".jpg", dst)
            c+=1

bd.close()
