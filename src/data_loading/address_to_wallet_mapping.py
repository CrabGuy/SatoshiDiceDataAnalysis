from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
import os

CACHE_FILE = "./data/processed/wallet_cache.csv"

def load_cache(cache_file: str = CACHE_FILE) -> dict:
    cache = {}
    if os.path.exists(cache_file):
        with open(cache_file, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) == 2:
                    address, wallet = row
                    cache[address] = wallet
    return cache

def load_driver():
    return webdriver.Chrome()

def cache_get_wallet(bitcoin_address, cache: dict):
    return cache.get(bitcoin_address)

def save_to_cache(bitcoin_address, attached_wallet, cache: dict, cache_file: str = CACHE_FILE):
    cache[bitcoin_address] = attached_wallet
    with open(cache_file, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([bitcoin_address, attached_wallet])

def get_div_content(driver, url: str, class_name: str) -> str:
    driver.get(url)
    target_element = driver.find_element(By.CLASS_NAME, class_name)
    return target_element.text

def online_get_wallet(driver, bitcoin_address):
    web_address = f"https://www.walletexplorer.com/address/{bitcoin_address}"
    result = get_div_content(driver, web_address, "wallet_name")
    return result

def get_wallet(cache: dict, driver, bitcoin_address):
    cached = cache_get_wallet(bitcoin_address, cache)
    if cached is not None:
        return cached

    wallet = online_get_wallet(driver, bitcoin_address)
    save_to_cache(bitcoin_address, wallet, cache)
    return wallet
