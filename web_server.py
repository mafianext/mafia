"""
MafiaNext Web — the same Mafia game as @MafiaNextBot, played from phones in a browser.

Lives next to mafia_bot.py and texts.py and imports the game logic from them, so the
rules, roles, night resolution, stories and points are identical. Shares mafia.db with
the bot. Site accounts use a login and password. A Telegram user links their account by
sending /web to the bot and entering the code on the site: then it is one account with one
profile and one points total for the bot and the site.

Environment (.env, same file as the bot):
  BOT_TOKEN=...          bot token (also signs the site's login sessions)
  HOST_ID=...            owner's Telegram ID: site admin, can take the host seat in any web room
  WEB_PORT=8080          port for Caddy to proxy to (optional)
  WEB_URL=https://...    the site address, shown by the bot's /web command (optional)
  BOT_USERNAME=...       bot username shown on the login page (optional, default MafiaNextBot)

Run:  python web_server.py
"""

import base64
import copy
import hashlib
import hmac
import json
import logging
import os
import random
import re
import secrets
import time
from pathlib import Path

from aiohttp import WSMsgType, web

import mafia_bot as mb
from texts import LANG_NAMES, PRESET_NAMES, ROLE_DESC, ROLE_EMOJI, ROLE_NAMES, T, TEAM_NAMES

BASE = Path(__file__).resolve().parent
STATIC = BASE / "web"
PORT = int(os.getenv("WEB_PORT", "8080"))
BOT_USERNAME = os.getenv("BOT_USERNAME", "MafiaNextBot")
SECRET = hashlib.sha256(("mafia-web-session:" + mb.TOKEN).encode()).digest()
SESSION_DAYS = 180

log = logging.getLogger("mafia-web")
DB = mb.DB
DB.executescript("""
CREATE TABLE IF NOT EXISTS web_guests (
    uid        INTEGER PRIMARY KEY,   -- negative ids, never clash with Telegram ids
    nick       TEXT NOT NULL,
    gender     TEXT,
    lang       TEXT NOT NULL DEFAULT 'ru',
    created_at TEXT
);
CREATE TABLE IF NOT EXISTS web_rooms (
    id    INTEGER PRIMARY KEY,
    state TEXT                        -- room state as JSON (games survive restarts)
);
CREATE TABLE IF NOT EXISTS web_accounts (
    uid        INTEGER PRIMARY KEY,   -- negative: site-only player; positive: linked Telegram user
    login      TEXT NOT NULL UNIQUE COLLATE NOCASE,
    pw         TEXT NOT NULL,         -- scrypt hash, never the password itself
    created_at TEXT
);
CREATE TABLE IF NOT EXISTS web_games (
    game_id INTEGER PRIMARY KEY       -- games played on the site (for the site leaderboard)
);
CREATE TABLE IF NOT EXISTS link_codes (
    code TEXT PRIMARY KEY, uid INTEGER NOT NULL, expires_at REAL NOT NULL
);
""")

# Web-only host settings. Stored in host_prefs next to the bot's settings;
# the bot ignores keys it doesn't know.
WEB_EXTRA = {"night_input": ["host", "phones"]}


class Oops(Exception):
    """A user-facing refusal; key is a text key known to the client."""
    def __init__(self, key, **kw):
        super().__init__(key)
        self.key, self.kw = key, kw


# ======================== users and sessions ========================
def user(uid):
    if uid < 0:
        row = DB.execute("SELECT * FROM web_guests WHERE uid = ?", (uid,)).fetchone()
        return dict(row) if row else None
    return mb.get_user(uid)


def uname(uid):
    u = user(uid)
    return u["nick"] if u else "?"


def lang_of(uid):
    u = user(uid)
    return (u or {}).get("lang") or "ru"


def set_user(uid, **fields):
    if uid < 0:
        sets = ", ".join(f"{k} = ?" for k in fields)
        DB.execute(f"UPDATE web_guests SET {sets} WHERE uid = ?", (*fields.values(), uid))
        DB.commit()
    else:
        mb.update_user(uid, **fields)


def sign(payload):
    raw = base64.urlsafe_b64encode(json.dumps(payload, separators=(",", ":")).encode()).decode().rstrip("=")
    sig = hmac.new(SECRET, raw.encode(), hashlib.sha256).hexdigest()[:40]
    return f"{raw}.{sig}"


def unsign(token):
    try:
        raw, sig = token.rsplit(".", 1)
        good = hmac.new(SECRET, raw.encode(), hashlib.sha256).hexdigest()[:40]
        if not hmac.compare_digest(sig, good):
            return None
        payload = json.loads(base64.urlsafe_b64decode(raw + "=" * (-len(raw) % 4)))
        return payload if payload.get("exp", 0) > time.time() else None
    except (ValueError, TypeError):
        return None


def new_session(uid):
    return sign({"uid": uid, "exp": int(time.time()) + SESSION_DAYS * 86400})


def clean_nick(nick):
    nick = " ".join(str(nick or "").split())
    if not (mb.NICK_MIN <= len(nick) <= mb.NICK_MAX) or nick.startswith("/"):
        raise Oops("nick_bad", a=mb.NICK_MIN, b=mb.NICK_MAX)
    return nick


# ---------- accounts: login + password ----------
LOGIN_RE = re.compile(r"^[\w.\-]{3,20}$")
PW_MIN, PW_MAX = 6, 100


def hash_pw(password):
    salt = secrets.token_bytes(16)
    digest = hashlib.scrypt(password.encode(), salt=salt, n=2**14, r=8, p=1, dklen=32)
    return f"scrypt${salt.hex()}${digest.hex()}"


def check_pw(password, stored):
    try:
        _, salt, digest = stored.split("$")
        calc = hashlib.scrypt(password.encode(), salt=bytes.fromhex(salt), n=2**14, r=8, p=1, dklen=32)
        return hmac.compare_digest(calc.hex(), digest)
    except (ValueError, TypeError):
        return False


