from bs4 import BeautifulSoup
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from csv import writer
import csv
import requests

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 '
                  'Safari/537.36 '
}

with open("people.csv", "a", encoding="utf-8", newline="") as f:
    header = ["Url", "Description", "Twitter", "E-Mail"]
    csv_writer = csv.writer(f, delimiter=";")
    csv_writer.writerow(header)

    list_attr = []

    browser = webdriver.Chrome("D:\\user\\Downloads\\chromedriver1\\chromedriver.exe")

    browser.get("https://www.indiehackers.com/groups")

    browser.maximize_window()
    time.sleep(5)

    html_text = browser.page_source

    soup = BeautifulSoup(html_text, "lxml")

    groups = soup.find_all("a", class_="ember-view group-list__group-link")


    def find_people(person):
        global list_attr

        list_attr.append("https://www.indiehackers.com" + person['href'])
        time.sleep(2)
        browser.get("https://www.indiehackers.com" + person['href'])

        browser.maximize_window()
        time.sleep(8)
        html_text = browser.page_source
        soup = BeautifulSoup(html_text, "lxml")

        time.sleep(2)
        credentials = soup.find("div", class_="user-header__metadata").text.strip()

        list_attr.append(' '.join(credentials.split()))

        twitter_mail = soup.find_all("a", class_="user-header__satellite user-header__satellite--contact")

        if len(twitter_mail) == 2:
            for link in twitter_mail:
                list_attr.append(link['href'])
        elif len(twitter_mail) == 0:
            list_attr.append("")
            list_attr.append("")
        elif "mailto" in twitter_mail[0]:
            list_attr.append("")
            list_attr.append(twitter_mail[0]['href'])
        else:
            list_attr.append(twitter_mail[0]['href'])
            list_attr.append("")

        csv_writer.writerow(list_attr)
        f.flush()
        list_attr = []


    for group in groups:
        browser.get("https://www.indiehackers.com" + group['href'])
        time.sleep(8)
        html_text = browser.page_source
        soup = BeautifulSoup(html_text, "lxml")

        members = soup.find("div", class_="about-section__info").text.strip().split(" ")
        num = int(members[0].replace(",",""))

        if num > 20000:
            browser.get("https://www.indiehackers.com" + group['href'] + "/members")
            csv_writer.writerow(["https://www.indiehackers.com" + group['href'] ])
            # Get scroll height
            last_height = browser.execute_script("return document.body.scrollHeight")

            while True:
                # Scroll down to bottom
                browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                # Wait to load page
                time.sleep(8)
                html_text = browser.page_source
                soup = BeautifulSoup(html_text, "lxml")
                people = soup.find_all("a", class_="user-link__link ember-view")
                for person in people:
                    find_people(person)

                # Calculate new scroll height and compare with last scroll height
                new_height = browser.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height
            break
