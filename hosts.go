package main

import (
	"net"
	"fmt"
	"os"
  "flag"
	"bufio"
	"strings"
)

// TODO
// Use Returns instead of side-effects outside of main.
// Use Case instead of if-else block in main.

func forward(address string, v bool) {
	// Return IP to Stdout 
	ips, err := net.LookupIP(address)
	if (err != nil && v == true) {
		fmt.Fprintf(os.Stderr, "Could not get IPs: %v\n", err)
	}
	  
	for _, ip := range ips {
		fmt.Printf("%s. IN A %s\n", address, ip.String())
	}
}

func reverse(ip string, v bool, ns bool) {
	// Return rDNS to Stdout
	response, err := net.LookupAddr(ip)
	if (err != nil && v == true) {
    fmt.Print(err)
		fmt.Printf("\n")
  }
  if len(response) > 0 {
		rdns := response[0]
		fmt.Printf("%s : %s\n", ip, rdns)

		if ns == true {
			domlst := strings.Split(rdns, ".")
			dslice := domlst[len(domlst)-3:]
			domain := strings.Join(dslice[:], ".")
			nslookup(domain)
		}
	}	
}

func nslookup(address string) {
	ns, _ := net.LookupNS(address)
		
	for _, s := range ns {
		resp := (*s).Host
		if resp != "" {
			fmt.Printf("\t%s\n", resp)
		}
	}
}

func fscan(address string, wlist string, v bool, ns bool) {
	// Forward scan 
	// File Handler. If Path DNE, exit
	file, err := os.Open(wlist)
	if err != nil {
		fmt.Print(err)
		os.Exit(1)
	}
	// Once scan() resolves
	defer file.Close()

	// Read wlist file into array hosts
	var hosts []string
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		hosts = append(hosts, scanner.Text())
	}

	// Concat hosts with domain address -> forward
	for _,host := range hosts {
		h := host + "." + address
		forward(h, v)
	}
	
	// If NS then call nslookup
	if (ns == true && len(hosts) > 0) {
		fmt.Printf(" Name Servers: \n")
		nslookup(address)
	}
}

func rscan(cidr string, v bool, ns bool) {
	// Reverse scan
	// Get network and base ip
	ip, net, err := net.ParseCIDR(cidr)
	if err != nil {
		fmt.Print(err)
	}
	
	// Build array of IPs in network
	var ips []string
	for ip := ip.Mask(net.Mask); net.Contains(ip); incr(ip) {
		ips = append(ips, ip.String())
	}

	// trim network and broadcast address 
	// then call reverse lookup for each each ip
	for _,ip := range ips[1: len(ips)-1] {
		reverse(ip, v, ns)
	}
}

func incr(ip net.IP) {
	// Increment IP address 
	// Called by rscan
	for j := len(ip)-1; j>=0; j-- {
		ip[j]++
		if ip[j] > 0 {
			break
		}
	}
}

func main() {

  // Argparse
	address := flag.String("a","","Address. Usage: -a [domain name], or -s [ip] -r ")
	scanner := flag.String("s","","Scan. Usage: -s [hosts wordlist] for forward lookup, or -s [CIDR] -r for rDNS lookup")
  rlookup := flag.Bool("r",false,"Reverse lookup mode.")
	nserver := flag.Bool("ns",false,"NS lookup mode.")
	verbose := flag.Bool("v",false,"Verbosity.")
  
	flag.Parse()
	
	// Forward Lookup 
  if ( *address != "" && *scanner == "" && *rlookup == false && *nserver == false ) {
    forward(*address, *verbose)

	// Reverse Lookup
	} else if ( *address != "" && *rlookup == true)  {
    reverse(*address, *verbose, *nserver)

	// Brute Force Hosts Forward Lookup
  } else if ( *rlookup == false && *scanner != "") {
		fscan(*address, *scanner, *verbose, *nserver)

	// Reverse Lookup w CIDR Network
	} else if ( *rlookup == true && *scanner != "" && *address == "") {
		rscan(*scanner, *verbose, *nserver)
	
	// Nameserver Lookup
	} else if (*nserver == true && *address != "") {
		nslookup(*address)
  } else {
		fmt.Printf("%s\n", flag.ErrHelp)
	}

}
