#!/usr/bin/env python3

from bs4 import BeautifulSoup as bs
from selenium import webdriver
from time import sleep
from requests.auth import HTTPBasicAuth
import requests
import getpass
import logging
import os


def login(username: str, password: str) -> None:
    """
    Recebe username e password do usuário e utiliza essas credenciais
    para tentar fazer login no sistema do notas online. Após a
    submissão do formulário, verifica se o conteúdo exibido corresponde
    à página inicial do sistema, retornando True ou False.
    """

    # abre página de login
    driver.get('https://www.notasonline.com/pages/nol_logon.asp')
    #logger.info(f'ACESSO À PÁGINA EFETUADO POR {username}!')
    sleep(1)

    # preenche credenciais do usuário
    driver.find_element_by_id('txtLogin').send_keys(username)
    driver.find_element_by_id('txtPassword').send_keys(password)
    driver.find_element_by_id('frmForm').submit()

    # verifica se o login foi efetuado, através da url atual
    if driver.current_url == 'https://www.notasonline.com/pages/home_teacher.asp':
        #logger.info('Logou com sucesso!')
        return True
    else:
        #logger.error('Não foi possível logar no sistema. Você digitou as credenciais corretas?')
        return False


# credenciais do usuário
username = str(input('Usuário: _ '))
password = getpass.getpass('Senha: _ ')

# inicializa driver
driver = webdriver.Chrome(executable_path=os.getcwd() + r'/drivers/chromedriver')

if login(username, password):
    page = driver.get('https://www.notasonline.com/pages/admin_divisions_diaries_fill_in.asp?default_year=2020')
    diarios = driver.find_element_by_id('seldivisions_teachers_subjects').get_attribute('innerHTML')
    soup = bs(diarios, 'html.parser')

    ops = soup.find_all('option')
    disc = {
        'D': 'DG',
        'F': 'FIS',
        'G': 'GMT'
    }
    for op in ops:
        code = op.get('value')
        text = op.get_text().strip().split('/')
        if len(text) > 1:
            turma = text[1].strip()
            disciplina = text[3].strip().upper()
            print(code, turma[2:], disc[disciplina[:1]], sep=',')
