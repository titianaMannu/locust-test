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

cd ../
locust -f locust-python/tinyFaasTest.py --web-port $parameterA --host $parameterB -u $parameterC --autostart --run-time 30m --html report-tiny.html --csv "tiny/tiny"

#command to execute
# /bin/bash tinyFaaS-test.sh -p 1234 -h "http://34.88.146.34:80" -u 100