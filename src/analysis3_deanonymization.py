from selenium import webdriver
from selenium.webdriver.common.by import By

# TODO: read top h longest chains from a file and link them to a wallet
bitcoin_address = "1LT7i483B8FoCFdA4bMQmbWMSQek7vYKfv"

def get_div_content(url: str, class_name: str) -> str:
    """Opens a URL and returns the text content of the first matching div class."""
    driver = webdriver.Chrome()

    try:
        driver.get(url)
        target_element = driver.find_element(By.CLASS_NAME, class_name)
        return target_element.text
    except Exception as error:
        return f"An error occurred: {error}"
    finally:
        driver.quit()

web_address = f"https://www.walletexplorer.com/address/{bitcoin_address}"
result = get_div_content(web_address, "wallet_name")
print(result)
