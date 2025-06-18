import network
import time
import urequests
from machine import Pin

# ————— CONFIGURATION —————
SSID = 'saron'
PASSWORD = 'tynaarlo'
SERVER_BASE = 'http://192.168.178.33:3000/question'
BUTTON_A_PIN = 14
BUTTON_B_PIN = 15
HEALTH_INTERVAL = 20  # seconds
# ————————————————————————

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("🔌 Connecting to Wi-Fi…")
        wlan.connect(SSID, PASSWORD)
        deadline = time.time() + 15
        while not wlan.isconnected():
            if time.time() > deadline:
                raise RuntimeError("❌ Wi-Fi connection failed")
            time.sleep(1)
    print("✅ Wi-Fi up, IP:", wlan.ifconfig()[0])
    try:
        rssi = wlan.status('rssi')
        print("📶 RSSI:", rssi)
    except:
        pass
    return wlan

def ensure_wifi(wlan):
    if not wlan.isconnected():
        print("⚠️ Wi-Fi dropped. Reconnecting…")
        wlan.disconnect()
        wlan.connect(SSID, PASSWORD)
        deadline = time.time() + 15
        while not wlan.isconnected():
            if time.time() > deadline:
                print("❌ Reconnect failed")
                return False
            time.sleep(1)
        print("✅ Reconnected, IP:", wlan.ifconfig()[0])
        try:
            rssi = wlan.status('rssi')
            print("📶 RSSI:", rssi)
        except:
            pass
    return True

def robust_post(wlan, url, payload, retries=3, delay=1):
    for i in range(retries):
        try:
            r = urequests.post(url, json=payload)
            print(f"📬 POST {url} replied:", r.status_code)
            r.close()  # explicitly close the socket
            return True
        except Exception as e:
            print(f"⚠️ POST failed (try {i+1}/{retries}):", e)
            if not ensure_wifi(wlan):
                return False
            time.sleep(delay)
    return False

def robust_get(wlan, url, retries=3, delay=1):
    for i in range(retries):
        try:
            r = urequests.get(url)
            print(f"📬 GET {url} replied:", r.status_code)
            r.close()
            return True
        except Exception as e:
            print(f"⚠️ GET failed (try {i+1}/{retries}):", e)
            if not ensure_wifi(wlan):
                return False
            time.sleep(delay)
    return False

def main():
    wlan = connect_wifi()
    btn_a = Pin(BUTTON_A_PIN, Pin.IN, Pin.PULL_UP)
    btn_b = Pin(BUTTON_B_PIN, Pin.IN, Pin.PULL_UP)

    prev_a = btn_a.value()
    prev_b = btn_b.value()
    last_health = time.time()

    while True:
        # keep Wi-Fi alive
        ensure_wifi(wlan)

        now = time.time()

        # Button A pressed?
        cur_a = btn_a.value()
        if prev_a == 1 and cur_a == 0:
            url = SERVER_BASE + '/answer'
            robust_post(wlan, url, {'response': 'waar'})
        prev_a = cur_a

        # Button B pressed?
        cur_b = btn_b.value()
        if prev_b == 1 and cur_b == 0:
            url = SERVER_BASE + '/answer'
            robust_post(wlan, url, {'response': 'nietwaar'})
        prev_b = cur_b

        # Periodic health check
        if now - last_health >= HEALTH_INTERVAL:
            url = SERVER_BASE + '/health'
            robust_get(wlan, url)
            last_health = now

        time.sleep_ms(20)

if __name__ == '__main__':
    main()