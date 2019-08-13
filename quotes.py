import random
import string
import requests
import json
import datetime
from typing import List
from html.parser import HTMLParser

# --- CONSTANTS

headers = {
    "User-Agent": "AsciiArt"
}

trekPath = "https://www.needsomefun.net/best-star-trek-quotes-ever/"


# --- HELPER FUNCTIONS

def replaceAll(string: str, replace: List[str], replace_with: str) -> str:
    for thing in replace:
        string = string.replace(thing, replace_with)
    return string

def listIn(string: str, check: List[str]) -> bool:
    for thing in check:
        if thing in string:
            return False
    return True

def linkFormat(string: str) -> str:
    if string[-1] == "-":
        string = string[:-1]
    return string.replace(" ", "-").replace("&", "and").lower()

class Parser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.handling_p = False
        self.to_add = ""
        self.ps = []

    def handle_starttag(self, tag, attrs):
        if tag == "p":
            self.handling_p = True

    def handle_endtag(self, tag):
        if tag == "p":
            self.handling_p = False
            self.ps.append(self.to_add.replace("\n", ""))
            self.to_add = ""
    
    def handle_data(self, data):
        if self.handling_p:
            self.to_add += " " + data
    
    def reset_quotes(self):
        self.found = False
        self.quotes = ""

def trek_quotes_json():
    trek_json = {"quotes": []}

    parser = Parser()

    page = requests.get(trekPath, headers=headers)
    parser.feed(page.text)
    quotes = parser.ps
    parser.reset_quotes()

    for quote in quotes[:-15]:
        quote = quote.replace("“", "\"").replace("”", "\"").replace("’", "'")
        printable = set(string.printable)
        filtered = list(filter(lambda x: x in printable, quote))
        filtered_string = ""

        for character in filtered:
            filtered_string += character

        if quote != "":
            trek_json["quotes"].append({
                "quote": filtered_string, 
            "occurences": 1
            })
    
    with open("trek_quotes.json", "w") as file:
        file.write(json.dumps(trek_json))

def build_trek_occurences():
    with open("trek_quotes.json", "r") as file:
        trek_json = json.load(file)
    
    with_occurences = []
    for quote in trek_json["quotes"]:
        for x in range(quote["occurences"]):
            with_occurences.append(quote["quote"])
    
    with open("trek_with_occurences.json", "w") as file:
        file.write(json.dumps({"quotes": with_occurences}))

        
# --- LAMBDA
def lambda_handler(event=None, context=None) -> dict:
    with open("trek_with_occurences.json", "r") as file:
        quotes_json = json.load(file)
    
    quote = quotes_json["quotes"][random.randint(0, len(quotes_json["quotes"]) - 1)]
    return {
        "statusCode": 200,
        "headers": {"content-type": "text/html"},
        "body": f"<html><body>{quote}</body></html>"
    }
