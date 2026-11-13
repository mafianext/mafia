**English** | [Русский](README.ru.md)

# MafiaNext — Telegram bot + web game

The party game Mafia in two forms that share one database:

- **@MafiaNextBot** — the Telegram bot (`mafia_bot.py`).
- **MafiaNext Web** — the same game on a website, for people who play from a computer (or phone) and may not have Telegram. Everyone plays from their own device: secret roles, night moves, voting and tie duels happen on each player's screen. The host runs the game from theirs (`web_server.py` + `web/index.html`).

The web server imports the bot's own code, so the rules, roles, night order, stories and points are identical. Rooms and games on the site and in Telegram are separate.

**Accounts.** On the site people log in with a username and password, or play as a guest. Someone who also plays in the bot sends `/web` to the bot, enters the code on the site, and gets **one account** with one nickname, one points total and one history for both.

## Files

| File | Purpose |
|---|---|
| `mafia_bot.py`, `texts.py` | The bot and all texts (six languages). Includes the `/web` command that sends website codes. The web version reuses both |
| `web_server.py` | Web game server: rooms, game flow, logins, WebSocket updates |
| `web/index.html` | The multiplayer web app (served by `web_server.py`) |
| `web/offline.html` | One-phone "host mode" version, works without a server |
| `deploy/mafiaweb.service` | systemd service for the web server |
| `deploy/Caddyfile` | HTTPS proxy config (Caddy gets the certificate automatically) |
| `.github/workflows/deploy.yml` | Auto-deploy: every push to `main` updates the server |
| `requirements.txt` | Python packages |
| `.env`, `mafia.db` | Secrets and data. **Only on the server, never in Git** |

## How the web game works

- **Login:** username and password, or guest (just a nickname; it lives in that browser and can be saved later with a username and password in the profile).
- **"I have Telegram":** send `/web` to the bot, enter the 6-digit code on the site (valid 10 minutes, works once), choose a username and password. The same code later resets a forgotten password. A site account can also be linked from the profile: its history moves into the Telegram account.
- **Admin** (only the owner, `HOST_ID`, after linking their Telegram): find accounts and reset a password to a temporary one.
- **Leaderboard:** everyone who has played on the site, with points from all their games.
- **Layout:** two columns on a computer screen (actions on the left, story, players and line-up on the right), one column on phones.
- **Rooms:** create a room and share the invite link (`https://your-domain/?room=3`). The creator becomes the host.
- **Host** settings are the same as in the bot (and shared with it), plus one web-only setting:
  - **Night moves:** *via host* (classic: players gesture, the host enters choices) or *from own devices* (each role picks on their own screen; the host sees ✓ when someone has chosen and can still override).
  - **Voting:** *via host* or *from own devices* (secret ballots), same as the bot.
- **Players** see their role card (hidden until tapped), private results (Detective/Lawyer checks if enabled, "you were killed", Turncoat joining the Mafia), ballots, rock-paper-scissors duels, the dice roll, and the story once the host publishes it.
- Games survive server restarts and deploys: room state is saved after every action.
- Finished web games are written to the same `games` / `game_players` tables as bot games.

## One-time server setup

Everything happens on the existing Oracle VM (`158.101.99.123`) next to the bot. Run the commands from Cloud Shell or the server as shown.

### 1. Get a free domain (DuckDNS)

Passwords must travel over HTTPS, and HTTPS needs a domain.

