#!/bin/sh
b=1
while [ $b -le 1 ]
do
 psql --username=postgres -c "SELECT database_name, pg_size_pretty(size) from (SELECT pg_database.datname as "database_name", pg_database_size(pg_database.datname) AS size FROM pg_database ORDER by size DESC) as ordered;"
psql --username=postgres -c "SELECT pg_size_pretty(pg_relation_size('t_random'));"
        psql --username=postgres -c "CREATE DATABASE testdatabase$b"
        psql --username=postgres -c "\c testdatabase$b" -c "CREATE TABLE t_random AS SELECT s, md5(random()::text) FROM generate_Series(1,5) s;" -c "INSERT INTO t_random VALUES (generate_series(1,80000000), md5(random()::text));"
        psql --username=postgres -c "SELECT pg_size_pretty(pg_relation_size('t_random'));"
 psql --username=postgres -c "SELECT database_name, pg_size_pretty(size) from (SELECT pg_database.datname as "database_name", pg_database_size(pg_database.datname) AS size FROM pg_database ORDER by size DESC) as ordered;"


#100 = 7699 kB
#1000000  = 79 MB
#10000000  = 731 MB
#100000000 = 6.2 GB
#80000000 rows= 5GB
#160000000 = 10GB

#3100000000 = 137GB
#5000000000 = 400 GB
b=`expr $b + 1`
done
exit
