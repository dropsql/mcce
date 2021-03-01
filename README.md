# MCCE (Minecraft Cache Exploit) ⛏

### This little code allow you to store code on victims computer

## How does it works

```
1. VICTIM : sends SLP handshake to the fake server
2. SERVER : handle the handshake
3. SERVER : hide code into favicon
4. SERVER : sends SLP response to the victim
5. VICTIM : handle the SLP response and store the code into servers.dat
```

## Credits

* dropsql

* ⚠ the idea is base on a checksum's project (https://github.com/ecriminal/Exploit-Discord-Cache-System-PoC)

