import os
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


def iniciar_driver():
    chrome_options = Options()

    arguments = ['--lang=pt-BR', '--window-size=1300,1000', '--incognito', ]

    for argument in arguments:
        chrome_options.add_argument(argument)

    chrome_options.add_experimental_option('prefs', {
        # Desabilitar confirmação de download
        'download.prompt_for_download': False,
        # Desabilitar notificações
        'profile.default_content_setting_values.notifications': 2,
        # Permitir multiplos download
        'profile.default_content_setting_values.automatic_downloads': 1,
    })

    driver = webdriver.Chrome(service=ChromeService(
        ChromeDriverManager().install()), options=chrome_options)

    return driver


driver = iniciar_driver()

# Navegar até o site
driver.get("https://www.olx.com.br/computadores-e-acessorios/estado-sp")
while True:
    # Carrecar todos elementos da página movendo até o final da tela
    sleep(20)
    driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
    sleep(2)


    # Encontrar títulos
    titulos = driver.find_elements(By.XPATH, "//div[@class='sc-12rk7z2-7 kDVQFY']//h2")

    # Encontrar preços
    precos = driver.find_elements(By.XPATH, "//span[@class='m7nrfa-0 eJCbzj sc-ifAKCX jViSDP']")

    # Encontrar links
    links = driver.find_elements(By.XPATH, "//a[@data-lurker-detail='list_id']")

    # Guardar isso em um arquivo .csv
    for titulo, preco, link in zip(titulos, precos, links):
        with open('precos.csv', 'a', encoding='utf-8', newline='') as arquivo:
            link_processado = link.get_attribute('href')
            arquivo.write(f'{titulo.text};{preco.text};{link_processado}{os.linesep}')

    # Fazer isso para todas as páginas existentes
    try:
        btn_prox_pag = driver.find_element(By.XPATH, "//span[text()='Próxima pagina']")
        sleep(2)
        btn_prox_pag.click()
    except:
        print('chegamos na última página')
        break
    
sleep(5)
driver.close()
