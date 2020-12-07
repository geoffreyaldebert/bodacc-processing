import pandas as pd
import json
import xmltodict
pd.options.display.max_columns = 1000
import glob
import sys

year1 = sys.argv[1]
year2 = sys.argv[2]
global bodaccdict


lists = ['acte.vente.opposition',
 'etablissement',
 'personnes.personne',
 'personnes.personne.adresse',
 'personnes.personne.personneMorale',
 'personnes.personne.personnePhysique.prenom',
 'precedentExploitantPM',
 'precedentExploitantPP',
 'precedentExploitantPP.prenom',
 'precedentProprietairePM',
 'precedentProprietairePP',
 'precedentProprietairePP.prenom']

def recursivedict(level,parent,el,elstring):
    if(elstring in lists):
        toto = parent[el]
        parent[el] = []
        parent[el].append(toto)
    if(type(parent[el]) is dict):
        for el2 in parent[el]:
            if(elstring == ''):
                elstring2 = el2
            else:
                elstring2 = elstring+'.'+el2
            recursivedict(level+1,parent[el],el2,elstring2)
            
    if(type(parent[el]) is list):
        for i in range(len(parent[el])):
            if(type(parent[el][i]) is dict):
                for el2 in parent[el][i]:
                    if(type(el2) is dict):
                        for el3 in el2:
                            elstring2 = elstring+"."+el3
                            recursivedict(level+1,el2,el3,elstring2)
                    else:
                        elstring2 = elstring+"."+el2
                        recursivedict(level+1,parent[el][i],el2,elstring2)


