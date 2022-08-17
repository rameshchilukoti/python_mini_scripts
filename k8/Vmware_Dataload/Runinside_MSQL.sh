#!/bin/bash
mysql --user=root --password=$MYSQL_ROOT_PASSWORD <<MY_QUERY
CREATE DATABASE tpcc1;
USE tpcc1;
source /tmp/tpcc1.sql;
MY_QUERY

rm -rf /tmp/*.sql
exit