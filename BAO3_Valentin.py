#Copyright (C) 2020 Valentin-Gabriel SOUMAH
# coding: utf-8
import time, os
from lxml import etree
def  extractionPatrons(patron, fichier):
    motif = patron.split() # On aura besoin de séparer chaque partie du discours recherchée
    if fichier.endswith(".tal.xml"):
        patronsxml(motif,fichier)
    elif fichier.endswith(".tal"):
        with open(fichier, encoding="utf8") as fic,open ("resultats/patrons.txt", "w", encoding="utf8") as out:
            phrases=fic.read().split("\n\n") #On coupe le contenu du fichier en paragraphes (soit chaque phrase traitée par talismane)
            for i,phrase in enumerate(phrases):
                lignes= phrase.split("\n") #Chaque paragraphe est composé de lignes (soit un mot avec toutes ses informations syntaxiques)
                for j, ligne in enumerate(lignes): 
                    elements=ligne.split() #On coupe chaque information de la ligne)
                    if  not ligne: continue #Debug les eventuelles lignes vides
                    if elements[3] == motif[0] and len(motif) < len(lignes[j-1:]):
                        '''la troisième information est le mot la partie du discours du mot
                        En parcourant chaque ligne on va regarder si on trouve la première partie du discours
                        On vérifie aussi si le nombre de mots restants dans la phrase est suffisant pour faire rentrer
                        toutes les parties du discours qui suivent'''
                        correspond = True #On initialise  une variable qui va nous dire si on a trouvé la suite qu'on cherche
                        match= elements[1]
                    
                        for k, PoS in enumerate(motif[1:]): 
                            lgnsuivantes=lignes[j+k+1].split() #On crée une liste contenant toutes les lignes à tester (lignes qui suivent susceptible de matcher le patron)
                            if  PoS!= lgnsuivantes[3]: #On compare chaque partie du discours suivant dans le motif aux partie du discours suivants dans la phrase
                                correspond=False #Si la PoS ne correspond pas, on enregistre que ça ne match pas.
                                break #Pas besoin de vérifier les lignes d'apres vu que ça match pas.
                            else:
                                #print(lignes[j+k])
                                match+=" "+ lgnsuivantes[1] #Et on retient le mot correspondant à chaque fois
                            
                        if correspond : #Si  on a jamais rencontré de non correspondance à la fin de la boucle alors on a trouvé notre suite!
                            out.write(match+"\n") #On l'écrit dans un fichier
    else:
        print("fichier non supporté, choisissez un autre fichier")
        
def patronsxml(motif,fichier):
    #Meme principe que la fonction du haut mais version xml avec xpath
    arbre = etree.parse(fichier)
    with open ("resultats/patrons.txt", "w", encoding="utf8") as out:
        for item in arbre.xpath("/basetalismane/p/item"):
            #print(item.xpath("a[1]")[0].text)
            if not item.xpath("a[4]"): continue
            if item.xpath("a[4]")[0].text == motif[0]:
                correspond = True
                match = item.xpath("a[2]")[0].text
                try:
                    for i in range(1, len(motif)):
                        if item.xpath("following-sibling::item["+str(i)+"]/a[4]")[0].text != motif[i]:
                            correspond = False
                        else: 
                            match += " " + item.xpath("following-sibling::item["+str(i)+"]/a[2]")[0].text
                    if correspond :
                        out.write(match+"\n")
                except IndexError:
                    pass
                    
    
                            
if __name__=='__main__':
    dicoPoS= {"nom propre": "NP", "nom commun": "NC", "adjectif":"ADJ","déterminant": "DET","verbe":"V","pronom":"PRO","adverbe":"ADV","préposition":"P","conjonction de subordination":"CS" ,"Conjonction de coordination":"CC"}
    for clé, valeur in dicoPoS.items():
        print(clé, ":" ,valeur)
    patron=input("\nQuel patron? Separez chaque partie du discours par un espace\n")
    lisfic = [fic for fic in os.listdir("resultats") if fic.endswith(".tal") or fic.endswith(".tal.xml")]
    fic = input("Dans quel fichier? Fichiers possibles: \n"+ str(lisfic) +"\n")
    debut=time.time()
    extractionPatrons(patron, "resultats/"+fic) #renseigner le fichier Talismane dans lequel extraire
    print("temps d'éxécution", time.time()-debut)
    if input("afficher le resultat?" ).lower() == "oui":
        with open("resultats/patrons.txt", encoding="utf8") as fichier:
            print(fichier.read())
