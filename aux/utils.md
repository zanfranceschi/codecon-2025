### run pygame locally
`nix-shell shell.nix`

### X11 - disable control access, any host client can connect
`xhost +`

### Tunneling
https://one.dash.cloudflare.com/
`cloudflared tunnel run codecon`

not used ↓
https://localhost.run/
`ssh -R 80:localhost:8000 nokey@localhost.run`
`ssh -R codecon.zanfranceschi.com.br:80:127.0.0.1:8000 plan@localhost.run`

### QR Code
https://qr.io/

`nix-shell -p qrencode`

`qrencode -t UTF8 https://codecon.zanfranceschi.com.br`


### Lang Icons
https://techicons.dev/
