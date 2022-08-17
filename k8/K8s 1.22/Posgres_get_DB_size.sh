#!/bin/bash
psql --username=postgres -c "SELECT database_name, pg_size_pretty(size) from (SELECT pg_database.datname as "database_name", pg_database_size(pg_database.datname) AS size FROM pg_database ORDER by size DESC) as ordered;"

exit
