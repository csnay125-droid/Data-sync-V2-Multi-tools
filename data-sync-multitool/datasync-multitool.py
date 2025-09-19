# -*- coding: utf-8 -*-
import os
import sys
import time
import threading
import socket
import smtplib
import requests
import subprocess
import hashlib
import random
import string
import platform
import psutil
import shutil
import queue

# Auto-install helper
def check_module(module, pip_name=None):
    try:
        __import__(module)
        return True
    except ImportError:
        if pip_name is None:
            pip_name = module
        subprocess.check_call([sys.executable, "-m", "pip", "install", pip_name])
        return True

# Ensure visual libs
check_module("pyfiglet")
check_module("rich")
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt
from rich.table import Table
import pyfiglet

console = Console()

# Helpers d'affichage
def big_title(text):
    fig = pyfiglet.figlet_format(text, font="slant")
    console.print(f"[magenta]{fig}[/magenta]")

def section_title(text):
    console.print(Panel(Text(text, justify="center", style="bold magenta"), expand=False))

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def pause():
    console.print("\n[magenta]Appuyez sur Entrée pour revenir au menu...[/magenta]")
    try:
        input()
    except KeyboardInterrupt:
        pass

def loader():
    clear()
    big_title("DATASYNC V2")
    console.print("[bold magenta]Initialisation de Data Sync v2...[/bold magenta]\n")
    with console.status("[magenta]Chargement...[/magenta]", spinner="dots"):
        for i in range(0, 101, 5):
            console.print(f"[magenta][{i}%] [/magenta]", end="\r")
            time.sleep(0.03)
    console.print("\n")

# --- Fonctions réseau / utilitaires (inchangées, affichage amélioré) ---
def port_scanner():
    clear()
    section_title("PORT SCANNER")
    host = Prompt.ask("Hôte/IP")
    try:
        start_port = int(Prompt.ask("Port de départ"))
        end_port = int(Prompt.ask("Port de fin"))
    except Exception:
        console.print("[magenta]Numéros de port invalides ![/magenta]")
        pause()
        return
    console.print(f"[magenta]Scan des ports sur {host}...[/magenta]")
    open_ports = []
    def scan(port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        try:
            if s.connect_ex((host, port)) == 0:
                open_ports.append(port)
                console.print(f"[magenta][OPEN] Port {port}[/magenta]")
        except Exception:
            pass
        finally:
            s.close()
    threads = []
    for port in range(start_port, end_port+1):
        t = threading.Thread(target=scan, args=(port,))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    console.print(f"\n[magenta]Ports ouverts: {open_ports}[/magenta]")
    with open("port_scan_results.txt", "w") as f:
        for p in open_ports:
            f.write(f"{p}\n")
    console.print("[magenta]Résultats sauvegardés dans port_scan_results.txt[/magenta]")
    pause()

def ip_lookup():
    clear()
    section_title("IP LOOKUP & GEOLOCATION")
    ip = Prompt.ask("Entrer l'IP")
    try:
        res = requests.get(f"http://ip-api.com/json/{ip}", timeout=5).json()
        if res.get("status") != "success":
            console.print(f"[magenta]Erreur: {res.get('message','Inconnu')}[/magenta]")
            pause()
            return
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Clé")
        table.add_column("Valeur")
        for k, v in res.items():
            table.add_row(str(k), str(v))
        console.print(table)
        with open("ip_lookup_results.txt", "w", encoding="utf-8") as f:
            for k, v in res.items():
                f.write(f"{k}: {v}\n")
        console.print("[magenta]Résultats sauvegardés dans ip_lookup_results.txt[/magenta]")
    except Exception as e:
        console.print(f"[magenta]Erreur: {e}[/magenta]")
    pause()

def mail_spammer():
    clear()
    section_title("MAIL SPAMMER")
    sender = Prompt.ask("Email expéditeur")
    password = Prompt.ask("Mot de passe", password=True)
    recipient = Prompt.ask("Email destinataire")
    subject = Prompt.ask("Sujet")
    message = Prompt.ask("Message")
    try:
        count = int(Prompt.ask("Nombre d'emails"))
    except:
        console.print("[magenta]Nombre invalide ![/magenta]")
        pause()
        return
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587, timeout=10)
        server.starttls()
        server.login(sender, password)
        full_msg = f"Subject: {subject}\n\n{message}"
        for i in range(count):
            server.sendmail(sender, recipient, full_msg)
            console.print(f"[magenta]Envoyé {i+1}/{count}[/magenta]", end="\r")
        server.quit()
        console.print("\n[magenta]Emails envoyés ![/magenta]")
    except Exception as e:
        console.print(f"[magenta]Erreur: {e}[/magenta]")
    pause()

def discord_webhook():
    clear()
    section_title("DISCORD WEBHOOK SPAMMER")
    url = Prompt.ask("URL Webhook")
    msg = Prompt.ask("Message")
    console.print("[magenta]Appuyez sur 'E' pour envoyer, 'Q' pour quitter.[/magenta]")
    try:
        while True:
            key = Prompt.ask("Choix").upper()
            if key == "Q":
                break
            elif key == "E":
                try:
                    res = requests.post(url, data={"content": msg}, timeout=5)
                    if res.status_code in (200, 204):
                        console.print("[magenta]Message envoyé ![/magenta]")
                    else:
                        console.print(f"[magenta]Échec ! Code: {res.status_code}[/magenta]")
                except Exception as e:
                    console.print(f"[magenta]Erreur: {e}[/magenta]")
    except Exception as e:
        console.print(f"[magenta]Erreur: {e}[/magenta]")
    pause()

