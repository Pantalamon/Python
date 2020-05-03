#Copyright (C) 2020 Valentin-Gabriel SOUMAH
# coding: utf-8
import os,re,time
from lxml import etree

dejatraite, k, l = set(),0,0 #Ensemble avec les titres déjà vu et compteurs des echecs et réussites

def parcours(dossierin,dossierout,rubrique="tout",extractiontype="lxml"):
    if extractiontype not in ["lxml","regex"]:
        raise ValueError('l\'argument extractiontype doit prendre la valeur "lxml" ou "regex"')
    rubrik=rubiconv(rubrique)
    try:
        os.mkdir(dossierout)
    except OSError:
        pass
    print("on extrait dans le dossier: ",os.path.join(os.getcwd(),dossierin))
    print("les résultats seront enregistrés dans le dossier: ",os.path.join(os.getcwd(),dossierout))
    #On ouvre les deux fichiers dans lesquels on va écrire. Un avec uniquement le texte et description et l'autre un fichier XML avec les balises correspondantes.
    with open(dossierout+"/"+rubrique+".xml","w",encoding="utf8") as extraitxml ,open(dossierout+"/"+rubrique+".txt","w", encoding="utf8") as extraittxt:
        extraitxml.write('<?xml version="1.0" encoding="UTF-8"?>\n<extraction>') #On met l'en-tête XML et on ouvre la balise racine
        for racine,dossiers,fichiers in os.walk(dossierin): #Permet de parcourir tous les repertoires du dossier par récursivité
            #print("dossier exploré: ", racine)
            for fichier in fichiers:
                if re.match(rf'{rubrik}.xml', fichier) and (fichier.endswith("xml")):
                    if extractiontype=="lxml":
                        extractionlxml(fichier,racine,extraitxml,extraittxt)
                    else:
                        extractionregex(fichier,racine,extraitxml,extraittxt)
        extraitxml.write("\n</extraction>")
    print("réussis :",k, ",echecs :",l, sep=" ")

def extractionlxml(fichier,racine,sortiexml, sortietxt):
    global k,l,dejatraite
    #On a besoin du chemin absolu pour parse. On le crée grace à path.join
    chemin=os.path.join(os.getcwd(),racine,fichier)
    try:
         
        
        #On ouvre en byte pour le donner directement à parser
        with open(chemin, "rb") as fic:
             lire=fic.read()
             #On déséchappe les caractères spéciaux
             c=lire.replace(bytes("&lt","utf8"),bytes("<","utf8")).replace(bytes("&gt;","utf8"),bytes(">","utf8"))


        #On va créer un objet spécial de type "etree" qui contient toute l'arborescence xml du fichier de manière accessible
        tree=etree.fromstring(c)
        #tree=etree.parse(chemin)
        sortietxt.write("\n------------------") #Pour séparer chaque fil rss. On en aura besoin dans la bao4
        elements=tree.xpath("//item/description|//item/title") #Une liste qui contient tous les éléments correspondant à la requête xpath
        i=0
        while i < len(elements)-1: #On va parcourir les éléments de la liste 2 par 2
            #uniquement les paires title-description ayant pour parent "item"
            if elements[i].tag == "title" and elements[i+1].tag == "description":
                title,descript=elements[i],elements[i+1]
                if title.text not in  dejatraite :
                    description=descript.text #Nous  permet de récup uniquement le contenu textuel
                    if description is None :
                         description="pas de description" #Evite les cas où l'élément n'a pas de contenu    
                    titre=title.text
                    #On écrit écrit successivement le texte brut dans un fichier et le texte encadré de balises dans l'ordre
                    sortietxt.write("\n"+titre+"\n"+description)
                    sortiexml.write(("\n"+"<item>"+"\n"+"<title>"+titre+".</title>\n<description>"+description+"</description>\n</item>").replace("&","&amp;"))
                    dejatraite.add(titre) #On remplit l'ensemble des titres déjà vu
                i+=2 #On passe à la paire suivante
            else:
                i+=1 #Pas de paire titre-descript donc on avance que d'un indice
        k+=1
    except etree.XMLSyntaxError:
        print("le document suivant : {} \n est mal formé. Il n'a pas pu être traité".format(chemin))
        l+=1
        
def extractionregex(fichier,racine,sortiexml, sortietxt):
    #Extraction avec regex
    global k,l,dejatraite
    with open(racine+"/"+fichier, encoding="UTF-8") as entree:
        texte=entree.read()
        sortietxt.write("\n------------------") #Pour séparer chaque fil rss. On en aura besoin dans la bao4
        #On cherche le pattern sur tout le fichier et on itére sur les  objets match en résultat
        for match in re.finditer("<title>(.*?)</title>.*?<description>(.*?)</description>",texte,re.DOTALL):
            #Plus qu'à capturer ce qu'on a trouvé entre les parenthèses avec .group()
            titre=match.group(1)
            if titre not in dejatraite:
                sortietxt.write("\n"+match.group(1)+"\n"+match.group(2))
                sortiexml.write("<item>"+"\n"+"<titre>"+match.group(1)+".</titre>\n<description>"+match.group(2)+"</description>\n</item>\n".replace("&","&amp;"))
                dejatraite.add(titre)
        k+=1
    

def rubiconv(nom): #conversion du nom de rubrique en indicatif chiffré. Crédit à Corentin Vialar pour cette fonction!
	corres = {'tout':'0,2-(.*),0|0,57-0,64-823353,0|env_sciences','une':'0,2-3208,1-0,0', 'international':'0,2-3210,1-0,0', 'europe':'0,2-3214,1-0,0', 'societe':'0,2-3224,1-0,0', 'idees':'0,2-3232,1-0,0', 'economie':'0,2-3234,1-0,0', 'actualite-medias':'0,2-3236,1-0,0', 'sport':'0,2-3242,1-0,0', 'planete':'0,2-3244,1-0,0', 'culture':'0,2-3246,1-0,0', 'livres':'0,2-3260,1-0,0', 'cinema':'0,2-3476,1-0,0', 'technologies':'0,2-3546,1-0,0', 'politique':'0,57-0,64-823353,0', 'sciences':'env_sciences'}
	return(corres.get(nom))

 ############################ Choisissez dossiers d'entrée et sortie et rubrique ###################################################

if __name__ == "__main__":
    parcours("2019","resultats",rubrique="societe",extractiontype="regex")

