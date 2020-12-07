#! /bin/bash

for i in $(eval echo {$1..$2});
do
    echo "Process "$i
    wget https://echanges.dila.gouv.fr/OPENDATA/BODACC/FluxHistorique/BODACC_$i.tar -P ../tarfiles/
    mkdir ../data/$i
    cd ../tarfiles && tar -xzvf BODACC_$i.tar --directory ../data/$i
    cd ../data/$i
    mkdir $i
    mv ./* $i
    cd $i
    mv */*.taz .
    rm -rf bodacc_*
    for f in ./*;
    do
        tar -zxvf $f
    done;
    rm *.taz
    cd ../../../scripts/
done;

