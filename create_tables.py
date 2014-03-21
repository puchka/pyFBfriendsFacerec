# -*- coding:Latin-1 -*-

import MySQLdb, sys
from dict_app import *

class GestionBD:
    """Mise en place et interfa�age d'une base de donn�es MySQL"""
    def __init__(self, dbName, user, passwd, host, port =3306):
        "�tablissement de la connexion - Cr�ation du curseur"
        try:
            self.baseDonn = MySQLdb.connect(db =dbName,
                  user =user, passwd =passwd, host =host, port =port)
        except Exception, err:
            print 'La connexion avec la base de donn�es a �chou� :\n'\
                  'Erreur d�tect�e :\n%s' % err
            self.echec =1
        else:    
            self.cursor = self.baseDonn.cursor()   # cr�ation du curseur
            self.echec =0

    def creerTables(self, dicTables):
        "Cr�ation des tables d�crites dans le dictionnaire <dicTables>."
        for table in dicTables:            # parcours des cl�s du dictionn.
            req = "CREATE TABLE %s (" % table
            pk =''
            for descr in dicTables[table]:
                nomChamp = descr[0]        # libell� du champ � cr�er
                tch = descr[1]             # type de champ � cr�er
                if tch =='i':
                    typeChamp ='INTEGER'
                elif tch =='k':
                    # champ 'cl� primaire' (incr�ment� automatiquement)
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
        "Suppression de toutes les tables d�crites dans <dicTables>"
        for table in dicTables.keys():
            req ="DROP TABLE %s" % table
            self.executerReq(req) 
        self.commit()                       # transfert -> disque

    def executerReq(self, req):
        "Ex�cution de la requ�te <req>, avec d�tection d'erreur �ventuelle"
        try:
            self.cursor.execute(req)
        except Exception, err:
            # afficher la requ�te et le message d'erreur syst�me :
            print "Requ�te SQL incorrecte :\n%s\nErreur d�tect�e :\n%s"\
                   % (req, err)
            return 0
        else:
            return 1

    def resultatReq(self):
        "renvoie le r�sultat de la requ�te pr�c�dente (un tuple de tuples)"
        return self.cursor.fetchall()

    def commit(self):
        if self.baseDonn:
            self.baseDonn.commit()         # transfert curseur -> disque        

    def close(self):
        if self.baseDonn:
            self.baseDonn.close()

class Enregistreur:
    """classe pour g�rer l'entr�e d'enregistrements divers"""
    def __init__(self, bd, table):
        self.bd =bd
        self.table =table
        self.descriptif =Glob.dicoT[table]   # descriptif des champs

    def entrer(self):
        "proc�dure d'entr�e d'un enregistrement entier"
        champs ="("           # �bauche de cha�ne pour les noms de champs
        valeurs ="("          # �bauche de cha�ne pour les valeurs
        # Demander successivement une valeur pour chaque champ :
        for cha, type, nom in self.descriptif:
            if type =="k":    # on ne demandera pas le n� d'enregistrement
                continue      # � l'utilisateur (num�rotation auto.)
            champs = champs + cha + ","
            val = raw_input("Entrez le champ %s :" % nom)
            if type =="i":
                valeurs = valeurs + val +","
            else: 
                valeurs = valeurs + "'%s'," % (val)
                
        champs = champs[:-1] + ")"    # supprimer la derni�re virgule, 
        valeurs = valeurs[:-1] + ")"  # ajouter une parenth�se
        req ="INSERT INTO %s %s VALUES %s" % (self.table, champs, valeurs)
        self.bd.executerReq(req)
        
        ch =raw_input("Continuer (O/N) ? ")
        if ch.upper() == "O":
            return 0
        else:
            return 1

###### Programme principal : #########

# Cr�ation de l'objet-interface avec la base de donn�es : 
bd = GestionBD(Glob.dbName, Glob.user, Glob.passwd, Glob.host)
if bd.echec:
    sys.exit()    

bd.creerTables(Glob.dicoT)
    
bd.close()
