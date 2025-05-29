#!/bin/bash 

declare -A array 

ips=$(awk '
    /32 host/ { print f } {f=$2}
' <<< "$(</proc/net/fib_trie)" | sort | uniq ) 


while IFS= read -r ip; do 
    dev_name=$(ip addr | grep -w -F "inet $ip" | awk '{print $NF}')
    array["$ip"]=$dev_name
done <<< "$ips"

for key in "${!array[@]}"; do 
    # echo "$key : ${array[$key]}"
    echo "${array[$key]}" : "$key"
done
