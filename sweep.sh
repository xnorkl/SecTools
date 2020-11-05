#!/bin/bash

function valid(){
  local ip=$1
  local stat=1
  exp="^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\/[1-9][0-9]?$|31$|32$"
  if [[ $ip =~ $exp ]]; then
    return 0
  else
    echo "...not a valid CIDR fam..."
    return 1
  fi
}

if valid $1 -eq 0; then
  # nmap -sL $1 | awk '/Nmap scan report/{print $NF}'
  nmap -sn $1 | awk '/Nmap scan/{gsub(/[()]/,"",$NF); print $NF > "nmap_scanned_ips"}'
fi

