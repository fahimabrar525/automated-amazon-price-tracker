import requests
from bs4 import BeautifulSoup
import lxml
import smtplib
import os
from dotenv import load_dotenv

load_dotenv()

MY_EMAIL = os.environ.get("MY_EMAIL")
MY_PASSWORD = os.environ.get("MY_PASSWORD")

url = "https://www.amazon.com/dp/B0C35HNPW9/ref=sbl_dpx_kitchen-electric-cookware_B0CKW18NKD_0"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0",
    "Accept-Language": "en-US,en;q=0.5"
}

response = requests.get(url=url, headers=headers)

soup = BeautifulSoup(response.content, "lxml")

price_tag = soup.find(name="span", class_="a-offscreen").getText()
price_without_currency = price_tag.split("$")[1]
price_as_float = float(price_without_currency)
print(price_as_float)

if price_as_float < 150:
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL,
                            to_addrs="fahimabrar.aiub@gmail.com",
                            msg=f"Subject:Price alert!\n\nnow {price_as_float}")
