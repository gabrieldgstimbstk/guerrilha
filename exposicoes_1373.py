# -------------------- Importações -----------------------------
import time

inicio = time.time()

import asyncio
import os
from playwright.async_api import async_playwright
import pandas as pd
import glob
from datetime import datetime, timedelta
import warnings
from openpyxl import load_workbook
from openpyxl.styles import PatternFill, Border, Side, Alignment

# Desativando Mensagens de erros
warnings.filterwarnings("ignore")

reiniciado = False

# -------------------- Funções ----------------------------------
async def main():
    async def handle_console(msg, browser):
        '''
        Função para lidar com o erro 502 - Bad Gateway, bastante recorrente em relatórios maiores
        '''

        print(f"Console do Navegador: {msg.text}")
        global reiniciado

        if "Failed to load resource: the server responded with a status of 502" in msg.text:
            print(10 * '-')
            print("Erro 502 detectado. Reiniciando o código...")
            print(10 * '-')

            if not reiniciado:
                await browser.close()
                await asyncio.sleep(10)
                await rel1373_emissao()

            reiniciado = True

    # -------------------- Funções ----------------------------------

    async def rel1373_emissao(data_inicio_formatado=None):
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                executable_path='C:\\Users\\gabriel.dagostim\\Documents\\chrome-win\\chrome.exe', headless=False)
            context = await browser.new_context(ignore_https_errors=True)
            page = await context.new_page()

            page.on('console', lambda msg: handle_console(msg, browser))

            # Acesse a URL de login
            await page.goto("https://bapi.bistek.com.br/relatorio/1373")

            # Preenche o campo de usuário e senha
            await page.fill('input[name="username"]', 'gabriel.dagostim')
            await page.fill('input[name="password"]', 'Bstk$$2024')

            # Clique no botão "Entrar"
            await page.click('input[name="login"]')

            # Aguarde até que a página de destino seja carregada
            await page.wait_for_selector('input[name="btConsulta"]', state='attached')

            # -------------------- FILTROS ----------------------------------
            lojas = ['2','4','5','7','9','10','11','12','14','16','17','18','19','20','21','22','23','24','25','26','27','29','31','32','33']
            for loja in lojas:
                await page.check(f'input[value="{loja}"]')
            
            # -------------------- FILTROS ----------------------------------

            # Clique no botão de consulta
            await page.click('input[name="btConsulta"]')

            # AGUARDANDO
            await page.wait_for_timeout(5000)

            # Aguarda até que o elemento para download esteja pronto
            await page.wait_for_selector('#imgExportaCSV', state='attached')

            await page.evaluate('''() => {
                document.querySelector('#imgExportaCSV').click();
            }''')

            try:
                download = await page.wait_for_event('download', timeout=180000)
            except Exception as e:
                print(f"Erro ao aguardar o evento de download: {e}")
                return None

            # Define o caminho da pasta de downloads
            downloads_folder = 'C:/Users/gabriel.dagostim/Downloads'

            # Mova o arquivo para a pasta de downloads desejada
            filename = download.suggested_filename
            await download.save_as(os.path.join(downloads_folder, filename))

            # Remove o iframe
            await page.evaluate('''() => {
                var iframe = document.querySelector('iframe');
                if (iframe) {
                    iframe.parentNode.removeChild(iframe);
                }
            }''')

            # Remove o cookie
            await page.evaluate('document.cookie = "fileDownload=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/"')

            # Define o caminho da pasta de downloads
            downloads_folder = 'C:/Users/gabriel.dagostim/Downloads'

            # Mova o arquivo para a pasta de downloads desejada
            filename = download.suggested_filename
            new_path = os.path.join('C:/Users/gabriel.dagostim/Desktop/Ruptura/automacoes', filename)
            await download.save_as(new_path)

            # Fechar navegador
            await browser.close()
        return filename

    await rel1373_emissao()

    # Define o caminho da pasta
    folder_path = 'C:/Users/gabriel.dagostim/Desktop/Ruptura/automacoes/'

    # Encontra todos os arquivos que começam com 'relatorio_1190' e terminam com '.csv'
    files = glob.glob(os.path.join(folder_path, 'relatorio_1373*.csv'))

    # Ordena os arquivos por data de modificação (o mais recente será o primeiro)
    files.sort(key=os.path.getmtime, reverse=True)

    # Pega o arquivo mais recente
    latest_file = files[0] if files else None

    print(f'O arquivo mais recente é: {latest_file}')
    print('\n')
    print('=====================================================================================================')
    print('Concluído com sucesso! - Baixamos o relatório 🤖')
    print('=====================================================================================================')
    print('\n')
    relatorio_1373 = pd.read_csv(latest_file, sep=';')

    print('=============================')
    print('Iniciando Tratamento de Dados')
    print('=============================')


    # Função para ajustar o formato dos valores
    def ajustar_formato(valor):
        if isinstance(valor, str):
            valor = valor.replace('.', '').replace(',', '.')
        return valor

    print(relatorio_1373.shape)
    print(relatorio_1373.head())

 
    # Análise de Tempo Executado
    print('-----------------')
    fim = time.time()
    tempo_total = fim - inicio
    print(f"Tempo total de execução: {round(tempo_total, 2)} segundos")

asyncio.run(main())