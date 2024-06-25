# Projekt TIP - Zarządzanie siecią hybrydową
## Wstęp
Celem projektu było przygotowanie sieci składającej się z części wirtualnej oraz części sprzętowej, a także zademonstrowanie w jaki sposób można wykorzystać zarządzanie programowe w takim środowisku.
Do zrealizowania celu wybrano technologię [Kathará](https://www.kathara.org/). Jest to narzędzie służące do tworzenia zwirtualizowanych sieci.
Do realizacji części sprzętowej wykorzystano switch L2 Cisco 2950.
## Środowisko
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
username X password Y
enable secret X-Y
exit
copy run start
```
#### Konfiguracja części wirtualnej
## Wnioski i napotkane problemy
## Źródła
[Kathará - github](https://github.com/KatharaFramework/Kathara)
[Kathará - przykłady](https://github.com/KatharaFramework/Kathara-Labs)
