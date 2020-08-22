#!/usr/bin/env python3

from bs4 import BeautifulSoup as bs
from selenium import webdriver
from time import sleep
import getpass
import os

# credenciais do usuário
username = str(input('Usuário: _ '))
password = getpass.getpass('Senha: _ ')

# inicializa driver
driver = webdriver.Chrome(executable_path=os.getcwd() + r'/../drivers/chromedriver')

# abre página de login
driver.get('https://www.notasonline.com/pages/nol_logon.asp')

# preenche credenciais do usuário
driver.find_element_by_id('txtLogin').send_keys(username)
driver.find_element_by_id('txtPassword').send_keys(password)
driver.find_element_by_id('frmForm').submit()
