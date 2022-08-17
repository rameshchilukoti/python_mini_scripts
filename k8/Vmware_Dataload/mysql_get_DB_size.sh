#!/bin/bash
mysql --user=root --password=$MYSQL_ROOT_PASSWORD <<MY_QUERY
select table_schema, sum((data_length+index_length)/1024/1024) AS MB from information_schema.tables group by 1;
MY_QUERY
exit
rm -rf /tmp/*.sql
exit