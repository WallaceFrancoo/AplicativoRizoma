import os
import main
from PIL import Image
import customtkinter
import BancoDeDados
from tkinter import messagebox



def abrir_janela_depara():
    # Criar uma nova janela
    janela_depara = customtkinter.CTkToplevel()
    janela_depara.title("Cadastrar dePara")
    janela_depara.geometry("300x200")

    # Trazer a janela para frente e focá-la
    janela_depara.focus_force()
    janela_depara.grab_set()

    # Label e campo de entrada para "DE"
    label_de = customtkinter.CTkLabel(janela_depara, text="DE:")
    label_de.grid(row=0, column=0, padx=20, pady=10)
    entry_de = customtkinter.CTkEntry(janela_depara, width=200)
    entry_de.grid(row=0, column=1, padx=20, pady=10)

    # Label e campo de entrada para "PARA"
    label_para = customtkinter.CTkLabel(janela_depara, text="PARA:")
    label_para.grid(row=1, column=0, padx=20, pady=10)
    entry_para = customtkinter.CTkEntry(janela_depara, width=200)
    entry_para.grid(row=1, column=1, padx=20, pady=10)

    # Função para pegar os valores das entradas e chamar adicionar_Dados
    def cadastrar():
        DE = entry_de.get()
        PARA = entry_para.get()
        if DE and PARA:
            # Pergunta de confirmação
            confirmar = messagebox.askokcancel(
                "Confirmação",
                f"Você digitou o historico {DE} para ir para a conta {PARA}. Deseja confirmar?"
            )
            if confirmar:
                BancoDeDados.adicionar_Dados(DE, PARA)
        else:
            messagebox.showwarning("Atenção", "Preencha todos os campos!")

    # Botão de Cadastrar
    botao_cadastrar = customtkinter.CTkButton(janela_depara, text="Cadastrar", command=cadastrar)
    botao_cadastrar.grid(row=2, column=0, columnspan=2, pady=20)
def abrir_janela_CliFor():
    # Criar uma nova janela
    janela_depara = customtkinter.CTkToplevel()
    janela_depara.title("Cadastrar CliFor")
    janela_depara.geometry("500x200")

    # Trazer a janela para frente e focá-la
    janela_depara.focus_force()
    janela_depara.grab_set()

    # Label e campo de entrada para "DE"
    label_de = customtkinter.CTkLabel(janela_depara, text="DESCRICAO:")
    label_de.grid(row=0, column=0, padx=20, pady=10)
    entry_de = customtkinter.CTkEntry(janela_depara, width=300, placeholder_text="Incluir os dados da planilha!")
    entry_de.grid(row=0, column=1, padx=20, pady=10)

    # Label e campo de entrada para "PARA"
    label_para = customtkinter.CTkLabel(janela_depara, text="CONTA:")
    label_para.grid(row=1, column=0, padx=20, pady=10)
    entry_para = customtkinter.CTkEntry(janela_depara, width=300, placeholder_text="Conta do cliente/fornecedor")
    entry_para.grid(row=1, column=1, padx=20, pady=10)

    # Função para pegar os valores das entradas e chamar adicionar_Dados
    def cadastrar():
        DE = entry_de.get()
        PARA = entry_para.get()
        if DE and PARA:
            # Pergunta de confirmação
            confirmar = messagebox.askokcancel(
                "Confirmação",
                f"Você digitou o historico {DE} para ir para a conta {PARA}. Deseja confirmar?"
            )
            if confirmar:
                    BancoDeDados.adicionar_CliFor(DE, PARA)
        else:
            messagebox.showwarning("Atenção", "Preencha todos os campos!")

    # Botão de Cadastrar
    botao_cadastrar = customtkinter.CTkButton(janela_depara, text="Cadastrar", command=cadastrar)
    botao_cadastrar.grid(row=2, column=0, columnspan=2, pady=20)

self = customtkinter.CTk()
self.title("Conversão CSV para Rizoma v4")
self.geometry("800x550")

