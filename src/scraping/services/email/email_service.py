from contextlib import suppress
from importlib import import_module


class EmailService:

    def enviar_email(self, destinatario, assunto, corpo):
        pythoncom = import_module("pythoncom")
        dispatch_module = import_module("win32com.client")

        pythoncom.CoInitialize()

        try:
            outlook = dispatch_module.Dispatch("Outlook.Application")
            email = outlook.CreateItem(0)

            email.To = destinatario
            email.Subject = assunto
            email.Body = corpo
            email.Send()
        finally:
            with suppress(Exception):
                pythoncom.CoUninitialize()

    def enviar_email_teste(self, destinatario):
        self.enviar_email(
            destinatario=destinatario,
            assunto="Erro Automação Tentativas Score",
            corpo="Olá, o script de automação de tentativas score detectou um erro na camada de extração: A sessão do usuário foi deslogada."
            "\n\nPor favor, verifique o acesso e realize o login manualmente."
            "\n\nAtenciosamente,"
            "\nAutomações Bahia",
        )
