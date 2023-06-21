from requests import get
from time import sleep

def main():
    """ Open List of IPs and read each line by line. Sleeps to not get blocked by API limitations """
    count = 0
    
    with open("..\\output\\outputfile.csv", 'w') as outfile:
        outfile.write("IP Address,Version,Country,Region,City,Country Capital,"
                      "Latitude,Longitude,Timezone,UTC-Offset,Country Calling Code,ASN,ORG\n")
        
        with open("..\\input\\IPlist.txt", 'r') as infile:
            for IP in infile:
                IP = IP.rstrip("\n")
                response = get_json(IP)
                count += 1; sleep(1)
                
                if count == 40:
                    sleep(70)
                    count = 0
                    
                if 'error' in response:
                    print(f"There was an error with IP: {IP} Skipping. Error: {response}")
                    continue

                write(outfile, response)


def get_json(IP):
    """ Query API with IP and retrieve JSON data """
    response = get(f'https://ipapi.co/{IP}/json/').json()
    return response


def write(outfile, json):
    """ Write retrieved data to output file """
    parsed_json = {
        "ip": json.get('ip'),
        "version": json.get('version'),
        "country": json.get('country_name'),
        "region": json.get('region'),
        "city": json.get('city'),
        "country_cap": json.get('country_capital'),
        "lat": json.get('latitude'),
        "long": json.get('longitude'),
        "tz": json.get('timezone'),
        "UTC": json.get('utc_offset'),
        "call_code": json.get('country_calling_code'),
        "asn": json.get('asn'),
        "org": json.get('org')
    }

    for value in parsed_json.values():
        outfile.write(f"{value},")
    outfile.write("\n")


if __name__ == "__main__":
    main()