def clean_login(login):
    login = str(login or "").strip()
    if not LOGIN_RE.match(login):
        raise Oops("login_bad")
    return login


def clean_pw(password):
    password = str(password or "")
    if not (PW_MIN <= len(password) <= PW_MAX):
        raise Oops("pw_bad", a=PW_MIN)
    return password


def account(uid):
    row = DB.execute("SELECT * FROM web_accounts WHERE uid = ?", (uid,)).fetchone()
    return dict(row) if row else None


def create_account(uid, login, password):
    login, password = clean_login(login), clean_pw(password)
    if DB.execute("SELECT 1 FROM web_accounts WHERE login = ?", (login,)).fetchone():
        raise Oops("login_taken")
    DB.execute("INSERT INTO web_accounts (uid, login, pw, created_at) VALUES (?, ?, ?, ?)",
               (uid, login, hash_pw(password), mb.iso(mb.now_utc())))
    DB.commit()


def set_password(uid, password):
    DB.execute("UPDATE web_accounts SET pw = ? WHERE uid = ?", (hash_pw(clean_pw(password)), uid))
    DB.commit()
    acc = account(uid)
    if acc:   # a reset also lifts a lockout from earlier wrong attempts
        for key in [k for k in ATTEMPTS if k.endswith(":" + acc["login"].lower())]:
            ATTEMPTS.pop(key, None)


def new_site_uid():
    uid = -random.randint(10**9, 2 * 10**9)
    while user(uid):
        uid = -random.randint(10**9, 2 * 10**9)
    return uid


def code_owner(code):
    """Telegram uid behind a valid /web code, or None."""
    code = re.sub(r"\D", "", str(code or ""))
    row = DB.execute("SELECT uid FROM link_codes WHERE code = ? AND expires_at > ?",
                     (code, time.time())).fetchone()
    return (row["uid"], code) if row and mb.get_user(row["uid"]) else (None, code)


def use_code(code):
    DB.execute("DELETE FROM link_codes WHERE code = ?", (code,))
    DB.commit()


def merge_into(old, tg_uid):
    """Moves a site-only player (negative uid) into a Telegram account: history, account, profile."""
    DB.execute("UPDATE OR IGNORE game_players SET uid = ? WHERE uid = ?", (tg_uid, old))
    DB.execute("DELETE FROM game_players WHERE uid = ?", (old,))
    DB.execute("UPDATE games SET host_id = ? WHERE host_id = ?", (tg_uid, old))
    if account(old):
        DB.execute("UPDATE web_accounts SET uid = ? WHERE uid = ?", (tg_uid, old))
    row = DB.execute("SELECT value FROM host_prefs WHERE uid = ?", (old,)).fetchone()
    if row and not DB.execute("SELECT 1 FROM host_prefs WHERE uid = ?", (tg_uid,)).fetchone():
        DB.execute("UPDATE host_prefs SET uid = ? WHERE uid = ?", (tg_uid, old))
    DB.execute("DELETE FROM web_guests WHERE uid = ?", (old,))
    DB.commit()


# ---------- brute-force protection ----------
ATTEMPTS = {}   # key -> list of failure times


def too_many(key, limit, window=600):
    now = time.time()
    hits = [x for x in ATTEMPTS.get(key, []) if now - x < window]
    ATTEMPTS[key] = hits
    return len(hits) >= limit


def failed(key):
    ATTEMPTS.setdefault(key, []).append(time.time())


def client_ip(request):
    # The server only listens on 127.0.0.1, so requests come through Caddy, which sets this header.
    return request.headers.get("X-Forwarded-For", request.remote or "").split(",")[0].strip()


# ======================== host settings ========================
def wprefs(uid):
    """Host settings fresh from the database (the bot may have changed them)."""
    mb.PREFS.pop(uid, None)
    p = mb.prefs(uid)
    row = DB.execute("SELECT value FROM host_prefs WHERE uid = ?", (uid,)).fetchone()
    raw = json.loads(row["value"]) if row else {}
    for k, opts in WEB_EXTRA.items():
        p[k] = raw.get(k) if raw.get(k) in opts else opts[0]
    return p


def save_wprefs(uid, p):
    mb.PREFS[uid] = p
    mb.save_prefs(uid)


def room_cfg(g):
    if g.get("cfg") and in_game(g):
        return g["cfg"]
    return wprefs(g["host"] or g.get("last_host") or mb.OWNER_ID)


# ======================== rooms ========================
ROOMS = {}     # id -> room
ROOM_OF = {}   # uid -> room id


def web_extra():
    return {"inbox": {}, "story_public": False, "story_pending": False, "story_seq": 0,
            "dice": None, "mafia_by": None}


def new_room(rid):
    g = mb.new_room(rid)
    g.update(web_extra())
    return g


def save_room(g):
    if g["id"] in ROOMS:
        DB.execute("INSERT OR REPLACE INTO web_rooms (id, state) VALUES (?, ?)",
                   (g["id"], json.dumps(g, ensure_ascii=False)))
        DB.commit()


def delete_room(g):
    ROOMS.pop(g["id"], None)
    DB.execute("DELETE FROM web_rooms WHERE id = ?", (g["id"],))
    DB.commit()


def load_rooms():
    for row in DB.execute("SELECT state FROM web_rooms"):
        g = json.loads(row["state"])
        for field in mb.INT_KEY_FIELDS + ("inbox",):
            g[field] = {int(k): v for k, v in (g.get(field) or {}).items()}
        g["night"] = {(k if k == "mafia" else int(k)): v for k, v in g.get("night", {}).items()}
        if g.get("rps"):
            g["rps"]["choices"] = {int(k): v for k, v in g["rps"]["choices"].items()}
        for k, v in web_extra().items():
            g.setdefault(k, v)
        ROOMS[g["id"]] = g
        for uid in g["members"]:
            ROOM_OF[uid] = g["id"]


def room_of(uid):
    return ROOMS.get(ROOM_OF.get(uid))


def in_game(g):
    return g["phase"] in ("night", "day")


