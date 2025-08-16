from flask import Flask, render_template, request
from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import urllib.parse

app = Flask(_name_)

def scrape_flipkart(product_name):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    flipkart_url = f'https://www.flipkart.com/search?q={urllib.parse.quote(product_name)}'
    response = requests.get(flipkart_url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    price = None
    for tag in soup.find_all("div", class_="_30jeq3"):
        if tag.text.strip():
            price = tag.text.strip()
            break
    return f'Flipkart: {price}' if price else 'Flipkart: Price not found'

def scrape_amazon(product_name):
    amazon_url = f'https://www.amazon.in/s?k={urllib.parse.quote(product_name)}'
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
    driver = webdriver.Chrome(options=options)
    driver.get(amazon_url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()
    price_element = soup.select_one(".a-price .a-offscreen")
    return f'Amazon: {price_element.text.strip()}' if price_element else 'Amazon: Price not found'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        product_name = request.form.get('product_name')
        if product_name:
            flipkart_price = scrape_flipkart(product_name)
            amazon_price = scrape_amazon(product_name)
            return render_template('index.html', flipkart_price=flipkart_price, amazon_price=amazon_price)
    return render_template('index.html', flipkart_price=None, amazon_price=None)

if _name_ == '_main_':
    app.run(debug=True)