smbscan() {
  h=("$@")
  for h in "${h[@]}";
    do
      nbtscan ${h} >> ./nbtscan
      enum4linux ${h} >> ./enum4linux
    done
  }
mapfile -t hosts < $1
smbscan "${hosts[@]}"