def P(g, uid):
    return g["players"][uid]


def is_alive(g, uid):
    return mb.is_alive_player(g, uid)


def add_player(g, uid):
    u = user(uid)
    nick = mb.unique_nick(g, u["nick"], uid)
    g["players"][uid] = {"nick": nick, "gender": u.get("gender"), "role": None, "alive": True}
    g["order"].append(uid)


def remove_player(g, uid):
    if uid in g["players"]:
        del g["players"][uid]
        g["order"].remove(uid)


def reset_game(g):
    keep = [u for u in g["order"] if u in g["members"] and u != g["host"]]
    g.update(mb.fresh_game())
    g.update(web_extra())
    for uid in keep:
        add_player(g, uid)


def push(g, uid, text):
    """A private message shown on one player's screen until the next story."""
    g["inbox"].setdefault(uid, []).append(text)


def join(uid, rid):
    g = ROOMS.get(rid)
    if not g:
        raise Oops("no_room")
    current = room_of(uid)
    if current is g:
        return g
    if current:
        leave(uid)
    g["members"].append(uid)
    ROOM_OF[uid] = rid
    if g["phase"] == "lobby":
        add_player(g, uid)
    return g


def leave(uid):
    g = room_of(uid)
    if not g:
        return
    if in_game(g) and is_alive(g, uid):
        raise Oops("cant_leave_alive")
    if g["host"] == uid:
        g["host"] = None
    if g["phase"] == "lobby":
        remove_player(g, uid)
    g["members"].remove(uid)
    ROOM_OF.pop(uid, None)
    if not g["members"]:
        delete_room(g)
    else:
        save_room(g)


def create_room(uid):
    rid = 1
    while rid in ROOMS:
        rid += 1
    if room_of(uid):
        leave(uid)
    ROOMS[rid] = new_room(rid)
    g = join(uid, rid)
    take_host(g, uid)
    return g


def take_host(g, uid, force=False):
    if g["host"] and not force:
        raise Oops("host_taken_already")
    if in_game(g) and is_alive(g, uid):
        raise Oops("cant_host_alive")
    if g["phase"] == "lobby":
        remove_player(g, uid)
    g["host"] = uid
    g["last_host"] = uid


# ======================== game flow (ports of the bot's async functions) ========================
def deal(g):
    n = len(g["order"])
    if n < 3:
        raise Oops("need_3")
    g["cfg"] = copy.deepcopy(wprefs(g["host"]))
    roles, _dropped = mb.plan_roles(g, n)
    random.shuffle(roles)
    for uid, role in zip(g["order"], roles):
        g["players"][uid].update(role=role, alive=True)
    first_night = g["cfg"]["first_phase"] == "night"
    g.update(round=1 if first_night else 0, phase="night" if first_night else "day",
             started_at=mb.iso(mb.now_utc()), inbox={}, events=[], notes=[],
             story_public=False, story_pending=False)


def set_night(g, actor, target):
    if actor == "mafia":
        if not mb.killers(g):
            return
    elif actor not in mb.night_actors(g):
        return
    if target and target not in mb.pick_candidates(g, actor):
        raise Oops("bad_target")
    if actor != "mafia" and mb.role_of(g, actor) == "driver":
        pair = list(g["night"].get(actor) or [])
        if not target:
            pair = []
        elif target in pair:
            pair.remove(target)
        elif len(pair) < 2:
            pair.append(target)
        else:
            pair = [target]
        g["night"][actor] = pair
        return
    if target:
        g["night"][actor] = target
    else:
        g["night"].pop(actor, None)


def turncoat_check(g, notes):
    if g["turned"]:
        return
    if not any(mb.role_of(g, u) == "mafia" and not P(g, u)["alive"] for u in g["order"]):
        return
    turncoats = [u for u in mb.alive(g) if mb.role_of(g, u) == "turncoat"]
    if not turncoats:
        return
    g["turned"] = True
    for tc in turncoats:
        notes.append(("note_turned", {"v": tc}))
        push(g, tc, "🐺 " + mb.t(lang_of(tc), "you_turned"))
        for u in mb.alive(g):
            if u != tc and mb.in_circle(g, u):
                push(g, u, "🐺 " + mb.gfmt(mb.t(lang_of(u), "turncoat_joined", v=mb.nm(g, tc)),
                                         P(g, tc)["gender"]))


def apply_night(g):
    out = mb.resolve(g)
    g["inbox"] = {}
    for d in out["deaths"]:
        P(g, d)["alive"] = False
    g["lucky_used"] += out["lucky_used"]
    for u in mb.alive(g):
        if mb.role_of(g, u) == "doctor":
            if g["night"].get(u):
                g["last_heal"][u] = g["night"][u]
            else:
                g["last_heal"].pop(u, None)
    g["lawyer_found"] += [u for u, (_, ok) in out["lawyer"].items() if ok]
    for uid, key in out["points"]:
        mb.add_points(g, uid, key)

    for d in out["deaths"]:
        push(g, d, "💀 " + mb.t(lang_of(d), "dead_night"))
    for u in out["lucky_used"]:
        push(g, u, "🍀 " + mb.t(lang_of(u), "lucky_saved"))
    if g["cfg"]["detective_dm"]:
        for u, (tg, is_mafia) in out["checks"].items():
            lang = lang_of(u)
            res = mb.t(lang, "res_mafia") if is_mafia else mb.t(lang, "res_town")
            push(g, u, "🔍 " + mb.t(lang, "dm_check", v=mb.nm(g, tg), res=res))
    if g["cfg"]["lawyer_dm"]:
        for u, (tg, ok) in out["lawyer"].items():
            push(g, u, "⚖️ " + mb.t(lang_of(u), "dm_lawyer_ok" if ok else "dm_lawyer_no", v=mb.nm(g, tg)))

    notes = out["notes"]
    for u, (tg, is_mafia) in out["checks"].items():
        notes.append(("note_check_mafia" if is_mafia else "note_check_town", {"d": u, "v": tg}))
    for u, (tg, ok) in out["lawyer"].items():
        notes.append(("note_lawyer_ok" if ok else "note_lawyer_no", {"d": u, "v": tg}))
    turncoat_check(g, notes)

    events = [{"k": "night_header", "r": g["round"]}] + out["events"]
    g.update(phase="day", night={}, votes={}, vote_stage=None, mafia_by=None)
    finish_story(g, events, notes)


