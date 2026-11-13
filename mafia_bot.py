"""
MafiaNextBot v3 — ведущий для игры в Мафию, с комнатами.

Файлы рядом друг с другом:
  mafia_bot.py — логика игры
  texts.py     — все тексты на русском и английском (роли, истории, кнопки)
  mafia.db     — база SQLite (создаётся сама): профили, история игр,
                 настройки ведущих и состояние всех комнат

Переменные окружения (.env на сервере):
  BOT_TOKEN=...   токен бота
  HOST_ID=...     Telegram ID владельца бота (может забрать ведущего командой /takehost)
  TZ_NAME=...     часовой пояс для дат (по умолчанию America/New_York)
"""

import asyncio
import copy
import html
import json
import logging
import os
import random
import re
import secrets
import sqlite3
import time
from collections import Counter
from datetime import datetime, timedelta, timezone

from telegram import BotCommand, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.error import BadRequest, Forbidden
from telegram.ext import (ApplicationBuilder, CallbackQueryHandler,
                          CommandHandler, ContextTypes, MessageHandler, filters)

from texts import (COMMANDS, LANG_NAMES, PRESET_NAMES, ROLE_DESC, ROLE_EMOJI,
                   ROLE_NAMES, STORIES, T, TEAM_NAMES)

try:
    from zoneinfo import ZoneInfo
    TZ = ZoneInfo(os.getenv("TZ_NAME", "America/New_York"))
except Exception:  # например, Windows без пакета tzdata
    TZ = timezone.utc

# ======================== НАСТРОЙКИ ========================
TOKEN = os.getenv("BOT_TOKEN", "ВСТАВЬТЕ_СЮДА_ТОКЕН")
OWNER_ID = int(os.getenv("HOST_ID", "0"))
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "mafia.db")
NICK_MIN, NICK_MAX = 2, 20
REALNAME_MAX = 40

# Неактивные комнаты
ROOM_IDLE_CLOSE = timedelta(days=1)    # после этого участники могут закрыть комнату
ROOM_IDLE_DELETE = timedelta(days=7)   # после этого комната удаляется сама
ROOM_IDLE_WARN = timedelta(days=6)     # когда предупредить участников об удалении
CLEANUP_EVERY = 3600                   # как часто проверять комнаты, в секундах

# Очки за игру
POINTS = {
    "win": 10,      # команда победила
    "survive": 3,   # дожил до конца
    "vote": 3,      # голосовал против команды мафии
    "save": 3,      # доктор спас цель мафии
    "check": 3,     # детектив нашёл настоящую мафию
    "kill": 2,      # мафия совершила убийство (каждому убийце)
    "guard": 3,     # телохранитель закрыл собой
    "lawyer": 3,    # адвокат угадал мафию
    "frame": 3,     # подставщик обманул детектива
    "block": 3,     # тусовщик заблокировал игрока команды мафии
}
# ===========================================================

HTML = ParseMode.HTML
logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s", level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)
BOT_USERNAME = "MafiaNextBot"   # уточняется при запуске

# ======================== РОЛИ ========================
ROLE_ORDER = ["mafia", "framer", "lawyer", "doctor", "detective", "bodyguard",
              "partyhost", "driver", "mayor", "immortal", "lucky", "bestfriend",
              "turncoat"]
MAX_COUNT = {"mafia": 10, "doctor": 3, "detective": 3, "lawyer": 3}  # остальные — до 1
SLOTS = {"bestfriend": 2}                    # лучшие друзья занимают два места
MAFIA_TEAM = {"mafia", "lawyer", "framer"}   # + оборотень после превращения
NIGHT_ROLES = ["partyhost", "driver", "framer", "doctor", "bodyguard",
               "detective", "lawyer"]        # порядок кнопок в ночной панели
NO_SELF = {"partyhost", "bodyguard", "detective", "lawyer"}
TRIM_ORDER = ["driver", "turncoat", "framer", "lucky", "immortal", "mayor",
              "partyhost", "bestfriend", "bodyguard", "lawyer"]

PRESETS = {
    "classic": {"mafia": 0, "doctor": 1, "detective": 1},
    "extended": {"mafia": 0, "doctor": 1, "detective": 1, "lawyer": 1,
                 "bodyguard": 1, "mayor": 1, "partyhost": 1},
    "chaos": {**{r: 1 for r in ROLE_ORDER}, "mafia": 0},
}

# Настройки ведущего: ключ -> возможные значения (первое — по умолчанию)
SETTINGS_SPEC = {
    "vote_mode": ["host", "phones"],
    "tie_default": ["nobody", "rps", "random", "revote"],
    "show_names": [True, False],
    "reveal": ["full", "team", "none"],
    "doctor_self": [True, False],
    "doctor_repeat": [False, True],
    "first_phase": ["night", "day"],
    "auto_broadcast": [False, True],
    "detective_dm": [False, True],
    "lawyer_dm": [False, True],
}
PREF_DEFAULTS = {
    "preset": "classic",
    "counts": dict(PRESETS["classic"]),
    "custom": dict(PRESETS["classic"]),
    **{k: v[0] for k, v in SETTINGS_SPEC.items()},
}
RPS_BEATS = {"r": "s", "s": "p", "p": "r"}   # камень бьёт ножницы и т.д.
RPS_EMOJI = {"r": "✊", "p": "✋", "s": "✌️"}

# ======================== БАЗА ДАННЫХ ========================
DB = sqlite3.connect(DB_PATH)
DB.row_factory = sqlite3.Row
DB.executescript("""
CREATE TABLE IF NOT EXISTS users (
    uid           INTEGER PRIMARY KEY,
    real_name     TEXT,
    nick          TEXT NOT NULL,
    gender        TEXT,             -- 'm', 'f' или NULL
    lang          TEXT NOT NULL DEFAULT 'ru',
    photo_id      TEXT,
    registered_at TEXT NOT NULL     -- UTC, ISO 8601
);
CREATE TABLE IF NOT EXISTS games (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    started_at TEXT,
    ended_at   TEXT,
    winner     TEXT,
    host_id    INTEGER,
    players    INTEGER
);
CREATE TABLE IF NOT EXISTS game_players (
    game_id  INTEGER,
    uid      INTEGER,
    nick     TEXT,
    role     TEXT,
    team     TEXT,
    survived INTEGER,
    won      INTEGER,
    points   INTEGER,
    PRIMARY KEY (game_id, uid)
);
CREATE TABLE IF NOT EXISTS host_prefs (
    uid   INTEGER PRIMARY KEY,
    value TEXT                      -- настройки ведущего в JSON
);
CREATE TABLE IF NOT EXISTS rooms (
    id    INTEGER PRIMARY KEY,
    state TEXT                      -- состояние комнаты в JSON
);
""")
# Одноразовые коды для входа на сайт (/web); сайт читает их из той же базы
DB.execute("CREATE TABLE IF NOT EXISTS link_codes (code TEXT PRIMARY KEY, uid INTEGER NOT NULL, "
           "expires_at REAL NOT NULL)")
WEB_URL = os.getenv("WEB_URL", "").rstrip("/")
WEB_CODE_TTL = 600   # секунд



def now_utc():
    return datetime.now(timezone.utc)


def iso(dt):
    return dt.isoformat(timespec="seconds")


def local(iso_str):
    return datetime.fromisoformat(iso_str).astimezone(TZ)


# ---------- пользователи ----------
def get_user(uid):
    row = DB.execute("SELECT * FROM users WHERE uid = ?", (uid,)).fetchone()
    return dict(row) if row else None


def ensure_user(tg_user):
    user = get_user(tg_user.id)
    if user:
        return user
    code = (tg_user.language_code or "ru")[:2]
    lang = TG_LANGS.get(code, "en")
    full = tg_user.full_name or "Player"
    DB.execute(
        "INSERT INTO users (uid, real_name, nick, gender, lang, photo_id, registered_at) "
        "VALUES (?, ?, ?, NULL, ?, NULL, ?)",
        (tg_user.id, full[:REALNAME_MAX], full[:NICK_MAX], lang, iso(now_utc())))
    DB.commit()
    return get_user(tg_user.id)


def update_user(uid, **fields):
    sets = ", ".join(f"{k} = ?" for k in fields)
    DB.execute(f"UPDATE users SET {sets} WHERE uid = ?", (*fields.values(), uid))
    DB.commit()


def lang_of(uid):
    user = get_user(uid)
    return user["lang"] if user else "ru"


# ---------- настройки ведущего (у каждого свои) ----------
PREFS = {}


def prefs(uid):
    if uid not in PREFS:
        p = copy.deepcopy(PREF_DEFAULTS)
        row = DB.execute("SELECT value FROM host_prefs WHERE uid = ?", (uid,)).fetchone()
        if row:
            p.update({k: v for k, v in json.loads(row["value"]).items() if k in PREF_DEFAULTS})
        PREFS[uid] = p
    return PREFS[uid]


def save_prefs(uid):
    DB.execute("INSERT OR REPLACE INTO host_prefs (uid, value) VALUES (?, ?)",
               (uid, json.dumps(PREFS[uid], ensure_ascii=False)))
    DB.commit()


# ---------- перенос данных из прошлых версий ----------
def migrate_old_versions():
    path = os.path.join(BASE_DIR, "profiles.json")          # версия 1
    if os.path.exists(path):
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
            for uid, prof in data.items():
                name = (prof.get("name") or "Player")[:NICK_MAX]
                DB.execute("INSERT OR IGNORE INTO users (uid, real_name, nick, lang, registered_at) "
                           "VALUES (?, ?, ?, 'ru', ?)", (int(uid), name, name, iso(now_utc())))
            DB.commit()
            os.replace(path, path + ".migrated")
        except (OSError, ValueError):
            pass
    has_old = DB.execute("SELECT name FROM sqlite_master WHERE name = 'settings'").fetchone()
    if has_old and OWNER_ID:                                 # версия 2: общие настройки
        old = {r["key"]: json.loads(r["value"]) for r in DB.execute("SELECT * FROM settings")}
        p = prefs(OWNER_ID)
        p.update({k: v for k, v in old.items() if k in PREF_DEFAULTS})
        save_prefs(OWNER_ID)
        DB.execute("DROP TABLE settings")
        DB.commit()


# ======================== КОМНАТЫ ========================
ROOMS = {}     # id -> комната
ROOM_OF = {}   # uid -> id комнаты, где он сейчас


def fresh_game():
    return {
        "phase": "lobby",       # lobby | night | day | over
        "players": {},          # uid -> {"nick", "gender", "role", "alive"}
        "order": [],
        "round": 0,
        "night": {},            # "mafia" / uid актёра -> цель (у таксиста — список из двух)
        "last_heal": {},        # доктор -> кого лечил прошлой ночью
        "votes": {},            # голосующий -> кандидат
        "vote_stage": None,     # None | open | result | rps | decided
        "vote_msgs": {},        # игрок -> id сообщения с кнопками голосования
        "tie_log": [],          # события ничьей для истории
        "rps": None,            # состояние дуэли «камень, ножницы, бумага»
        "decided": None,        # кого определили дуэль или кубик
        "events": [],
        "notes": [],
        "points": {},
        "turned": False,
        "mayor_used": False,
        "lawyer_found": [],
        "lucky_used": [],
        "started_at": None,
        "winner": None,
        "cfg": None,            # снимок настроек ведущего на время партии
    }


def new_room(rid):
    return {"id": rid, "host": None, "last_host": None, "members": [],
            "ui": {}, "active_at": iso(now_utc()), "warned": False, **fresh_game()}


def touch(g):
    """Отмечает, что в комнате что-то произошло."""
    g["active_at"] = iso(now_utc())
    g["warned"] = False


def idle_time(g):
    return now_utc() - datetime.fromisoformat(g["active_at"])


def can_close(g, uid):
    return uid == OWNER_ID or (uid in g["members"] and idle_time(g) >= ROOM_IDLE_CLOSE)


def free_room_id():
    i = 1
    while i in ROOMS:
        i += 1
    return i


INT_KEY_FIELDS = ("players", "last_heal", "votes", "points", "vote_msgs")


def save_room(g):
    DB.execute("INSERT OR REPLACE INTO rooms (id, state) VALUES (?, ?)",
               (g["id"], json.dumps(g, ensure_ascii=False)))
    DB.commit()


def delete_room(g):
    ROOMS.pop(g["id"], None)
    DB.execute("DELETE FROM rooms WHERE id = ?", (g["id"],))
    DB.commit()


