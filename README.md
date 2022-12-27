# Edge-Core switches automation via telnet (Device Telnet Tools)
## Quick examples

Get current version of switch:
```
# python3 ec_getversion.py 192.168.101.1
# python3 ec_getversion.py "192.168.101.1 192.168.101.3 192.168.101.4 192.168.101.20"
```

Update firmware:
```
python3 ec_update.py 192.168.101.1 /ec/3528mv2/ es3528mv2_1.5.2.17.bix
python3 ec_update.py "192.168.101.1 192.168.101.3 192.168.101.4 192.168.101.20" 10.25.17.2 /ec/3528mv2/ es3528mv2_1.5.2.17.bix
```

