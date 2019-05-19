# Shivam Saheb
# This is the tool to analyze trading card prices

import csv
from lxml import html
import requests
from datetime import datetime

def CPIdentifier():
    get_table()


def get_table():
    card_list_table_updated = []

    now = datetime.now()

    identifier = now.strftime("%B_%d_%Y_%H_%M_%S")

    with open("card_list_original.csv", "r") as file:
        card_list_table = csv.reader(file, delimiter = ',')

        for i, row in enumerate(card_list_table):
            print("Fetching card data at index:", i)

            if i == 0:
                row.append("PPC_" + identifier)
                row.append("TPC_" + identifier)

            else:
                cardId = row[1]
                url = row[2]
                rarity = row[3]
                quantity = int(row[6])

                (name, price) = get_details(url)

                row.append(str(price))
                row.append(str(quantity * price))

            card_list_table_updated.append(row)

    with open("card_list_currents.csv", "w", newline="") as file:
        card_list_writer = csv.writer(file, delimiter = ",")

        for row in card_list_table_updated:
            print("Writing card data at index:", i)

            card_list_writer.writerow(row)


def get_details(url):
    page = requests.get(url)
    tree = html.fromstring(page.content)
    name = tree.xpath("//div[@itemprop='name']/text()")
    price = get_price(tree)

    return (name[0], price)

def get_price(tree):
    p = tree.xpath("//div[@class='price']/text()")[0]
    p = p[1:]

    return float(p)


if __name__ == "__main__":
    CPIdentifier()



