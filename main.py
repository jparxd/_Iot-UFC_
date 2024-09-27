import network
import time
from machine import Pin
import urequests

# Configurações da rede WiFi
SSID = "Wokwi-GUEST"
PASSWORD = ""

# Configurações do TagoIO
TAGOIO_URL = "https://api.tago.io/data"  # URL da API do TagoIO
TAGOIO_DEVICE_TOKEN = "f183a18e-4ca0-4c7a-b434-aecc4b03afa0"  # Substitua pelo seu Device Token do TagoIO

# Configurações dos pinos
PIR_PIN = 13
LED_PIN = 12
BUZZER_PIN = 14

# Inicialização dos pinos
pir = Pin(PIR_PIN, Pin.IN)
led = Pin(LED_PIN, Pin.OUT)
buzzer = Pin(BUZZER_PIN, Pin.OUT)

# Função para conectar ao WiFi
def connect_wifi():
    print("Conectando-se à rede WiFi...")
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    while not wlan.isconnected():
        time.sleep(0.5)
        print(".", end="")
    print("\nConectado ao WiFi!")
    print("Endereço IP:", wlan.ifconfig()[0])

# Função para enviar dados ao TagoIO via HTTP
def send_tagoio_data():
    print("Enviando dados ao TagoIO...")
    headers = {
        "Content-Type": "application/json",
        "Device-Token": TAGOIO_DEVICE_TOKEN  # Autenticação com o token do dispositivo
    }
    data = {
        "variable": "motion_detected",
        "value": 1,  # Valor enviado quando o movimento é detectado
        "unit": ""  # Unidade, caso seja necessário
    }
    
    try:
        response = urequests.post(TAGOIO_URL, json=data, headers=headers)
        print("Resposta do servidor:", response.text)
        response.close()
    except Exception as e:
        print("Erro ao enviar requisição:", e)

# Função para tratar a detecção de movimento
def handle_motion():
    while True:
        if pir.value() == 1:
            print("Movimento detectado!")
            send_tagoio_data()  # Enviar a requisição ao TagoIO
            led.value(1)
            buzzer.value(1)
            time.sleep(0.5)  # Ativar o LED e o buzzer por 0.5 segundos
            led.value(0)
            buzzer.value(0)
        time.sleep(0.1)

# Conectar ao WiFi
connect_wifi()

# Iniciar o monitoramento do sensor PIR
handle_motion()