def load_rooms():
    for row in DB.execute("SELECT state FROM rooms"):
        g = json.loads(row["state"])
        for field in INT_KEY_FIELDS:
            g[field] = {int(k): v for k, v in g.get(field, {}).items()}
        g["night"] = {(k if k == "mafia" else int(k)): v for k, v in g.get("night", {}).items()}
        if g.get("rps"):
            g["rps"]["choices"] = {int(k): v for k, v in g["rps"]["choices"].items()}
        g.setdefault("ui", {})
        g.setdefault("active_at", iso(now_utc()))   # комнаты из прошлой версии
        g.setdefault("warned", False)
        ROOMS[g["id"]] = g
        for uid in g["members"]:
            ROOM_OF[uid] = g["id"]


def room_of(uid):
    rid = ROOM_OF.get(uid)
    return ROOMS.get(rid) if rid else None


def cfg(g):
    """Настройки, по которым идёт игра: снимок на время партии или настройки ведущего."""
    if g.get("cfg") and g["phase"] in ("night", "day"):
        return g["cfg"]
    return prefs(g["host"] or g.get("last_host") or OWNER_ID)


# ======================== ТЕКСТЫ ========================
GENDER_RE = re.compile(r"\[([^\[\]|]*)\|([^\[\]]*)\]")


TG_LANGS = {"ru": "ru", "uk": "ru", "be": "ru", "en": "en",
            "tt": "tt", "kk": "kk", "ky": "ky", "ba": "ba"}   # язык Telegram → язык бота


def loc(table, lang):
    """Таблица текстов на нужном языке; если перевода нет — русская."""
    return table.get(lang) or table["ru"]


def t(lang, key, **kw):
    text = loc(T, lang).get(key, T["ru"][key])
    return text.format(**kw) if kw else text


def gfmt(text, gender):
    """[мужской|женский] -> нужная форма. Если пол не указан — мужская."""
    return GENDER_RE.sub(lambda m: m.group(2) if gender == "f" else m.group(1), text)


def role_name(role, lang, gender=None, emoji=True):
    male, female = loc(ROLE_NAMES, lang)[role]
    name = female if gender == "f" else male
    return f"{ROLE_EMOJI[role]} {name}" if emoji else name


def plural(n, lang, forms_key):
    forms = loc(T, lang).get(forms_key) or T["en"][forms_key]
    if lang != "ru":
        return f"{n} {forms[0] if n == 1 else forms[-1]}"
    if n % 10 == 1 and n % 100 != 11:
        form = forms[0]
    elif 2 <= n % 10 <= 4 and not 12 <= n % 100 <= 14:
        form = forms[1]
    else:
        form = forms[2]
    return f"{n} {form}"


def tenure(start, end, lang):
    y, m, d = end.year - start.year, end.month - start.month, end.day - start.day
    if d < 0:
        m -= 1
        d += (end.replace(day=1) - timedelta(days=1)).day
    if m < 0:
        y -= 1
        m += 12
    parts = []
    if y:
        parts.append(plural(y, lang, "years"))
    if m:
        parts.append(plural(m, lang, "months"))
    if d or not parts:
        parts.append(plural(d, lang, "days"))
    return ", ".join(parts)


def room_link(rid):
    return f"https://t.me/{BOT_USERNAME}?start=room{rid}"


# ======================== СОСТОЯНИЕ ИГРЫ ========================
def P(g, uid):
    return g["players"][uid]


def nm(g, uid):
    """Ник для всех (с HTML-экранированием)."""
    if uid in g["players"]:
        return html.escape(g["players"][uid]["nick"])
    user = get_user(uid)
    return html.escape(user["nick"]) if user else "?"


def hn(g, uid):
    """Ник для ведущего: с настоящим именем в скобках, если так настроено."""
    name = nm(g, uid)
    if cfg(g)["show_names"]:
        user = get_user(uid)
        real = user["real_name"] if user else None
        if real and real != (g["players"][uid]["nick"] if uid in g["players"] else user["nick"]):
            name += f" <i>({html.escape(real)})</i>"
    return name


def in_game(g):
    return g["phase"] in ("night", "day")


def alive(g):
    return [u for u in g["order"] if P(g, u)["alive"]]


def is_alive_player(g, uid):
    return uid in g["players"] and P(g, uid)["alive"]


def role_of(g, uid):
    return P(g, uid)["role"]


def team_of(g, uid):
    role = role_of(g, uid)
    if role in MAFIA_TEAM or (role == "turncoat" and g["turned"]):
        return "mafia"
    return "town"


def in_circle(g, uid):
    """Мафиози, которые знают друг друга: мафия, подставщик, превращённый оборотень."""
    role = role_of(g, uid)
    return role in ("mafia", "framer") or (role == "turncoat" and g["turned"])


def killers(g):
    return [u for u in alive(g)
            if role_of(g, u) == "mafia" or (role_of(g, u) == "turncoat" and g["turned"])]


def night_actors(g):
    return [u for r in NIGHT_ROLES for u in alive(g)
            if role_of(g, u) == r and not (r == "lawyer" and u in g["lawyer_found"])]


def check_winner(g):
    mafia = sum(1 for u in alive(g) if team_of(g, u) == "mafia")
    others = len(alive(g)) - mafia
    if mafia == 0:
        return "town"
    if mafia >= others:
        return "mafia"
    return None


def add_points(g, uid, key):
    g["points"][uid] = g["points"].get(uid, 0) + POINTS[key]


def nick_taken(g, nick, uid):
    return any(p["nick"].lower() == nick.lower() for u, p in g["players"].items() if u != uid)


def unique_nick(g, nick, uid):
    if not nick_taken(g, nick, uid):
        return nick
    i = 2
    while nick_taken(g, f"{nick} {i}", uid):
        i += 1
    return f"{nick} {i}"


def add_player(g, uid):
    user = get_user(uid)
    nick = unique_nick(g, user["nick"], uid)
    g["players"][uid] = {"nick": nick, "gender": user["gender"], "role": None, "alive": True}
    g["order"].append(uid)
    return nick


def remove_player(g, uid):
    if uid in g["players"]:
        del g["players"][uid]
        g["order"].remove(uid)


def reset_game(g, keep_players=True):
    old = [u for u in g["order"] if u in g["members"]] if keep_players else []
    g.update(fresh_game())
    for uid in old:
        if uid != g["host"]:
            add_player(g, uid)


