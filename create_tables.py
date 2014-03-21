# -*- coding:Latin-1 -*-

import MySQLdb, sys
from dict_app import *

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

class Enregistreur:
    """classe pour gérer l'entrée d'enregistrements divers"""
    def __init__(self, bd, table):
        self.bd =bd
        self.table =table
        self.descriptif =Glob.dicoT[table]   # descriptif des champs

    def entrer(self):
        "procédure d'entrée d'un enregistrement entier"
        champs ="("           # ébauche de chaîne pour les noms de champs
        valeurs ="("          # ébauche de chaîne pour les valeurs
        # Demander successivement une valeur pour chaque champ :
        for cha, type, nom in self.descriptif:
            if type =="k":    # on ne demandera pas le n° d'enregistrement
                continue      # à l'utilisateur (numérotation auto.)
            champs = champs + cha + ","
            val = raw_input("Entrez le champ %s :" % nom)
            if type =="i":
                valeurs = valeurs + val +","
            else: 
                valeurs = valeurs + "'%s'," % (val)
                
        champs = champs[:-1] + ")"    # supprimer la dernière virgule, 
        valeurs = valeurs[:-1] + ")"  # ajouter une parenthèse
        req ="INSERT INTO %s %s VALUES %s" % (self.table, champs, valeurs)
        self.bd.executerReq(req)
        
        ch =raw_input("Continuer (O/N) ? ")
        if ch.upper() == "O":
            return 0
        else:
            return 1

###### Programme principal : #########

# Création de l'objet-interface avec la base de données : 
bd = GestionBD(Glob.dbName, Glob.user, Glob.passwd, Glob.host)
if bd.echec:
    sys.exit()    

bd.creerTables(Glob.dicoT)
    
bd.close()
