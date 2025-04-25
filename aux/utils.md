`nix-shell shell.nix`

# Lang Icons
https://techicons.dev/


# Tunneling
https://localhost.run/

`ssh -R 80:localhost:8000 nokey@localhost.run`

`ssh -R codecon.zanfranceschi.com.br:80:127.0.0.1:8000 plan@localhost.run`


https://one.dash.cloudflare.com/2787e018a20b0e54da22ffa4420ebc1b/networks/tunnels
`cloudflared tunnel run codecon`


# QR Code
https://qr.io/

`nix-shell -p qrencode`

`qrencode -t UTF8 https://codecon.zanfranceschi.com.br`
