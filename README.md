# Projekt TIP - Zarządzanie siecią hybrydową
#### *Tobiasz Szulc - Nikodem Oleniacz - Michał Szewc*
## Wstęp
Celem projektu było przygotowanie sieci składającej się z części wirtualnej oraz części sprzętowej, a także zademonstrowanie w jaki sposób można wykorzystać zarządzanie programowe w takim środowisku.
Do zrealizowania celu wybrano technologię [Kathará](https://www.kathara.org/). Jest to narzędzie służące do tworzenia zwirtualizowanych sieci, wykorzystujące linuxowe kontenery dockerowe.
Do realizacji części sprzętowej wykorzystano switch L2 Cisco 2950.
## Środowisko
#### Schemat:
![image](./images/architecture_diagram_light.png#gh-light-mode-only)
![image](./images/architecture_diagram_dark.png#gh-dark-mode-only)

Komunikacja między komputerem a switchem przechodzi przez port 24 vlan 100. Wszystkie wirtualne sieci przechodzą przez trunk.
## Jak zreplikować
#### Konfiguracja switcha
```bash
enable
config t
vlan 100
exit
int range fa0/1 - 10
switchport access vlan 100
switchport mode access
exit
interface fa0/24
switchport mode trunk
interface vlan 100
ip address 10.100.0.1 255.255.255.0
no shutdown
exit
line vty 0 4
transport input telnet
login local
exit
username Q password BA
enable secret Q-BA
exit
copy run start
```
Switch należy podłączyć do komputera na porcie 24.
Na komputerze należy dodać interfejs vlanu 100 dodanego do odpowiedniego interfejsu fizycznego i nadać mu adres IP.
Uwaga: należy podstawić odpowiednią nazwę interfejsu.
```
sudo ip link add link enp3s0 name enp3s0.100 type vlan id 100
sudo ip addr add 10.100.0.2/24 dev enp3s0.100
```
#### Przygotowanie środowiska
1. [Instalacja Dockera](https://docs.docker.com/engine/install/)
2. [Instalacja Kathary](https://github.com/KatharaFramework/Kathara/wiki/Linux?fbclid=IwZXh0bgNhZW0CMTAAAR35LvcFxyMJ0MfLR0GGqlDhiOrKGSJKdCP6XbczOfalIP8QpHiyP_wWje0_aem_U0aDp5UPpKc-KBYvvxhOsQ), na systemie Linux, w wersji 3.7.5.
3. Przestawienie Kathary na starszą wersję pluginu sieciowego.
  ```bash
  kathara settings
    ╔═════════════════════════════════════════════════════════════════════════╗
    ║                                                                         ║
    ║                            Kathara Settings                             ║
    ║                                                                         ║
    ╠═════════════════════════════════════════════════════════════════════════╣
    ║                                                                         ║
    ║                      Choose the option to change.                       ║
    ║                                                                         ║
    ╠═════════════════════════════════════════════════════════════════════════╣
    ║                                                                         ║
    ║    1 - Choose default manager                                           ║
    ║    2 - Choose default image                                             ║
    ║    3 - Automatically open terminals on startup                          ║
    ║    4 - Choose device shell to be used                                   ║
    ║    5 - Choose terminal emulator to be used                              ║
    ║    6 - Choose Kathara prefixes                                          ║
    ║    7 - Choose logging level to be used                                  ║
    ║    8 - Print Startup Logs on device startup                             ║
    ║    9 - Enable IPv6                                                      ║
    ║   10 - Choose Docker Network Plugin version                             ║
    ║   11 - Automatically mount /hosthome on startup                         ║
    ║   12 - Automatically mount /shared on startup                           ║
    ║   13 - Docker Image Update Policy                                       ║
    ║   14 - Enable Shared Collision Domains                                  ║
    ║   15 - Configure a remote Docker connection                             ║
    ║   16 - Exit                                                             ║
    ║                                                                         ║
    ║                                                                         ║
    ╚═════════════════════════════════════════════════════════════════════════╝
  >> 10
  ```
  Wybieramy opcję 10
  ```
    ╔═════════════════════════════════════════════════════════════════════════╗
    ║                                                                         ║
    ║                  Choose Docker Network Plugin version                   ║
    ║                                                                         ║
    ║                     Current: kathara/katharanp_vde                      ║
    ║                                                                         ║
    ╠═════════════════════════════════════════════════════════════════════════╣
    ║                                                                         ║
    ║       Choose Docker Network Plugin version for collision domains.       ║
    ║          kathara/katharanp plugin is based on Linux bridges.            ║
    ║        kathara/katharanp_vde plugin is based on VDE switches.           ║
    ║                   Default is kathara/katharanp_vde.                     ║
    ║                                                                         ║
    ╠═════════════════════════════════════════════════════════════════════════╣
    ║                                                                         ║
    ║    1 - kathara/katharanp                                                ║
    ║    2 - kathara/katharanp_vde                                            ║
    ║    3 - Return to Kathara Settings                                       ║
    ║                                                                         ║
    ║                                                                         ║
    ╚═════════════════════════════════════════════════════════════════════════╝
  >> 1
  ```
  Wybieramy opcję 1

4. Instalacja Netmiko
   + Instalacja Pythona 3.11.9
   + Utworzenie wirtualnego środowiska pythona: ```python -m venv venv```
   + Aktywacja wirtualnego środowiska: ```source venv/bin/activate```
   + Instalacja paczek: ```pip install -r requirements.txt```
#### Konfiguracja części wirtualnej
Wyświetlenie informacji o interfejsach:
```
$ ip link
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
2: enp3s0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc fq_codel state DOWN mode DEFAULT group default qlen 1000
    link/ether 8c:16:45:66:3a:6b brd ff:ff:ff:ff:ff:ff
3: wlp2s0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP mode DORMANT group default qlen 1000
    link/ether 7c:76:35:88:0c:0c brd ff:ff:ff:ff:ff:ff
4: enp3s0.100@enp3s0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state LOWERLAYERDOWN mode DEFAULT group default qlen 1000
    link/ether 8c:16:45:66:3a:6b brd ff:ff:ff:ff:ff:ff
5: docker0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN mode DEFAULT group default 
    link/ether 02:42:b1:05:cb:38 brd ff:ff:ff:ff:ff:ff
```
Z podanych interfejsów wybieramy ten na którym mają być utworzone vlany i podpięte do wirtualnych domen kolizyjnych.
Tutaj został wybrany interfejs enp3s0.

W pliku scenario/lab.ext należy ustawić nazwę interfejsu:
```
A <interface name>.10
B <interface name>.20
C <interface name>.30
D <interface name>.40
E <interface name>.50

->

A enp3s0.10
B enp3s0.20
C enp3s0.30
D enp3s0.40
E enp3s0.50
```
#### Uruchomienie środwiska
1. ```cd scenario```
2. Uruchomienie Kathary: ```sudo kathara lstart```
3. ```cd ..```
4. Uruchomienie Netmiko: ```./venv/bin/python lab.py```
#### Zatrzymanie środowiska
- Zatrzymanie Kathary: ```sudo kathara lclean```
- Skrypt Netmiko nie wprowadza trwałych zmian, można wrócić do stanu bazowego restartując switch.
## Napotkane problemy i wnioski
#### Problemy:
+ Główny napotkany problem to konieczność zmiany pluginu sieciowego na starszą wersję.
  Przyczyna: nowszy plugin *katharanp_vde* powodował błędy, gdy zdefiniowany był więcej niż jeden ExternalLink.
  Po zmianie na *katharanp*, problem zniknął.
+ Python api do Kathary nie działa zbyt dobrze z ExternalLink-ami. Pojawiają się błędy przy deploy-u oraz undeploy-u.
#### Wnioski
Kathará jest ciekawym narzędziem które ma potencjał, ale ma swoje problemy - ciągle jest rozwijane.
Jest ona wstecznie kompatybilna z Netkitem, istnieje duża pula gotowych scenariuszy, które można zaadaptować.
Dostępne jest także wiele tutoriali, które ułatwiają naukę korzystania z narzędzia.
## Źródła
[Kathará - github](https://github.com/KatharaFramework/Kathara)
[Kathará - przykłady](https://github.com/KatharaFramework/Kathara-Labs)
