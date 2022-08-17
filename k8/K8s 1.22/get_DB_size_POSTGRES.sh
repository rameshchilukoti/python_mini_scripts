#!/bin/sh
b=1
while [ $b -le 10 ]
do
echo "namespace-$b"
        result=$( kubectl get pods -n namespace-$b | grep postgres | awk '{{print$1}}' ); for i in $result ;do kubectl cp /home/core/performance/dataload/Posgres_get_DB_size.sh  --namespace=namespace-$b $i:/tmp/; done;




        result=$( kubectl get pods -n namespace-$b | grep postgres | awk '{{print$1}}' ); for i in $result ;do echo $i;kubectl -it exec $i --namespace=namespace-$b -- bash -c "sh /tmp/Posgres_get_DB_size.sh"; done
echo "*********************************************************************"
b=`expr $b + 1`
done

