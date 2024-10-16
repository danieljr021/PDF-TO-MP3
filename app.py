import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import PyPDF2
import pyttsx3
import threading

class Aplicacao:
    def __init__(self, master):
        self.master = master
        self.master.title("Conversor de PDF para Audiolivro")
        self.master.geometry('400x300')
        self.master.resizable(False, False)
        # Definir o ícone da janela (opcional)
        # self.master.iconbitmap('icone.ico')

        # Estilo personalizado
        self.estilo = ttk.Style()
        self.estilo.theme_use('clam')  # Escolhendo um tema que permite personalização

        # Configurar cores do fundo e do texto
        self.estilo.configure('.', background='black', foreground='white')
        self.estilo.configure('TButton', background='black', foreground='white', borderwidth=2, relief='raised')
        self.estilo.map('TButton',
                        background=[('active', 'gray')],
                        foreground=[('active', 'white')],
                        bordercolor=[('focus', 'white')],
                        borderwidth=[('active', 2)])

        self.estilo.configure('TLabel', background='black', foreground='white')
        self.estilo.configure('TFrame', background='black')

        # Frame principal
        self.frame_principal = ttk.Frame(master, style='TFrame')
        self.frame_principal.pack(fill='both', expand=True)

        # Título
        self.label_titulo = ttk.Label(self.frame_principal, text="Conversor de PDF para Audio", font=('Arial', 16, 'bold'))
        self.label_titulo.pack(pady=10)

        # Botão para selecionar arquivo PDF
        self.botao_selecionar = ttk.Button(self.frame_principal, text="Selecionar Arquivo PDF", command=self.selecionar_arquivo)
        self.botao_selecionar.pack(pady=10)

        # Barra de progresso
        self.estilo.configure('TProgressbar', background='white')
        self.barra_progresso = ttk.Progressbar(self.frame_principal, orient='horizontal', length=250, mode='determinate', style='TProgressbar')
        self.barra_progresso.pack(pady=10)

        # Label de status
        self.label_status = ttk.Label(self.frame_principal, text="")
        self.label_status.pack(pady=10)

    def selecionar_arquivo(self):
        caminho_arquivo = filedialog.askopenfilename(filetypes=[("Arquivos PDF", "*.pdf")])
        if caminho_arquivo:
            threading.Thread(target=self.converter_pdf_para_audio, args=(caminho_arquivo,)).start()

    def converter_pdf_para_audio(self, caminho_arquivo):
        try:
            self.label_status.config(text="Lendo o arquivo PDF...")
            with open(caminho_arquivo, 'rb') as arquivo_pdf:
                leitor_pdf = PyPDF2.PdfReader(arquivo_pdf)
                speaker = pyttsx3.init()
                texto = ""
                total_paginas = len(leitor_pdf.pages)

                for i, pagina in enumerate(leitor_pdf.pages):
                    texto += pagina.extract_text()
                    progresso = int((i+1)/total_paginas * 100)
                    self.barra_progresso['value'] = progresso
                    self.master.update_idletasks()

            self.label_status.config(text="Selecionando local para salvar o áudio...")
            caminho_audio = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("Arquivo MP3", "*.mp3")])
            if caminho_audio:
                self.label_status.config(text="Convertendo para áudio, aguarde...")
                speaker.save_to_file(texto, caminho_audio)
                speaker.runAndWait()
                speaker.stop()

                self.barra_progresso['value'] = 100
                self.label_status.config(text="Conversão concluída com sucesso!")
            else:
                self.label_status.config(text="Conversão cancelada.")
        except Exception as e:
            self.label_status.config(text=f"Ocorreu um erro: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = Aplicacao(root)
    root.mainloop()
