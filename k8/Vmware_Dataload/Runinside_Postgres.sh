#!/bin/bash
psql postgres -c "CREATE DATABASE tpcc"
psql --username=postgres tpcc < /tmp/tpcc_postgres.sql
exit





#!/bin/bash
su postgres <<MY_QUERY
psql postgres -c "CREATE DATABASE tpcc"
psql --username=postgres tpcc < /tmp/tpcc_postgres.sql
MY_QUERY
rm -rf /tmp/*.sql
exit
