import pandas as pd
import json
import xmltodict
pd.options.display.max_columns = 1000
import glob
import sys

year1 = sys.argv[1]
year2 = sys.argv[2]
global bodaccdict

lists = ['activite',
 'adresse',
 'enseigne',
 'inscriptionRM',
 'nonInscrit',
 'numeroImmatriculation',
 'personneMorale',
 'personnePhysique',
 'personnePhysique.prenom']

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
    directories = glob.glob("../data/"+year+"/"+year+"/PCL_*")
    directories2 = glob.glob("../data/"+year+"/"+year+"/BXA*")
    directories = directories + directories2
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

        if(type(bodaccdict['PCL_REDIFF']['annonces']['annonce']) is list):
            for i in range(len(bodaccdict['PCL_REDIFF']['annonces']['annonce'])):
                recursivedict(0,bodaccdict['PCL_REDIFF']['annonces']['annonce'],i,'')

                
            for i in range(len(bodaccdict['PCL_REDIFF']['annonces']['annonce'])):
                mydict['originalFile'] = d.split("../data/"+year+"/"+year+"/")[1]
                mydict['parution'] = bodaccdict['PCL_REDIFF']['parution']
                mydict['dateParution'] = bodaccdict['PCL_REDIFF']['dateParution']
                mydict['nojo'] = bodaccdict['PCL_REDIFF']['annonces']['annonce'][i]['nojo']
                mydict['data'] = bodaccdict['PCL_REDIFF']['annonces']['annonce'][i]
                globarr1.append(mydict)
                mydict = {}
                

                if "inscriptionRM" in bodaccdict['PCL_REDIFF']['annonces']['annonce'][i]:
                    if(type(bodaccdict['PCL_REDIFF']['annonces']['annonce'][i]['inscriptionRM']) is list):
                        for k in range(len(bodaccdict['PCL_REDIFF']['annonces']['annonce'][i]['inscriptionRM'])):
                            if "numeroIdentificationRM" in bodaccdict['PCL_REDIFF']['annonces']['annonce'][i]['inscriptionRM'][k]:
                                mydict['siren'] = bodaccdict['PCL_REDIFF']['annonces']['annonce'][i]['inscriptionRM'][k]['numeroIdentificationRM']
                                mydict['nojo'] = bodaccdict['PCL_REDIFF']['annonces']['annonce'][i]['nojo']
                                mydict['type'] = 'PCL-numeroIdentificationRM'  
                                globarr2.append(mydict)
                                mydict = {}
                                
                if "numeroImmatriculation" in bodaccdict['PCL_REDIFF']['annonces']['annonce'][i]:
                    if(type(bodaccdict['PCL_REDIFF']['annonces']['annonce'][i]['numeroImmatriculation']) is list):
                        for k in range(len(bodaccdict['PCL_REDIFF']['annonces']['annonce'][i]['numeroImmatriculation'])):
                            if "numeroIdentificationRCS" in bodaccdict['PCL_REDIFF']['annonces']['annonce'][i]['numeroImmatriculation'][k]:
                                mydict['siren'] = bodaccdict['PCL_REDIFF']['annonces']['annonce'][i]['numeroImmatriculation'][k]['numeroIdentificationRCS']
                                mydict['nojo'] = bodaccdict['PCL_REDIFF']['annonces']['annonce'][i]['nojo']
                                mydict['type'] = 'PCL-numeroIdentificationRCS'  
                                globarr2.append(mydict)
                                mydict = {}
        else:
            recursivedict(0,bodaccdict['PCL_REDIFF']['annonces'],'annonce','')

            mydict['originalFile'] = d.split("../data/"+year+"/"+year+"/")[1]
            mydict['parution'] = bodaccdict['PCL_REDIFF']['parution']
            mydict['dateParution'] = bodaccdict['PCL_REDIFF']['dateParution']
            mydict['nojo'] = bodaccdict['PCL_REDIFF']['annonces']['annonce']['nojo']
            mydict['data'] = bodaccdict['PCL_REDIFF']['annonces']['annonce']
            globarr1.append(mydict)
            mydict = {}
            

            if "inscriptionRM" in bodaccdict['PCL_REDIFF']['annonces']['annonce']:
                if(type(bodaccdict['PCL_REDIFF']['annonces']['annonce']['inscriptionRM']) is list):
                    for k in range(len(bodaccdict['PCL_REDIFF']['annonces']['annonce']['inscriptionRM'])):
                        if "numeroIdentificationRM" in bodaccdict['PCL_REDIFF']['annonces']['annonce']['inscriptionRM'][k]:
                            mydict['siren'] = bodaccdict['PCL_REDIFF']['annonces']['annonce']['inscriptionRM'][k]['numeroIdentificationRM']
                            mydict['nojo'] = bodaccdict['PCL_REDIFF']['annonces']['annonce']['nojo']
                            mydict['type'] = 'PCL-numeroIdentificationRM'  
                            globarr2.append(mydict)
                            mydict = {}
                            
            if "numeroImmatriculation" in bodaccdict['PCL_REDIFF']['annonces']['annonce']:
                if(type(bodaccdict['PCL_REDIFF']['annonces']['annonce']['numeroImmatriculation']) is list):
                    for k in range(len(bodaccdict['PCL_REDIFF']['annonces']['annonce']['numeroImmatriculation'])):
                        if "numeroIdentificationRCS" in bodaccdict['PCL_REDIFF']['annonces']['annonce']['numeroImmatriculation'][k]:
                            mydict['siren'] = bodaccdict['PCL_REDIFF']['annonces']['annonce']['numeroImmatriculation'][k]['numeroIdentificationRCS']
                            mydict['nojo'] = bodaccdict['PCL_REDIFF']['annonces']['annonce']['nojo']
                            mydict['type'] = 'PCL-numeroIdentificationRCS'  
                            globarr2.append(mydict)
                            mydict = {}


            
        bodaccdict = None
        

    df = pd.DataFrame(globarr1)
    df2 = pd.DataFrame(globarr2)
    print(df.shape)
    print(df2.shape)

    df2['siren'] = df2['siren'].apply(lambda x: x.replace(" ","") if x != None else None)
    df.data = df.data.apply(lambda x: json.dumps(x))

    df.to_csv("../csv/"+year+"-PCL-data.csv",index=False)
    df2.to_csv("../csv/"+year+"-PCL-siren.csv",index=False)