def open_vote(g, revote=False):
    g.update(vote_stage="open", rps=None, decided=None, dice=None, votes={})
    if revote and not any(e["k"] == "tie_revote" for e in g["tie_log"]):
        g["tie_log"].append({"k": "tie_revote"})


def rps_resolve(g):
    rps = g["rps"]
    ch = rps["choices"]
    line = " · ".join(f"{mb.nm(g, u)} {mb.RPS_EMOJI[ch[u]]}" for u in rps["duel"])
    symbols = set(ch.values())
    if len(symbols) != 2:
        rps["log"].append(line + " — 🔁")
        rps["round"] += 1
        rps["choices"] = {}
        return
    a, b = symbols
    winner = a if mb.RPS_BEATS[a] == b else b
    losers = [u for u in rps["duel"] if ch[u] != winner]
    rps["log"].append(line)
    rps["duel"] = losers
    rps["choices"] = {}
    if len(losers) == 1:
        g["tie_log"].append({"k": "tie_rps", "v": losers[0], "x": "\n".join(rps["log"])})
        g["decided"] = losers[0]
        g["vote_stage"] = "decided"
    else:
        rps["round"] += 1


def roll_dice(g):
    cands = mb.leaders(g)
    n = len(cands)
    if n > 6:
        chosen = random.choice(cands)
        g["tie_log"].append({"k": "tie_random", "v": chosen})
        g["dice"] = None
    else:
        allowed = 6 - 6 % n
        mapping = []
        for i, c in enumerate(cands):
            faces = ", ".join(str(v) for v in range(1, allowed + 1) if (v - 1) % n == i)
            mapping.append(f"{faces} → {mb.nm(g, c)}")
        rolls = []
        while True:
            value = random.randint(1, 6)
            rolls.append(value)
            if value <= allowed:
                break
        chosen = cands[(value - 1) % n]
        g["tie_log"].append({"k": "tie_dice", "v": chosen, "x": f"🎲 {value}\n" + "\n".join(mapping)})
        g["dice"] = {"rolls": rolls, "mapping": mapping, "seq": random.randrange(10**9)}
    g["decided"] = chosen
    g["vote_stage"] = "decided"


def finalize_day(g, target, mayor=False):
    for voter, cand in g["votes"].items():
        if is_alive(g, voter) and cand in g["players"] and mb.team_of(g, voter) == "town" \
                and mb.team_of(g, cand) == "mafia":
            mb.add_points(g, voter, "vote")
    g["inbox"] = {}
    events = [{"k": "day_header", "r": g["round"]}] + g["tie_log"]
    notes = []
    if mayor and target:
        g["mayor_used"] = True
        events.append({"k": "mayor", "v": target})
        notes.append(("note_mayor", {"v": target}))
    elif target and is_alive(g, target):
        P(g, target)["alive"] = False
        events.append({"k": "exile", "v": target, "reveal": True})
        push(g, target, "🗳 " + mb.t(lang_of(target), "dead_day"))
        turncoat_check(g, notes)
    else:
        events.append({"k": "no_exile"})
    g["round"] += 1
    g.update(phase="night", night={}, votes={}, vote_stage=None, tie_log=[], rps=None,
             decided=None, dice=None, mafia_by=None)
    finish_story(g, events, notes)


def finish_story(g, events, notes):
    winner = mb.check_winner(g)
    if winner:
        events.append({"k": f"win_{winner}"})
        mb.end_game(g, winner)          # writes games/game_players: same history as the bot
        row = DB.execute("SELECT id FROM games WHERE started_at = ? AND host_id IS ? ORDER BY id DESC LIMIT 1",
                         (g["started_at"], g["host"])).fetchone()
        if row:
            DB.execute("INSERT OR IGNORE INTO web_games (game_id) VALUES (?)", (row["id"],))
            DB.commit()
    for e in events:
        e.setdefault("i", random.randrange(1000))
    g["events"] = events
    g["notes"] = notes
    g["story_seq"] += 1
    g["story_pending"] = True
    g["story_public"] = bool(g["cfg"]["auto_broadcast"])


# ======================== actions ========================
def to_int(v):
    try:
        return int(v)
    except (TypeError, ValueError):
        return 0


