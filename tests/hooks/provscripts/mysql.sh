#!/bin/bash

# This script provisions a MySQL docker instance

OPTIND=1

# Initialize our own variables:
host=""
user=""
secret=""
port=""

while getopts "h:u:s:p:" opt; do
    case "$opt" in
    h)  host=$OPTARG
        ;;
    u)  user=$OPTARG
        ;;
    s)  secret=$OPTARG
        ;;
    p)  port=$OPTARG
        ;;
    esac
done

shift $((OPTIND-1))

[ "$1" = "--" ] && shift

echo "Provisioning host='$host' with user='$user' at port='$port'"

function fail {
    echo $1
    exit
}

mysql -u $user -P $port -p$secret -h $host -e 'create database test' || fail "Could not create database"
