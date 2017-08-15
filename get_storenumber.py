import csv
import json

import requests

# url = "http://storelocator.sprint.com/locator/GetData.ashx?r=10&sar=1&loc="
# store = quote(str(raw_input('Enter Zip, or City, State: ')))
# request = requests.get(url=url + store)


print("Start")
zip_list = []
with open('zips', 'r') as f:
    for line in f:
        zip_list.append(line.replace('\n', ''))
print("Got Zip List")

with open('eggs.csv', 'wb') as csvfile:
    csv_writer = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
    for zip_code in zip_list:
        print("Parsing zip: %s" % zip_code)
        url = "http://storelocator.sprint.com/locator/GetData.ashx?r=10&sar=1&loc="
        request = requests.get(url=url + zip_code)
        data = json.loads(request.text)
        try:
            for store in data["Hits"]:
                try:
                    sn = store["Retailer"]["StoreNumber"]
                    phone = store["Retailer"]["PhoneNumber"]
                    addr1 = store["Retailer"]["PostalAddress"]["Address1"]
                    addr2 = store["Retailer"]["PostalAddress"]["Address2"]
                    city = store["Retailer"]["PostalAddress"]["City"]
                    state = store["Retailer"]["PostalAddress"]["State"]
                    csv_writer.writerow([sn, phone, addr1, addr2, city, state])
                except UnicodeEncodeError:
                    print("UnicodeEncodeError")
        except KeyError:
            print("No Hits")