def host_action(g, uid, m):
    cmd, x, y = m.get("c"), m.get("x"), m.get("y")
    ph, stage = g["phase"], g["vote_stage"]

    if cmd == "release":
        g["host"] = None
        return
    if cmd == "abort" and in_game(g):
        reset_game(g)
        return
    if cmd == "publish":
        g["story_public"] = True
        return
    if cmd == "story_next":
        g["story_pending"] = False
        return

    if ph in ("lobby", "over"):
        p = wprefs(uid)
        if cmd == "preset" and x in ("classic", "extended", "chaos", "custom"):
            p["counts"] = dict(p["custom"] if x == "custom" else mb.PRESETS[x])
            p["preset"] = x
            save_wprefs(uid, p)
            return
        if cmd == "rc" and x in mb.ROLE_ORDER and y in ("+", "-", "auto"):
            c = p["counts"]
            if y == "auto":
                c["mafia"] = 0
            else:
                cur = c.get(x, 0)
                if x == "mafia" and cur == 0:
                    cur = mb.mafia_count(g, max(len(g["order"]), 3))
                low = 1 if x == "mafia" else 0
                c[x] = max(low, min(mb.MAX_COUNT.get(x, 1), cur + (1 if y == "+" else -1)))
            p["preset"] = "custom"
            p["custom"] = dict(c)
            save_wprefs(uid, p)
            return
        if cmd == "st":
            options = mb.SETTINGS_SPEC.get(x) or WEB_EXTRA.get(x)
            if options:
                p[x] = options[(options.index(p[x]) + 1) % len(options)] if p[x] in options else options[0]
                save_wprefs(uid, p)
            return

    if ph == "lobby":
        if cmd == "kick":
            remove_player(g, to_int(x))
        elif cmd == "deal":
            deal(g)
        return
    if ph == "over" and cmd == "rematch":
        reset_game(g)
        return

    if ph == "night":
        if cmd == "nt":
            set_night(g, "mafia" if x == "mafia" else to_int(x), to_int(y))
        elif cmd == "endnight":
            apply_night(g)
        return

    if ph == "day":
        if cmd == "nightstart" and g["round"] == 0:
            g.update(phase="night", round=1, night={})
        elif cmd == "vopen" and stage is None and g["round"] > 0:
            open_vote(g)
        elif stage == "open" and cmd == "vt":
            voter, cand = to_int(x), to_int(y)
            if is_alive(g, voter):
                if not cand:
                    g["votes"].pop(voter, None)
                elif is_alive(g, cand) and cand != voter:
                    g["votes"][voter] = cand
        elif stage == "open" and cmd == "vclose":
            g["vote_stage"] = "result"
        elif stage == "result" and cmd == "revote":
            open_vote(g, revote=True)
        elif stage == "result" and cmd == "rps" and len(mb.leaders(g)) > 1:
            g["rps"] = {"duel": mb.leaders(g), "choices": {}, "round": 1, "log": []}
            g["vote_stage"] = "rps"
        elif stage == "result" and cmd == "dice" and len(mb.leaders(g)) > 1:
            roll_dice(g)
        elif stage == "rps" and g["rps"] and cmd == "rpsrand":
            for u in g["rps"]["duel"]:
                g["rps"]["choices"].setdefault(u, random.choice("rps"))
            rps_resolve(g)
        elif stage == "rps" and cmd == "rpsx":
            g.update(rps=None, vote_stage="result")
        elif stage in ("result", "decided") and cmd == "ex":
            finalize_day(g, to_int(x) or None)
        elif stage in ("result", "decided") and cmd == "mayor" and mb.mayor_available(g) and to_int(x):
            finalize_day(g, to_int(x), mayor=True)


def player_action(g, uid, a, m):
    if a == "play" and g["phase"] == "lobby" and uid not in g["players"] and uid != g["host"]:
        add_player(g, uid)
    elif a == "watch" and g["phase"] == "lobby":
        remove_player(g, uid)
    elif a == "take_host":
        take_host(g, uid)
    elif a == "owner_host":
        if uid != mb.OWNER_ID:
            raise Oops("owner_only")
        take_host(g, uid, force=True)
    elif a == "abort":
        if not in_game(g) or (g["host"] and g["host"] != uid):
            raise Oops("only_host")
        reset_game(g)
    elif a == "night":
        if g["phase"] != "night" or g["cfg"].get("night_input") != "phones" or not is_alive(g, uid):
            raise Oops("bad_target")
        target = to_int(m.get("target"))
        if uid in mb.killers(g):
            set_night(g, "mafia", target)
            g["mafia_by"] = uid if target else None
        elif uid in mb.night_actors(g):
            set_night(g, uid, target)
        else:
            raise Oops("bad_target")
    elif a in ("vote", "unvote"):
        if (g["phase"] != "day" or g["vote_stage"] != "open" or g["cfg"]["vote_mode"] != "phones"
                or not is_alive(g, uid)):
            raise Oops("vote_not_open")
        if a == "unvote":
            g["votes"].pop(uid, None)
            return
        cand = to_int(m.get("target"))
        if uid in g["votes"]:
            raise Oops("already_voted")
        if is_alive(g, cand) and cand != uid:
            g["votes"][uid] = cand
    elif a == "rps":
        rps = g["rps"]
        c = m.get("c")
        if (g["vote_stage"] != "rps" or not rps or uid not in rps["duel"]
                or uid in rps["choices"] or c not in ("r", "p", "s")):
            raise Oops("rps_expired")
        rps["choices"][uid] = c
        if all(u in rps["choices"] for u in rps["duel"]):
            rps_resolve(g)


def profile_action(uid, m):
    fields = {}
    if "nick" in m:
        nick = clean_nick(m["nick"])
        g = room_of(uid)
        if g and uid in g["players"]:
            if g["phase"] != "lobby":
                raise Oops("nick_after_game")
            if mb.nick_taken(g, nick, uid):
                raise Oops("nick_taken_web")
            P(g, uid)["nick"] = nick
        fields["nick"] = nick
    if "gender" in m:
        fields["gender"] = m["gender"] if m["gender"] in ("m", "f") else None
        g = room_of(uid)
        if g and uid in g["players"] and g["phase"] == "lobby":
            P(g, uid)["gender"] = fields["gender"]
    if "lang" in m and m["lang"] in LANG_NAMES:
        fields["lang"] = m["lang"]
    if fields:
        set_user(uid, **fields)


# ======================== what each person sees ========================
def plist(g, uids):
    return [{"uid": u, "nick": P(g, u)["nick"]} for u in uids]


def rooms_list():
    out = []
    for rid in sorted(ROOMS):
        g = ROOMS[rid]
        out.append({"id": rid, "phase": g["phase"], "round": g["round"], "n": len(g["order"]),
                    "host": uname(g["host"]) if g["host"] else None})
    return out


