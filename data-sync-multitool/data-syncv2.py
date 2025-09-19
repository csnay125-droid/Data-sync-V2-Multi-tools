# -*- coding: utf-8 -*-
import os, sys, time, threading, socket, smtplib, requests, subprocess, hashlib, random, string, platform, psutil, shutil

class colors:
    PURPLE = '\033[95m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def clear():
    os.system('cls' if os.name=='nt' else 'clear')

def pause():
    input(f"\n{colors.PURPLE}Press Enter to return to menu...{colors.ENDC}")

def check_module(module):
    try:
        __import__(module)
        return True
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", module])
        return True

for m in ["requests","tkinter","psutil","pyfiglet","whois"]:
    check_module(m)

def loader():
    clear()
    print(f"{colors.PURPLE}{colors.BOLD}DATASYNC V2{colors.ENDC}")
    print(f"{colors.PURPLE}Initializing Data Sync v2...{colors.ENDC}")
    for i in range(0, 101, 5):
        sys.stdout.write(f"\r[{colors.PURPLE}{i}%{colors.ENDC}] Loading...")
        sys.stdout.flush()
        time.sleep(0.03)
    print("\n")

def port_scanner():
    clear()
    print(f"{colors.PURPLE}{colors.BOLD}PORT SCANNER{colors.ENDC}")
    host = input("Enter host/IP: ")
    try:
        start_port = int(input("Start port: "))
        end_port = int(input("End port: "))
    except:
        print(f"{colors.PURPLE}Invalid port numbers!{colors.ENDC}")
        pause()
        return
    print(f"{colors.PURPLE}Scanning ports on {host}...{colors.ENDC}")
    open_ports = []
    def scan(port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        if s.connect_ex((host, port)) == 0:
            open_ports.append(port)
            print(f"{colors.PURPLE}[OPEN] Port {port}{colors.ENDC}")
        s.close()
    threads = []
    for port in range(start_port, end_port+1):
        t = threading.Thread(target=scan, args=(port,))
        threads.append(t)
        t.start()
    for t in threads: t.join()
    print(f"\nOpen ports: {open_ports}")
    with open("port_scan_results.txt","w") as f:
        for p in open_ports: f.write(f"{p}\n")
    print(f"{colors.PURPLE}Results saved to port_scan_results.txt{colors.ENDC}")
    pause()

def ip_lookup():
    clear()
    print(f"{colors.PURPLE}{colors.BOLD}IP LOOKUP & GEOLOCATION{colors.ENDC}")
    ip = input("Enter IP: ")
    try:
        res = requests.get(f"http://ip-api.com/json/{ip}").json()
        if res["status"] != "success":
            print(f"{colors.PURPLE}Error: {res.get('message','Unknown')}{colors.ENDC}")
            pause()
            return
        for k,v in res.items():
            print(f"{colors.PURPLE}{k}:{colors.ENDC} {v}")
        with open("ip_lookup_results.txt","w") as f:
            for k,v in res.items():
                f.write(f"{k}: {v}\n")
        print(f"{colors.PURPLE}Results saved to ip_lookup_results.txt{colors.ENDC}")
    except Exception as e:
        print(f"{colors.PURPLE}Error: {e}{colors.ENDC}")
    pause()

def mail_spammer():
    clear()
    print(f"{colors.PURPLE}{colors.BOLD}MAIL SPAMMER{colors.ENDC}")
    sender = input("Sender Email: ")
    password = input("Password: ")
    recipient = input("Recipient Email: ")
    subject = input("Subject: ")
    message = input("Message: ")
    try:
        count = int(input("Number of emails: "))
    except:
        print(f"{colors.PURPLE}Invalid number!{colors.ENDC}")
        pause()
        return
    try:
        server = smtplib.SMTP("smtp.gmail.com",587)
        server.starttls()
        server.login(sender,password)
        full_msg = f"Subject: {subject}\n\n{message}"
        for i in range(count):
            server.sendmail(sender,recipient,full_msg)
            print(f"{colors.PURPLE}Sent {i+1}/{count}{colors.ENDC}", end="\r")
        server.quit()
        print(f"\n{colors.PURPLE}Emails sent!{colors.ENDC}")
    except Exception as e:
        print(f"{colors.PURPLE}Error: {e}{colors.ENDC}")
    pause()

def discord_webhook():
    clear()
    print(f"{colors.PURPLE}{colors.BOLD}DISCORD WEBHOOK SPAMMER{colors.ENDC}")
    url = input("Webhook URL: ")
    msg = input("Message: ")
    print(f"{colors.PURPLE}Press 'E' to send message repeatedly, 'Q' to quit.{colors.ENDC}")
    try:
        while True:
            key = input().upper()
            if key == "Q": break
            elif key == "E":
                res = requests.post(url, data={"content": msg})
                if res.status_code == 204:
                    print(f"{colors.PURPLE}Message sent!{colors.ENDC}")
                else:
                    print(f"{colors.PURPLE}Failed! Status code: {res.status_code}{colors.ENDC}")
    except Exception as e:
        print(f"{colors.PURPLE}Error: {e}{colors.ENDC}")
    pause()

def subnet_scanner():
    clear(); print(f"{colors.PURPLE}Subnet Scanner (Ping all IPs in subnet){colors.ENDC}")
    subnet = input("Enter subnet (e.g., 192.168.1): ")
    active = []
    for i in range(1,255):
        ip = f"{subnet}.{i}"
        response = os.system(f"ping -n 1 -w 100 {ip} >nul" if os.name=='nt' else f"ping -c 1 -W 1 {ip} > /dev/null")
        if response == 0: active.append(ip)
    print(f"{colors.PURPLE}Active IPs: {active}{colors.ENDC}")
    pause()

def whois_lookup():
    clear()
    print(f"{colors.PURPLE}Whois Lookup{colors.ENDC}")
    domain = input("Enter domain: ")
    try:
        import whois
    except:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "python-whois"])
        import whois
    try:
        data = whois.whois(domain)
        print(f"{colors.PURPLE}{data}{colors.ENDC}")
    except Exception as e:
        print(f"{colors.PURPLE}Error: {e}{colors.ENDC}")
    pause()

