import pandas as pd
import json
import xmltodict
pd.options.display.max_columns = 1000
import glob
import sys

year1 = sys.argv[1]
year2 = sys.argv[2]
global bodaccdict

for yearint in range(int(year1),int(year2)):
    year = str(yearint)
    directories = glob.glob("../data/"+year+"/"+year+"/BILAN_*")
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
        
        if(type(bodaccdict['Bilan_XML_Rediff']['listeAvis']['avis']) is list):
            for i in range(len(bodaccdict['Bilan_XML_Rediff']['listeAvis']['avis'])):
                mydict['originalFile'] = d.split("../data/"+year+"/"+year+"/")[1]
                mydict['parution'] = bodaccdict['Bilan_XML_Rediff']['parution']
                mydict['dateParution'] = bodaccdict['Bilan_XML_Rediff']['dateParution']
                mydict['nojo'] = bodaccdict['Bilan_XML_Rediff']['listeAvis']['avis'][i]['nojo']
                mydict['data'] = bodaccdict['Bilan_XML_Rediff']['listeAvis']['avis'][i]
                globarr1.append(mydict)
                mydict = {}
                try:
                    if "numeroImmatriculation" in bodaccdict['Bilan_XML_Rediff']['listeAvis']['avis'][i]:
                        mydict['siren'] = bodaccdict['Bilan_XML_Rediff']['listeAvis']['avis'][i]['numeroImmatriculation']['numeroIdentificationRCS']
                        mydict['nojo'] = bodaccdict['Bilan_XML_Rediff']['listeAvis']['avis'][i]['nojo']
                        mydict['type'] = 'bilan'  
                        globarr2.append(mydict)
                        mydict = {}
                except:
                    if "numeroImmatriculation" in bodaccdict['Bilan_XML_Rediff']['listeAvis']['avis'][i]:
                        mydict['siren'] = bodaccdict['Bilan_XML_Rediff']['listeAvis']['avis'][i]['numeroImmatriculation']['numeroIdentification']
                        mydict['nojo'] = bodaccdict['Bilan_XML_Rediff']['listeAvis']['avis'][i]['nojo']
                        mydict['type'] = 'bilan'  
                        globarr2.append(mydict)
                        mydict = {}

        else:
            mydict['originalFile'] = d.split("../data/"+year+"/"+year+"/")[1]
            mydict['parution'] = bodaccdict['Bilan_XML_Rediff']['parution']
            mydict['dateParution'] = bodaccdict['Bilan_XML_Rediff']['dateParution']
            mydict['nojo'] = bodaccdict['Bilan_XML_Rediff']['listeAvis']['avis']['nojo']
            mydict['data'] = bodaccdict['Bilan_XML_Rediff']['listeAvis']['avis']
            globarr1.append(mydict)
            mydict = {}
            
            try:
                if "numeroImmatriculation" in bodaccdict['Bilan_XML_Rediff']['listeAvis']['avis']:
                    mydict['siren'] = bodaccdict['Bilan_XML_Rediff']['listeAvis']['avis']['numeroImmatriculation']['numeroIdentificationRCS']
                    mydict['nojo'] = bodaccdict['Bilan_XML_Rediff']['listeAvis']['avis']['nojo']
                    mydict['type'] = 'bilan'  
                    globarr2.append(mydict)
                    mydict = {}
            except:
                if "numeroImmatriculation" in bodaccdict['Bilan_XML_Rediff']['listeAvis']['avis']:
                    mydict['siren'] = bodaccdict['Bilan_XML_Rediff']['listeAvis']['avis']['numeroImmatriculation']['numeroIdentification']
                    mydict['nojo'] = bodaccdict['Bilan_XML_Rediff']['listeAvis']['avis']['nojo']
                    mydict['type'] = 'bilan'  
                    globarr2.append(mydict)
                    mydict = {}



            
        bodaccdict = None


    df = pd.DataFrame(globarr1)
    df2 = pd.DataFrame(globarr2)
    print(df.shape)
    print(df2.shape)

    df2['siren'] = df2['siren'].apply(lambda x: x.replace(" ","") if x != None else None)
    df.data = df.data.apply(lambda x: json.dumps(x))

    df.to_csv("../csv/"+year+"-BILAN-data.csv",index=False)
    df2.to_csv("../csv/"+year+"-BILAN-siren.csv",index=False)