for yearint in range(int(year1),int(year2)):
    year = str(yearint)
    directories = glob.glob("../data/"+year+"/"+year+"/RCS-A_*")
    globarr1 = []
    globarr2 = []
    mydict = {}
    for d in directories:
        print(d)
        try:
            with open(d, encoding='windows-1252') as fd:
                doc = xmltodict.parse(fd.read())
        except:
            with open(d, encoding='utf-8') as fd:
                doc = xmltodict.parse(fd.read())
        bodaccdict = json.loads(json.dumps(doc))
        if(type(bodaccdict['RCS-A_IMMAT']['listeAvis']['avis']) is list):    
            for i in range(len(bodaccdict['RCS-A_IMMAT']['listeAvis']['avis'])):
                recursivedict(0,bodaccdict['RCS-A_IMMAT']['listeAvis']['avis'],i,'')

            for i in range(len(bodaccdict['RCS-A_IMMAT']['listeAvis']['avis'])):
                mydict['originalFile'] = d.split("../data/"+year+"/"+year+"/")[1]
                mydict['parution'] = bodaccdict['RCS-A_IMMAT']['parution']
                mydict['dateParution'] = bodaccdict['RCS-A_IMMAT']['dateParution']
                mydict['nojo'] = bodaccdict['RCS-A_IMMAT']['listeAvis']['avis'][i]['nojo']
                mydict['data'] = bodaccdict['RCS-A_IMMAT']['listeAvis']['avis'][i]
                globarr1.append(mydict)
                mydict = {}

                if(type(bodaccdict['RCS-A_IMMAT']['listeAvis']['avis'][i]['personnes']['personne']) is list):
                    for k in range(len(bodaccdict['RCS-A_IMMAT']['listeAvis']['avis'][i]['personnes']['personne'])):
                        if "personneMorale" in bodaccdict['RCS-A_IMMAT']['listeAvis']['avis'][i]['personnes']['personne'][k]:
                            for j in range(len(bodaccdict['RCS-A_IMMAT']['listeAvis']['avis'][i]['personnes']['personne'][k]['personneMorale'])):
                                if "numeroImmatriculation" in bodaccdict['RCS-A_IMMAT']['listeAvis']['avis'][i]['personnes']['personne'][k]['personneMorale'][j]:
                                    mydict['siren'] = bodaccdict['RCS-A_IMMAT']['listeAvis']['avis'][i]['personnes']['personne'][k]['personneMorale'][j]['numeroImmatriculation']['numeroIdentification']
                                    mydict['nojo'] = bodaccdict['RCS-A_IMMAT']['listeAvis']['avis'][i]['nojo']
                                    mydict['type'] = 'personneMorale'  
                                    globarr2.append(mydict)
                                    mydict = {}

                        if "personnePhysique" in bodaccdict['RCS-A_IMMAT']['listeAvis']['avis'][i]['personnes']['personne'][k]:
                            if "numeroImmatriculation" in bodaccdict['RCS-A_IMMAT']['listeAvis']['avis'][i]['personnes']['personne'][k]['personnePhysique']:
                                mydict['siren'] = bodaccdict['RCS-A_IMMAT']['listeAvis']['avis'][i]['personnes']['personne'][k]['personnePhysique']['numeroImmatriculation']['numeroIdentification']
                                mydict['nojo'] = bodaccdict['RCS-A_IMMAT']['listeAvis']['avis'][i]['nojo']
                                mydict['type'] = 'personnePhysique'        
                                globarr2.append(mydict)
                                mydict = {}    

                if "precedentExploitantPM" in bodaccdict['RCS-A_IMMAT']['listeAvis']['avis'][i]:
                    if(type(bodaccdict['RCS-A_IMMAT']['listeAvis']['avis'][i]['precedentExploitantPM']) is list):
                        for k in range(len(bodaccdict['RCS-A_IMMAT']['listeAvis']['avis'][i]['precedentExploitantPM'])):
                            if "numeroImmatriculation" in bodaccdict['RCS-A_IMMAT']['listeAvis']['avis'][i]['precedentExploitantPM'][k]:
                                mydict['siren'] = bodaccdict['RCS-A_IMMAT']['listeAvis']['avis'][i]['precedentExploitantPM'][k]['numeroImmatriculation']['numeroIdentification']
                                mydict['nojo'] = bodaccdict['RCS-A_IMMAT']['listeAvis']['avis'][i]['nojo']
                                mydict['type'] = 'precedentExploitantPM'  
                                globarr2.append(mydict)
                                mydict = {}
                if "precedentExploitantPP" in bodaccdict['RCS-A_IMMAT']['listeAvis']['avis'][i]:
                    if(type(bodaccdict['RCS-A_IMMAT']['listeAvis']['avis'][i]['precedentExploitantPP']) is list):
                        for k in range(len(bodaccdict['RCS-A_IMMAT']['listeAvis']['avis'][i]['precedentExploitantPP'])):
                            if "numeroImmatriculation" in bodaccdict['RCS-A_IMMAT']['listeAvis']['avis'][i]['precedentExploitantPP'][k]:
                                mydict['siren'] = bodaccdict['RCS-A_IMMAT']['listeAvis']['avis'][i]['precedentExploitantPP'][k]['numeroImmatriculation']['numeroIdentification']
                                mydict['nojo'] = bodaccdict['RCS-A_IMMAT']['listeAvis']['avis'][i]['nojo']
                                mydict['type'] = 'precedentExploitantPP'  
                                globarr2.append(mydict)
                                mydict = {}
                if "precedentProprietairePP" in bodaccdict['RCS-A_IMMAT']['listeAvis']['avis'][i]:
                    if(type(bodaccdict['RCS-A_IMMAT']['listeAvis']['avis'][i]['precedentProprietairePP']) is list):
                        for k in range(len(bodaccdict['RCS-A_IMMAT']['listeAvis']['avis'][i]['precedentProprietairePP'])):
                            if "numeroImmatriculation" in bodaccdict['RCS-A_IMMAT']['listeAvis']['avis'][i]['precedentProprietairePP'][k]:
                                mydict['siren'] = bodaccdict['RCS-A_IMMAT']['listeAvis']['avis'][i]['precedentProprietairePP'][k]['numeroImmatriculation']['numeroIdentification']
                                mydict['nojo'] = bodaccdict['RCS-A_IMMAT']['listeAvis']['avis'][i]['nojo']
                                mydict['type'] = 'precedentProprietairePP'  
                                globarr2.append(mydict)
                                mydict = {}
                if "precedentProprietairePM" in bodaccdict['RCS-A_IMMAT']['listeAvis']['avis'][i]:
                    if(type(bodaccdict['RCS-A_IMMAT']['listeAvis']['avis'][i]['precedentProprietairePM']) is list):
                        for k in range(len(bodaccdict['RCS-A_IMMAT']['listeAvis']['avis'][i]['precedentProprietairePM'])):
                            if "numeroImmatriculation" in bodaccdict['RCS-A_IMMAT']['listeAvis']['avis'][i]['precedentProprietairePM'][k]:
                                mydict['siren'] = bodaccdict['RCS-A_IMMAT']['listeAvis']['avis'][i]['precedentProprietairePM'][k]['numeroImmatriculation']['numeroIdentification']
                                mydict['nojo'] = bodaccdict['RCS-A_IMMAT']['listeAvis']['avis'][i]['nojo']
                                mydict['type'] = 'precedentProprietairePM'  
                                globarr2.append(mydict)
                                mydict = {}
        else:
            recursivedict(0,bodaccdict['RCS-A_IMMAT']['listeAvis'],'avis','')
            mydict['originalFile'] = d.split("../data/"+year+"/"+year+"/")[1]
            mydict['parution'] = bodaccdict['RCS-A_IMMAT']['parution']
            mydict['dateParution'] = bodaccdict['RCS-A_IMMAT']['dateParution']
            mydict['nojo'] = bodaccdict['RCS-A_IMMAT']['listeAvis']['avis']['nojo']
            mydict['data'] = bodaccdict['RCS-A_IMMAT']['listeAvis']['avis']
            globarr1.append(mydict)
            mydict = {}

            if(type(bodaccdict['RCS-A_IMMAT']['listeAvis']['avis']['personnes']['personne']) is list):

                for k in range(len(bodaccdict['RCS-A_IMMAT']['listeAvis']['avis']['personnes']['personne'])):
                    if "personneMorale" in bodaccdict['RCS-A_IMMAT']['listeAvis']['avis']['personnes']['personne'][k]:
                        for j in range(len(bodaccdict['RCS-A_IMMAT']['listeAvis']['avis']['personnes']['personne'][k]['personneMorale'])):
                            if "numeroImmatriculation" in bodaccdict['RCS-A_IMMAT']['listeAvis']['avis']['personnes']['personne'][k]['personneMorale'][j]:
                                mydict['siren'] = bodaccdict['RCS-A_IMMAT']['listeAvis']['avis']['personnes']['personne'][k]['personneMorale'][j]['numeroImmatriculation']['numeroIdentification']
                                mydict['nojo'] = bodaccdict['RCS-A_IMMAT']['listeAvis']['avis']['nojo']
                                mydict['type'] = 'personneMorale'  
                                globarr2.append(mydict)
                                mydict = {}

                    if "personnePhysique" in bodaccdict['RCS-A_IMMAT']['listeAvis']['avis']['personnes']['personne'][k]:
                        if "numeroImmatriculation" in bodaccdict['RCS-A_IMMAT']['listeAvis']['avis']['personnes']['personne'][k]['personnePhysique']:
                            mydict['siren'] = bodaccdict['RCS-A_IMMAT']['listeAvis']['avis']['personnes']['personne'][k]['personnePhysique']['numeroImmatriculation']['numeroIdentification']
                            mydict['nojo'] = bodaccdict['RCS-A_IMMAT']['listeAvis']['avis']['nojo']
                            mydict['type'] = 'personnePhysique'        
                            globarr2.append(mydict)
                            mydict = {}    

            if "precedentExploitantPM" in bodaccdict['RCS-A_IMMAT']['listeAvis']['avis']:
                if(type(bodaccdict['RCS-A_IMMAT']['listeAvis']['avis']['precedentExploitantPM']) is list):
                    for k in range(len(bodaccdict['RCS-A_IMMAT']['listeAvis']['avis']['precedentExploitantPM'])):
                        if "numeroImmatriculation" in bodaccdict['RCS-A_IMMAT']['listeAvis']['avis']['precedentExploitantPM'][k]:
                            mydict['siren'] = bodaccdict['RCS-A_IMMAT']['listeAvis']['avis']['precedentExploitantPM'][k]['numeroImmatriculation']['numeroIdentification']
                            mydict['nojo'] = bodaccdict['RCS-A_IMMAT']['listeAvis']['avis']['nojo']
                            mydict['type'] = 'precedentExploitantPM'  
                            globarr2.append(mydict)
                            mydict = {}
            if "precedentExploitantPP" in bodaccdict['RCS-A_IMMAT']['listeAvis']['avis']:
                if(type(bodaccdict['RCS-A_IMMAT']['listeAvis']['avis']['precedentExploitantPP']) is list):
                    for k in range(len(bodaccdict['RCS-A_IMMAT']['listeAvis']['avis']['precedentExploitantPP'])):
                        if "numeroImmatriculation" in bodaccdict['RCS-A_IMMAT']['listeAvis']['avis']['precedentExploitantPP'][k]:
                            mydict['siren'] = bodaccdict['RCS-A_IMMAT']['listeAvis']['avis']['precedentExploitantPP'][k]['numeroImmatriculation']['numeroIdentification']
                            mydict['nojo'] = bodaccdict['RCS-A_IMMAT']['listeAvis']['avis']['nojo']
                            mydict['type'] = 'precedentExploitantPP'  
                            globarr2.append(mydict)
                            mydict = {}
            if "precedentProprietairePP" in bodaccdict['RCS-A_IMMAT']['listeAvis']['avis']:
                if(type(bodaccdict['RCS-A_IMMAT']['listeAvis']['avis']['precedentProprietairePP']) is list):
                    for k in range(len(bodaccdict['RCS-A_IMMAT']['listeAvis']['avis']['precedentProprietairePP'])):
                        if "numeroImmatriculation" in bodaccdict['RCS-A_IMMAT']['listeAvis']['avis']['precedentProprietairePP'][k]:
                            mydict['siren'] = bodaccdict['RCS-A_IMMAT']['listeAvis']['avis']['precedentProprietairePP'][k]['numeroImmatriculation']['numeroIdentification']
                            mydict['nojo'] = bodaccdict['RCS-A_IMMAT']['listeAvis']['avis']['nojo']
                            mydict['type'] = 'precedentProprietairePP'  
                            globarr2.append(mydict)
                            mydict = {}
            if "precedentProprietairePM" in bodaccdict['RCS-A_IMMAT']['listeAvis']['avis']:
                if(type(bodaccdict['RCS-A_IMMAT']['listeAvis']['avis']['precedentProprietairePM']) is list):
                    for k in range(len(bodaccdict['RCS-A_IMMAT']['listeAvis']['avis']['precedentProprietairePM'])):
                        if "numeroImmatriculation" in bodaccdict['RCS-A_IMMAT']['listeAvis']['avis']['precedentProprietairePM'][k]:
                            mydict['siren'] = bodaccdict['RCS-A_IMMAT']['listeAvis']['avis']['precedentProprietairePM'][k]['numeroImmatriculation']['numeroIdentification']
                            mydict['nojo'] = bodaccdict['RCS-A_IMMAT']['listeAvis']['avis']['nojo']
                            mydict['type'] = 'precedentProprietairePM'  
                            globarr2.append(mydict)
                            mydict = {}
            
        bodaccdict = None
        
    df = pd.DataFrame(globarr1)
    df2 = pd.DataFrame(globarr2)
    print(df.shape)
    print(df2.shape)

    df2['siren'] = df2['siren'].apply(lambda x: x.replace(" ","") if x != None else None)
    df.data = df.data.apply(lambda x: json.dumps(x))

    df.to_csv("../csv/"+year+"-RCS-A-data.csv",index=False)
    df2.to_csv("../csv/"+year+"-RCS-A-siren.csv",index=False)