def traceroute():
    clear()
    host = input("Enter host/IP: ")
    print(f"{colors.PURPLE}Traceroute to {host}:{colors.ENDC}")
    cmd = "tracert" if os.name=='nt' else "traceroute"
    os.system(f"{cmd} {host}")
    pause()

def password_generator():
    clear()
    length = int(input("Password length: "))
    chars = string.ascii_letters + string.digits + string.punctuation
    pw = ''.join(random.choice(chars) for _ in range(length))
    print(f"{colors.PURPLE}Generated password: {pw}{colors.ENDC}")
    pause()

def brute_force_tester():
    clear()
    print(f"{colors.PURPLE}Brute Force Password Tester (local test){colors.ENDC}")
    target = input("Enter password to test: ")
    chars = string.ascii_letters + string.digits
    attempts = 0
    found = False
    print(f"{colors.PURPLE}Testing passwords...{colors.ENDC}")
    while not found:
        guess = ''.join(random.choice(chars) for _ in range(len(target)))
        attempts += 1
        if guess == target: found = True
    print(f"{colors.PURPLE}Password cracked: {guess} in {attempts} attempts{colors.ENDC}")
    pause()

def hash_generator():
    clear()
    text = input("Text to hash: ")
    md5 = hashlib.md5(text.encode()).hexdigest()
    sha256 = hashlib.sha256(text.encode()).hexdigest()
    print(f"{colors.PURPLE}MD5: {md5}\nSHA256: {sha256}{colors.ENDC}")
    pause()

def system_info():
    clear()
    print(f"{colors.PURPLE}System Information:{colors.ENDC}")
    print(f"{colors.PURPLE}OS: {platform.system()} {platform.release()}{colors.ENDC}")
    print(f"{colors.PURPLE}CPU: {platform.processor()}{colors.ENDC}")
    print(f"{colors.PURPLE}RAM: {round(psutil.virtual_memory().total/1e9,2)} GB{colors.ENDC}")
    pause()

def process_killer():
    clear()
    pid = int(input("Enter PID to kill: "))
    try:
        p = psutil.Process(pid)
        p.terminate()
        print(f"{colors.PURPLE}Process {pid} terminated{colors.ENDC}")
    except Exception as e:
        print(f"{colors.PURPLE}Error: {e}{colors.ENDC}")
    pause()

def disk_usage():
    clear()
    usage = shutil.disk_usage("/")
    print(f"{colors.PURPLE}Total: {usage.total//(2**30)} GB, Used: {usage.used//(2**30)} GB, Free: {usage.free//(2**30)} GB{colors.ENDC}")
    pause()

def http_header_grabber():
    clear()
    url = input("Enter URL: ")
    try:
        res = requests.head(url)
        for k,v in res.headers.items():
            print(f"{colors.PURPLE}{k}: {v}{colors.ENDC}")
    except Exception as e:
        print(f"{colors.PURPLE}Error: {e}{colors.ENDC}")
    pause()

def url_shortener():
    clear()
    url = input("Enter URL to shorten: ")
    try:
        res = requests.get(f"https://tinyurl.com/api-create.php?url={url}").text
        print(f"{colors.PURPLE}Shortened URL: {res}{colors.ENDC}")
    except Exception as e:
        print(f"{colors.PURPLE}Error: {e}{colors.ENDC}")
    pause()

def weather_checker():
    clear()
    city = input("Enter city: ")
    api = "http://api.openweathermap.org/data/2.5/weather?q={}&appid=YOUR_API_KEY&units=metric"
    try:
        res = requests.get(api.format(city)).json()
        print(f"{colors.PURPLE}Weather in {city}: {res['weather'][0]['description']}, Temp: {res['main']['temp']}°C{colors.ENDC}")
    except:
        print(f"{colors.PURPLE}Check your API key or city name.{colors.ENDC}")
    pause()

