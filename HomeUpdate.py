# Install Python module, uncomment if required
# pip install pip3
# pip install ipcalc
# pip install networkscan
# pip install python-netbox

import ipcalc
import networkscan
from netbox import netbox
import requests
import datetime

API_TOKEN = "33fa91b269fc489065e9476d91488d66b856e1c3"
HEADERS = {'Authorization': f'Token {API_TOKEN}', 'Content-Type': 'application/json', 'Accept': 'application/json'}
NB_URL = "http://192.168.1.165"
netbox = NetBox(host="192.168.165", port=8000, use_ssl=False, auth_token="33fa91b269fc489065e9476d91488d66b856e1c3")

if __name__ == '__main__':
    # Define the network to scan here
    my_network = "192.168.1.0/24"

    # Create the object
    my_scan = networkscan.Networkscan(my_network)

    # Run the scan of hosts using pings
    my_scan.run()

    # Here we define existing IP addresses in our network and write them to a list
    found_ip_in_network = [str(address) for address in my_scan.list_of_hosts_found]

    # Get all IP addresses from the prefix
    for ipaddress in ipcalc.Network(my_network):
        ip_str = str(ipaddress)

        # Check if IP address is in the network range
        if ip_str in found_ip_in_network:
            # Check if IP address exists in NetBox
            request_url = f"{NB_URL}/api/ipam/ip-addresses/?q={ipaddress}/"
            ipaddress1 = requests.get(request_url, headers=HEADERS)
            netboxip = ipaddress1.json()

            # If IP address does not exist in NetBox, create it as deprecated
            if netboxip['count'] == 0:
                netbox.ipam.create_ip_address(ip_str, status="deprecated")
        else:
            # Check if IP address exists in NetBox
            request_url = f"{NB_URL}/api/ipam/ip-addresses/?q={ipaddress}/"
            ipaddress1 = requests.get(request_url, headers=HEADERS)
            netboxip = ipaddress1.json()

            # If IP address does not exist in NetBox, create it as deprecated
            if netboxip['count'] == 0:
                netbox.ipam.create_ip_address(ip_str, status="deprecated")
