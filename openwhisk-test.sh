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


locust -f openwhiskTest.py --web-port $parameterA --host $parameterB -u $parameterC -r 0.1 --run-time 10m --html report-openwhisk.html --csv "openwhisk/openwhisk"

#command to execute

# /bin/bash openwhisk-test.sh -p 1234 -h "http://34.151.90.112:9090/api/23bc46b1-71f6-4ed5-8c54-816aa4f8c502" -u 100