# ======================== РАСПРЕДЕЛЕНИЕ РОЛЕЙ ========================
def mafia_count(g, n):
    m = cfg(g)["counts"].get("mafia", 0)
    return m if m > 0 else max(1, n // 4)


def plan_roles(g, n):
    """Возвращает (список ролей длиной n, список убранных ролей)."""
    counts = cfg(g)["counts"]
    c = {r: counts.get(r, 0) for r in ROLE_ORDER}
    c["mafia"] = mafia_count(g, n)
    dropped = []

    def total():
        return sum(v * SLOTS.get(r, 1) for r, v in c.items())

    def mafia_team():
        return sum(v for r, v in c.items() if r in MAFIA_TEAM)

    for r in TRIM_ORDER + ["doctor", "detective"]:
        floor = 1 if r in ("doctor", "detective") else 0
        while total() > n and c[r] > floor:
            c[r] -= 1
            dropped.append(r)
    while total() > n and c["mafia"] > 1:
        c["mafia"] -= 1
        dropped.append("mafia")
    for r in reversed(list(dropped)):        # вернуть важные роли, если место освободилось
        if total() + SLOTS.get(r, 1) <= n:
            c[r] += 1
            dropped.remove(r)
    while mafia_team() >= n - mafia_team():  # команда мафии должна быть меньше города
        for r in ("lawyer", "framer", "mafia"):
            if c[r] > (1 if r == "mafia" else 0):
                c[r] -= 1
                dropped.append(r)
                break
        else:
            break
    for r in reversed(list(dropped)):        # освободившееся место — мирной роли
        if r not in MAFIA_TEAM and total() + SLOTS.get(r, 1) <= n:
            c[r] += 1
            dropped.remove(r)

    roles = [r for r in ROLE_ORDER for _ in range(c[r] * SLOTS.get(r, 1))]
    roles += ["civilian"] * (n - len(roles))
    return roles[:n], dropped


def roles_line(roles):
    counts = Counter(roles)
    return " ".join(f"{ROLE_EMOJI[r]}×{counts[r]}" for r in ROLE_ORDER + ["civilian"] if counts[r])


# ======================== НОЧЬ: РАСЧЁТ ========================
def resolve(g):
    """Считает итог ночи, ничего не меняя. Порядок:
    тусовщик → таксист → подставщик → защита → убийство → проверки."""
    n = g["night"]
    blocked = {n[u] for u in alive(g) if role_of(g, u) == "partyhost" and n.get(u)}
    redirect = {}
    for u in alive(g):
        if role_of(g, u) == "driver" and u not in blocked:
            pair = n.get(u) or []
            if len(pair) == 2 and pair[0] != pair[1]:
                a, b = pair
                redirect[a], redirect[b] = b, a

    def target(u):
        if u in blocked or not n.get(u) or role_of(g, u) == "driver":
            return None
        return redirect.get(n[u], n[u])

    out = {"blocked": blocked, "deaths": [], "events": [], "notes": [],
           "checks": {}, "lawyer": {}, "points": [], "lucky_used": []}

    for u in alive(g):
        if role_of(g, u) == "partyhost" and n.get(u) and team_of(g, n[u]) == "mafia":
            out["points"].append((u, "block"))

    framed = {target(u) for u in alive(g) if role_of(g, u) == "framer" and target(u)}
    healed, guards = {}, {}
    for u in alive(g):
        tg = target(u)
        if tg and role_of(g, u) == "doctor":
            healed.setdefault(tg, []).append(u)
        if tg and role_of(g, u) == "bodyguard":
            guards[tg] = u

    kill_choice = n.get("mafia")
    team = killers(g)
    if kill_choice and team:
        if any(k in blocked for k in team):
            out["events"].append({"k": "quiet"})
            out["notes"].append(("note_kill_blocked", {}))
        else:
            victim = redirect.get(kill_choice, kill_choice)
            if not is_alive_player(g, victim):
                out["events"].append({"k": "quiet"})
            elif role_of(g, victim) == "immortal":
                out["events"].append({"k": "survived"})
                out["notes"].append(("note_immortal", {"v": victim}))
            elif victim in healed:
                out["events"].append({"k": "saved"})
                out["notes"].append(("note_saved", {"v": victim}))
                out["points"] += [(d, "save") for d in healed[victim]]
            elif victim in guards:
                bg = guards[victim]
                out["deaths"].append(bg)
                out["events"].append({"k": "bodyguard", "v": bg, "reveal": True})
                out["notes"].append(("note_guarded", {"v": victim, "b": bg}))
                out["points"].append((bg, "guard"))
            elif role_of(g, victim) == "lucky" and victim not in g["lucky_used"]:
                out["lucky_used"].append(victim)
                out["events"].append({"k": "survived"})
                out["notes"].append(("note_lucky", {"v": victim}))
            else:
                out["deaths"].append(victim)
                out["events"].append({"k": "kill", "v": victim, "reveal": True})
                out["points"] += [(k, "kill") for k in team]
            if victim != kill_choice:
                out["notes"].append(("note_redirected", {"v": kill_choice, "b": victim}))
    else:
        out["events"].append({"k": "quiet"})

    for u in alive(g):
        if role_of(g, u) == "detective" and target(u):
            tg = target(u)
            really = team_of(g, tg) == "mafia" and role_of(g, tg) != "lawyer"
            out["checks"][u] = (tg, really or tg in framed)
            if really:
                out["points"].append((u, "check"))
            elif tg in framed:
                out["points"] += [(f, "frame") for f in alive(g)
                                  if role_of(g, f) == "framer" and target(f) == tg]

    for u in alive(g):
        if role_of(g, u) == "lawyer" and u not in g["lawyer_found"] and target(u):
            tg = target(u)
            ok = in_circle(g, tg)
            out["lawyer"][u] = (tg, ok)
            if ok:
                out["points"].append((u, "lawyer"))
    return out


# ======================== ИСТОРИИ ========================
def reveal_line(g, uid, lang):
    mode = cfg(g)["reveal"]
    if mode == "full":
        return "\n" + t(lang, "reveal_role", role=role_name(role_of(g, uid), lang, P(g, uid)["gender"]))
    if mode == "team":
        return "\n" + t(lang, "reveal_team", team=loc(TEAM_NAMES, lang)[team_of(g, uid)])
    return ""


def render_events(g, events, lang):
    parts = []
    for e in events:
        variants = loc(STORIES, lang)[e["k"]]
        text = variants[e.get("i", 0) % len(variants)]
        uid = e.get("v")
        text = gfmt(text, P(g, uid)["gender"] if uid else None)
        text = text.format(v=nm(g, uid) if uid else "", r=e.get("r", ""), x=e.get("x", ""))
        if uid and e.get("reveal"):
            text += reveal_line(g, uid, lang)
        parts.append(text)
    return "\n\n".join(parts)


def render_notes(g, notes, lang):
    return "\n".join("• " + t(lang, key, **{k: nm(g, v) for k, v in params.items()})
                     for key, params in notes)


# ======================== ПОМОЩНИКИ ДЛЯ TELEGRAM ========================
def B(text, data):
    return InlineKeyboardButton(text, callback_data=data)


def grid(buttons, per_row=2):
    return [buttons[i:i + per_row] for i in range(0, len(buttons), per_row)]


def kb(*rows):
    return InlineKeyboardMarkup([r for r in rows if r])


async def notify(context, uid, text, markup=None):
    try:
        msg = await context.bot.send_message(uid, text, parse_mode=HTML, reply_markup=markup)
        return msg
    except (Forbidden, BadRequest):
        return None


async def edit(context, uid, msg_id, text, markup=None):
    try:
        await context.bot.edit_message_text(text, chat_id=uid, message_id=msg_id,
                                            parse_mode=HTML, reply_markup=markup)
    except (Forbidden, BadRequest):
        pass


async def safe_edit(query, text, markup):
    try:
        await query.edit_message_text(text, parse_mode=HTML, reply_markup=markup)
    except BadRequest as e:
        if "not modified" not in str(e):
            raise


async def notify_members(context, g, key, exclude=(), **kw):
    for uid in list(g["members"]):
        if uid not in exclude:
            lang = lang_of(uid)
            await notify(context, uid, t(lang, key, **{k: (v(lang) if callable(v) else v)
                                                       for k, v in kw.items()}))


def role_message(g, uid, lang):
    p = P(g, uid)
    role = p["role"]
    text = (f"🎭 <b>{t(lang, 'your_role')}: {role_name(role, lang, p['gender'])}</b>\n\n"
            f"{loc(ROLE_DESC, lang)[role]}")
    if in_circle(g, uid):
        mates = [f"{nm(g, u)} ({role_name(role_of(g, u), lang, P(g, u)['gender'], emoji=False)})"
                 for u in g["order"] if u != uid and in_circle(g, u)]
        if mates:
            text += f"\n\n{t(lang, 'your_team')}: " + ", ".join(mates)
    if role == "bestfriend":
        friend = [u for u in g["order"] if u != uid and role_of(g, u) == "bestfriend"]
        if friend:
            text += "\n\n" + gfmt(t(lang, "your_friend", v=nm(g, friend[0])), P(g, friend[0])["gender"])
    if role == "lucky" and uid in g["lucky_used"]:
        text += "\n\n" + t(lang, "lucky_spent")
    if role == "lawyer" and uid in g["lawyer_found"]:
        text += "\n\n" + t(lang, "lawyer_done")
    text += "\n\n" + ("💀 " + t(lang, "you_are_out") if not p["alive"]
                      else "🤫 " + t(lang, "keep_secret"))
    return text


# ======================== ЭКРАНЫ ИГРОКОВ ========================
def room_status(g, lang):
    if g["phase"] == "lobby":
        return "⏳ " + t(lang, "status_lobby")
    if g["phase"] == "over":
        return "🏁 " + t(lang, "status_over")
    if not g["host"]:
        return "⏸ " + t(lang, "status_paused")
    if g["phase"] == "night":
        return f"🌙 {t(lang, 'night')} {g['round']}"
    return f"☀️ {t(lang, 'day')} {g['round']}"


def idle_text(g, lang):
    hours = int(idle_time(g).total_seconds() // 3600)
    if hours >= 24:
        return plural(hours // 24, lang, "days")
    return plural(hours, lang, "hours")


def rooms_screen(uid):
    lang = lang_of(uid)
    mine = ROOM_OF.get(uid)
    lines = [f"🏘 <b>{t(lang, 'rooms_title')}</b>\n"]
    rows = []
    for rid in sorted(ROOMS):
        g = ROOMS[rid]
        host = nm(g, g["host"]) if g["host"] else "—"
        here = " 📍" if rid == mine else ""
        lines.append(f"🏠 <b>{t(lang, 'room')} {rid}</b>{here} — {room_status(g, lang)} · "
                     f"👥 {len(g['order'])} · 👑 {host}")
        row = [B(f"🏠 {t(lang, 'room')} {rid} · {room_status(g, lang)}", f"go:{rid}")]
        if uid == OWNER_ID:
            row.append(B("🗑", f"own:close:{rid}"))
        rows.append(row)
    free = free_room_id()
    rows.append([B(f"🆕 {t(lang, 'free_room')} {free}", f"go:{free}")])
    rows.append([roles_button(lang), B("👤 " + t(lang, "profile"), "p:profile")])
    if len(lines) == 1:
        lines.append(f"<i>{t(lang, 'no_rooms')}</i>")
    return "\n".join(lines), InlineKeyboardMarkup(rows)


def room_screen(g, uid):
    lang = lang_of(uid)
    players = []
    for u in g["order"]:
        mark = "" if P(g, u)["alive"] or g["phase"] == "lobby" else " 💀"
        players.append(f"• {nm(g, u)}{mark}")
    watchers = [nm(g, u) for u in g["members"] if u not in g["players"] and u != g["host"]]
    host = nm(g, g["host"]) if g["host"] else f"<i>{t(lang, 'no_host')}</i>"
    text = (f"🏠 <b>{t(lang, 'room')} {g['id']}</b> — {room_status(g, lang)}\n"
            f"👑 {t(lang, 'host')}: {host}\n\n"
            f"<b>{t(lang, 'players')} ({len(players)}):</b>\n"
            + ("\n".join(players) or f"<i>{t(lang, 'nobody_yet')}</i>"))
    if watchers:
        text += f"\n\n👀 {t(lang, 'watchers')}: " + ", ".join(watchers)
    text += f"\n\n🔗 {t(lang, 'invite')}: {room_link(g['id'])}"
    if idle_time(g) >= ROOM_IDLE_CLOSE:
        text += "\n💤 " + t(lang, "idle_for", v=idle_text(g, lang))

    rows = []
    if g["phase"] == "lobby":
        if uid in g["players"]:
            rows.append([B("👀 " + t(lang, "btn_watch"), "rm:watch")])
        else:
            rows.append([B("🙋 " + t(lang, "btn_play"), "rm:play")])
    if uid in g["players"] and P(g, uid)["role"]:
        rows.append([B("🎭 " + t(lang, "btn_my_role"), "rm:role")])
    if not g["host"] and (not in_game(g) or not is_alive_player(g, uid)):
        rows.append([B("👑 " + t(lang, "btn_take_host"), "rm:take")])
    if in_game(g) and not g["host"]:
        rows.append([B("⏹ " + t(lang, "btn_end_game"), "rm:end")])
    if can_close(g, uid):
        rows.append([B("🗑 " + t(lang, "btn_close_room"), "rm:close")])
    rows.append([B("🔄 " + t(lang, "btn_refresh"), "rm:show"),
                 B("🚪 " + t(lang, "btn_leave_room"), "rm:leave")])
    rows.append([B("🏘 " + t(lang, "rooms_title"), "rm:list"),
                 B("👤 " + t(lang, "profile"), "p:profile")])
    rows.append([roles_button(lang)])
    return text, InlineKeyboardMarkup(rows)


# ======================== СПРАВКА О РОЛЯХ (для всех) ========================
GUIDE_ORDER = ["mafia", "framer", "lawyer", "turncoat", "doctor", "detective", "bodyguard",
               "partyhost", "driver", "mayor", "immortal", "lucky", "bestfriend", "civilian"]


def roles_guide(uid):
    lang = lang_of(uid)
    teams = loc(TEAM_NAMES, lang)

    def names(roles):
        return ", ".join(role_name(r, lang, emoji=False) for r in roles)

    town = [r for r in GUIDE_ORDER if r not in MAFIA_TEAM and r != "turncoat"]
    text = (f"📖 <b>{t(lang, 'roles_guide')}</b>\n\n"
            f"<b>{teams['mafia']}:</b> {names([r for r in GUIDE_ORDER if r in MAFIA_TEAM])}\n"
            f"<b>{teams['town']}:</b> {names(town)}\n"
            f"<b>{teams['town']} → {teams['mafia']}:</b> {names(['turncoat'])}\n\n"
            f"<i>{t(lang, 'roles_guide_hint')}</i>")
    rows = grid([B(role_name(r, lang), f"rl:c:{r}") for r in GUIDE_ORDER])
    return text, InlineKeyboardMarkup(rows)


def role_card(role, lang):
    male, female = loc(ROLE_NAMES, lang)[role]
    name = male if male == female else f"{male} / {female}"
    teams = loc(TEAM_NAMES, lang)
    if role == "turncoat":
        team = f"{teams['town']} → {teams['mafia']}"
    else:
        team = teams["mafia"] if role in MAFIA_TEAM else teams["town"]
    text = (f"{ROLE_EMOJI[role]} <b>{html.escape(name)}</b>\n{t(lang, 'team')}: {team}\n\n"
            f"{loc(ROLE_DESC, lang)[role]}")
    if role == "bestfriend":
        text += f"\n\n<i>{t(lang, 'card_pair')}</i>"
    return text, kb([B("« " + t(lang, "back_to_roles"), "rl:list")])


def roles_button(lang):
    return B("📖 " + t(lang, "btn_roles"), "rl:open")


async def on_roles_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    uid = q.from_user.id
    await q.answer()
    parts = q.data.split(":")
    if parts[1] == "open":        # из других экранов — новым сообщением
        text, markup = roles_guide(uid)
        await notify(context, uid, text, markup)
        return
    if parts[1] == "c" and len(parts) > 2 and parts[2] in ROLE_EMOJI:
        text, markup = role_card(parts[2], lang_of(uid))
    else:
        text, markup = roles_guide(uid)
    await safe_edit(q, text, markup)


# ======================== ЭКРАНЫ ВЕДУЩЕГО ========================
def game_footer(L):
    return [B("⏹ " + t(L, "btn_end_game"), "end"), B("🙌 " + t(L, "btn_release"), "release")]


def view_lobby(g, L):
    lines = [f"{i}. {hn(g, u)}" for i, u in enumerate(g["order"], 1)]
    watchers = [hn(g, u) for u in g["members"] if u not in g["players"] and u != g["host"]]
    n = len(g["order"])
    c = cfg(g)
    text = (f"🎭 <b>{t(L, 'room')} {g['id']} — {t(L, 'lobby')}</b>\n\n"
            f"<b>{t(L, 'players')} ({n}):</b>\n"
            + ("\n".join(lines) or f"<i>{t(L, 'nobody_yet')}</i>"))
    if watchers:
        text += f"\n👀 {t(L, 'watchers')}: " + ", ".join(watchers)
    text += f"\n\n<b>{t(L, 'preset')}:</b> {loc(PRESET_NAMES, L)[c['preset']]}"
    if n >= 3:
        roles, dropped = plan_roles(g, n)
        text += f"\n{roles_line(roles)}"
        if dropped:
            text += "\n⚠️ " + t(L, "will_drop", roles=", ".join(
                role_name(r, L) for r in dict.fromkeys(dropped)))
    text += f"\n🗳 {t(L, 'set_vote_mode')}: {t(L, 'val_vote_mode_' + c['vote_mode'])}"
    text += f"\n\n🔗 {t(L, 'invite')}: {room_link(g['id'])}"
    return text, kb(
        [B("⚙️ " + t(L, "btn_roles"), "roles"), B("🛠 " + t(L, "btn_settings"), "settings")],
        [B("👥 " + t(L, "btn_players"), "players"), B("🔄 " + t(L, "btn_refresh"), "m")],
        [B("🎲 " + t(L, "btn_deal"), "deal")],
        [B("🙌 " + t(L, "btn_release"), "release")],
    )


def view_roles(g, L):
    c = cfg(g)
    n = len(g["order"])
    lines = [f"⚙️ <b>{t(L, 'roles_title')}</b> — {loc(PRESET_NAMES, L)[c['preset']]}\n"]
    for r in ROLE_ORDER:
        v = c["counts"].get(r, 0)
        shown = f"{t(L, 'auto')} ({mafia_count(g, max(n, 3))})" if r == "mafia" and v == 0 else str(v)
        lines.append(f"{role_name(r, L)} — <b>{shown}</b>")
    if n >= 3:
        roles, dropped = plan_roles(g, n)
        lines.append(f"\n{t(L, 'players')}: {n} → {roles_line(roles)}")
        if dropped:
            lines.append("⚠️ " + t(L, "will_drop", roles=", ".join(
                role_name(r, L) for r in dict.fromkeys(dropped))))
    lines.append(f"\n<i>{t(L, 'roles_hint')}</i>")
    rows = grid([B(("✓ " if c["preset"] == p else "") + loc(PRESET_NAMES, L)[p], f"preset:{p}")
                 for p in ("classic", "extended", "chaos", "custom")])
    rows += grid([B(role_name(r, L), f"rcard:{r}") for r in ROLE_ORDER])
    rows.append([B("« " + t(L, "back"), "m")])
    return "\n".join(lines), InlineKeyboardMarkup(rows)


def view_rcard(g, L, role):
    c = cfg(g)
    v = c["counts"].get(role, 0)
    if role == "mafia" and v == 0:
        count = f"{t(L, 'auto')} ({mafia_count(g, max(len(g['order']), 3))})"
    else:
        count = str(v)
    team = "mafia" if role in MAFIA_TEAM else "town"
    extra = ""
    if role == "turncoat":
        extra = f" → {loc(TEAM_NAMES, L)['mafia']}"
    if role == "bestfriend":
        extra = f"\n<i>{t(L, 'card_pair')}</i>"
    text = (f"<b>{role_name(role, L)}</b>\n{t(L, 'team')}: {loc(TEAM_NAMES, L)[team]}{extra}\n\n"
            f"{loc(ROLE_DESC, L)[role]}\n\n"
            f"{t(L, 'count')}: <b>{count}</b> (max {MAX_COUNT.get(role, 1)})")
    rows = [[B("➖", f"rc:{role}:-"), B("➕", f"rc:{role}:+")]]
    if role == "mafia":
        rows.append([B("🔄 " + t(L, "mafia_auto"), "rc:mafia:auto")])
    rows.append([B("« " + t(L, "back_to_roles"), "roles")])
    return text, InlineKeyboardMarkup(rows)


def setting_label(c, key, L):
    value = c[key]
    shown = ("✅" if value else "❌") if isinstance(value, bool) else t(L, f"val_{key}_{value}")
    return f"{t(L, f'set_{key}')}: {shown}"


def view_settings(g, L):
    c = cfg(g)
    text = f"🛠 <b>{t(L, 'settings_title')}</b>\n\n<i>{t(L, 'settings_hint')}</i>"
    rows = [[B(setting_label(c, k, L), f"st:{k}")] for k in SETTINGS_SPEC]
    rows.append([B("« " + t(L, "back"), "m")])
    return text, InlineKeyboardMarkup(rows)


def view_players(g, L):
    rows = grid([B(f"👀 {P(g, u)['nick']}", f"kick:{u}") for u in g["order"]])
    rows.append([B("« " + t(L, "back"), "m")])
    return f"👥 <b>{t(L, 'btn_players')}</b>\n\n{t(L, 'kick_hint')}", InlineKeyboardMarkup(rows)


def roles_summary(g, L, with_points=False):
    lines = []
    for u in g["order"]:
        p = P(g, u)
        extra = "" if p["alive"] else " 💀"
        if p["role"] == "lucky" and u in g["lucky_used"]:
            extra += " 🍀✖"
        if p["role"] == "turncoat" and g["turned"]:
            extra += " ➡️🔪"
        if p["role"] == "lawyer" and u in g["lawyer_found"]:
            extra += " ✅"
        if with_points:
            extra += f" — <b>{g['points'].get(u, 0)}</b> {t(L, 'pts')}"
        lines.append(f"{role_name(p['role'], L, p['gender'])} — {hn(g, u)}{extra}")
    return "\n".join(lines)


def view_lineup(g, L):
    return (f"📋 <b>{t(L, 'btn_view')}</b>\n\n{roles_summary(g, L, with_points=True)}",
            kb([B("« " + t(L, "back"), "m")]))


def actor_line(g, u, L, preview):
    role = role_of(g, u)
    sel = g["night"].get(u)
    if role == "driver":
        pair = sel or []
        target = " ⇄ ".join(nm(g, x) for x in pair) + (" ⇄ …" if len(pair) == 1 else "")
        target = target or "—"
    else:
        target = nm(g, sel) if sel else "—"
    line = f"{role_name(role, L, P(g, u)['gender'])} {hn(g, u)} → {target}"
    if u in preview["blocked"]:
        line += f"  🚫 {t(L, 'blocked')}"
    if u in preview["checks"]:
        tg, is_mafia = preview["checks"][u]
        line += f"  ⇒ {nm(g, tg)}: <b>{t(L, 'res_mafia') if is_mafia else t(L, 'res_town')}</b>"
    if u in preview["lawyer"]:
        tg, ok = preview["lawyer"][u]
        line += f"  ⇒ {nm(g, tg)}: <b>{t(L, 'res_right') if ok else t(L, 'res_wrong')}</b>"
    return line


def view_night(g, L):
    preview = resolve(g)
    lines = [f"🌙 <b>{t(L, 'room')} {g['id']} — {t(L, 'night')} {g['round']}</b>\n"]
    rows = []
    if killers(g):
        sel = g["night"].get("mafia")
        lines.append(f"{ROLE_EMOJI['mafia']} {t(L, 'mafia_team_kill')} → {nm(g, sel) if sel else '—'}")
        rows.append([B(f"{ROLE_EMOJI['mafia']} {t(L, 'mafia_team_kill')}", "na:mafia")])
    actors = night_actors(g)
    lines += [actor_line(g, u, L, preview) for u in actors]
    rows += grid([B(f"{ROLE_EMOJI[role_of(g, u)]} {P(g, u)['nick']}", f"na:{u}") for u in actors])
    lines.append(f"\n<i>{t(L, 'night_hint')}</i>")
    rows.append([B("📋 " + t(L, "btn_view"), "lineup"), B("🌅 " + t(L, "btn_end_night"), "endnight")])
    rows.append(game_footer(L))
    return "\n".join(lines), InlineKeyboardMarkup(rows)


def pick_candidates(g, actor):
    if actor == "mafia":
        return [u for u in alive(g) if not in_circle(g, u)]
    role = role_of(g, actor)
    c = cfg(g)
    cands = alive(g)
    if role in NO_SELF or (role == "doctor" and not c["doctor_self"]):
        cands = [u for u in cands if u != actor]
    if role == "doctor" and not c["doctor_repeat"]:
        cands = [u for u in cands if u != g["last_heal"].get(actor)]
    return cands


def view_pick(g, L, actor):
    if actor == "mafia":
        title = f"{ROLE_EMOJI['mafia']} {t(L, 'pick_mafia')}"
        chosen = [g["night"].get("mafia")]
    else:
        role = role_of(g, actor)
        title = f"{role_name(role, L, P(g, actor)['gender'])} {hn(g, actor)}: {t(L, 'pick_' + role)}"
        sel = g["night"].get(actor)
        chosen = sel if isinstance(sel, list) else [sel]
    rows = grid([B(P(g, u)["nick"] + (" ✔️" if u in chosen else ""), f"nt:{actor}:{u}")
                 for u in pick_candidates(g, actor)])
    rows.append([B("🚫 " + t(L, "skip"), f"nt:{actor}:0")])
    rows.append([B("« " + t(L, "back"), "m")])
    return f"<b>{title}</b>", InlineKeyboardMarkup(rows)


def tally(g):
    return Counter(c for v, c in g["votes"].items()
                   if is_alive_player(g, v) and is_alive_player(g, c))


def mayor_available(g):
    return not g["mayor_used"] and any(role_of(g, u) == "mayor" for u in alive(g))


def view_day(g, L):
    if g["round"] == 0:
        text = f"☀️ <b>{t(L, 'room')} {g['id']} — {t(L, 'intro_day')}</b>\n\n{t(L, 'intro_hint')}"
        return text, kb([B("🌙 " + t(L, "btn_start_night"), "nightstart")],
                        [B("📋 " + t(L, "btn_view"), "lineup")], game_footer(L))
    names = "\n".join(f"• {hn(g, u)}" for u in alive(g))
    text = (f"☀️ <b>{t(L, 'room')} {g['id']} — {t(L, 'day')} {g['round']}</b>\n\n"
            f"{t(L, 'alive')} ({len(alive(g))}):\n{names}\n\n"
            f"🗳 {t(L, 'set_vote_mode')}: {t(L, 'val_vote_mode_' + cfg(g)['vote_mode'])}")
    return text, kb([B("🗳 " + t(L, "btn_open_vote"), "vopen")],
                    [B("📋 " + t(L, "btn_view"), "lineup")], game_footer(L))


def view_vote(g, L):
    counts = tally(g)
    phones = cfg(g)["vote_mode"] == "phones"
    voted = [u for u in alive(g) if u in g["votes"]]
    waiting = [u for u in alive(g) if u not in g["votes"]]
    lines = [f"🗳 <b>{t(L, 'vote_title')}</b> 🔒\n",
             t(L, "vote_hint_phones" if phones else "vote_hint_host"), ""]
    lines += [f"{hn(g, c)} — <b>{n}</b>" for c, n in counts.most_common()] or [t(L, "no_votes")]
    lines.append(f"\n✅ {t(L, 'voted')}: {len(voted)}/{len(alive(g))}")
    if waiting:
        lines.append(f"⏳ {t(L, 'not_voted')}: " + ", ".join(nm(g, u) for u in waiting))
    rows = []
    if not phones:
        rows += grid([B(f"{P(g, u)['nick']} ({counts[u]})", f"vc:{u}") for u in alive(g)])
    rows.append([B("↩️ " + t(L, "btn_cancel_votes"), "vcancel"), B("🔄 " + t(L, "btn_refresh"), "m")])
    rows.append([B("✅ " + t(L, "btn_close_vote"), "vclose")])
    rows.append(game_footer(L))
    return "\n".join(lines), InlineKeyboardMarkup(rows)


def view_voters(g, L, cand):
    buttons = []
    for u in alive(g):
        if u == cand:
            continue
        mark = "☑️" if g["votes"].get(u) == cand else ("▫️" if u in g["votes"] else "⬜")
        buttons.append(B(f"{mark} {P(g, u)['nick']}", f"vt:{cand}:{u}"))
    rows = grid(buttons)
    rows.append([B("« " + t(L, "back_to_vote"), "m")])
    text = f"🗳 {t(L, 'who_voted_for', v=hn(g, cand))}\n\n<i>{t(L, 'voters_hint')}</i>"
    return text, InlineKeyboardMarkup(rows)


def view_vcancel(g, L):
    rows = [[B(f"❌ {P(g, v)['nick']} → {P(g, c)['nick']}", f"vx:{v}")]
            for v, c in g["votes"].items() if is_alive_player(g, v)]
    rows.append([B("« " + t(L, "back_to_vote"), "m")])
    text = f"↩️ <b>{t(L, 'btn_cancel_votes')}</b>\n\n{t(L, 'cancel_hint')}"
    if len(rows) == 1:
        text += f"\n\n<i>{t(L, 'no_votes')}</i>"
    return text, InlineKeyboardMarkup(rows)


def leaders(g):
    counts = tally(g)
    if not counts:
        return []
    top = max(counts.values())
    return [c for c, n in counts.items() if n == top]


def exile_buttons(g, L, cand):
    rows = [[B("⚖️ " + t(L, "btn_exile", v=P(g, cand)["nick"]), f"ex:{cand}")]]
    if mayor_available(g):
        rows.append([B("🎩 " + t(L, "btn_mayor"), f"mayor:{cand}")])
    return rows


def view_result(g, L):
    counts = tally(g)
    lead = leaders(g)
    lines = [f"🗳 <b>{t(L, 'vote_result')}</b>\n"]
    lines += [f"{hn(g, c)} — <b>{n}</b>" for c, n in counts.most_common()] or [t(L, "no_votes")]
    rows = []
    if len(lead) == 1:
        lines.append("\n" + t(L, "leader", v=hn(g, lead[0])))
        rows += exile_buttons(g, L, lead[0])
        rows.append([B("🤝 " + t(L, "btn_no_exile"), "ex:0")])
    elif len(lead) > 1:
        lines.append("\n" + t(L, "tie", v=", ".join(hn(g, c) for c in lead)))
        lines.append(t(L, "tie_choose"))
        star = cfg(g)["tie_default"]
        opts = [("nobody", "🤝", "ex:0"), ("rps", "✊", "rps"),
                ("random", "🎲", "dice"), ("revote", "🔁", "revote")]
        opts.sort(key=lambda o: o[0] != star)
        rows += [[B(("⭐ " if key == star else "") + f"{emo} {t(L, 'tie_' + key)}", data)]
                 for key, emo, data in opts]
    else:
        rows.append([B("🤝 " + t(L, "btn_no_exile"), "ex:0")])
        rows.append([B("🔁 " + t(L, "tie_revote"), "revote")])
    rows.append(game_footer(L))
    return "\n".join(lines), InlineKeyboardMarkup(rows)


def view_rps(g, L):
    rps = g["rps"]
    lines = [f"✊✋✌️ <b>{t(L, 'rps_title')}</b> — {t(L, 'rps_round')} {rps['round']}\n"]
    for u in rps["duel"]:
        lines.append(f"{'✅' if u in rps['choices'] else '⏳'} {hn(g, u)}")
    if rps["log"]:
        lines.append("\n" + "\n".join(rps["log"]))
    rows = [[B("🔄 " + t(L, "btn_refresh"), "m")],
            [B("🎲 " + t(L, "btn_rps_random"), "rpsrand")],
            [B("✖️ " + t(L, "btn_rps_cancel"), "rpsx")],
            game_footer(L)]
    return "\n".join(lines), InlineKeyboardMarkup(rows)


def view_decided(g, L):
    cand = g["decided"]
    text = f"⚖️ <b>{t(L, 'decided', v=hn(g, cand))}</b>"
    rows = exile_buttons(g, L, cand)
    rows.append([B("🤝 " + t(L, "btn_no_exile"), "ex:0")])
    rows.append(game_footer(L))
    return text, InlineKeyboardMarkup(rows)


def view_over(g, L):
    title = f"{t(L, 'room')} {g['id']} — {t(L, 'game_over')}"
    if g["winner"]:
        title += " — " + loc(TEAM_NAMES, L)[g["winner"]]
    text = f"🏁 <b>{title}</b>\n\n{roles_summary(g, L, with_points=True)}"
    return text, kb([B("🔁 " + t(L, "btn_rematch"), "rematch")],
                    [B("⚙️ " + t(L, "btn_roles"), "roles"), B("🛠 " + t(L, "btn_settings"), "settings")],
                    [B("🙌 " + t(L, "btn_release"), "release")])


def view_story(g, L):
    text = f"📖 <b>{t(L, 'story_title')}</b>\n\n{render_events(g, g['events'], L)}"
    if g["notes"]:
        text += f"\n\n<i>🤫 {t(L, 'for_host')}:\n{render_notes(g, g['notes'], L)}</i>"
    rows = []
    if cfg(g)["auto_broadcast"]:
        text += f"\n\n✅ {t(L, 'auto_sent')}"
    else:
        rows.append([B("📢 " + t(L, "btn_broadcast"), "bc")])
    rows.append([B("➡️ " + t(L, "btn_next"), "m")])
    return text, InlineKeyboardMarkup(rows)


def view_endconfirm(g, L):
    return (f"⏹ <b>{t(L, 'end_confirm')}</b>",
            kb([B("✅ " + t(L, "end_yes"), "endyes")], [B("« " + t(L, "end_no"), "m")]))


def view_main(g, L):
    if g["phase"] == "lobby":
        return view_lobby(g, L)
    if g["phase"] == "over":
        return view_over(g, L)
    if g["phase"] == "night":
        return view_night(g, L)
    stage = g["vote_stage"]
    if stage == "open":
        return view_vote(g, L)
    if stage == "result":
        return view_result(g, L)
    if stage == "rps" and g["rps"]:
        return view_rps(g, L)
    if stage == "decided" and g["decided"]:
        return view_decided(g, L)
    return view_day(g, L)


VIEWS = {
    "main": view_main, "roles": view_roles, "rcard": view_rcard, "settings": view_settings,
    "players": view_players, "lineup": view_lineup, "pick": view_pick, "voters": view_voters,
    "vcancel": view_vcancel, "story": view_story, "endconfirm": view_endconfirm,
}


def render_view(g, L, view, arg=None):
    func = VIEWS.get(view, view_main)
    text, markup = func(g, L, arg) if arg is not None else func(g, L)
    if view == "main" and g["host"] and can_close(g, g["host"]):
        rows = [list(r) for r in markup.inline_keyboard]
        rows.append([B("🗑 " + t(L, "btn_close_room"), "close")])
        markup = InlineKeyboardMarkup(rows)
    return text, markup


def view_closeconfirm(g, L):
    return (f"🗑 <b>{t(L, 'close_confirm', n=g['id'])}</b>",
            kb([B("✅ " + t(L, "close_yes"), "closeyes")], [B("« " + t(L, "end_no"), "m")]))


VIEWS["closeconfirm"] = view_closeconfirm


async def send_panel(context, g):
    if not g["host"]:
        return
    L = lang_of(g["host"])
    text, markup = render_view(g, L, "main")
    msg = await notify(context, g["host"], text, markup)
    if msg:
        g["ui"] = {"msg": msg.message_id, "view": "main", "arg": None}


async def refresh_panel(context, g):
    """Обновляет панель ведущего, если он сейчас смотрит на главный экран."""
    ui = g.get("ui") or {}
    if not g["host"] or not ui.get("msg") or ui.get("view") != "main":
        return
    text, markup = render_view(g, lang_of(g["host"]), "main")
    await edit(context, g["host"], ui["msg"], text, markup)


# ======================== КОМНАТЫ: ВХОД, ВЫХОД, ВЕДУЩИЙ ========================
def can_leave(g, uid):
    return not (in_game(g) and is_alive_player(g, uid))


async def enter_room(context, uid, rid):
    """Возвращает (комната, ключ ошибки или None)."""
    current = room_of(uid)
    if current and current["id"] == rid:
        return current, None
    if current:
        if not can_leave(current, uid):
            return None, "cant_leave_alive"
        await leave_room(context, uid)
    g = ROOMS.get(rid)
    if not g:
        g = new_room(rid)
        ROOMS[rid] = g
    g["members"].append(uid)
    ROOM_OF[uid] = rid
    if g["phase"] == "lobby":
        nick = add_player(g, uid)
        if g["host"]:
            await notify(context, g["host"], "➕ " + t(lang_of(g["host"]), "player_joined",
                                                       v=html.escape(nick), n=len(g["order"])))
    touch(g)
    save_room(g)
    await refresh_panel(context, g)
    return g, None


async def leave_room(context, uid):
    g = room_of(uid)
    if not g:
        return
    if g["host"] == uid:
        await release_host(context, g, uid, quiet=True)
    if g["phase"] == "lobby":
        remove_player(g, uid)
    g["members"].remove(uid)
    ROOM_OF.pop(uid, None)
    if not g["members"]:
        delete_room(g)
        return
    if g["host"]:
        await notify(context, g["host"], "➖ " + t(lang_of(g["host"]), "player_left", v=nm(g, uid)))
    touch(g)
    save_room(g)
    await refresh_panel(context, g)


async def take_host(context, g, uid, force=False):
    if g["host"] and not force:
        return "host_taken_already"
    if in_game(g) and is_alive_player(g, uid):
        return "cant_host_alive"
    old = g["host"]
    if g["phase"] == "lobby":
        remove_player(g, uid)
    g["host"] = uid
    g["last_host"] = uid
    g["ui"] = {}
    touch(g)
    if old and old != uid:
        await notify(context, old, "👑 " + t(lang_of(old), "host_taken_by_owner"))
    await notify_members(context, g, "new_host", exclude=(uid,), v=nm(g, uid))
    await notify(context, uid, "👑 " + t(lang_of(uid), "you_are_host"))
    await send_panel(context, g)
    save_room(g)
    return None


async def release_host(context, g, uid, quiet=False):
    g["host"] = None
    g["ui"] = {}
    touch(g)
    key = "host_released_game" if in_game(g) else "host_released"
    await notify_members(context, g, key, exclude=(uid,), v=nm(g, uid))
    if not quiet:
        await notify(context, uid, "🙌 " + t(lang_of(uid), "you_released"))
    save_room(g)


# ======================== ХОД ИГРЫ ========================
async def deal(context, g, L):
    n = len(g["order"])
    if n < 3:
        return t(L, "need_3")
    g["cfg"] = copy.deepcopy(prefs(g["host"]))
    roles, dropped = plan_roles(g, n)
    random.shuffle(roles)
    for uid, role in zip(g["order"], roles):
        g["players"][uid].update(role=role, alive=True)
    first_night = g["cfg"]["first_phase"] == "night"
    g.update(round=1 if first_night else 0, phase="night" if first_night else "day",
             started_at=iso(now_utc()))

    failed = []
    for uid in g["order"]:
        if not await notify(context, uid, role_message(g, uid, lang_of(uid))):
            failed.append(nm(g, uid))
    for uid in g["members"]:
        if uid not in g["players"] and uid != g["host"]:
            await notify(context, uid, "🎲 " + t(lang_of(uid), "game_started_watch"))

    msg = f"🎲 <b>{t(L, 'roles_dealt')}</b>\n\n{roles_summary(g, L)}"
    if dropped:
        msg += "\n\n⚠️ " + t(L, "dropped", roles=", ".join(role_name(r, L) for r in dropped))
    if failed:
        msg += "\n\n⚠️ " + t(L, "dm_failed", v=", ".join(failed))
    await notify(context, g["host"], msg)
    return None


async def turncoat_check(context, g, notes):
    if g["turned"]:
        return
    if not any(role_of(g, u) == "mafia" and not P(g, u)["alive"] for u in g["order"]):
        return
    turncoats = [u for u in alive(g) if role_of(g, u) == "turncoat"]
    if not turncoats:
        return
    g["turned"] = True
    for tc in turncoats:
        notes.append(("note_turned", {"v": tc}))
        await notify(context, tc, "🐺 " + t(lang_of(tc), "you_turned") + "\n\n"
                     + role_message(g, tc, lang_of(tc)))
        for u in alive(g):
            if u != tc and in_circle(g, u):
                lang = lang_of(u)
                await notify(context, u, "🐺 " + gfmt(t(lang, "turncoat_joined", v=nm(g, tc)),
                                                      P(g, tc)["gender"]))


async def apply_night(context, g, L):
    out = resolve(g)
    for d in out["deaths"]:
        P(g, d)["alive"] = False
    g["lucky_used"] += out["lucky_used"]
    for u in alive(g):
        if role_of(g, u) == "doctor":
            if g["night"].get(u):
                g["last_heal"][u] = g["night"][u]
            else:
                g["last_heal"].pop(u, None)
    g["lawyer_found"] += [u for u, (_, ok) in out["lawyer"].items() if ok]
    for uid, key in out["points"]:
        add_points(g, uid, key)

    for d in out["deaths"]:
        await notify(context, d, "💀 " + t(lang_of(d), "dead_night"))
    for u in out["lucky_used"]:
        await notify(context, u, "🍀 " + t(lang_of(u), "lucky_saved"))
    if g["cfg"]["detective_dm"]:
        for u, (tg, is_mafia) in out["checks"].items():
            lang = lang_of(u)
            res = t(lang, "res_mafia") if is_mafia else t(lang, "res_town")
            await notify(context, u, "🔍 " + t(lang, "dm_check", v=nm(g, tg), res=res))
    if g["cfg"]["lawyer_dm"]:
        for u, (tg, ok) in out["lawyer"].items():
            lang = lang_of(u)
            await notify(context, u, "⚖️ " + t(lang, "dm_lawyer_ok" if ok else "dm_lawyer_no",
                                               v=nm(g, tg)))

    notes = out["notes"]
    for u, (tg, is_mafia) in out["checks"].items():
        notes.append(("note_check_mafia" if is_mafia else "note_check_town", {"d": u, "v": tg}))
    for u, (tg, ok) in out["lawyer"].items():
        notes.append(("note_lawyer_ok" if ok else "note_lawyer_no", {"d": u, "v": tg}))
    await turncoat_check(context, g, notes)

    events = [{"k": "night_header", "r": g["round"]}] + out["events"]
    g.update(phase="day", night={}, votes={}, vote_stage=None)
    return await finish_story(context, g, events, notes)


# ---------- голосование ----------
def ballot(g, uid):
    lang = lang_of(uid)
    if uid in g["votes"]:
        text = "🗳 " + t(lang, "your_vote", v=nm(g, g["votes"][uid])) + "\n\n" + t(lang, "your_vote_hint")
        return text, kb([B("↩️ " + t(lang, "btn_cancel_my_vote"), "v:x")])
    text = f"🗳 <b>{t(lang, 'ballot_title')}</b>\n\n{t(lang, 'ballot_hint')}"
    return text, InlineKeyboardMarkup(grid([B(P(g, c)["nick"], f"v:{c}")
                                            for c in alive(g) if c != uid]))


async def send_ballots(context, g):
    for uid in alive(g):
        text, markup = ballot(g, uid)
        msg = await notify(context, uid, text, markup)
        if msg:
            g["vote_msgs"][uid] = msg.message_id


async def close_ballots(context, g):
    for uid, msg_id in g["vote_msgs"].items():
        lang = lang_of(uid)
        cand = g["votes"].get(uid)
        text = "🔒 " + t(lang, "vote_closed")
        if cand and is_alive_player(g, cand):
            text += "\n" + t(lang, "your_vote", v=nm(g, cand))
        await edit(context, uid, msg_id, text)
    g["vote_msgs"] = {}


async def open_vote(context, g, revote=False):
    g["vote_stage"] = "open"
    g["rps"] = None
    g["decided"] = None
    if revote and not any(e["k"] == "tie_revote" for e in g["tie_log"]):
        g["tie_log"].append({"k": "tie_revote"})
    if g["cfg"]["vote_mode"] == "phones":
        await send_ballots(context, g)


async def on_ballot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    uid = q.from_user.id
    lang = lang_of(uid)
    g = room_of(uid)
    if not g or g["phase"] != "day" or g["vote_stage"] != "open" or not is_alive_player(g, uid):
        await q.answer(t(lang, "vote_not_open"), show_alert=True)
        await safe_edit(q, "🔒 " + t(lang, "vote_closed"), None)
        return
    arg = q.data[2:]
    if arg == "x":
        g["votes"].pop(uid, None)
    else:
        cand = int(arg)
        if uid in g["votes"]:
            await q.answer(t(lang, "already_voted"), show_alert=True)
            return
        if not is_alive_player(g, cand) or cand == uid:
            await q.answer()
            return
        g["votes"][uid] = cand
    await q.answer()
    g["vote_msgs"][uid] = q.message.message_id
    text, markup = ballot(g, uid)
    await safe_edit(q, text, markup)
    touch(g)
    save_room(g)
    await refresh_panel(context, g)


# ---------- ничья: камень, ножницы, бумага ----------
def rps_prompt(g, uid):
    lang = lang_of(uid)
    rps = g["rps"]
    rivals = ", ".join(nm(g, u) for u in rps["duel"] if u != uid)
    text = (f"✊✋✌️ <b>{t(lang, 'rps_title')}</b> — {t(lang, 'rps_round')} {rps['round']}\n\n"
            + t(lang, "rps_prompt", v=rivals))
    r = rps["round"]
    return text, kb([B("✊", f"r:{r}:r"), B("✋", f"r:{r}:p"), B("✌️", f"r:{r}:s")])


async def rps_send_round(context, g):
    g["rps"]["choices"] = {}
    for uid in g["rps"]["duel"]:
        text, markup = rps_prompt(g, uid)
        await notify(context, uid, text, markup)


async def rps_start(context, g):
    g["rps"] = {"duel": leaders(g), "choices": {}, "round": 1, "log": []}
    g["vote_stage"] = "rps"
    await rps_send_round(context, g)


async def rps_resolve(context, g):
    rps = g["rps"]
    ch = rps["choices"]
    line = " · ".join(f"{nm(g, u)} {RPS_EMOJI[ch[u]]}" for u in rps["duel"])
    symbols = set(ch.values())
    if len(symbols) != 2:
        rps["log"].append(line + " — 🔁")
        rps["round"] += 1
        await rps_send_round(context, g)
        return
    a, b = symbols
    winner = a if RPS_BEATS[a] == b else b
    losers = [u for u in rps["duel"] if ch[u] != winner]
    rps["log"].append(line)
    for u in rps["duel"]:
        if u not in losers:
            await notify(context, u, "✊✋✌️ " + t(lang_of(u), "rps_you_safe") + f"\n{line}")
    rps["duel"] = losers
    if len(losers) == 1:
        loser = losers[0]
        await notify(context, loser, "✊✋✌️ " + t(lang_of(loser), "rps_you_lost") + f"\n{line}")
        g["tie_log"].append({"k": "tie_rps", "v": loser, "x": "\n".join(rps["log"])})
        g["decided"] = loser
        g["vote_stage"] = "decided"
    else:
        rps["round"] += 1
        await rps_send_round(context, g)


async def on_rps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    uid = q.from_user.id
    lang = lang_of(uid)
    g = room_of(uid)
    _, rnd, choice = q.data.split(":")
    rps = g["rps"] if g and g["vote_stage"] == "rps" else None
    if not rps or uid not in rps["duel"] or int(rnd) != rps["round"] or uid in rps["choices"]:
        await q.answer(t(lang, "rps_expired"), show_alert=True)
        return
    await q.answer()
    rps["choices"][uid] = choice
    await safe_edit(q, t(lang, "rps_chosen", v=RPS_EMOJI[choice]), None)
    if len(rps["choices"]) == len(rps["duel"]):
        await rps_resolve(context, g)
    touch(g)
    save_room(g)
    await refresh_panel(context, g)


# ---------- ничья: кубик ----------
async def roll_dice(context, g, L):
    cands = leaders(g)
    n = len(cands)
    if n > 6:
        chosen = random.choice(cands)
        g["tie_log"].append({"k": "tie_random", "v": chosen})
    else:
        allowed = 6 - 6 % n
        mapping = []
        for i, c in enumerate(cands):
            faces = ", ".join(str(v) for v in range(1, allowed + 1) if (v - 1) % n == i)
            mapping.append(f"{faces} → {nm(g, c)}")
        mapping_text = "\n".join(mapping)
        for uid in g["members"]:
            await notify(context, uid, f"🎲 <b>{t(lang_of(uid), 'dice_title')}</b>\n\n{mapping_text}")
        chosen, value = None, None
        for _ in range(10):
            try:
                msg = await context.bot.send_dice(g["host"], emoji="🎲")
            except (Forbidden, BadRequest):
                break
            value = msg.dice.value
            for uid in g["members"]:
                if uid != g["host"]:
                    try:
                        await context.bot.forward_message(uid, g["host"], msg.message_id)
                    except (Forbidden, BadRequest):
                        pass
            if value <= allowed:
                chosen = cands[(value - 1) % n]
                break
        if chosen is None:
            chosen = random.choice(cands)
            g["tie_log"].append({"k": "tie_random", "v": chosen})
        else:
            g["tie_log"].append({"k": "tie_dice", "v": chosen, "x": f"🎲 {value}\n{mapping_text}"})
    g["decided"] = chosen
    g["vote_stage"] = "decided"


# ---------- итог дня ----------
async def finalize_day(context, g, L, target, mayor=False):
    await close_ballots(context, g)
    for voter, cand in g["votes"].items():
        if is_alive_player(g, voter) and team_of(g, voter) == "town" and team_of(g, cand) == "mafia":
            add_points(g, voter, "vote")

    events = [{"k": "day_header", "r": g["round"]}] + g["tie_log"]
    notes = []
    if mayor and target:
        g["mayor_used"] = True
        events.append({"k": "mayor", "v": target})
        notes.append(("note_mayor", {"v": target}))
    elif target and is_alive_player(g, target):
        P(g, target)["alive"] = False
        events.append({"k": "exile", "v": target, "reveal": True})
        await notify(context, target, "🗳 " + t(lang_of(target), "dead_day"))
        await turncoat_check(context, g, notes)
    else:
        events.append({"k": "no_exile"})

    g["round"] += 1
    g.update(phase="night", night={}, votes={}, vote_stage=None, tie_log=[], rps=None, decided=None)
    return await finish_story(context, g, events, notes)


async def finish_story(context, g, events, notes):
    winner = check_winner(g)
    if winner:
        events.append({"k": f"win_{winner}"})
        end_game(g, winner)
    for e in events:
        e.setdefault("i", random.randrange(1000))
    g["events"] = events
    g["notes"] = notes
    if g["cfg"]["auto_broadcast"]:
        await broadcast(context, g)
    return "story"


def end_game(g, winner):
    g["phase"] = "over"
    g["winner"] = winner
    cur = DB.execute("INSERT INTO games (started_at, ended_at, winner, host_id, players) "
                     "VALUES (?, ?, ?, ?, ?)",
                     (g["started_at"], iso(now_utc()), winner, g["host"], len(g["order"])))
    game_id = cur.lastrowid
    for u in g["order"]:
        p = P(g, u)
        won = team_of(g, u) == winner
        if won:
            add_points(g, u, "win")
        if p["alive"]:
            add_points(g, u, "survive")
        DB.execute("INSERT INTO game_players (game_id, uid, nick, role, team, survived, won, points) "
                   "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                   (game_id, u, p["nick"], p["role"], team_of(g, u), int(p["alive"]), int(won),
                    g["points"].get(u, 0)))
    DB.commit()


async def close_room(context, g, by_uid=None):
    """Закрывает комнату: прерывает игру, всех возвращает к списку комнат."""
    if in_game(g):
        await close_ballots(context, g)
    for uid in list(g["members"]):
        lang = lang_of(uid)
        if by_uid:
            text = t(lang, "room_closed_by", n=g["id"], v=nm(g, by_uid))
        else:
            text = t(lang, "room_closed_idle", n=g["id"])
        ROOM_OF.pop(uid, None)
        await notify(context, uid, "🗑 " + text,
                     kb([B("🏘 " + t(lang, "rooms_title"), "rm:list")]))
    delete_room(g)


async def cleanup_rooms(context):
    for g in list(ROOMS.values()):
        idle = idle_time(g)
        if idle >= ROOM_IDLE_DELETE:
            await close_room(context, g)
        elif idle >= ROOM_IDLE_WARN and not g["warned"]:
            g["warned"] = True
            save_room(g)
            for uid in g["members"]:
                lang = lang_of(uid)
                await notify(context, uid, "⏰ " + t(lang, "room_idle_warning", n=g["id"]),
                             kb([B("✋ " + t(lang, "btn_keep_room"), "rm:keep")]))


async def cleanup_loop(app):
    context = type("Ctx", (), {"bot": app.bot})()
    while True:
        try:
            await cleanup_rooms(context)
        except Exception:
            logging.exception("Ошибка при очистке комнат")
        await asyncio.sleep(CLEANUP_EVERY)


async def abort_game(context, g, by_uid):
    await close_ballots(context, g)
    who = nm(g, by_uid)
    reset_game(g)
    touch(g)
    for uid in g["members"]:
        await notify(context, uid, "⏹ " + t(lang_of(uid), "game_aborted", v=who))
    save_room(g)


async def broadcast(context, g):
    sent = 0
    for uid in g["members"]:
        if await notify(context, uid, render_events(g, g["events"], lang_of(uid))):
            sent += 1
    return sent


# ======================== КНОПКИ ВЕДУЩЕГО ========================
def parse_actor(raw):
    return "mafia" if raw == "mafia" else int(raw)


# Нажатия, которые только листают экраны и не считаются активностью в комнате
NAV_CMDS = {"m", "roles", "rcard", "settings", "players", "lineup", "na", "vc",
            "vcancel", "end", "close", "preset", "rc", "st"}


async def host_action(context, g, uid, L, data):
    """Возвращает (экран, аргумент, всплывающее сообщение)."""
    cmd, *parts = data.split(":")
    ph = g["phase"]
    stage = g["vote_stage"]

    if cmd == "m":
        return "main", None, None
    if cmd == "bc":
        return "keep", None, t(L, "broadcast_done", n=await broadcast(context, g))
    if cmd == "release":
        await release_host(context, g, uid)
        return "released", None, None
    if cmd == "end" and in_game(g):
        return "endconfirm", None, None
    if cmd == "endyes" and in_game(g):
        await abort_game(context, g, uid)
        return "main", None, None
    if cmd == "lineup" and in_game(g):
        return "lineup", None, None
    if cmd == "close" and can_close(g, uid):
        return "closeconfirm", None, None
    if cmd == "closeyes" and can_close(g, uid):
        await close_room(context, g, uid)
        return "closed", None, None

    if ph in ("lobby", "over"):
        p = prefs(uid)
        if cmd == "roles":
            return "roles", None, None
        if cmd == "rcard":
            return "rcard", parts[0], None
        if cmd == "preset":
            p["counts"] = dict(p["custom"] if parts[0] == "custom" else PRESETS[parts[0]])
            p["preset"] = parts[0]
            save_prefs(uid)
            return "roles", None, None
        if cmd == "rc":
            role, op = parts
            c = p["counts"]
            if op == "auto":
                c["mafia"] = 0
            else:
                cur = c.get(role, 0)
                if role == "mafia" and cur == 0:
                    cur = mafia_count(g, max(len(g["order"]), 3))
                low = 1 if role == "mafia" else 0
                c[role] = max(low, min(MAX_COUNT.get(role, 1), cur + (1 if op == "+" else -1)))
            p["preset"] = "custom"
            p["custom"] = dict(c)
            save_prefs(uid)
            return "rcard", role, None
        if cmd == "settings":
            return "settings", None, None
        if cmd == "st":
            options = SETTINGS_SPEC[parts[0]]
            p[parts[0]] = options[(options.index(p[parts[0]]) + 1) % len(options)]
            save_prefs(uid)
            return "settings", None, None

    if ph == "lobby":
        if cmd == "players":
            return "players", None, None
        if cmd == "kick":
            kid = int(parts[0])
            if kid in g["players"]:
                remove_player(g, kid)
                await notify(context, kid, t(lang_of(kid), "kicked"))
            return "players", None, None
        if cmd == "deal":
            err = await deal(context, g, L)
            return ("sent", None, None) if not err else ("main", None, err)

    if ph == "over" and cmd == "rematch":
        reset_game(g)
        for p_uid in g["order"]:
            await notify(context, p_uid, "🔁 " + t(lang_of(p_uid), "rematch"))
        return "main", None, None

    if ph == "night":
        if cmd in ("na", "nt"):
            actor = parse_actor(parts[0])
            if actor != "mafia" and actor not in night_actors(g):
                return "main", None, None
            if cmd == "na":
                return "pick", actor, None
            target = int(parts[1])
            if actor != "mafia" and role_of(g, actor) == "driver":
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
                return ("main" if len(pair) == 2 else "pick"), (None if len(pair) == 2 else actor), None
            if target:
                g["night"][actor] = target
            else:
                g["night"].pop(actor, None)
            return "main", None, None
        if cmd == "endnight":
            return await apply_night(context, g, L), None, None

    if ph == "day":
        if cmd == "nightstart" and g["round"] == 0:
            g.update(phase="night", round=1, night={})
            return "main", None, None
        if cmd == "vopen" and stage is None:
            await open_vote(context, g)
            return "main", None, None
        if stage == "open":
            if cmd == "vc":
                return "voters", int(parts[0]), None
            if cmd == "vt":
                cand, voter = int(parts[0]), int(parts[1])
                if voter in g["votes"]:
                    return "voters", cand, t(L, "already_voted_host")
                if is_alive_player(g, cand) and is_alive_player(g, voter):
                    g["votes"][voter] = cand
                return "voters", cand, None
            if cmd == "vcancel":
                return "vcancel", None, None
            if cmd == "vx":
                voter = int(parts[0])
                g["votes"].pop(voter, None)
                if voter in g["vote_msgs"]:
                    text, markup = ballot(g, voter)
                    await edit(context, voter, g["vote_msgs"][voter], text, markup)
                return "vcancel", None, None
            if cmd == "vclose":
                await close_ballots(context, g)
                g["vote_stage"] = "result"
                return "main", None, None
        if stage == "result":
            if cmd == "revote":
                await open_vote(context, g, revote=True)
                return "main", None, None
            if cmd == "rps" and len(leaders(g)) > 1:
                await rps_start(context, g)
                return "main", None, None
            if cmd == "dice" and len(leaders(g)) > 1:
                await roll_dice(context, g, L)
                return "main", None, None
        if stage == "rps" and g["rps"]:
            if cmd == "rpsrand":
                for u in g["rps"]["duel"]:
                    g["rps"]["choices"].setdefault(u, random.choice("rps"))
                await rps_resolve(context, g)
                return "main", None, None
            if cmd == "rpsx":
                for u in g["rps"]["duel"]:
                    await notify(context, u, t(lang_of(u), "rps_cancelled"))
                g.update(rps=None, vote_stage="result")
                return "main", None, None
        if stage in ("result", "decided"):
            if cmd == "ex":
                return await finalize_day(context, g, L, int(parts[0]) or None), None, None
            if cmd == "mayor" and mayor_available(g):
                return await finalize_day(context, g, L, int(parts[0]), mayor=True), None, None
    return "main", None, None


async def on_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    data = q.data
    uid = q.from_user.id
    ensure_user(q.from_user)
    if data == "noop":
        await q.answer()
        return
    for prefix, handler in (("p:", on_player_button), ("go:", on_go), ("rm:", on_room_button),
                            ("v:", on_ballot), ("r:", on_rps), ("own:", on_owner_button),
                            ("rl:", on_roles_button)):
        if data.startswith(prefix):
            await handler(update, context)
            return

    g = room_of(uid)
    L = lang_of(uid)
    if not g or g["host"] != uid:
        await q.answer(t(L, "only_host"), show_alert=True)
        return
    view, arg, alert = await host_action(context, g, uid, L, data)
    await q.answer(alert, show_alert=bool(alert))
    if view == "closed":
        text, markup = rooms_screen(uid)
        await safe_edit(q, text, markup)
        return
    if data.split(":")[0] not in NAV_CMDS:
        touch(g)
    if view == "keep":
        return
    if view == "released":
        text, markup = room_screen(g, uid)
        await safe_edit(q, text, markup)
        return
    if view == "sent":
        await safe_edit(q, "✅ " + t(L, "roles_dealt"), None)
        await send_panel(context, g)
        save_room(g)
        return
    text, markup = render_view(g, L, view, arg)
    await safe_edit(q, text, markup)
    g["ui"] = {"msg": q.message.message_id, "view": view, "arg": arg}
    save_room(g)


# ======================== КНОПКИ УЧАСТНИКОВ КОМНАТЫ ========================
async def show_home(context, uid):
    """Главный экран: панель ведущего, экран комнаты или список комнат."""
    g = room_of(uid)
    if g and g["host"] == uid:
        await send_panel(context, g)
        save_room(g)
        return
    text, markup = room_screen(g, uid) if g else rooms_screen(uid)
    await notify(context, uid, text, markup)


async def on_go(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    uid = q.from_user.id
    g, err = await enter_room(context, uid, int(q.data[3:]))
    if err:
        await q.answer(t(lang_of(uid), err), show_alert=True)
        return
    await q.answer()
    text, markup = room_screen(g, uid)
    await safe_edit(q, text, markup)


async def on_room_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    uid = q.from_user.id
    lang = lang_of(uid)
    action = q.data[3:]
    g = room_of(uid)
    if action == "list" or not g:
        await q.answer()
        text, markup = rooms_screen(uid)
        await safe_edit(q, text, markup)
        return
    if g["host"] == uid:
        await q.answer()
        await send_panel(context, g)
        return

    alert = None
    if action == "close":
        if not can_close(g, uid):
            await q.answer(t(lang, "cant_close_yet"), show_alert=True)
            return
        await q.answer()
        await safe_edit(q, f"🗑 <b>{t(lang, 'close_confirm', n=g['id'])}</b>",
                        kb([B("✅ " + t(lang, "close_yes"), "rm:closeyes")],
                           [B("« " + t(lang, "end_no"), "rm:show")]))
        return
    if action == "closeyes":
        if not can_close(g, uid):
            await q.answer(t(lang, "cant_close_yet"), show_alert=True)
            return
        await q.answer()
        await close_room(context, g, uid)
        text, markup = rooms_screen(uid)
        await safe_edit(q, text, markup)
        return
    if action == "keep":
        touch(g)
        save_room(g)
        await q.answer(t(lang, "room_kept"), show_alert=True)
        return
    if action in ("play", "watch", "take", "endyes"):
        touch(g)
    if action == "play" and g["phase"] == "lobby" and uid not in g["players"]:
        nick = add_player(g, uid)
        if g["host"]:
            await notify(context, g["host"], "➕ " + t(lang_of(g["host"]), "player_joined",
                                                       v=html.escape(nick), n=len(g["order"])))
    elif action == "watch" and g["phase"] == "lobby":
        remove_player(g, uid)
    elif action == "take":
        err = await take_host(context, g, uid)
        if err:
            alert = t(lang, err)
        else:
            await q.answer()
            await safe_edit(q, "👑 " + t(lang, "you_are_host"), None)
            return
    elif action == "leave":
        if not can_leave(g, uid):
            alert = t(lang, "cant_leave_alive")
        else:
            await leave_room(context, uid)
            await q.answer()
            text, markup = rooms_screen(uid)
            await safe_edit(q, text, markup)
            return
    elif action == "role" and uid in g["players"] and P(g, uid)["role"]:
        await notify(context, uid, role_message(g, uid, lang))
    elif action == "end" and in_game(g) and not g["host"]:
        await q.answer()
        await safe_edit(q, f"⏹ <b>{t(lang, 'end_confirm')}</b>",
                        kb([B("✅ " + t(lang, "end_yes"), "rm:endyes")],
                           [B("« " + t(lang, "end_no"), "rm:show")]))
        return
    elif action == "endyes" and in_game(g) and not g["host"]:
        await abort_game(context, g, uid)

    await q.answer(alert, show_alert=bool(alert))
    save_room(g)
    await refresh_panel(context, g)
    text, markup = room_screen(g, uid)
    await safe_edit(q, text, markup)


async def on_owner_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Владелец может закрыть любую комнату в любой момент."""
    q = update.callback_query
    uid = q.from_user.id
    lang = lang_of(uid)
    if uid != OWNER_ID:
        await q.answer(t(lang, "owner_only"), show_alert=True)
        return
    _, action, rid = q.data.split(":")
    g = ROOMS.get(int(rid))
    await q.answer()
    if g and action == "close":
        await safe_edit(q, f"🗑 <b>{t(lang, 'close_confirm', n=g['id'])}</b>",
                        kb([B("✅ " + t(lang, "close_yes"), f"own:closeyes:{rid}")],
                           [B("« " + t(lang, "end_no"), "rm:list")]))
        return
    if g and action == "closeyes":
        await close_room(context, g, uid)
    text, markup = rooms_screen(uid)
    await safe_edit(q, text, markup)


# ======================== ПРОФИЛЬ ИГРОКА ========================
def profile_menu(lang):
    return kb(
        [B("🎭 " + t(lang, "btn_nick"), "p:nick"), B("✏️ " + t(lang, "btn_name"), "p:name")],
        [B("⚧ " + t(lang, "btn_gender"), "p:gender"), B("🌐 " + t(lang, "btn_lang"), "p:lang")],
        [B("📷 " + t(lang, "btn_photo"), "p:photo"), B("📜 " + t(lang, "btn_games"), "p:games")],
        [B("🏘 " + t(lang, "rooms_title"), "rm:list"), roles_button(lang)],
    )


def user_games(uid):
    return DB.execute(
        "SELECT g.started_at, gp.role, gp.won, gp.points, gp.survived "
        "FROM game_players gp JOIN games g ON g.id = gp.game_id "
        "WHERE gp.uid = ? ORDER BY g.started_at DESC", (uid,)).fetchall()


def profile_text(uid):
    user = get_user(uid)
    lang = user["lang"]
    games = user_games(uid)
    total = sum(gm["points"] for gm in games)
    wins = sum(gm["won"] for gm in games)
    last = games[0]["points"] if games else "—"
    reg = local(user["registered_at"])
    gender = t(lang, f"gender_{user['gender'] or 'none'}")
    real = html.escape(user["real_name"] or "—")
    text = (f"👤 <b>{t(lang, 'profile')}</b>\n\n"
            f"🎭 {t(lang, 'nick')}: <b>{html.escape(user['nick'])}</b>\n"
            f"✏️ {t(lang, 'real_name')}: {real}\n"
            f"⚧ {t(lang, 'gender')}: {gender}\n"
            f"🌐 {t(lang, 'language')}: {loc(LANG_NAMES, lang)}\n\n"
            f"📅 {t(lang, 'registered')}: {reg:%d.%m.%Y}\n"
            f"⏳ {t(lang, 'tenure')}: {tenure(reg.date(), datetime.now(TZ).date(), lang)}\n\n"
            f"🏆 {t(lang, 'points_total')}: <b>{total}</b>\n"
            f"🎯 {t(lang, 'points_last')}: {last}\n"
            f"🎮 {t(lang, 'games_played')}: {len(games)} · {t(lang, 'wins')}: {wins}")
    g = room_of(uid)
    if g:
        text += f"\n\n📍 {t(lang, 'room')} {g['id']}"
    return text


async def send_profile(context, uid):
    user = get_user(uid)
    text, markup = profile_text(uid), profile_menu(user["lang"])
    if user["photo_id"]:
        try:
            await context.bot.send_photo(uid, user["photo_id"], caption=text,
                                         parse_mode=HTML, reply_markup=markup)
            return
        except BadRequest:
            update_user(uid, photo_id=None)
    await notify(context, uid, text, markup)


def games_text(uid):
    lang = lang_of(uid)
    gender = get_user(uid)["gender"]
    rows = user_games(uid)
    if not rows:
        return t(lang, "no_games")
    lines = [f"📜 <b>{t(lang, 'btn_games')}</b> ({len(rows)})\n"]
    for gm in rows[:20]:
        when = local(gm["started_at"])
        result = "🏆" if gm["won"] else "✖️"
        lines.append(f"{when:%d.%m.%Y %H:%M} · {role_name(gm['role'], lang, gender)} · "
                     f"{result} · <b>{gm['points']}</b> {t(lang, 'pts')}")
    if len(rows) > 20:
        lines.append(f"\n<i>{t(lang, 'games_more', n=len(rows) - 20)}</i>")
    return "\n".join(lines)


async def apply_nick(update, context, text):
    uid = update.effective_user.id
    lang = lang_of(uid)
    nick = " ".join(text.split())
    g = room_of(uid)
    if not NICK_MIN <= len(nick) <= NICK_MAX or nick.startswith("/"):
        await update.effective_message.reply_text("⚠️ " + t(lang, "bad_nick", a=NICK_MIN, b=NICK_MAX))
        return
    if g and uid in g["players"] and in_game(g):
        await update.effective_message.reply_text("⏳ " + t(lang, "nick_after_game"))
        return
    if g and nick_taken(g, nick, uid):
        await update.effective_message.reply_text("⚠️ " + t(lang, "nick_taken"))
        return
    old = get_user(uid)["nick"]
    update_user(uid, nick=nick)
    if g and uid in g["players"]:
        P(g, uid)["nick"] = nick
        touch(g)
        save_room(g)
        if g["host"] and old != nick:
            await notify(context, g["host"], "✏️ " + t(lang_of(g["host"]), "nick_changed",
                                                       a=html.escape(old), b=html.escape(nick)))
        await refresh_panel(context, g)
    await update.effective_message.reply_text(
        "✅ " + t(lang, "nick_saved", v=html.escape(nick)), parse_mode=HTML,
        reply_markup=profile_menu(lang))


async def apply_real_name(update, context, text):
    uid = update.effective_user.id
    lang = lang_of(uid)
    name = " ".join(text.split())[:REALNAME_MAX]
    if not name or name.startswith("/"):
        await update.effective_message.reply_text("⚠️ " + t(lang, "bad_name"))
        return
    update_user(uid, real_name=name)
    await update.effective_message.reply_text(
        "✅ " + t(lang, "name_saved", v=html.escape(name)), parse_mode=HTML,
        reply_markup=profile_menu(lang))


async def on_player_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    uid = q.from_user.id
    lang = lang_of(uid)
    await q.answer()
    data = q.data
    if data == "p:profile":
        await send_profile(context, uid)
    elif data == "p:nick":
        context.user_data["awaiting"] = "nick"
        await notify(context, uid, "🎭 " + t(lang, "ask_nick", a=NICK_MIN, b=NICK_MAX))
    elif data == "p:name":
        context.user_data["awaiting"] = "name"
        await notify(context, uid, "✏️ " + t(lang, "ask_name"))
    elif data == "p:gender":
        await notify(context, uid, "⚧ " + t(lang, "ask_gender"), kb(
            [B(t(lang, "gender_m"), "p:g:m"), B(t(lang, "gender_f"), "p:g:f")],
            [B(t(lang, "gender_none"), "p:g:none")]))
    elif data.startswith("p:g:"):
        key = data[4:]
        gender = None if key == "none" else key
        update_user(uid, gender=gender)
        g = room_of(uid)
        if g and uid in g["players"] and not in_game(g):
            P(g, uid)["gender"] = gender
            save_room(g)
        await notify(context, uid, "✅ " + t(lang, "gender_saved", v=t(lang, f"gender_{key}")),
                     profile_menu(lang))
    elif data == "p:lang":
        buttons = [B(("✓ " if code == lang else "") + name, f"p:L:{code}")
                   for code, name in LANG_NAMES.items()]
        await notify(context, uid, "🌐 " + t(lang, "ask_lang"), InlineKeyboardMarkup(grid(buttons)))
    elif data.startswith("p:L:") and data[4:] in LANG_NAMES:
        new = data[4:]
        update_user(uid, lang=new)
        await notify(context, uid, "✅ " + t(new, "lang_saved"), profile_menu(new))
    elif data == "p:photo":
        context.user_data["awaiting"] = "photo"
        has_photo = get_user(uid)["photo_id"]
        await notify(context, uid, "📷 " + t(lang, "ask_photo"),
                     kb([B("🗑 " + t(lang, "delete_photo"), "p:delphoto")]) if has_photo else None)
    elif data == "p:delphoto":
        context.user_data.pop("awaiting", None)
        update_user(uid, photo_id=None)
        await notify(context, uid, "✅ " + t(lang, "photo_deleted"), profile_menu(lang))
    elif data == "p:games":
        await notify(context, uid, games_text(uid))


async def on_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ensure_user(update.effective_user)
    awaiting = context.user_data.pop("awaiting", None)
    if awaiting == "nick":
        await apply_nick(update, context, update.message.text)
    elif awaiting == "name":
        await apply_real_name(update, context, update.message.text)
    else:
        if awaiting == "photo":
            context.user_data["awaiting"] = "photo"
        await update.message.reply_text(t(lang_of(update.effective_user.id), "help_short"))


async def on_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    ensure_user(update.effective_user)
    lang = lang_of(uid)
    if context.user_data.get("awaiting") != "photo":
        await update.message.reply_text(t(lang, "photo_hint"))
        return
    context.user_data.pop("awaiting", None)
    update_user(uid, photo_id=update.message.photo[-1].file_id)
    await update.message.reply_text("✅ " + t(lang, "photo_saved"))
    await send_profile(context, uid)


# ======================== КОМАНДЫ ========================
async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    ensure_user(user)
    if OWNER_ID == 0:
        await update.message.reply_text(
            f"Telegram ID: <code>{user.id}</code>\n\n"
            "Добавьте в .env строку HOST_ID=этот_номер и перезапустите бота.", parse_mode=HTML)
        return
    payload = context.args[0] if context.args else ""
    if payload.startswith("room") and payload[4:].isdigit():
        g, err = await enter_room(context, user.id, int(payload[4:]))
        if err:
            await update.message.reply_text(t(lang_of(user.id), err))
            return
    await show_home(context, user.id)


async def cmd_rooms(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ensure_user(update.effective_user)
    text, markup = rooms_screen(update.effective_user.id)
    await update.message.reply_text(text, parse_mode=HTML, reply_markup=markup)


async def cmd_roles(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ensure_user(update.effective_user)
    text, markup = roles_guide(update.effective_user.id)
    await update.message.reply_text(text, parse_mode=HTML, reply_markup=markup)


async def cmd_web(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Одноразовый код: связать аккаунт с сайтом или сбросить пароль на сайте."""
    user = ensure_user(update.effective_user)
    uid = user["uid"]
    now = time.time()
    DB.execute("DELETE FROM link_codes WHERE uid = ? OR expires_at < ?", (uid, now))
    while True:
        code = f"{secrets.randbelow(10**6):06d}"
        if not DB.execute("SELECT 1 FROM link_codes WHERE code = ?", (code,)).fetchone():
            break
    DB.execute("INSERT INTO link_codes (code, uid, expires_at) VALUES (?, ?, ?)", (code, uid, now + WEB_CODE_TTL))
    DB.commit()
    lang = lang_of(uid)
    url = WEB_URL or t(lang, "web_site")
    await update.message.reply_text(t(lang, "web_code", code=code, url=url), parse_mode=HTML,
                                    disable_web_page_preview=True)


async def cmd_leave(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    g = room_of(uid)
    if g and not can_leave(g, uid):
        await update.message.reply_text(t(lang_of(uid), "cant_leave_alive"))
        return
    await leave_room(context, uid)
    await show_home(context, uid)


async def cmd_role(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    lang = lang_of(uid)
    g = room_of(uid)
    if g and uid in g["players"] and P(g, uid)["role"]:
        await update.message.reply_text(role_message(g, uid, lang), parse_mode=HTML)
    else:
        await update.message.reply_text(t(lang, "no_role"))


async def cmd_profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ensure_user(update.effective_user)
    await send_profile(context, update.effective_user.id)


async def cmd_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    g = room_of(uid)
    if g and g["host"] == uid:
        await send_panel(context, g)
        save_room(g)
    else:
        await show_home(context, uid)


async def cmd_takehost(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    lang = lang_of(uid)
    if uid != OWNER_ID:
        await update.message.reply_text(t(lang, "owner_only"))
        return
    g = room_of(uid)
    if not g:
        await update.message.reply_text(t(lang, "takehost_no_room"))
        return
    err = await take_host(context, g, uid, force=True)
    if err:
        await update.message.reply_text(t(lang, err))


async def cmd_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.pop("awaiting", None)
    await update.message.reply_text(t(lang_of(update.effective_user.id), "cancelled"))


async def cmd_myid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Telegram ID: <code>{update.effective_user.id}</code>",
                                    parse_mode=HTML)


async def post_init(app):
    global BOT_USERNAME
    BOT_USERNAME = (await app.bot.get_me()).username
    app.create_task(cleanup_loop(app))
    for lang in COMMANDS:
        try:
            await app.bot.set_my_commands([BotCommand(c, d) for c, d in COMMANDS[lang]],
                                          language_code=None if lang == "en" else lang)
        except Exception:
            logging.exception("Не удалось задать меню команд для языка %s", lang)


def main():
    if TOKEN.startswith("ВСТАВЬТЕ"):
        raise SystemExit("Нет токена: задайте BOT_TOKEN в .env")
    migrate_old_versions()
    load_rooms()
    app = ApplicationBuilder().token(TOKEN).post_init(post_init).build()
    private = filters.ChatType.PRIVATE
    for name, func in [("start", cmd_start), ("rooms", cmd_rooms), ("join", cmd_rooms), ("roles", cmd_roles),
                       ("leave", cmd_leave), ("role", cmd_role), ("profile", cmd_profile),
                       ("panel", cmd_panel), ("takehost", cmd_takehost),
                       ("cancel", cmd_cancel), ("myid", cmd_myid), ("web", cmd_web)]:
        app.add_handler(CommandHandler(name, func, filters=private))
    app.add_handler(CallbackQueryHandler(on_button))
    app.add_handler(MessageHandler(private & filters.PHOTO, on_photo))
    app.add_handler(MessageHandler(private & filters.TEXT & ~filters.COMMAND, on_text))
    print("🎭 MafiaNextBot v3 запущен. Остановить: Ctrl+C")
    app.run_polling()


if __name__ == "__main__":
    main()
