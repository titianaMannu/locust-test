#!/bin/bash

helpFunction()
{
   echo ""
   echo "Usage: $0 -p web-ui-port -h server-host -u num-of-users"
   exit 1 # Exit script after printing help
}

while getopts "p:h:u:" opt
do
   case "$opt" in
      p ) parameterA="$OPTARG" ;;
      h ) parameterB="$OPTARG" ;;
      u ) parameterC="$OPTARG" ;;
      ? ) helpFunction ;; # Print helpFunction in case parameter is non-existent
   esac
done

# Print helpFunction in case parameters are empty
if [ -z "$parameterA" ] || [ -z "$parameterB" ] || [ -z "$parameterC" ]
then
   echo "Some or all of the parameters are empty";
   helpFunction
fi


locust -f serverledge.py --web-port $parameterA --host $parameterB -u $parameterC -r 1 --run-time 10m --html report-mix.html --csv "reports/mix"

#/bin/bash serverledge-test.sh -p 5555 -h "http://34.65.39.175:1323" -u 5