# set grid layout 1x2
self.grid_rowconfigure(0, weight=1)
self.grid_columnconfigure(1, weight=1)

# load images with light and dark mode image
image_path = "Z:\Diversos\Projetos T.I\Rizoma\imagens"
logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "Transparente2.png")), size=(26, 26))
large_test_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "Simbolo.png")), size=(150, 100))
image_icon_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "pdf.png")), size=(20, 20))
image_icon_image2 = customtkinter.CTkImage(Image.open(os.path.join(image_path, "excel.png")), size=(20, 20))

# create navigation frame = column 0
navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
navigation_frame.grid(row=0, column=0, sticky="nsew")
navigation_frame.grid_rowconfigure(6, weight=1)
navigation_frame_label = customtkinter.CTkLabel(navigation_frame, text="  Sergecont Contabilidade", image=logo_image,
                                                compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

# create textbox
textbox = customtkinter.CTkTextbox(navigation_frame,
                                   corner_radius=10,
                                   width=100,
                                   fg_color="transparent",
                                   wrap="word")
textbox.grid(row=1, column=0, rowspan=6, padx=(10, 10), pady=(10, 10), sticky="nsew")
textbox.insert("0.0", "Segue aplicativo para conversão do arquivo CSV para TXT da empresa Instituto Rizoma\n\n"
                      "1. Site para retirar planilha: https://contas.granatum.com.br/users/sign_in\n\n"
                      "   Login: brendha@sergecont.com.br\n"
                      "   Senha: P@lhares1266\n\n"
                      "2. Ir na aba lançamentos, filtrar o mês desejado e Exportar Arquivo\n\n"
                      "3. Esse arquivo irá utilizar ao lado para gerar o TXT! !\n\n\n"
                      "4. Esse TXT irá importar os lançamentos de:\n\n"
                      "- Lançamentos Itau\n"
                      "- Lançamentos conta Cora\n\n"
                      "- Os lançamentos com categoria: Direcionado, Doações, PJ Recorrente, Livre, Pontuais, Recorrente, Eventos e Campanhas\n\n"
                      "5. Ira ser feito um lançamento para faturamento na conta 407\n"
                      "6. Se atentar a linha cliente/fornecedores caso tenha dados ali, cadastrar como Cliente, se não cadastrar no dePara"

               )

# create home frame column 1
home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
home_frame.grid_columnconfigure(0, weight=1)
home_frame_large_image_label = customtkinter.CTkLabel(home_frame, text="", image=large_test_image)
home_frame_large_image_label.grid(row=0, column=0, columnspan=2, padx=10, pady=15)

# Botão Selecionar arquivo PDF
botao_pdf = customtkinter.CTkButton(home_frame, text="Selecionar Arquivo", image=image_icon_image2, compound="right",
                                    command=main.buscarArquivo)
botao_pdf.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)
botao_pdf.grid(row=2, column=0, pady=50, columnspan=2)

# Botão onde salvar Excel
botao_gerar = customtkinter.CTkButton(home_frame, text="Gerar Arquivo", compound="right",
                                      command=main.gerarArquivo)
botao_gerar.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)
botao_gerar.grid(row=3, column=0, pady=0, columnspan=2)

frame_cadastro = customtkinter.CTkFrame(home_frame,fg_color="transparent")
frame_cadastro.grid(row=4, column=0, pady=10, columnspan=2)

# Botão Cadastrar dePara
botao_cadastrodePara = customtkinter.CTkButton(frame_cadastro, text="Cadastrar dePara", compound="left",command=abrir_janela_depara)
botao_cadastrodePara.grid(row=0, column=0, padx=10, pady=10)

# Botão Cadastrar Cliente
botao_cadastroCliente = customtkinter.CTkButton(frame_cadastro, text="Cadastrar Cliente", compound="left",command=abrir_janela_CliFor)
botao_cadastroCliente.grid(row=0, column=1, padx=10, pady=10)

home_frame.grid(row=0, column=1, sticky="nsew")

self.mainloop()