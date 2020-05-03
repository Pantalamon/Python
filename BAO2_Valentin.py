#Copyright (C) 2020 Valentin-Gabriel SOUMAH
# coding: utf-8
import os,subprocess,html
from BAO1_Valentin import * #On importe les fonctions dans le fichier BAO1_Valentin.py
def main():
    global fileouttree,fileouttal
    rss=input("voulez-vous extraire les fils rss avant l'étiquettage?")
    aChoisir = False
    if rss.lower() == "oui":
        
        dossierRss= input("dossier rss?")
        rubrique = input("quelle rubrique?")
        parcours(dossierRss,"resultats",rubrique) # On run notre function
        filein="../resultats/" + rubrique + ".txt"
    else:
        aChoisir = True
        
        
    
    fileouttree,fileouttal="",""
    while True:
        choix = input('''Quel  parseur utiliser?
Pour utiliser TreeTagger tapez 1, 
Pour utiliser Talismane tapez 2,
Pour utiliser les 2 tapez 3\n''')
        if choix == "1":
            if aChoisir:
                fichiers=[fichier for fichier in os.listdir("resultats/") if fichier.endswith(".xml")]
                filein="../resultats/"+input("Dans quel fichier est le texte à étiquetter? fichiers possibles:\n"+str(fichiers)+"\n")
            fileouttree=Treetag(filein)
            break
        elif choix =="2":
            if aChoisir:
                fichiers=[fichier for fichier in os.listdir("resultats/") if fichier.endswith(".txt")]
                filein="../resultats/"+input("Dans quel fichier est le texte à étiquetter? fichiers possibles:\n"+str(fichiers)+"\n")
            fileouttal=Talis(filein)
            break
        elif choix =="3":
            if aChoisir:
                fichiers1=[fichier for fichier in os.listdir("resultats/") if fichier.endswith(".txt")]
                fichiers2=[fichier for fichier in os.listdir("resultats/") if fichier.endswith(".xml")]
                filein1="../resultats/"+input("Dans quel fichier est le texte à étiquetter par Talismane? fichiers possibles:\n"+str(fichiers)+"\n")
                filein2="../resultats/"+input("Dans quel fichier est le texte à étiquetter par Treetagger? fichiers possibles:\n"+str(fichiers)+"\n")
            fileouttal=Talis(filein1)
            fileouttree=Treetag(filein2)
            break
        else:
            print("Selection incorrecte")
    fileout= fileouttree+".xml "+fileouttal
    print("terminé! Les résultats sont dans "+fileout)

def Talis(filein):
    fileouttal=os.path.splitext(filein)[0] + ".tal" #On recupère les chemins des fichiers dont on a besoin
    dossier="TALISMANE-BAO2019-DISTRIB"
    os.chdir(dossier) #On se déplace dans le dossier talismane avant de lancer la commande shell
    #On concatène les fichiers que la commande shell utilise comme argument
    print(os.getcwd)
    commande="java -Xmx1G -Dconfig.file=talismane-fr-5.0.4.conf -jar talismane-core-5.1.2.jar --analyse --sessionId=fr --encoding=UTF8 --inFile="+filein+" --outFile="+fileouttal
    #On run la commande  comme si elle était passé en commande directement au shell (shell= true)
    subprocess.run(commande, shell=True, check=True)
    conversiontalXML(fileouttal,fileouttal+".xml")
    os.chdir("..")
    return fileouttal
    
def Treetag(filein): #Meme principe avec Treetagger
    fileouttree=os.path.splitext(filein)[0] + "_treetagger.tsv"
    os.chdir("Treetagger")
    #commande="cat "+filein+" |cmd/tree-tagger-french > "+ fileouttree
    commande="perl tokenise.pl "+filein+" |cmd/tree-tagger-french > "+fileouttree
    subprocess.run(commande, shell=True, check=True)
    conversiontreeXML(fileouttree, fileouttree+".xml")
    #subprocess.run("perl treetagger2xml-utf8.pl "+fileouttree +" utf8", shell = True, check=True)
    os.chdir("..")
    return fileouttree

def conversiontreeXML(fichier1,fichier2):
    with open(fichier1, encoding="utf8") as entree, open(fichier2, "w", encoding="utf8") as sortie:
        if fichier1.endswith(".tsv"):
            for ligne in entree:
                lig=ligne
                if not ligne.startswith("<"):
                    lig=ligne.strip("\n").replace("&amp", "&amp;").replace("<unknown>","unknown")
                    colonnes=lig.split("\t")
                    colonnes.append("<data type=\"string\">"+colonnes.pop(0)+"</data>")
                    colonnes[0]="<data type=\"type\">"+colonnes[0]+"</data>"
                    colonnes[1]="<data type=\"lemma\">"+colonnes[1]+"</data>"
                    lig="<element>"+"".join(colonnes)+"</element>\n"
                sortie.write(lig+"\n")

def conversiontalXML(fichier1, fichier2):
    with open(fichier1, encoding="utf8") as entree, open(fichier2, "w", encoding="utf8") as sortie:
        sortie.write('<?xml version="1.0" encoding="utf-8"?>\n<basetalismane>\n')
        for paragraphe in html.escape(entree.read()).split("\n\n"):
            if not paragraphe.startswith("1\t-"):
                sortie.write("<p>\n")
                for ligne in paragraphe.split("\n"):
                    sortie.write("<item><a>")
                    sortie.write("</a><a>".join(ligne.split("\t"))[:-1])
                    sortie.write("</a></item>\n")    
                sortie.write("</p>\n")
        sortie.write("</basetalismane>")

if __name__ == "__main__":
    main()

    
    