def ascii_art_generator():
    clear()
    text = input("Text to ASCII: ")
    try:
        import pyfiglet
    except:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyfiglet"])
        import pyfiglet
    print(f"{colors.PURPLE}{pyfiglet.figlet_format(text)}{colors.ENDC}")
    pause()

def random_joke():
    clear()
    try:
        res = requests.get("https://v2.jokeapi.dev/joke/Any").json()
        if res["type"]=="single": print(f"{colors.PURPLE}{res['joke']}{colors.ENDC}")
        else: print(f"{colors.PURPLE}{res['setup']} ... {res['delivery']}{colors.ENDC}")
    except:
        print(f"{colors.PURPLE}Failed to fetch joke.{colors.ENDC}")
    pause()

def file_encrypt_decrypt():
    clear()
    mode = input("Encrypt (E) or Decrypt (D): ").upper()
    path = input("File path: ")
    key = 5
    try:
        with open(path,"rb") as f: data = f.read()
        if mode=="E": data = bytearray([b+key for b in data])
        else: data = bytearray([b-key for b in data])
        with open(path,"wb") as f: f.write(data)
        print(f"{colors.PURPLE}Operation complete!{colors.ENDC}")
    except:
        print(f"{colors.PURPLE}Error processing file.{colors.ENDC}")
    pause()

def network_tools_menu():
    while True:
        clear()
        print(f"{colors.PURPLE}{colors.BOLD}NETWORK & RECON TOOLS{colors.ENDC}")
        print(f"{colors.PURPLE}1. Subnet Scanner\n2. Whois Lookup\n3. Traceroute\n4. Return{colors.ENDC}")
        choice = input("Option: ")
        if choice=="1": subnet_scanner()
        elif choice=="2": whois_lookup()
        elif choice=="3": traceroute()
        elif choice=="4": break

def password_tools_menu():
    while True:
        clear()
        print(f"{colors.PURPLE}{colors.BOLD}PASSWORD & SECURITY TOOLS{colors.ENDC}")
        print(f"{colors.PURPLE}1. Password Generator\n2. Brute Force Tester\n3. Hash Generator\n4. Return{colors.ENDC}")
        choice = input("Option: ")
        if choice=="1": password_generator()
        elif choice=="2": brute_force_tester()
        elif choice=="3": hash_generator()
        elif choice=="4": break

def system_tools_menu():
    while True:
        clear()
        print(f"{colors.PURPLE}{colors.BOLD}SYSTEM & INFO TOOLS{colors.ENDC}")
        print(f"{colors.PURPLE}1. System Info\n2. Process Killer\n3. Disk Usage Analyzer\n4. Return{colors.ENDC}")
        choice = input("Option: ")
        if choice=="1": system_info()
        elif choice=="2": process_killer()
        elif choice=="3": disk_usage()
        elif choice=="4": break

def web_tools_menu():
    while True:
        clear()
        print(f"{colors.PURPLE}{colors.BOLD}WEB & API TOOLS{colors.ENDC}")
        print(f"{colors.PURPLE}1. HTTP Header Grabber\n2. URL Shortener / Expander\n3. Weather Checker\n4. Return{colors.ENDC}")
        choice = input("Option: ")
        if choice=="1": http_header_grabber()
        elif choice=="2": url_shortener()
        elif choice=="3": weather_checker()
        elif choice=="4": break

def fun_tools_menu():
    while True:
        clear()
        print(f"{colors.PURPLE}{colors.BOLD}FUN & MISC TOOLS{colors.ENDC}")
        print(f"{colors.PURPLE}1. ASCII Art Generator\n2. Random Joke / Quote\n3. File Encrypt / Decrypt\n4. Return{colors.ENDC}")
        choice = input("Option: ")
        if choice=="1": ascii_art_generator()
        elif choice=="2": random_joke()
        elif choice=="3": file_encrypt_decrypt()
        elif choice=="4": break

def main_menu():
    while True:
        clear()
        print(f"{colors.PURPLE}{colors.BOLD}=== DATASYNC V2 ==={colors.ENDC}")
        print(f"{colors.PURPLE}1. Port Scanner\n2. IP Lookup + Geolocation\n3. Mail Spammer\n4. Discord Webhook Spammer\n5. Network & Recon Tools\n6. Password & Security Tools\n7. System & Info Tools\n8. Web & API Tools\n9. Fun & Misc Tools\n10. Exit{colors.ENDC}")
        choice = input("Option: ")
        if choice=="1": port_scanner()
        elif choice=="2": ip_lookup()
        elif choice=="3": mail_spammer()
        elif choice=="4": discord_webhook()
        elif choice=="5": network_tools_menu()
        elif choice=="6": password_tools_menu()
        elif choice=="7": system_tools_menu()
        elif choice=="8": web_tools_menu()
        elif choice=="9": fun_tools_menu()
        elif choice=="10": sys.exit()
        else:
            print(f"{colors.PURPLE}Invalid option!{colors.ENDC}")
            time.sleep(1)

if __name__=="__main__":
    loader()
    main_menu()
