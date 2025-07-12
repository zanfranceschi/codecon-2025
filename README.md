# Codecon Summit 2025

## Instruções para Rodar o Jogo

### 1. Tunnel
Start tunnel.
```shell 
cloudflared tunnel run codecon
```
[one dashboard](https://one.dash.cloudflare.com/)


### 2. X11
Disable control access, any host client can connect.
```shell
xhost +
```

### 3. Docker
Start [docker compose](./containerization/docker-compose.yml).
```shell
docker compose up
```


### Gerar QR Code
https://qr.io/

```shell
nix-shell -p qrencode --run "qrencode -t UTF8 https://codecon.zanfranceschi.com.br"
```
