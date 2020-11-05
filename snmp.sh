snmpscan() {
  h=("$@")
  for h in "${h[@]}";
    do
      echo 'System Processes'
      snmpwalk -c public -t 10 -v1  ${h} 1.3.6.1.2.1.25.1.6.0
      echo 'Running Programs'
      snmpwalk -c public -t 10 -v1  ${h} 1.3.6.1.2.1.25.4.2.1.2
      echo 'Processes Path'
      snmpwalk -c public -t 10 -v1  ${h} 1.3.6.1.2.1.25.4.2.1.4
      echo 'Storage Units'
      snmpwalk -c public -t 10 -v1  ${h} 1.3.6.1.2.1.25.2.3.1.4
      echo 'Software Name'
      snmpwalk -c public -t 10 -v1  ${h} 1.3.6.1.2.1.25.6.3.1.2
      echo 'User Accounts'
      snmpwalk -c public -t 10 -v1  ${h} 1.3.6.1.4.1.77.1.2.25
      echo 'TCP Local Ports'
      snmpwalk -c public -t 10 -v1  ${h} 1.3.6.1.2.1.6.13.1.3
    done
  }
mapfile -t hosts < $1
snmpscan "${hosts[@]}"

