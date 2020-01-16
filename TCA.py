# Shivam Saheb
# This is the tool to analyze trading card prices

import csv
from lxml import html
import requests
from datetime import datetime


def CPIdentifier():
    get_table()


def run_prompt():
    prompt1 = input("Do you wish to search for a card? ")

    if prompt1 in ("Y", "y", "yes", "Yes"):
        prompt2 = input("Enter the card type (Monster/Spell/Trap/Fusion/XYZ/Synchro): ")
        prompt3 = input("What is the name of the card which you wish to find in the database: ")
        card_search(prompt2)

    elif prompt1 in ("N", "n", "no", "No"):
        print("\n This script shall now proceed to update the existing Card Price Entries... \n")

        get_table()

    elif prompt1 == "end":
        print("\n Thank you for using this script. Goodbye. \n")

    else:
        print("\n Illegal entry; It's a Yes or No question! \n")
        run_prompt()


def card_search(prompt2):
    with open("card_list_currents.csv", "r") as file:
        card_list_table = csv.DictReader(file, delimiter=',')

        types = [[], []]

        for row in card_list_table:
            types.append([row["Card Type"], row["Card Name"]])



        # if prompt2 in names:
        #     print("\n That card exists in the database! \n")
        #     run_prompt()
        #
        # else:
        #     print("\n That card does not exist in the database. \n")
        #     run_prompt()


def get_table():
    card_list_table_updated = []

    now = datetime.now()

    identifier = now.strftime("%B_%d_%Y_%H_%M_%S")

    with open("card_list_currents.csv", "r") as file:
        card_list_table = csv.reader(file, delimiter=',')

        for i, row in enumerate(card_list_table):
            print("Fetching card data at index:", i)

            if i == 0:
                row.append("PPC_" + identifier)
                row.append("TPC_" + identifier)

            else:
                cardId = row[2]
                url = row[3]
                rarity = row[4]
                quantity = int(row[7])

                (name, price) = get_details(url)

                row.append(str(price))
                row.append(str(quantity * price))

            card_list_table_updated.append(row)

    with open("card_list_currents.csv", "w", newline="") as file:
        card_list_writer = csv.writer(file, delimiter=",")

        for row in card_list_table_updated:
            card_list_writer.writerow(row)


def get_details(url):
    page = requests.get(url)
    tree = html.fromstring(page.content)
    name = tree.xpath("//h1[@itemprop='name']/text()")
    price = get_price(tree)

    return (name[0], price)


def get_price(tree):
    p = tree.xpath("//div[@class='d-flex flex-column']/span/text()")[0]
    p = p[1:]

    return float(p)


if __name__ == "__main__":
    CPIdentifier()
