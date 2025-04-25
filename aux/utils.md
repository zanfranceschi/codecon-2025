`nix-shell shell.nix`

disable control access, any host client can connect
`xhost +`

# Lang Icons
https://techicons.dev/


# Tunneling
https://localhost.run/

`ssh -R 80:localhost:8000 nokey@localhost.run`

`ssh -R codecon.zanfranceschi.com.br:80:127.0.0.1:8000 plan@localhost.run`


https://one.dash.cloudflare.com/
`cloudflared tunnel run codecon`


# QR Code
https://qr.io/

`nix-shell -p qrencode`

`qrencode -t UTF8 https://codecon.zanfranceschi.com.br`
