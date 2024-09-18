import pandas as pd
from tkinter import filedialog, Button, Label, Tk, messagebox
import BancoDeDados
from datetime import datetime
import re
import os
from unidecode import unidecode
import PyPDF2
cabecarioErro = "Verificar se na linha da planilha tem cliente/fornecedor, caso SIM cadastrar Cliente/Fornecedor em CliFor se NÃO cadastrar o historico no dePara!\n\nCaso o historico comece com data o lançamento irá para Cartão de credito\n\n"
def ProcessamentoDeDados(arquivo):
    try:
        # Lendo o arquivo CSV
        dados = pd.read_csv(arquivo, delimiter=";", encoding='ISO-8859-1')

        # Definindo variáveis e colunas
        ClienteOuFornecedor = 'Cliente/Fornecedor'
        DescricaoCol = 'Descrição'
        ContaCol = 'Conta'
        DataCol = 'Data de pagamento'
        ValorCol = 'Valor'
        FormaDePagamentoCol = 'Forma de pagamento'
        ContaCartaoDeCredito = "672"
        CentroDeCusto = 'Centro de custo/lucro'
        CategoriaCol = 'Categoria'

        # Filtrando linhas onde a data está vazia
        dados = dados[dados[DataCol].notna() & (dados[DataCol] != '')]

        relatorio_acertos = []
        relatorio_separado = []

        # Função para formatar a linha
        def formatar_linha(linha):
            Debito = ''
            Credito = ''

            Conta = str(linha[ContaCol])
            if Conta == "Aplicação CDB":
                return None
            elif Conta == "Itaú Unibanco S.A.":
                ContaBanco = "536"
            elif Conta == "CORA SOCIEDADE DE CRÉDITO DIRETO S.A.":
                ContaBanco = "563"

            Data = str(linha[DataCol])[:10]
            # Se a data estiver vazia, ignore a linha
            if not Data or Data == 'nan':
                return None
            custo = ''
            if str(linha[CentroDeCusto]) == "Institucional":
                custo = '2'
            elif str(linha[CentroDeCusto]) == 'Contraturno':
                custo = '3'
            elif str(linha[CentroDeCusto]) == 'Rizoarte':
                custo = '4'
            elif str(linha[CentroDeCusto]) == 'Socioemocional':
                custo = '5'
            else:
                custo = ''
            Valor = str(linha[ValorCol]).replace('-', '').replace('.', '')
            ConsultaContraPartida = str(linha[ClienteOuFornecedor])
            complemento = ''
            Cliente = ''
            Historico = ''
            if ConsultaContraPartida == 'nan':
                historico = str(linha[DescricaoCol])[:5]
                if re.match(r'\d{2}/\d{2}', historico):
                    ContraPartida = '672'
                    Cliente = str(linha[DescricaoCol])
                else:
                    ContraPartida = BancoDeDados.ConsultarHistorico(str(linha[DescricaoCol]))
                    Cliente = str(linha[DescricaoCol])
            else:
                ContraPartida = BancoDeDados.ConsultarCliente(str(linha[ClienteOuFornecedor]))
                Cliente = str(linha[ClienteOuFornecedor])
            ContraPartidaCartao = "672" if linha[FormaDePagamentoCol] == "Cartão de Crédito" else ""
            if ContraPartidaCartao == "672":
                if "-" in str(linha[ValorCol]):
                    Debito = ContaCartaoDeCredito
                    Credito = ContaBanco
                    custo = custo
                    Historico = f"PAGAMENTO REF. {str(linha[DescricaoCol])}"
                else:
                    Debito = ContaBanco
                    Credito = ContaCartaoDeCredito
                    custo = custo
                    Historico = f"RECEBIMENTO REF. {str(linha[DescricaoCol])}"
            else:
                if "-" in str(linha[ValorCol]):
                    Debito = ContraPartida
                    Credito = ContaBanco
                    custo = custo
                    Historico = f"PAGAMENTO REF. {str(linha[DescricaoCol])}"
                else:
                    Debito = ContaBanco
                    Credito = ContraPartida
                    Historico = f"RECEBIMENTO REF. {str(linha[DescricaoCol])}"
                    custo = custo
                    if str(linha[CategoriaCol]) in ["Direcionado", "Doações PJ Recorrente", "Livre", "Pontuais", "Recorrente"]:
                        HistoricoFaturamento = f"VALOR REF. {str(linha[DescricaoCol])}"
                        complemento = f"\n{Data};{Credito};407;{Valor};;{HistoricoFaturamento};1;;;"

            linha_formatada = unidecode(f"{Data};{Debito};{Credito};{Valor};;{Historico};1;;{custo};{custo}{complemento}").upper()
            linhas_erros = unidecode(f"Aviso: No Dia {Data} o lançamento com o historico: - ({str(linha[DescricaoCol])}) O lançamento irá para acerto!")

            relatorio_acertos.append(linha_formatada)
            if Debito == "6" or Credito == "¨6":
                relatorio_separado.append(linhas_erros)

            return linha_formatada

        # Aplicando a formatação em todas as linhas
        texto_formatado = dados.apply(formatar_linha, axis=1)

        # Filtrando linhas não nulas antes de criar o resultado final
        resultadoFinal = [texto for texto in texto_formatado if texto is not None]

        return resultadoFinal, relatorio_separado

    except UnicodeDecodeError:
        print("Ocorreu um erro de codificação ao ler o arquivo!")
        return None, None

dados_extraidos = []
relatorio_separado = []
def buscarArquivo():

  global dados_extraidos, relatorio_separado
  arquivo = filedialog.askopenfilename(
    title="Selecione um arquivo CSV",
    filetypes=(("Arquivos CSV", "*.csv"), ("Todos os arquivos", "*.*"))
  )
  if arquivo:
    print(f"Arquivo Seleciona {arquivo}")
    dados_extraidos, relatorio_separado = ProcessamentoDeDados(arquivo)
    return
  else:
    return None
def gerarArquivo():
    global dados_extraidos, relatorio_separado
    messagebox.showinfo('Aviso',
                        'Irá gerar 2 arquivos, o primeiro é para integrar e o segundo é um relatorio de contas em acerto!')
    caminho_arquivo_txt = filedialog.asksaveasfilename(
        title="Salvar arquivo como",
        defaultextension=".txt",
        filetypes=(("Arquivo de Texto", "*.txt"), ("Todos os arquivos", "*.*"))
    )
    if caminho_arquivo_txt:
        try:
            with open(caminho_arquivo_txt, "w") as arquivo:
                for dado in dados_extraidos:
                    arquivo.write(dado.upper() + '\n')
            messagebox.showinfo('Sucesso', f"Arquivo geral salvo com sucesso!")
            # Salvar o relatório de débitos e créditos igual a 6
            caminho_relatorio_txt = filedialog.asksaveasfilename(
                title="Salvar relatório de erros como",
                defaultextension=".txt",
                filetypes=(("Arquivo de Texto", "*.txt"), ("Todos os arquivos", "*.*"))
            )
            if caminho_relatorio_txt:
                with open(caminho_relatorio_txt, "w") as relatorio_arquivo:
                    relatorio_arquivo.write(cabecarioErro)
                    for relatorio in relatorio_separado:
                        relatorio_arquivo.write(relatorio.upper() + '\n')
                messagebox.showinfo('Sucesso', f"Relatório de erros salvo com sucesso!")
                os.startfile(caminho_relatorio_txt)
        except Exception as e:
            print(f"Erro ao salvar arquivo TXT: {e}")
    else:
        print("Local de salvamento não selecionado")

