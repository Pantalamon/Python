#Copyright (C) 2020 Valentin-Gabriel SOUMAH
# coding: utf-8
import os
import BAO1_Valentin as Bao1
from sklearn.naive_bayes import GaussianNB,ComplementNB,MultinomialNB 
from sklearn.feature_extraction.text import TfidfVectorizer
from numpy import nditer

#On réutilise le dictionnaire avec toutes les rubrique de la BAO1
corres = {'tout':'0,2-(.*),0|0,57-0,64-823353,0|env_sciences','une':'0,2-3208,1-0,0', 'international':'0,2-3210,1-0,0', 'europe':'0,2-3214,1-0,0', 'societe':'0,2-3224,1-0,0', 'idees':'0,2-3232,1-0,0', 'economie':'0,2-3234,1-0,0', 'actualite-medias':'0,2-3236,1-0,0', 'sport':'0,2-3242,1-0,0', 'planete':'0,2-3244,1-0,0', 'culture':'0,2-3246,1-0,0', 'livres':'0,2-3260,1-0,0', 'cinema':'0,2-3476,1-0,0', 'technologies':'0,2-3546,1-0,0', 'politique':'0,57-0,64-823353,0', 'sciences':'env_sciences'}


def constitutioncorpus():
    if not os.path.isdir("bao4donnees"):
            os.mkdir("bao4donnees")
    textes,classes=[],[] #On crée des listes vide qu'on remplira avec le contenu de chaque fil rss et leur classe associées
    for rubrik in corres:
        if rubrik == "tout":continue
        #Pour chaque rubrique on lance la Bao1, on a donc un fichier txt par rubrique.
        Bao1.parcours("2019","bao4donnees",rubrique=rubrik,extractiontype="lxml")

        with open("bao4donnees/"+rubrik+".txt") as fichier:
            #On coupe le fichier selon les fils rss originaux
            #La division a été marquée dans la bao1 par des tirets
            for filrss in fichier.read().split("------------------\n"):
                if not filrss: continue #On ignore les fils rss ou rien n'a été extrait (à cause des doublons)
                textes.append(filrss)
                classes.append(rubrik)
    return textes,classes #On renvoie les textes avec les classes associées pour l'entraînement

def entrainement(textes,classes):
    print("entraînement")
    vecto = TfidfVectorizer(max_features=4500,ngram_range=(1, 2))
    vecteurs = vecto.fit_transform(textes).toarray()  #On vectorise selon le nombre d'occurence de chaque type

    modele = MultinomialNB().fit(vecteurs,classes) #On entraîne le modèle avec les données
    return modele
if __name__ == "__main__":
    textes,classes= constitutioncorpus()
    classesu=[]
    for classe in classes:
        if classe not in classesu: #On aura besoin par la suite de la liste des classes dans l'ordre
            classesu.append(classe)
    modele=entrainement(textes,classes) #On entraîne le modèle en lui donnant les titres et description de chaque fil rss avec la rubrique à laquelle ils appartiennent

    #Maintenant on va tester le modèle
    
    txttest=[open("bao4donnees/echantillontest/"+fichier).read() for fichier in os.listdir("bao4donnees/echantillontest")] #On récupère une liste de tous les contenus textuels des fichiers de l'echantillon de test
    vraiesrubriques = [fichier[:-4] for fichier in os.listdir("bao4donnees/echantillontest")  ] #On voudra afficher les vraies rubriques de chaque fichier
    vecteurstest = TfidfVectorizer(max_features=4500,ngram_range=(1, 2)).fit_transform(txttest).toarray() #On les vectorise aussi pour pouvoir les rendre comparables à données d'entrainements

    i=0
    with open("resultats/classificationrubriques.txt", "w") as sortie:
        for vecteur in vecteurstest:
            sortie.write("vraie rubrique: "+vraiesrubriques[i]+"\n")
            print("vraie rubrique:",vraiesrubriques[i])
            #On utilise notre modèle pour prédire la rubrique pour chaque fil rss
            resultat=modele.predict_proba(vecteur.reshape(1, -1) )[0]
            j=0
            #On affiche les probabilités estimées par  notre modèle
            for nb in nditer(resultat):
                sortie.write("\t"+classesu[j] + str(nb)+"\n")
                print("\t",classesu[j], nb)
                j+=1
            prediction=modele.predict(vecteur.reshape(1,-1))[0]
            sortie.write("rubrique prédite "+prediction+"\n")
            print("rubrique prédite:",prediction,"\n")
            #Est ce que notre modèle a eu juste?
            if prediction==vraiesrubriques[i]:
                sortie.write("Prédiction exacte!\n\n")
                print("Prédiction exacte!\n")
            else:
                sortie.write("Raté\n\n")
                print("Raté\n")
            i+=1

