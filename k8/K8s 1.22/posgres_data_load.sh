#!/bin/sh
b=10
while [ $b -le 10 ]
do

echo "namespace-$b"

        result=$( kubectl get pods -n namespace-$b | grep postgres  | awk '{{print$1}}' ); for i in $result ;do echo "kubectl cp /home/administrator/dataload/Runinside_Postgres.sh  --namespace=namespace-$b $i:/tmp/";kubectl cp home/administrator/dataload/Runinside_Postgres.sh  --namespace=namespace-$b $i:/tmp/; done;

        result=$( kubectl get pods -n namespace-$b | grep postgres  | awk '{{print$1}}' ); for i in $result ;do echo "kubectl -it exec $i --namespace=namespace-$b -- bash -c "sh /tmp/Runinside_Postgres.sh"";kubectl -it exec $i --namespace=namespace-$b -- bash -c ""sh /tmp/Runinside_Postgres.sh""; done;


b=`expr $b + 1`
done
