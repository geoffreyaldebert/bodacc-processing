#! /bin/bash

for i in $(eval echo {$1..$2});
do
    echo "Process "$i
    mkdir -p ../data/$i/$i
    cd ../data/$i/$i/
    wget -r -np -nH --reject "index.html*" https://echanges.dila.gouv.fr/OPENDATA/BODACC/FluxHistorique/$i/
    mv ./*/*/*/*/*.taz .
    rm -rf OPENDATA
    for f in ./*;
    do
        tar -zxvf $f
    done;
    rm *.taz
    cd ../../../scripts/
done;