1. Open [duckdns.org](https://www.duckdns.org) and sign in (GitHub or Google).
2. Add a subdomain, for example `mafianext` → `mafianext.duckdns.org`.
3. In **current ip** enter `158.101.99.123` and press **update ip**.

### 2. Open ports 80 and 443

**In the Oracle Cloud console:** Networking → Virtual cloud networks → your VCN → your subnet → *Default Security List* → **Add Ingress Rules**: Source CIDR `0.0.0.0/0`, IP protocol TCP, destination port range `80,443`.

**On the server** (Oracle's Ubuntu image also blocks ports in its own firewall):

```bash
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 80 -j ACCEPT
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 443 -j ACCEPT
sudo netfilter-persistent save
```

### 3. Install Caddy (HTTPS)

```bash
sudo apt install -y debian-keyring debian-archive-keyring apt-transport-https curl
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | sudo gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | sudo tee /etc/apt/sources.list.d/caddy-stable.list
sudo apt update && sudo apt install -y caddy
```

### 4. Put the code on GitHub

1. Create a repository on github.com (public is fine, because secrets stay in `.env` on the server; for a private repo see *Private repository* below).
2. **Add file → Upload files** and drag in everything from this folder.
3. The `.github` folder is hidden on many computers and may not upload. If `.github/workflows/deploy.yml` is missing in the repo, create it: **Add file → Create new file**, type `.github/workflows/deploy.yml` as the name and paste the file's contents.

### 5. Turn `~/mafia` on the server into a copy of the repository

This is done once. After that the server updates itself from GitHub. On the server (`ubuntu@instance-...`):

```bash
cd ~/mafia
mkdir -p ~/backup && cp *.py .env mafia.db ~/backup/
rm -f mafia_bot.py texts.py
git init -b main
git remote add origin https://github.com/YOUR-USER/YOUR-REPO.git
git fetch origin main
git reset --hard origin/main
./venv/bin/pip install -r requirements.txt
```

`.env` and `mafia.db` stay untouched: they are ignored by Git.

### 6. Start the web server

```bash
sudo cp ~/mafia/deploy/mafiaweb.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now mafiaweb
sudo systemctl restart mafiabot
sudo systemctl status mafiaweb --no-pager
```

Then point Caddy at your domain:

```bash
sed "s/YOUR-NAME.duckdns.org/mafianext.duckdns.org/" ~/mafia/deploy/Caddyfile | sudo tee /etc/caddy/Caddyfile
sudo systemctl reload caddy
```

Open `https://mafianext.duckdns.org` — the game should load. The first start may take a minute while Caddy gets the certificate.

### 7. Tell the bot the site address

Add this line to `~/mafia/.env`, then restart the bot so `/web` shows the link:

```bash
echo "WEB_URL=https://mafianext.duckdns.org" >> ~/mafia/.env
sudo systemctl restart mafiabot mafiaweb
```

Then link your own Telegram account: send `/web` to the bot, open the site → **I have Telegram**, enter the code, choose a username and password. Your account becomes the site admin (Profile → Admin).

### 8. Connect GitHub auto-deploy

In the repository: **Settings → Secrets and variables → Actions → New repository secret**, three times:

| Name | Value |
|---|---|
| `SSH_HOST` | `158.101.99.123` |
| `SSH_USER` | `ubuntu` |
| `SSH_KEY` | the full contents of `oracle.key` (in Cloud Shell: `cat oracle.key`, copy everything including the `BEGIN` and `END` lines) |

Test it: **Actions → Deploy to Oracle VM → Run workflow**. A green check means the server pulled the code and restarted both services.

## Everyday workflow

Edit a file on GitHub (pencil icon) or upload a new version → **Commit**. GitHub Actions deploys within about a minute: it pulls the code, installs packages, and restarts the bot and the web server. Running games continue after the restart.

The old Cloud Shell routine (`scp` + `ssh` + `systemctl restart`) is no longer needed. Don't edit files directly on the server either, because the next deploy overwrites them.

Logs on the server:

```bash
journalctl -u mafiaweb -n 50 --no-pager
journalctl -u mafiabot -n 50 --no-pager
```

## Troubleshooting

- **Site doesn't open:** check DuckDNS points to the right IP, both firewall steps (console *and* `iptables`) are done, and `sudo systemctl status caddy mafiaweb --no-pager` is green.
- **The `/web` code is rejected:** codes work for 10 minutes and only once; send `/web` again. If the bot doesn't know `/web` at all, it's still running the old version (check the deploy).
- **Someone forgot their password:** with Telegram, they send `/web` and set a new one. Without Telegram, you reset it in Profile → Admin and give them the temporary password.
- **Deploy fails at `git fetch`:** the server folder isn't a Git copy yet (step 5) or the repo is private (see below).
- **Deploy fails at SSH:** the `SSH_KEY` secret must contain the whole key, including the first and last lines.
- **"Connection lost — reconnecting…" on the site:** the web server is restarting (a deploy) or stopped. Check `journalctl -u mafiaweb`.

## Private repository

If the repo is private, the server needs read access:

```bash
ssh-keygen -t ed25519 -f ~/.ssh/github_deploy -N ""
cat ~/.ssh/github_deploy.pub
printf "Host github.com\n  IdentityFile ~/.ssh/github_deploy\n" >> ~/.ssh/config
cd ~/mafia && git remote set-url origin git@github.com:YOUR-USER/YOUR-REPO.git
```

Paste the printed key into the repo under **Settings → Deploy keys → Add deploy key** (read-only), then run `git fetch origin main` once and answer `yes`.

## Good to know

- **Passwords** are stored only as scrypt hashes. After 5 wrong attempts a username is locked for 10 minutes (a reset lifts the lock).
- **Languages:** the site offers all six bot languages. Game texts (roles, stories, buttons from `texts.py`) are translated; the few site-only texts (login, accounts) and the bot's `/web` message use Russian for Tatar, Kazakh, Kyrgyz and Bashkir until translated. The `/web` menu labels in those four languages are my translations, so please check them.
- **Settings are shared with the bot** (for linked accounts), but the bot keeps its own copy in memory: a change made on the site reaches the bot after its next restart (every deploy restarts it). The bot also drops the web-only *Night moves* setting when it saves its own settings, so check it before a web game.
- **Site data** lives in the same `mafia.db` in tables the bot doesn't use: `web_accounts`, `web_guests` (site-only profiles), `web_rooms`, `web_games`, `link_codes` (shared with `/web`).
- The 1 GB Micro VM handles the bot, the web server and Caddy together with room to spare for a few dozen simultaneous players.