def subnet_scanner():
    clear()
    section_title("Subnet Scanner")
    subnet = Prompt.ask("Entrer le subnet (ex: 192.168.1)")
    active = []
    for i in range(1, 255):
        ip = f"{subnet}.{i}"
        cmd = f"ping -n 1 -w 100 {ip} >nul" if os.name == 'nt' else f"ping -c 1 -W 1 {ip} > /dev/null"
        response = os.system(cmd)
        if response == 0:
            active.append(ip)
    console.print(f"[magenta]IPs actives: {active}[/magenta]")
    pause()

def whois_lookup():
    clear()
    section_title("Whois Lookup")
    domain = Prompt.ask("Domaine")
    try:
        check_module("whois", "python-whois")
        import whois
        data = whois.whois(domain)
        console.print(Panel(str(data), title=f"[magenta]{domain}[/magenta]"))
    except Exception as e:
        console.print(f"[magenta]Erreur: {e}[/magenta]")
    pause()

def traceroute():
    clear()
    host = Prompt.ask("Hôte/IP")
    section_title(f"Traceroute -> {host}")
    cmd = "tracert" if os.name == 'nt' else "traceroute"
    os.system(f"{cmd} {host}")
    pause()

def password_generator():
    clear()
    section_title("Password Generator")
    try:
        length = int(Prompt.ask("Longueur du mot de passe"))
    except:
        console.print("[magenta]Longueur invalide ![/magenta]")
        pause(); return
    chars = string.ascii_letters + string.digits + string.punctuation
    pw = ''.join(random.choice(chars) for _ in range(length))
    console.print(Panel(Text(pw, style="bold magenta"), title="[magenta]Mot de passe généré[/magenta]"))
    pause()

# --- Nouvelle option: brute-force multithreaded complet ---
def full_brute_force():
    clear()
    section_title("Full Brute Force Password Tester (Local & Legal)")
    target = Prompt.ask("Mot de passe à tester (test local uniquement)")
    chars = string.ascii_letters + string.digits + string.punctuation
    q = queue.Queue()
    found = threading.Event()
    max_threads = 10

    def generate_combinations(length):
        for comb in map(''.join, __import__('itertools').product(chars, repeat=length)):
            if found.is_set():
                break
            q.put(comb)

    def worker():
        while not found.is_set():
            try:
                guess = q.get(timeout=1)
            except queue.Empty:
                break
            if guess == target:
                found.set()
                console.print(f"\n[magenta]Mot de passe trouvé: {guess}[/magenta]")
            q.task_done()

    start = time.time()
    threads = []
    for length in range(1, len(target)+1):
        t_gen = threading.Thread(target=generate_combinations, args=(length,))
        t_gen.start()
        for _ in range(max_threads):
            t = threading.Thread(target=worker)
            t.start()
            threads.append(t)
        t_gen.join()
        q.join()
    for t in threads:
        t.join()
    console.print(f"[magenta]Temps écoulé: {round(time.time() - start, 2)}s[/magenta]")
    pause()

def hash_generator():
    clear()
    section_title("Hash Generator")
    text = Prompt.ask("Texte à hasher")
    md5 = hashlib.md5(text.encode()).hexdigest()
    sha256 = hashlib.sha256(text.encode()).hexdigest()
    console.print(Panel(f"MD5: {md5}\nSHA256: {sha256}", title="[magenta]Résultats[/magenta]"))
    pause()

# --- Menus mis à jour ---
def password_tools_menu():
    while True:
        clear()
        section_title("PASSWORD & SECURITY TOOLS")
        console.print("[magenta]1. Générateur de mdp   2. Full Brute Force Tester   3. Générateur de hash   4. Retour[/magenta]")
        choice = Prompt.ask("Option")
        if choice == "1":
            password_generator()
        elif choice == "2":
            full_brute_force()
        elif choice == "3":
            hash_generator()
        elif choice == "4":
            break

# --- Le reste du script reste inchangé ---
# system_tools_menu, web_tools_menu, fun_tools_menu, main_menu etc.

# --- MAIN MENU ---
def main_menu():
    while True:
        clear()
        big_title("DATASYNC V2")
        console.print(Panel(Text("1.Port Scanner  2.IP Lookup  3.Mail Spammer  4.Discord Webhook\n5.Network Tools  6.Password Tools  7.System Tools\n8.Web Tools  9.Fun Tools  10.Exit", justify="center"), title="[magenta]MENU[/magenta]"))
        choice = Prompt.ask("Option")
        if choice == "1": port_scanner()
        elif choice == "2": ip_lookup()
        elif choice == "3": mail_spammer()
        elif choice == "4": discord_webhook()
        elif choice == "5": network_tools_menu()
        elif choice == "6": password_tools_menu()
        elif choice == "7": system_tools_menu()
        elif choice == "8": web_tools_menu()
        elif choice == "9": fun_tools_menu()
        elif choice == "10":
            console.print("[magenta]Au revoir ![/magenta]")
            sys.exit()
        else:
            console.print("[magenta]Option invalide ![/magenta]")
            time.sleep(1)

if __name__ == "__main__":
    loader()
    main_menu()
