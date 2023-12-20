#This emulator took two variable as input host and port as command line arguments as do in telnet,


#!/usr/bin/bash

# Code executable on Macbook
host=$1
port=$2

# one way if telnet command use
#telnet $host $port


# Second way - Check ping



a=$(ping -c 1 "$host"|grep "$host"|awk '{print $3}'|cut -d":" -f1|grep -v 'ping')
echo "telnet $host $port"
echo "Trying $a..."

# another way to check nc command also check conenction  ------ This is alternate another one which yeild output as "Connection to google.com 8080 port [tcp/http-alt] succeeded!"
# nc -z -w5 $host $port
b=$(echo $?)
if [  $b = 0  ]
then
        echo "Connected to $host"
        echo "Escape character is '^]'"
fi
#------------------------------- Code work till here if connection persist 
# Since I tried on MacBook where netstat is missing so wrote  port check  $PORT code which not executed to get response, may be little twiks required"


portCheck = $(netstat -a|grep -w "$port"|awk -F'\t' '{print $6}')

if [ $portCheck = $port -a $b = 0  ]
then
        echo "Connected to $host"
        echo "Escape character is '^]'."
fi

