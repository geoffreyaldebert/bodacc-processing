import pandas as pd
import json
import xmltodict
pd.options.display.max_columns = 1000
import glob
import sys

year1 = sys.argv[1]
year2 = sys.argv[2]
global bodaccdict

lists = ['modificationsGenerales.precedentExploitantPM',
 'modificationsGenerales.precedentExploitantPP',
 'personnes.personne',
 'personnes.personne.personnePhysique.prenom']

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
    directories = glob.glob("../data/"+year+"/"+year+"/RCS-B*")
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

        if(type(bodaccdict['RCS-B_REDIFF']['listeAvis']['avis']) is list):
            for i in range(len(bodaccdict['RCS-B_REDIFF']['listeAvis']['avis'])):
                recursivedict(0,bodaccdict['RCS-B_REDIFF']['listeAvis']['avis'],i,'')

            for i in range(len(bodaccdict['RCS-B_REDIFF']['listeAvis']['avis'])):
                mydict['originalFile'] = d.split("../data/"+year+"/"+year+"/")[1]
                mydict['parution'] = bodaccdict['RCS-B_REDIFF']['parution']
                mydict['dateParution'] = bodaccdict['RCS-B_REDIFF']['dateParution']
                mydict['nojo'] = bodaccdict['RCS-B_REDIFF']['listeAvis']['avis'][i]['nojo']
                mydict['data'] = bodaccdict['RCS-B_REDIFF']['listeAvis']['avis'][i]
                globarr1.append(mydict)
                mydict = {}
                
                if(type(bodaccdict['RCS-B_REDIFF']['listeAvis']['avis'][i]['personnes']['personne']) is list):
                    for k in range(len(bodaccdict['RCS-B_REDIFF']['listeAvis']['avis'][i]['personnes']['personne'])):
                        if "numeroImmatriculation" in bodaccdict['RCS-B_REDIFF']['listeAvis']['avis'][i]['personnes']['personne'][k]:
                            mydict['siren'] = bodaccdict['RCS-B_REDIFF']['listeAvis']['avis'][i]['personnes']['personne'][k]['numeroImmatriculation']['numeroIdentificationRCS']
                            mydict['nojo'] = bodaccdict['RCS-B_REDIFF']['listeAvis']['avis'][i]['nojo']
                            mydict['type'] = 'personne'  
                            globarr2.append(mydict)
                            mydict = {}

                            
                if "precedentExploitantPM" in bodaccdict['RCS-B_REDIFF']['listeAvis']['avis'][i]:
                    if(type(bodaccdict['RCS-B_REDIFF']['listeAvis']['avis'][i]['precedentExploitantPM']) is list):
                        for k in range(len(bodaccdict['RCS-B_REDIFF']['listeAvis']['avis'][i]['precedentExploitantPM'])):
                            if "numeroImmatriculation" in bodaccdict['RCS-B_REDIFF']['listeAvis']['avis'][i]['precedentExploitantPM'][k]:
                                mydict['siren'] = bodaccdict['RCS-B_REDIFF']['listeAvis']['avis'][i]['precedentExploitantPM'][k]['numeroImmatriculation']['numeroIdentification']
                                mydict['nojo'] = bodaccdict['RCS-B_REDIFF']['listeAvis']['avis'][i]['nojo']
                                mydict['type'] = 'precedentExploitantPM'  
                                globarr2.append(mydict)
                                mydict = {}
                                
                if "precedentExploitantPP" in bodaccdict['RCS-B_REDIFF']['listeAvis']['avis'][i]:
                    if(type(bodaccdict['RCS-B_REDIFF']['listeAvis']['avis'][i]['precedentExploitantPP']) is list):
                        for k in range(len(bodaccdict['RCS-B_REDIFF']['listeAvis']['avis'][i]['precedentExploitantPP'])):
                            if "numeroImmatriculation" in bodaccdict['RCS-B_REDIFF']['listeAvis']['avis'][i]['precedentExploitantPP']:
                                mydict['siren'] = bodaccdict['RCS-B_REDIFF']['listeAvis']['avis'][i]['precedentExploitantPP'][k]['numeroImmatriculation']['numeroIdentification']
                                mydict['nojo'] = bodaccdict['RCS-B_REDIFF']['listeAvis']['avis'][i]['nojo']
                                mydict['type'] = 'precedentExploitantPP'  
                                globarr2.append(mydict)
                                
        else:
            recursivedict(0,bodaccdict['RCS-B_REDIFF']['listeAvis'],'avis','')

            mydict['originalFile'] = d.split("../data/"+year+"/"+year+"/")[1]
            mydict['parution'] = bodaccdict['RCS-B_REDIFF']['parution']
            mydict['dateParution'] = bodaccdict['RCS-B_REDIFF']['dateParution']
            mydict['nojo'] = bodaccdict['RCS-B_REDIFF']['listeAvis']['avis']['nojo']
            mydict['data'] = bodaccdict['RCS-B_REDIFF']['listeAvis']['avis']
            globarr1.append(mydict)
            mydict = {}
            
            if(type(bodaccdict['RCS-B_REDIFF']['listeAvis']['avis']['personnes']['personne']) is list):
                for k in range(len(bodaccdict['RCS-B_REDIFF']['listeAvis']['avis']['personnes']['personne'])):
                    if "numeroImmatriculation" in bodaccdict['RCS-B_REDIFF']['listeAvis']['avis']['personnes']['personne'][k]:
                        mydict['siren'] = bodaccdict['RCS-B_REDIFF']['listeAvis']['avis']['personnes']['personne'][k]['numeroImmatriculation']['numeroIdentificationRCS']
                        mydict['nojo'] = bodaccdict['RCS-B_REDIFF']['listeAvis']['avis']['nojo']
                        mydict['type'] = 'personne'  
                        globarr2.append(mydict)
                        mydict = {}

                        
            if "precedentExploitantPM" in bodaccdict['RCS-B_REDIFF']['listeAvis']['avis']:
                if(type(bodaccdict['RCS-B_REDIFF']['listeAvis']['avis']['precedentExploitantPM']) is list):
                    for k in range(len(bodaccdict['RCS-B_REDIFF']['listeAvis']['avis']['precedentExploitantPM'])):
                        if "numeroImmatriculation" in bodaccdict['RCS-B_REDIFF']['listeAvis']['avis']['precedentExploitantPM'][k]:
                            mydict['siren'] = bodaccdict['RCS-B_REDIFF']['listeAvis']['avis']['precedentExploitantPM'][k]['numeroImmatriculation']['numeroIdentification']
                            mydict['nojo'] = bodaccdict['RCS-B_REDIFF']['listeAvis']['avis']['nojo']
                            mydict['type'] = 'precedentExploitantPM'  
                            globarr2.append(mydict)
                            mydict = {}
                            
            if "precedentExploitantPP" in bodaccdict['RCS-B_REDIFF']['listeAvis']['avis']:
                if(type(bodaccdict['RCS-B_REDIFF']['listeAvis']['avis']['precedentExploitantPP']) is list):
                    for k in range(len(bodaccdict['RCS-B_REDIFF']['listeAvis']['avis']['precedentExploitantPP'])):
                        if "numeroImmatriculation" in bodaccdict['RCS-B_REDIFF']['listeAvis']['avis']['precedentExploitantPP']:
                            mydict['siren'] = bodaccdict['RCS-B_REDIFF']['listeAvis']['avis']['precedentExploitantPP'][k]['numeroImmatriculation']['numeroIdentification']
                            mydict['nojo'] = bodaccdict['RCS-B_REDIFF']['listeAvis']['avis']['nojo']
                            mydict['type'] = 'precedentExploitantPP'  
                            globarr2.append(mydict)
    
        bodaccdict = None
        

    df = pd.DataFrame(globarr1)
    df2 = pd.DataFrame(globarr2)
    print(df.shape)
    print(df2.shape)

    df2['siren'] = df2['siren'].apply(lambda x: x.replace(" ","") if x != None else None)
    df.data = df.data.apply(lambda x: json.dumps(x))

    df.to_csv("../csv/"+year+"-RCS-B-data.csv",index=False)
    df2.to_csv("../csv/"+year+"-RCS-B-siren.csv",index=False)