from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
import pandas as pd
import matplotlib.pyplot as plt
import csv
import re
import time

URL = "https://www.divan.ru/category/divany?sort=4"


def get_prices():
    # Настраиваем Selenium под Firefox
    options = webdriver.FirefoxOptions()
    
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)

    driver.get(URL)
    time.sleep(5)  # ждём загрузку динамического контента

    prices = []
    # каждый блок с ценой
    price_elements = driver.find_elements(By.CSS_SELECTOR, ".product-card__price")

    for elem in price_elements:
        try:
            # пробуем взять акционную цену
            disc = elem.find_element(By.CSS_SELECTOR, ".product-card__price--discounted")
            text = disc.text
        except:
            # если её нет — берём любую цену
            text = elem.text

        match = re.search(r"([\d\s]+)", text)
        if match:
            num = int(match.group(1).replace(" ", ""))
            prices.append(num)

    driver.quit()
    return prices


def save_to_csv(prices, filename="divan_prices.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["price"])
        for p in prices:
            writer.writerow([p])


def load_and_analyze(filename="divan_prices.csv"):
    df = pd.read_csv(filename)
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df = df.dropna(subset=["price"])
    mean_price = df["price"].mean()
    print(f"Средняя цена дивана: {mean_price:.2f} руб.")
    # Строим гистограмму
    plt.figure(figsize=(10, 6))
    plt.hist(df["price"], bins=30, color='skyblue', edgecolor='black')
    plt.title("Гистограмма цен на диваны (руб.)")
    plt.xlabel("Цена, руб.")
    plt.ylabel("Количество моделей")
    plt.grid(axis='y', alpha=0.75)
    plt.tight_layout()
    plt.show()


def main():
    prices = get_prices()
    if not prices:
        print("Не удалось найти цены — проверьте селекторы.")
        return
    save_to_csv(prices)
    load_and_analyze()


if __name__ == "__main__":
    main()
