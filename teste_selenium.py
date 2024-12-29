from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

try:
    driver = webdriver.Chrome()

    driver.get("https://www.google.com/finance/quote/PETR4:BVMF")

    barra_de_busca = driver.find_element(By.CLASS_NAME, "Ax4B8.ZAGvjd")

    sleep(5)
    barra_de_busca.click()


    barra_de_busca.clear()

    barra_de_busca.send_keys("mxrf11")

    botão_de_pesquisa = driver.find_element(By.CLASS_NAME, "gb_De")
    botão_de_pesquisa.click()

    sleep(60)
    driver.quit()

except Exception as e:
    print("Erro inesperado ", e)