#!/bin/bash
# Source: http://tarunlalwani.com/post/mysql-master-slave-using-docker/
BASE_PATH=$(dirname $0)

echo "Waiting for mysql to get up"
# Give 60 seconds for master and slave to come up
sleep 60

echo "Create MySQL Servers (master / slave repl)"
echo "-----------------"


echo "* Create replication user"

mysql --host mysqlslave -uroot -p$MYSQL_SLAVE_PASSWORD -AN -e 'STOP SLAVE;';
mysql --host mysqlslave2 -uroot -p$MYSQL_SLAVE_PASSWORD -AN -e 'STOP SLAVE;';
mysql --host mysqlmaster -uroot -p$MYSQL_MASTER_PASSWORD -AN -e 'RESET SLAVE ALL;';

mysql --host mysqlmaster -uroot -p$MYSQL_MASTER_PASSWORD -AN -e "CREATE USER '$MYSQL_REPLICATION_USER'@'%';"
mysql --host mysqlmaster -uroot -p$MYSQL_MASTER_PASSWORD -AN -e "GRANT REPLICATION SLAVE ON *.* TO '$MYSQL_REPLICATION_USER'@'%' IDENTIFIED BY '$MYSQL_REPLICATION_PASSWORD';"
mysql --host mysqlmaster -uroot -p$MYSQL_MASTER_PASSWORD -AN -e 'flush privileges;'


echo "* Set Master on slaves"

MYSQL01_Position=$(eval "mysql --host mysqlmaster -uroot -p$MYSQL_MASTER_PASSWORD -e 'show master status \G' | grep Position | sed -n -e 's/^.*: //p'")
MYSQL01_File=$(eval "mysql --host mysqlmaster -uroot -p$MYSQL_MASTER_PASSWORD -e 'show master status \G'     | grep File     | sed -n -e 's/^.*: //p'")
MASTER_IP=$(eval "getent hosts mysqlmaster|awk '{print \$1}'")
echo $MASTER_IP

mysql --host mysqlslave -uroot -p$MYSQL_SLAVE_PASSWORD -AN -e "CHANGE MASTER TO master_host='mysqlmaster', master_port=3306, \
        master_user='$MYSQL_REPLICATION_USER', master_password='$MYSQL_REPLICATION_PASSWORD', master_log_file='$MYSQL01_File', \
        master_log_pos=$MYSQL01_Position;"

mysql --host mysqlslave2 -uroot -p$MYSQL_SLAVE_PASSWORD -AN -e "CHANGE MASTER TO master_host='mysqlmaster', master_port=3306, \
        master_user='$MYSQL_REPLICATION_USER', master_password='$MYSQL_REPLICATION_PASSWORD', master_log_file='$MYSQL01_File', \
        master_log_pos=$MYSQL01_Position;"


echo "* Start Slave on both slaves"
mysql --host mysqlslave -uroot -p$MYSQL_SLAVE_PASSWORD -AN -e "start slave;"
mysql --host mysqlslave2 -uroot -p$MYSQL_SLAVE_PASSWORD -AN -e "start slave;"

echo "Increase the max_connections to 2000"
mysql --host mysqlmaster -uroot -p$MYSQL_MASTER_PASSWORD -AN -e 'set GLOBAL max_connections=2000';
mysql --host mysqlslave -uroot -p$MYSQL_SLAVE_PASSWORD -AN -e 'set GLOBAL max_connections=2000';
mysql --host mysqlslave2 -uroot -p$MYSQL_SLAVE_PASSWORD -AN -e 'set GLOBAL max_connections=2000';

mysql --host mysqlslave -uroot -p$MYSQL_SLAVE_PASSWORD -e "show slave status \G"
mysql --host mysqlslave2 -uroot -p$MYSQL_SLAVE_PASSWORD -e "show slave status \G"

echo "MySQL servers created!"
echo "--------------------"
echo
echo Variables available fo you :-
echo
echo MYSQL01_IP       : mysqlmaster
echo MYSQL02_IP       : mysqlslave
echo MYSQL03_IP       : mysqlslave2