def task_state(g, uid, lang):
    if g["phase"] != "night" or not is_alive(g, uid):
        return None
    if g["cfg"].get("night_input") != "phones":
        return {"sleep": "host"}
    if uid in mb.killers(g):
        sel = g["night"].get("mafia")
        return {"actor": "mafia", "title": f"{ROLE_EMOJI['mafia']} {mb.t(lang, 'pick_mafia')}",
                "cands": plist(g, mb.pick_candidates(g, "mafia")), "chosen": [sel] if sel else [],
                "by": uname(g["mafia_by"]) if g.get("mafia_by") else None,
                "team": [P(g, u)["nick"] for u in mb.killers(g) if u != uid]}
    if uid in mb.night_actors(g):
        role = mb.role_of(g, uid)
        sel = g["night"].get(uid)
        return {"actor": uid, "multi": role == "driver",
                "title": f"{mb.role_name(role, lang, P(g, uid)['gender'])}: {mb.t(lang, 'pick_' + role)}",
                "cands": plist(g, mb.pick_candidates(g, uid)),
                "chosen": (sel if isinstance(sel, list) else [sel]) if sel else []}
    return {"sleep": "none"}


def host_state(g, uid, lang):
    h = {"story_pending": g["story_pending"] and bool(g["events"])}
    if g["phase"] in ("lobby", "over"):
        p = wprefs(uid)
        h["prefs"] = {k: p[k] for k in ["preset", "counts", *mb.SETTINGS_SPEC, *WEB_EXTRA]}
        n = len(g["order"])
        h["auto_mafia"] = max(1, max(n, 3) // 4)
        if n >= 3:
            roles, dropped = mb.plan_roles(g, n)
            h["plan"] = mb.roles_line(roles)
            h["dropped"] = ", ".join(mb.role_name(r, lang) for r in dropped)
    if g["phase"] != "lobby" and any(P(g, u)["role"] for u in g["order"]):
        h["lineup"] = [{"uid": u, "name": mb.hn(g, u),
                        "role": mb.role_name(P(g, u)["role"], lang, P(g, u)["gender"]),
                        "alive": P(g, u)["alive"], "pts": g["points"].get(u, 0)} for u in g["order"]]
    if g["notes"]:
        h["notes"] = mb.render_notes(g, g["notes"], lang)
    if g["phase"] == "night":
        preview = mb.resolve(g)
        rows = []
        if mb.killers(g):
            sel = g["night"].get("mafia")
            rows.append({"actor": "mafia",
                         "html": f"{ROLE_EMOJI['mafia']} {mb.t(lang, 'mafia_team_kill')} → {mb.nm(g, sel) if sel else '—'}",
                         "title": f"{ROLE_EMOJI['mafia']} {mb.t(lang, 'pick_mafia')}",
                         "cands": plist(g, mb.pick_candidates(g, "mafia")), "chosen": [sel] if sel else [],
                         "done": bool(sel)})
        for u in mb.night_actors(g):
            role = mb.role_of(g, u)
            sel = g["night"].get(u)
            rows.append({"actor": u, "html": mb.actor_line(g, u, lang, preview), "multi": role == "driver",
                         "title": f"{mb.role_name(role, lang, P(g, u)['gender'])} {mb.hn(g, u)}: {mb.t(lang, 'pick_' + role)}",
                         "cands": plist(g, mb.pick_candidates(g, u)),
                         "chosen": (sel if isinstance(sel, list) else [sel]) if sel else [],
                         "done": bool(sel) and (role != "driver" or len(sel) == 2)})
        h["night"] = rows
    if g["phase"] == "day":
        counts = mb.tally(g)
        h["votes"] = {str(v): c for v, c in g["votes"].items()}
        h["tally"] = [{"uid": c, "nick": P(g, c)["nick"], "n": n} for c, n in counts.most_common()]
        h["leaders"] = mb.leaders(g)
        h["mayor"] = mb.mayor_available(g)
        h["tie_default"] = g["cfg"]["tie_default"]
    return h


def room_state(g, uid, lang):
    ing = in_game(g)
    am_host = g["host"] == uid
    cfg = room_cfg(g)
    r = {
        "id": g["id"], "phase": g["phase"], "round": g["round"], "am_host": am_host,
        "host": {"uid": g["host"], "nick": uname(g["host"])} if g["host"] else None,
        "paused": ing and not g["host"],
        "status": "host" if am_host else ("player" if uid in g["players"] else "watcher"),
        "players": [{"uid": u, "nick": P(g, u)["nick"], "alive": P(g, u)["alive"]} for u in g["order"]],
        "watchers": [uname(u) for u in g["members"] if u not in g["players"] and u != g["host"]],
        "vote_stage": g["vote_stage"], "vote_mode": cfg["vote_mode"],
        "night_input": cfg.get("night_input", "host"),
        "can_take_host": not g["host"] and not (ing and is_alive(g, uid)),
        "can_leave": not (ing and is_alive(g, uid)),
        "can_abort": ing and (am_host or not g["host"]),
        "winner": g["winner"], "inbox": g["inbox"].get(uid, []),
    }
    if uid in g["players"] and P(g, uid)["role"]:
        r["me"] = {"alive": P(g, uid)["alive"], "role": P(g, uid)["role"],
                   "html": mb.role_message(g, uid, lang)}
    if g["events"] and (g["story_public"] or am_host):
        r["story"] = {"html": mb.render_events(g, g["events"], lang), "seq": g["story_seq"],
                      "public": g["story_public"]}
    r["task"] = task_state(g, uid, lang)
    if g["phase"] == "day" and g["vote_stage"] == "open" and cfg["vote_mode"] == "phones" and is_alive(g, uid):
        mine = g["votes"].get(uid)
        r["ballot"] = {"cands": plist(g, [c for c in mb.alive(g) if c != uid]),
                       "mine": mine, "mine_nick": P(g, mine)["nick"] if mine else None}
    if g["phase"] == "day" and g["vote_stage"] == "open":
        r["voted"] = [v for v in g["votes"] if is_alive(g, v)]
    if g["vote_stage"] == "rps" and g["rps"]:
        rps = g["rps"]
        r["rps"] = {"round": rps["round"], "log": rps["log"],
                    "duel": [{"uid": u, "nick": P(g, u)["nick"], "done": u in rps["choices"]} for u in rps["duel"]],
                    "mine": uid in rps["duel"] and uid not in rps["choices"],
                    "rivals": ", ".join(mb.nm(g, u) for u in rps["duel"] if u != uid)}
    if g["dice"]:
        r["dice"] = g["dice"]
    if g["decided"]:
        r["decided"] = {"uid": g["decided"], "nick": P(g, g["decided"])["nick"]}
    if g["phase"] == "over":
        r["lineup"] = [{"nick": P(g, u)["nick"],
                        "role": mb.role_name(P(g, u)["role"], lang, P(g, u)["gender"]),
                        "alive": P(g, u)["alive"], "pts": g["points"].get(u, 0)}
                       for u in g["order"] if P(g, u)["role"]]
    if am_host:
        r["host_view"] = host_state(g, uid, lang)
    return r


def state_for(uid):
    u = user(uid) or {}
    lang = u.get("lang") or "ru"
    acc = account(uid)
    s = {"t": "state", "me": {"uid": uid, "nick": u.get("nick", "?"), "gender": u.get("gender"),
                              "lang": lang, "login": acc["login"] if acc else None, "linked": uid > 0,
                              "owner": uid == mb.OWNER_ID}}
    g = room_of(uid)
    if g:
        s["room"] = room_state(g, uid, lang)
    else:
        s["rooms"] = rooms_list()
    return s


def profile_for(uid):
    u = user(uid) or {}
    games = mb.user_games(uid)
    acc = account(uid)
    return {"t": "profile", "nick": u.get("nick"), "gender": u.get("gender"), "lang": u.get("lang", "ru"),
            "login": acc["login"] if acc else None, "linked": uid > 0,
            "since": u.get("registered_at") or u.get("created_at"),
            "total": sum(gm["points"] for gm in games), "wins": sum(gm["won"] for gm in games),
            "count": len(games), "last": games[0]["points"] if games else None,
            "games": [{"date": gm["started_at"], "role": gm["role"], "won": bool(gm["won"]),
                       "survived": bool(gm["survived"]), "pts": gm["points"]} for gm in games[:40]]}


def leaders_list():
    rows = DB.execute(
        "SELECT gp.uid, COUNT(*) AS games, SUM(gp.won) AS wins, SUM(gp.points) AS pts "
        "FROM game_players gp WHERE gp.uid IN "
        "(SELECT DISTINCT uid FROM game_players WHERE game_id IN (SELECT game_id FROM web_games)) "
        "GROUP BY gp.uid ORDER BY pts DESC, wins DESC LIMIT 100").fetchall()
    return [{"nick": uname(r["uid"]), "games": r["games"], "wins": r["wins"] or 0, "pts": r["pts"] or 0,
             "linked": r["uid"] > 0} for r in rows]


def admin_list(query):
    q = f"%{str(query or '').strip()}%"
    rows = DB.execute("SELECT uid, login, created_at FROM web_accounts WHERE login LIKE ? "
                      "ORDER BY created_at DESC LIMIT 100", (q,)).fetchall()
    return [{"uid": r["uid"], "login": r["login"], "nick": uname(r["uid"]), "linked": r["uid"] > 0,
             "created": r["created_at"]} for r in rows]


# ======================== connections ========================
CONNS = {}   # uid -> set of websockets


async def send(uid, obj):
    text = json.dumps(obj, ensure_ascii=False)
    for ws in list(CONNS.get(uid, ())):
        try:
            await ws.send_str(text)
        except (ConnectionError, RuntimeError):
            CONNS.get(uid, set()).discard(ws)


async def broadcast():
    for uid in list(CONNS):
        try:
            await send(uid, state_for(uid))
        except Exception:  # one broken state must not stop the others
            log.exception("state for %s failed", uid)


async def handle(uid, m):
    a = m.get("a")
    try:
        if a == "profile":
            await send(uid, profile_for(uid))
            return
        if a == "leaders":
            await send(uid, {"t": "leaders", "rows": leaders_list()})
            return
        if a in ("admin_list", "admin_reset"):
            if uid != mb.OWNER_ID:
                raise Oops("owner_only")
            temp = None
            if a == "admin_reset":
                target = to_int(m.get("uid"))
                if not account(target):
                    raise Oops("bad_request")
                temp = "".join(secrets.choice("abcdefghjkmnpqrstuvwxyz23456789") for _ in range(8))
                set_password(target, temp)
                temp = {"login": account(target)["login"], "password": temp}
            await send(uid, {"t": "admin", "rows": admin_list(m.get("q")), "temp": temp})
            return
        if a == "create_account":
            if account(uid):
                raise Oops("bad_request")
            create_account(uid, m.get("login"), m.get("password"))
            await send(uid, {"t": "toast", "key": "account_saved", "kw": {}})
            await send(uid, profile_for(uid))
        elif a == "change_password":
            acc = account(uid)
            if not acc or not check_pw(str(m.get("old") or ""), acc["pw"]):
                raise Oops("pw_wrong")
            set_password(uid, m.get("password"))
            await send(uid, {"t": "toast", "key": "pw_changed", "kw": {}})
            return
        elif a == "link_tg":
            if uid > 0:
                raise Oops("bad_request")
            if room_of(uid):
                raise Oops("leave_first")
            key = f"code:{uid}"
            if too_many(key, 10):
                raise Oops("too_many")
            tg_uid, code = code_owner(m.get("code"))
            if not tg_uid:
                failed(key)
                raise Oops("code_bad")
            if account(uid) and account(tg_uid):
                raise Oops("tg_has_account", v=account(tg_uid)["login"])
            if room_of(tg_uid):
                raise Oops("leave_first")
            use_code(code)
            merge_into(uid, tg_uid)
            await send(uid, {"t": "session", "token": new_session(tg_uid)})
            return
        elif a == "set_profile":
            profile_action(uid, m)
            save_room(room_of(uid)) if room_of(uid) else None
            await send(uid, profile_for(uid))
        elif a == "create":
            save_room(create_room(uid))
        elif a == "join":
            save_room(join(uid, to_int(m.get("room"))))
        elif a == "leave":
            leave(uid)
        else:
            g = room_of(uid)
            if not g:
                raise Oops("not_in_room")
            if a == "h":
                if g["host"] != uid:
                    raise Oops("only_host")
                host_action(g, uid, m)
            else:
                player_action(g, uid, a, m)
            save_room(g)
    except Oops as e:
        await send(uid, {"t": "toast", "key": e.key, "kw": e.kw})
        return
    await broadcast()


async def ws_handler(request):
    payload = unsign(request.query.get("token", ""))
    ws = web.WebSocketResponse(heartbeat=25)
    await ws.prepare(request)
    uid = payload and payload.get("uid")
    if not uid or not user(uid):
        await ws.close(code=4001, message=b"auth")
        return ws
    CONNS.setdefault(uid, set()).add(ws)
    await send(uid, state_for(uid))
    try:
        async for msg in ws:
            if msg.type != WSMsgType.TEXT:
                continue
            try:
                data = json.loads(msg.data)
            except ValueError:
                continue
            if isinstance(data, dict):
                try:
                    await handle(uid, data)
                except Exception:
                    log.exception("action failed: %s", data)
                    await send(uid, {"t": "toast", "key": "server_error", "kw": {}})
    finally:
        CONNS.get(uid, set()).discard(ws)
        if not CONNS.get(uid):
            CONNS.pop(uid, None)
    return ws


# ======================== HTTP ========================
async def index(_request):
    return web.FileResponse(STATIC / "index.html", headers={"Cache-Control": "no-cache"})


async def api_config(_request):
    return web.json_response({"bot": BOT_USERNAME})


async def api_texts(_request):
    return web.json_response({
        "T": T, "ROLE_NAMES": ROLE_NAMES, "ROLE_DESC": ROLE_DESC, "ROLE_EMOJI": ROLE_EMOJI,
        "TEAM_NAMES": TEAM_NAMES, "PRESET_NAMES": PRESET_NAMES, "LANG_NAMES": LANG_NAMES,
        "ROLE_ORDER": mb.ROLE_ORDER, "MAX_COUNT": mb.MAX_COUNT, "MAFIA_TEAM": sorted(mb.MAFIA_TEAM),
        "SETTINGS": {**mb.SETTINGS_SPEC, **WEB_EXTRA},
    }, headers={"Cache-Control": "no-cache"})


def fail(key, status=400, **kw):
    return web.json_response({"error": key, "kw": kw}, status=status)


async def body(request):
    try:
        data = await request.json()
        return data if isinstance(data, dict) else {}
    except ValueError:
        return {}


def new_site_player(nick, gender, lang):
    uid = new_site_uid()
    DB.execute("INSERT INTO web_guests (uid, nick, gender, lang, created_at) VALUES (?, ?, ?, ?, ?)",
               (uid, nick, gender if gender in ("m", "f") else None,
                lang if lang in LANG_NAMES else "ru", mb.iso(mb.now_utc())))
    return uid


async def api_guest(request):
    data = await body(request)
    try:
        nick = clean_nick(data.get("nick"))
    except Oops as e:
        return fail(e.key, **e.kw)
    uid = new_site_player(nick, data.get("gender"), data.get("lang"))
    DB.commit()
    return web.json_response({"token": new_session(uid)})


async def api_register(request):
    data = await body(request)
    try:
        nick = clean_nick(data.get("nick") or data.get("login"))
        login, password = clean_login(data.get("login")), clean_pw(data.get("password"))
        if DB.execute("SELECT 1 FROM web_accounts WHERE login = ?", (login,)).fetchone():
            raise Oops("login_taken")
    except Oops as e:
        return fail(e.key, **e.kw)
    uid = new_site_player(nick, data.get("gender"), data.get("lang"))
    create_account(uid, login, password)
    return web.json_response({"token": new_session(uid)})


async def api_login(request):
    data = await body(request)
    login, password = str(data.get("login") or "").strip(), str(data.get("password") or "")
    key = f"login:{client_ip(request)}:{login.lower()}"
    if too_many(key, 5):
        return fail("too_many", status=429)
    row = DB.execute("SELECT uid, pw FROM web_accounts WHERE login = ?", (login,)).fetchone()
    if not row or not check_pw(password, row["pw"]):
        failed(key)
        return fail("login_wrong", status=403)
    ATTEMPTS.pop(key, None)
    return web.json_response({"token": new_session(row["uid"])})


async def api_code(request):
    """Step 1 (check=true): who is behind the code. Step 2: create the account or set a new password."""
    data = await body(request)
    key = f"code:{client_ip(request)}"
    if too_many(key, 10):
        return fail("too_many", status=429)
    tg_uid, code = code_owner(data.get("code"))
    if not tg_uid:
        failed(key)
        return fail("code_bad", status=403)
    acc = account(tg_uid)
    if data.get("check"):
        return web.json_response({"nick": uname(tg_uid), "login": acc["login"] if acc else None})
    try:
        if acc:
            set_password(tg_uid, data.get("password"))
        else:
            create_account(tg_uid, data.get("login"), data.get("password"))
    except Oops as e:
        return fail(e.key, **e.kw)
    use_code(code)
    return web.json_response({"token": new_session(tg_uid)})


def make_app():
    load_rooms()
    app = web.Application(client_max_size=64 * 1024)
    app.router.add_get("/", index)
    app.router.add_get("/ws", ws_handler)
    app.router.add_get("/api/config", api_config)
    app.router.add_get("/api/texts", api_texts)
    app.router.add_post("/api/guest", api_guest)
    app.router.add_post("/api/register", api_register)
    app.router.add_post("/api/login", api_login)
    app.router.add_post("/api/code", api_code)
    app.router.add_get("/health", lambda _r: web.Response(text="ok"))
    app.router.add_static("/static/", STATIC)
    return app


if __name__ == "__main__":
    logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s", level=logging.INFO)
    print(f"🎭 MafiaNext Web on http://127.0.0.1:{PORT}")
    web.run_app(make_app(), host="127.0.0.1", port=PORT, print=None)
