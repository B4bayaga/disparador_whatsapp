from boot_respostas import BootResposta
from time import sleep

boot = BootResposta()
boot.driver.get("https://web.whatsapp.com/")
boot.espera_login()


def Boot():
    try:
        boot.clica_bolinha()
        numero = boot.captura_numero_telefone()
        mensagem = boot.ler_mensagens_recebidas()
        print(numero, mensagem)
        sleep(1)
        boot.envia_mensagem("Olá, eu sou um boot!")
        sleep(1)
        boot.fecha_janela_mensagem()
    except:
        print("Ainda aguardado mensagem...")
        sleep(1)


while True:
    Boot()
