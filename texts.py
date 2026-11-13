"""
Все тексты бота на русском и английском.

В историях и некоторых фразах есть формы по полу: [мужская|женская].
Бот подставит нужную по полу игрока {v}. Если пол не указан — мужская
(она согласуется со словом «игрок»).
"""

LANG_NAMES = {"ru": "Русский", "en": "English"}

ROLE_EMOJI = {
    "mafia": "🔪", "framer": "🃏", "lawyer": "⚖️", "doctor": "💉", "detective": "🔍",
    "bodyguard": "🛡", "partyhost": "🎉", "driver": "🚕", "mayor": "🎩",
    "immortal": "♾️", "lucky": "🍀", "bestfriend": "🤝", "turncoat": "🐺",
    "civilian": "🙂",
}

# (мужская форма, женская форма)
ROLE_NAMES = {
    "ru": {
        "mafia": ("Мафия", "Мафия"),
        "framer": ("Подставщик", "Подставщица"),
        "lawyer": ("Адвокат", "Адвокат"),
        "doctor": ("Доктор", "Доктор"),
        "detective": ("Детектив", "Детектив"),
        "bodyguard": ("Телохранитель", "Телохранительница"),
        "partyhost": ("Тусовщик", "Тусовщица"),
        "driver": ("Таксист", "Таксистка"),
        "mayor": ("Мэр", "Мэр"),
        "immortal": ("Бессмертный", "Бессмертная"),
        "lucky": ("Везунчик", "Везунья"),
        "bestfriend": ("Лучший друг", "Лучшая подруга"),
        "turncoat": ("Оборотень", "Оборотень"),
        "civilian": ("Мирный житель", "Мирная жительница"),
    },
    "en": {
        "mafia": ("Mafia", "Mafia"),
        "framer": ("Framer", "Framer"),
        "lawyer": ("Lawyer", "Lawyer"),
        "doctor": ("Doctor", "Doctor"),
        "detective": ("Detective", "Detective"),
        "bodyguard": ("Bodyguard", "Bodyguard"),
        "partyhost": ("Party Host", "Party Host"),
        "driver": ("Driver", "Driver"),
        "mayor": ("Mayor", "Mayor"),
        "immortal": ("Immortal", "Immortal"),
        "lucky": ("Lucky", "Lucky"),
        "bestfriend": ("Best Friend", "Best Friend"),
        "turncoat": ("Turncoat", "Turncoat"),
        "civilian": ("Civilian", "Civilian"),
    },
}

TEAM_NAMES = {
    "ru": {"town": "🏘 Город", "mafia": "🔪 Мафия"},
    "en": {"town": "🏘 Town", "mafia": "🔪 Mafia"},
}

PRESET_NAMES = {
    "ru": {"classic": "Классика", "extended": "Расширенная", "chaos": "Хаос", "custom": "Своя"},
    "en": {"classic": "Classic", "extended": "Extended", "chaos": "Chaos", "custom": "Custom"},
}

ROLE_DESC = {
    "ru": {
        "mafia": "Ночью вы вместе с остальной мафией выбираете жертву. Днём притворяйтесь мирным.",
        "framer": "Вы играете за мафию. Каждую ночь выбирайте игрока: если детектив проверит его "
                  "этой ночью, то увидит «мафия». Ваша цель — запутать детективов.",
        "lawyer": "Вы играете за мафию, но не знаете, кто она. Каждую ночь пытайтесь угадать "
                  "мафиози. Угадали — отмазывайте его днём. Не угадали — топите того, "
                  "кого проверили, ведь он мирный. При подсчёте победы вы в команде мафии.",
        "doctor": "Каждую ночь вы лечите одного игрока. Если мафия придёт к нему, он выживет.",
        "detective": "Каждую ночь вы проверяете одного игрока и узнаёте, мафия ли он.",
        "bodyguard": "Каждую ночь вы охраняете одного игрока. Если мафия нападёт на него, "
                     "вы погибнете вместо него.",
        "partyhost": "Каждую ночь вы уводите одного игрока на вечеринку — его ночное действие "
                     "не срабатывает. Уведёте мафиози — убийства не будет.",
        "driver": "Каждую ночь вы меняете местами двух игроков: всё, что направлено на одного, "
                  "достанется другому. Можно спасти, а можно запутать — выбирайте с умом.",
        "mayor": "Днём ваш голос обычный, а личность — тайна. Один раз за игру после "
                 "голосования вы можете отменить изгнание. Скажите ведущему, когда он объявит.",
        "immortal": "Мафия не может убить вас ночью. Изгнать вас днём — может.",
        "lucky": "Первое ночное нападение на вас не сработает. После этого вы обычный мирный. "
                 "Изгнать вас днём можно в любой момент.",
        "bestfriend": "Вы и ваш лучший друг — мирные, и вы оба это знаете. Держитесь вместе!",
        "turncoat": "Пока вы мирный. Но когда погибнет первый мафиози, вы перейдёте в мафию "
                    "и узнаете своих новых союзников.",
        "civilian": "Ночью вы спите. Днём ищите мафию и голосуйте с умом.",
    },
    "en": {
        "mafia": "Each night you and the rest of the Mafia choose a victim. By day, act innocent.",
        "framer": "You play for the Mafia. Each night choose a player: if a Detective checks them "
                  "tonight, they will show up as Mafia. Your goal is to mislead the Detectives.",
        "lawyer": "You play for the Mafia, but you don't know who they are. Each night try to "
                  "guess a Mafia member. Guessed right — defend them by day. Guessed wrong — "
                  "push to eliminate that player, they are town. You count as Mafia for victory.",
        "doctor": "Each night you heal one player. If the Mafia attacks them, they survive.",
        "detective": "Each night you check one player and learn whether they are Mafia.",
        "bodyguard": "Each night you guard one player. If the Mafia attacks them, "
                     "you die in their place.",
        "partyhost": "Each night you take one player to your party — their night action fails. "
                     "Take a Mafia member and there will be no kill.",
        "driver": "Each night choose two players and switch their places: any action targeting "
                  "one affects the other. It can save players or create confusion — choose carefully.",
        "mayor": "By day your vote counts as a regular vote and your identity is secret. "
                 "Once per game, after the vote, you may cancel the elimination. Tell the host "
                 "when they announce it.",
        "immortal": "The Mafia cannot kill you at night. You can still be voted out by day.",
        "lucky": "The first night attack on you fails. After that you are a regular player. "
                 "You can still be voted out by day.",
        "bestfriend": "You and your best friend are both town, and you both know it. Stick together!",
        "turncoat": "For now you are town. But when the first Mafia member dies, "
                    "you will join the Mafia and learn who your new allies are.",
        "civilian": "At night you sleep. By day, find the Mafia and vote wisely.",
    },
}

# ---------------------------------------------------------------------------
# Истории. {v} — имя игрока, {r} — номер ночи/дня, [м|ж] — форма по полу {v}.
# ---------------------------------------------------------------------------
STORIES = {
    "ru": {
        "night_header": ["🌅 <b>Утро после ночи {r}. Город просыпается…</b>"],
        "day_header": ["🌆 <b>Вечер {r}-го дня. Итоги голосования</b>"],
        "kill": [
            "Ночь выдалась туманной. Город спал, но не все. На рассвете жители нашли "
            "игрока {v} у старого фонтана — мафия не знает жалости.",
            "Когда часы пробили три, в одном из домов погас свет. "
            "Утром соседи поняли: {v} больше не [проснётся|проснётся].",
            "Город уснул под шум дождя. Мафия выбрала цель, и доктор не успел. "
            "{v} [покидает|покидает] игру навсегда.",
            "Луна скрылась за тучами, и в тишине раздался выстрел. "
            "Наутро стало ясно: {v} [был убит|была убита] мафией.",
            "Ночью по улицам проехала чёрная машина без номеров. "
            "А утром город недосчитался одного жителя: {v} [исчез|исчезла] без следа.",
        ],
        "bodyguard": [
            "Ночью мафия вышла на охоту, но на пути убийц встал телохранитель. "
            "{v} [закрыл|закрыла] собой другого и [погиб|погибла] как [герой|героиня].",
            "Выстрел прозвучал в темноте, но пуля нашла не того, кому предназначалась: "
            "{v} [бросился|бросилась] наперерез и [спас|спасла] чужую жизнь ценой своей.",
        ],
        "saved": [
            "Ночью мафия вышла на охоту, но доктор оказался быстрее. Все проснулись "
            "живыми — хотя кто-то явно провёл ночь под капельницей. 💉",
            "Тени подкрались к дому жертвы, но на пороге уже стоял доктор "
            "со своим чемоданчиком. Мафия ушла ни с чем.",
            "Эта ночь могла стать для кого-то последней. Но доктор сотворил чудо: все живы!",
        ],
        "survived": [
            "Ночью мафия напала, но жертва… просто не умерла. Город шепчется: "
            "то ли чудо, то ли кто-то здесь не так прост.",
            "Убийцы сделали своё дело, но утром их цель вышла на улицу живой и невредимой. "
            "Мафия в замешательстве.",
        ],
        "quiet": [
            "Ночь прошла на удивление спокойно. Мафия затаилась… или что-то замышляет. 🤔",
            "Город спал крепко, и даже мафия, кажется, взяла выходной. Все живы — пока.",
            "Где-то до утра гремела музыка, а мафия так и не вышла на дело. "
            "Странная выдалась ночь.",
        ],
        "exile": [
            "Споры не утихали до самого вечера. Наконец город вынес решение: "
            "{v} [изгнан|изгнана].",
            "Голосование было напряжённым, но большинство указало на игрока {v}. "
            "Решение принято.",
            "Город решил не рисковать: {v} [покидает|покидает] игру.",
            "Обвинения, оправдания, крики… В итоге жители проголосовали против игрока {v}.",
        ],
        "no_exile": [
            "Подозрений было много, а доказательств мало. "
            "Жители разошлись по домам, никого не изгнав.",
            "Город так и не смог договориться. Сегодня никто не покидает игру… "
            "но ночь уже близко. 🌙",
        ],
        "mayor": [
            "Город уже решил изгнать игрока {v}, но в последний момент пришёл указ из мэрии: "
            "изгнание отменено! Кто же мэр? 🎩",
            "{v} уже [стоял|стояла] у городских ворот, когда прибежал гонец с печатью мэра. "
            "Приговор отменён — {v} [остаётся|остаётся] в городе.",
        ],
        "tie_revote": ["Голоса разделились поровну, и город решил переголосовать."],
        "tie_rps": ["Голоса разделились поровну, и судьбу решила дуэль «камень, ножницы, бумага»:\n{x}\n"
                    "Проиграл[|а] {v}."],
        "tie_dice": ["Голоса разделились поровну, и судьбу решил кубик:\n{x}\nЖребий пал на игрока {v}."],
        "tie_random": ["Голоса разделились поровну, и жребий пал на игрока {v}."],
        "win_town": ["🎉 <b>Мирные жители победили!</b> Вся мафия поймана, "
                     "город может спать спокойно."],
        "win_mafia": ["🔪 <b>Мафия победила!</b> Мирных жителей осталось слишком мало — "
                      "город теперь в руках мафии."],
    },
    "en": {
        "night_header": ["🌅 <b>Morning after night {r}. The town wakes up…</b>"],
        "day_header": ["🌆 <b>Evening of day {r}. The vote results</b>"],
        "kill": [
            "The night was foggy. The town slept, but not everyone. At dawn people found "
            "{v} by the old fountain — the Mafia shows no mercy.",
            "When the clock struck three, a light went out in one of the houses. "
            "In the morning the neighbors realized {v} would never wake up again.",
            "The town fell asleep to the sound of rain. The Mafia chose a target and the doctor "
            "was too late. {v} is gone for good.",
            "The moon hid behind the clouds and a shot rang out in the silence. "
            "By morning it was clear: {v} had been killed by the Mafia.",
            "At night a black car without plates drove through the streets. "
            "In the morning the town was one person short: {v} had vanished without a trace.",
        ],
        "bodyguard": [
            "The Mafia went hunting, but a bodyguard stood in their way. "
            "{v} shielded someone else and died a hero.",
            "A shot rang out in the dark, but the bullet found the wrong person: "
            "{v} jumped in front of it and saved a life at the cost of [his|her] own.",
        ],
        "saved": [
            "The Mafia went hunting, but the doctor was faster. Everyone woke up alive — "
            "though someone clearly spent the night on an IV drip. 💉",
            "Shadows crept up to the victim's house, but the doctor was already at the door "
            "with a medical bag. The Mafia left empty-handed.",
            "This night could have been someone's last. But the doctor worked a miracle: "
            "everyone is alive!",
        ],
        "survived": [
            "The Mafia attacked, but the victim… simply didn't die. The town whispers: "
            "a miracle, or is someone here not what they seem?",
            "The killers did their job, yet in the morning their target walked out "
            "alive and well. The Mafia is baffled.",
        ],
        "quiet": [
            "The night was surprisingly calm. The Mafia is lying low… or plotting something. 🤔",
            "The town slept soundly, and even the Mafia seems to have taken a night off. "
            "Everyone is alive — for now.",
            "Music played somewhere until dawn, and the Mafia never went out to work. "
            "A strange night indeed.",
        ],
        "exile": [
            "The arguments went on until evening. Finally the town decided: {v} is exiled.",
            "The vote was tense, but the majority pointed at {v}. The decision is made.",
            "The town chose not to take chances: {v} leaves the game.",
            "Accusations, excuses, shouting… In the end the town voted against {v}.",
        ],
        "no_exile": [
            "Plenty of suspicion, little proof. Everyone went home without exiling anyone.",
            "The town couldn't agree. Nobody leaves today… but night is coming. 🌙",
        ],
        "mayor": [
            "The town had already decided to exile {v}, but at the last moment a decree "
            "arrived from City Hall: the exile is cancelled! Who is the Mayor? 🎩",
            "{v} was already at the town gates when a messenger ran up with the Mayor's seal. "
            "The sentence is lifted — {v} stays.",
        ],
        "tie_revote": ["The votes were split evenly, so the town voted again."],
        "tie_rps": ["The votes were split evenly, and a game of rock, paper, scissors decided:\n{x}\n"
                    "{v} lost."],
        "tie_dice": ["The votes were split evenly, and the dice decided:\n{x}\nThe lot fell on {v}."],
        "tie_random": ["The votes were split evenly, and the lot fell on {v}."],
        "win_town": ["🎉 <b>The town wins!</b> All the Mafia have been caught — "
                     "the town can sleep peacefully."],
        "win_mafia": ["🔪 <b>The Mafia wins!</b> Too few townspeople are left — "
                      "the town is now in the Mafia's hands."],
    },
}

# ---------------------------------------------------------------------------
# Интерфейс
# ---------------------------------------------------------------------------
T = {
    "ru": {
        # закрытие комнат
        "btn_close_room": "Закрыть комнату", "close_yes": "Да, закрыть",
        "close_confirm": "Закрыть комнату {n}? Если там идёт игра, она не будет засчитана.",
        "cant_close_yet": "Закрыть комнату можно после суток без активности.",
        "room_closed_by": "{v} закрыл(а) комнату {n}.",
        "room_closed_idle": "Комната {n} удалена: неделю в ней ничего не происходило.",
        "room_idle_warning": "Комната {n} будет удалена через сутки: в ней давно ничего не происходит. "
                             "Нажмите кнопку, чтобы её сохранить.",
        "btn_keep_room": "Сохранить комнату", "room_kept": "Комната сохранена!",
        "idle_for": "Без активности: {v}",
        "hours": ("час", "часа", "часов"),
        # комнаты
        "rooms_title": "Комнаты", "room": "Комната", "free_room": "Свободная комната",
        "no_rooms": "Пока нет ни одной комнаты — откройте свободную!",
        "host": "Ведущий", "no_host": "нет ведущего", "watchers": "Зрители",
        "invite": "Пригласить", "status_lobby": "набор", "status_over": "игра окончена",
        "status_paused": "пауза — нет ведущего",
        "btn_play": "Играть", "btn_watch": "Только смотреть", "btn_my_role": "Моя роль",
        "btn_take_host": "Взять ведущего", "btn_release": "Отпустить ведущего",
        "btn_end_game": "Завершить игру", "btn_leave_room": "Выйти из комнаты",
        "cant_leave_alive": "Вы живой игрок в идущей партии — выйти можно после её конца.",
        "host_taken_already": "У этой комнаты уже есть ведущий.",
        "cant_host_alive": "Вы живой игрок в идущей партии — ведущим может стать только выбывший или зритель.",
        "new_host": "👑 {v} теперь ведущий этой комнаты.",
        "you_released": "Вы больше не ведущий.",
        "host_released": "🙌 {v} отпустил(а) место ведущего. Любой может его занять.",
        "host_released_game": "⏸ {v} отпустил(а) место ведущего — игра на паузе. "
                              "Взять ведущего могут выбывшие и зрители.",
        "host_taken_by_owner": "Владелец бота забрал роль ведущего.",
        "takehost_no_room": "Сначала зайдите в комнату: /rooms",
        "game_started_watch": "Игра началась! Вы смотрите как зритель.",
        "game_aborted": "{v} завершил(а) игру. Она не засчитана. Комната вернулась в набор.",
        "end_confirm": "Точно завершить игру? Она не будет засчитана.",
        "end_yes": "Да, завершить", "end_no": "Нет, вернуться",
        # карточка роли
        "back_to_roles": "К ролям", "team": "Команда", "count": "Количество",
        "card_pair": "Считается парой: занимает два места.",
        # голосование
        "set_vote_mode": "Голосование",
        "val_vote_mode_host": "через ведущего", "val_vote_mode_phones": "с телефонов",
        "set_tie_default": "Ничья по умолчанию",
        "val_tie_default_nobody": "никто", "val_tie_default_rps": "камень-ножницы-бумага",
        "val_tie_default_random": "кубик", "val_tie_default_revote": "переголосование",
        "set_show_names": "Имена в скобках",
        "btn_open_vote": "Открыть голосование", "btn_close_vote": "Закрыть голосование",
        "btn_cancel_votes": "Отмена голосов",
        "vote_hint_host": "Выберите кандидата и отметьте, кто за него голосовал. "
                          "Изменить голос можно только через «Отмена голосов».",
        "vote_hint_phones": "Игроки голосуют в личке с ботом. Счёт видите только вы.",
        "voted": "Проголосовали", "not_voted": "Ещё не голосовали",
        "already_voted_host": "Этот игрок уже проголосовал. Отменить голос можно в «Отмена голосов».",
        "cancel_hint": "Нажмите на голос, чтобы его отменить. После этого игрок может проголосовать заново.",
        "ballot_title": "Голосование!", "ballot_hint": "Кого изгнать из города? Голос тайный.",
        "your_vote": "Ваш голос: <b>{v}</b>",
        "your_vote_hint": "Чтобы изменить голос, сначала отмените его.",
        "btn_cancel_my_vote": "Отменить мой голос",
        "already_voted": "Вы уже проголосовали. Чтобы изменить голос, отмените его.",
        "vote_closed": "Голосование закрыто.", "vote_not_open": "Голосование сейчас закрыто.",
        "tie_choose": "Как решаем?",
        "tie_nobody": "Никто не выбывает", "tie_rps": "Камень, ножницы, бумага",
        "tie_random": "Кубик", "tie_revote": "Переголосование",
        "decided": "Выбывает: {v}",
        # камень, ножницы, бумага
        "rps_title": "Камень, ножницы, бумага", "rps_round": "раунд",
        "rps_prompt": "Ничья в голосовании! Ваши соперники: {v}. Проигравший покинет город. Ваш ход:",
        "rps_chosen": "Ваш выбор: {v}. Ждём соперников…",
        "rps_expired": "Этот раунд уже неактуален.",
        "rps_you_safe": "Вы победили в дуэли и остаётесь в игре!",
        "rps_you_lost": "Вы проиграли дуэль.",
        "rps_cancelled": "Ведущий отменил дуэль.",
        "btn_rps_random": "Случайный выбор за тех, кто не выбрал",
        "btn_rps_cancel": "Отменить дуэль",
        "dice_title": "Ничья! Бросаем кубик:",
        # общее
        "back": "Назад", "skip": "Никого / пропуск", "auto": "авто", "pts": "очк.",
        "years": ("год", "года", "лет"), "months": ("месяц", "месяца", "месяцев"),
        "days": ("день", "дня", "дней"),
        "only_host": "Эти кнопки только для ведущего",
        # лобби
        "lobby": "Лобби", "players": "Игроки", "nobody_yet": "пока никого",
        "preset": "Набор ролей",
        "will_drop": "не хватит игроков для: {roles}",
        "btn_roles": "Роли", "btn_settings": "Настройки", "btn_players": "Игроки", "btn_deal": "Раздать роли",
        "btn_refresh": "Обновить",
        "kick_hint": "Нажмите на игрока, чтобы перевести его в зрители.",
        "kicked": "Ведущий перевёл вас в зрители. Чтобы играть, нажмите «Играть» в комнате.",
        "player_joined": "{v} присоединяется (всего: {n})",
        "player_left": "{v} выходит из комнаты",
        "nick_changed": "{a} теперь зовётся {b}",
        # роли
        "roles_title": "Набор ролей",
        "roles_hint": "Мирных жителей бот добавит сам, только если ролей меньше, чем игроков. "
                      "Если игроков не хватает, лишние роли убираются автоматически.",
        "mafia_auto": "Мафия: авто (1 на 4 игроков)",
        # настройки
        "settings_title": "Настройки ведущего",
        "settings_hint": "Нажмите на настройку, чтобы переключить её.",
        "set_reveal": "Раскрывать выбывших",
        "val_reveal_full": "роль", "val_reveal_team": "команду", "val_reveal_none": "нет",
        "set_doctor_self": "Доктор лечит себя",
        "set_doctor_repeat": "Доктор лечит одного 2 ночи подряд",
        "set_first_phase": "Начало игры",
        "val_first_phase_night": "ночь", "val_first_phase_day": "день знакомства",
        "set_auto_broadcast": "Авторассылка историй",
        "set_detective_dm": "Результат детективу в личку",
        "set_lawyer_dm": "Результат адвокату в личку",
        # раздача
        "need_3": "Нужно минимум 3 игрока.",
        "roles_dealt": "Роли розданы!",
        "dropped": "Не хватило игроков, убраны: {roles}",
        "dm_failed": "Не удалось отправить роль: {v}. Пусть нажмут Start у бота.",
        "your_role": "Ваша роль", "your_team": "Ваша команда",
        "your_friend": "Ваш лучший друг: {v} — [он|она] тоже мирный.",
        "keep_secret": "Никому не показывайте это сообщение!",
        "you_are_out": "Вы выбыли из игры.",
        "lucky_spent": "🍀 Ваша удача уже использована.",
        "lawyer_done": "✅ Вы уже нашли мафию — теперь защищайте её днём.",
        # ночь
        "night": "Ночь", "mafia_team_kill": "Мафия",
        "night_hint": "⇒ — предварительный результат с учётом всех выборов.",
        "blocked": "на вечеринке",
        "res_mafia": "МАФИЯ", "res_town": "не мафия",
        "res_right": "угадал(а)", "res_wrong": "мимо",
        "pick_mafia": "Кого выбрала мафия?",
        "pick_doctor": "кого лечит?", "pick_detective": "кого проверяет?",
        "pick_lawyer": "кого считает мафией?", "pick_bodyguard": "кого охраняет?",
        "pick_partyhost": "кого зовёт на вечеринку?", "pick_framer": "кого подставляет?",
        "pick_driver": "кого меняет местами? (выберите двоих)",
        "btn_view": "Состав", "btn_end_night": "Закончить ночь",
        # день
        "day": "День", "alive": "В живых",
        "intro_day": "День знакомства",
        "intro_hint": "Игроки представляются. Голосования сегодня нет.",
        "btn_start_night": "Начать ночь",
        "vote_title": "Голосование",
        "who_voted_for": "Кто голосовал против: <b>{v}</b>?",
        "voters_hint": "☑️ — голосует за этого кандидата, ▫️ — уже за другого (нажмите, чтобы перенести).",
        "back_to_vote": "К кандидатам",
        "vote_result": "Итог голосования", "no_votes": "Голосов нет.",
        "leader": "Больше всего голосов: <b>{v}</b>",
        "tie": "Ничья: {v}",
        "btn_exile": "Изгнать: {v}", "btn_mayor": "Мэр отменил изгнание",
        "btn_no_exile": "Никого не изгонять",
        "dead_night": "Этой ночью вас убили. Можно остаться и наблюдать, но молча! 🤫",
        "dead_day": "Город проголосовал против вас. Можно остаться и наблюдать, но молча! 🤫",
        "lucky_saved": "Этой ночью на вас напали, но вам повезло! Больше удача не поможет.",
        "dm_check": "Результат проверки: {v} — <b>{res}</b>",
        "dm_lawyer_ok": "Вы угадали: {v} — мафия! Теперь защищайте её.",
        "dm_lawyer_no": "Мимо: {v} — не мафия.",
        "you_turned": "Первый мафиози погиб. Теперь вы — мафия!",
        "turncoat_joined": "Оборотень {v} [перешёл|перешла] на вашу сторону!",
        # история
        "story_title": "История для чтения вслух", "for_host": "Для ведущего",
        "btn_broadcast": "Отправить историю всем игрокам", "btn_next": "Дальше",
        "auto_sent": "История разослана игрокам.",
        "broadcast_done": "Отправлено игрокам: {n}",
        "reveal_role": "Роль: {role}.", "reveal_team": "Команда: {team}.",
        "note_kill_blocked": "тусовщик увёл мафиози — убийства нет",
        "note_immortal": "мафия напала на бессмертного: {v}",
        "note_saved": "доктор спас: {v}",
        "note_guarded": "телохранитель {b} погиб, защищая {v}",
        "note_lucky": "{v} выжил(а) благодаря удаче",
        "note_redirected": "таксист перенаправил удар с {v} на {b}",
        "note_check_mafia": "детектив {d} проверил(а) {v}: мафия",
        "note_check_town": "детектив {d} проверил(а) {v}: не мафия",
        "note_lawyer_ok": "адвокат {d} угадал(а) мафию: {v}",
        "note_lawyer_no": "адвокат {d} не угадал(а): {v}",
        "note_turned": "оборотень {v} перешёл в мафию",
        "note_mayor": "мэр отменил изгнание игрока {v}",
        # конец
        "game_over": "Игра окончена",
        "btn_rematch": "Новая партия в этой комнате",
        "rematch": "Новая партия в той же комнате! Ждите свою роль.",
        # передача ведущего
        "you_are_host": "Вы — ведущий! Панель ниже.",
        "owner_only": "Эта команда только для владельца бота.",
        # игроки
        "no_role": "У вас пока нет роли.",
        "cancelled": "Хорошо, ничего не меняем 🙂",
        "help_short": "Команды: /rooms — комнаты, /profile — профиль, /role — моя роль, "
                      "/leave — выйти из комнаты.",
        # профиль
        "profile": "Профиль", "nick": "Ник", "real_name": "Имя", "gender": "Пол",
        "language": "Язык", "registered": "С нами с", "tenure": "Стаж",
        "points_total": "Очков всего", "points_last": "Очков в последней игре",
        "games_played": "Игр", "wins": "побед",
        "gender_m": "Мужской", "gender_f": "Женский", "gender_none": "Не указан",
        "btn_nick": "Ник", "btn_name": "Имя", "btn_gender": "Пол", "btn_lang": "Язык",
        "btn_photo": "Фото", "btn_games": "Мои игры",
        "ask_nick": "Напишите игровой ник ({a}–{b} символов). Его увидят все игроки. Отмена: /cancel",
        "ask_name": "Напишите своё настоящее имя. Его видит только ведущий. Отмена: /cancel",
        "ask_gender": "Выберите пол — так истории будут с правильными окончаниями:",
        "ask_photo": "Отправьте фото одним сообщением. Отмена: /cancel",
        "bad_nick": "Ник должен быть от {a} до {b} символов и не начинаться с «/». Ещё раз: /profile",
        "bad_name": "Имя не подходит. Попробуйте ещё раз через /profile",
        "nick_after_game": "Ник можно сменить после окончания игры.",
        "nick_taken": "Этот ник уже занят другим игроком в лобби. Выберите другой: /profile",
        "nick_saved": "Ваш ник: <b>{v}</b>",
        "name_saved": "Ваше имя: <b>{v}</b>",
        "gender_saved": "Пол: {v}",
        "lang_saved": "Язык: Русский",
        "ask_lang": "Выберите язык:",
        "photo_saved": "Фото сохранено!",
        "photo_deleted": "Фото удалено.",
        "delete_photo": "Удалить фото",
        "photo_hint": "Чтобы сменить фото профиля, откройте /profile → Фото.",
        "no_games": "Вы ещё не сыграли ни одной игры.",
        "games_more": "…и ещё {n}",
    },
    "en": {
        "btn_close_room": "Close room", "close_yes": "Yes, close it",
        "close_confirm": "Close room {n}? A running game there won't count.",
        "cant_close_yet": "A room can be closed after a day without activity.",
        "room_closed_by": "{v} closed room {n}.",
        "room_closed_idle": "Room {n} was deleted: nothing happened there for a week.",
        "room_idle_warning": "Room {n} will be deleted in a day: nothing has happened there for a while. "
                             "Tap the button to keep it.",
        "btn_keep_room": "Keep the room", "room_kept": "The room is kept!",
        "idle_for": "Inactive for: {v}",
        "hours": ("hour", "hours"),
        "rooms_title": "Rooms", "room": "Room", "free_room": "Free room",
        "no_rooms": "No rooms yet — open the free one!",
        "host": "Host", "no_host": "no host", "watchers": "Watching",
        "invite": "Invite", "status_lobby": "gathering", "status_over": "game over",
        "status_paused": "paused — no host",
        "btn_play": "Play", "btn_watch": "Just watch", "btn_my_role": "My role",
        "btn_take_host": "Become host", "btn_release": "Step down as host",
        "btn_end_game": "End game", "btn_leave_room": "Leave room",
        "cant_leave_alive": "You are alive in a running game — you can leave after it ends.",
        "host_taken_already": "This room already has a host.",
        "cant_host_alive": "You are alive in a running game — only eliminated players or watchers can host.",
        "new_host": "👑 {v} is now the host of this room.",
        "you_released": "You are no longer the host.",
        "host_released": "🙌 {v} stepped down as host. Anyone can take the role.",
        "host_released_game": "⏸ {v} stepped down as host — the game is paused. "
                              "Eliminated players and watchers can become host.",
        "host_taken_by_owner": "The bot owner took over the host role.",
        "takehost_no_room": "Join a room first: /rooms",
        "game_started_watch": "The game has started! You are watching.",
        "game_aborted": "{v} ended the game. It won't count. The room is gathering again.",
        "end_confirm": "End the game? It won't count.",
        "end_yes": "Yes, end it", "end_no": "No, go back",
        "back_to_roles": "To roles", "team": "Team", "count": "Count",
        "card_pair": "Counts as a pair: takes two places.",
        "set_vote_mode": "Voting",
        "val_vote_mode_host": "via host", "val_vote_mode_phones": "from phones",
        "set_tie_default": "Default on a tie",
        "val_tie_default_nobody": "nobody", "val_tie_default_rps": "rock-paper-scissors",
        "val_tie_default_random": "dice", "val_tie_default_revote": "revote",
        "set_show_names": "Names in brackets",
        "btn_open_vote": "Open the vote", "btn_close_vote": "Close the vote",
        "btn_cancel_votes": "Cancel votes",
        "vote_hint_host": "Pick a candidate and mark who voted for them. "
                          "A vote can only be changed via “Cancel votes”.",
        "vote_hint_phones": "Players vote in their chat with the bot. Only you see the count.",
        "voted": "Voted", "not_voted": "Not voted yet",
        "already_voted_host": "This player already voted. Cancel the vote in “Cancel votes”.",
        "cancel_hint": "Tap a vote to cancel it. The player can then vote again.",
        "ballot_title": "Vote!", "ballot_hint": "Who should be exiled? The vote is secret.",
        "your_vote": "Your vote: <b>{v}</b>",
        "your_vote_hint": "To change your vote, cancel it first.",
        "btn_cancel_my_vote": "Cancel my vote",
        "already_voted": "You already voted. To change it, cancel your vote first.",
        "vote_closed": "The vote is closed.", "vote_not_open": "Voting is closed right now.",
        "tie_choose": "How do we break it?",
        "tie_nobody": "Nobody leaves", "tie_rps": "Rock, paper, scissors",
        "tie_random": "Dice", "tie_revote": "Revote",
        "decided": "Leaving: {v}",
        "rps_title": "Rock, paper, scissors", "rps_round": "round",
        "rps_prompt": "The vote is tied! Your rivals: {v}. The loser leaves town. Your move:",
        "rps_chosen": "Your choice: {v}. Waiting for the others…",
        "rps_expired": "This round is no longer active.",
        "rps_you_safe": "You won the duel and stay in the game!",
        "rps_you_lost": "You lost the duel.",
        "rps_cancelled": "The host cancelled the duel.",
        "btn_rps_random": "Random choice for those who haven't picked",
        "btn_rps_cancel": "Cancel the duel",
        "dice_title": "It's a tie! Rolling the dice:",
        "back": "Back", "skip": "Nobody / skip", "auto": "auto", "pts": "pts",
        "years": ("year", "years"), "months": ("month", "months"), "days": ("day", "days"),
        "only_host": "These buttons are for the host only",
        "lobby": "Lobby", "players": "Players", "nobody_yet": "nobody yet",
        "preset": "Role set",
        "will_drop": "not enough players for: {roles}",
        "btn_roles": "Roles", "btn_settings": "Settings", "btn_players": "Players", "btn_deal": "Deal roles", "btn_refresh": "Refresh",
        "kick_hint": "Tap a player to move them to watchers.",
        "kicked": "The host moved you to watchers. To play, press “Play” in the room.",
        "player_joined": "{v} joined (total: {n})",
        "player_left": "{v} left the room",
        "nick_changed": "{a} is now called {b}",
        "roles_title": "Role set",
        "roles_hint": "Civilians are added only if there are fewer roles than players. "
                      "If there aren't enough players, extra roles are removed automatically.",
        "mafia_auto": "Mafia: auto (1 per 4 players)",
        "settings_title": "Host settings",
        "settings_hint": "Tap a setting to switch it.",
        "set_reveal": "Reveal eliminated",
        "val_reveal_full": "role", "val_reveal_team": "team", "val_reveal_none": "no",
        "set_doctor_self": "Doctor can heal self",
        "set_doctor_repeat": "Doctor can heal same player twice in a row",
        "set_first_phase": "Game starts with",
        "val_first_phase_night": "night", "val_first_phase_day": "intro day",
        "set_auto_broadcast": "Auto-send stories",
        "set_detective_dm": "Detective gets result by DM",
        "set_lawyer_dm": "Lawyer gets result by DM",
        "need_3": "At least 3 players are needed.",
        "roles_dealt": "Roles dealt!",
        "dropped": "Not enough players, removed: {roles}",
        "dm_failed": "Couldn't send a role to: {v}. Ask them to press Start in the bot.",
        "your_role": "Your role", "your_team": "Your team",
        "your_friend": "Your best friend: {v} — [he|she] is town too.",
        "keep_secret": "Don't show this message to anyone!",
        "you_are_out": "You are out of the game.",
        "lucky_spent": "🍀 Your luck has already been used.",
        "lawyer_done": "✅ You've already found the Mafia — now defend them by day.",
        "night": "Night", "mafia_team_kill": "Mafia",
        "night_hint": "⇒ — preliminary result considering all choices.",
        "blocked": "at the party",
        "res_mafia": "MAFIA", "res_town": "not Mafia",
        "res_right": "right", "res_wrong": "wrong",
        "pick_mafia": "Who did the Mafia choose?",
        "pick_doctor": "who to heal?", "pick_detective": "who to check?",
        "pick_lawyer": "who do they think is Mafia?", "pick_bodyguard": "who to guard?",
        "pick_partyhost": "who to invite to the party?", "pick_framer": "who to frame?",
        "pick_driver": "who to switch? (pick two)",
        "btn_view": "Line-up", "btn_end_night": "End night",
        "day": "Day", "alive": "Alive",
        "intro_day": "Intro day",
        "intro_hint": "Players introduce themselves. No vote today.",
        "btn_start_night": "Start night",
        "vote_title": "Vote",
        "who_voted_for": "Who voted against <b>{v}</b>?",
        "voters_hint": "☑️ — votes for this candidate, ▫️ — already voted for someone else (tap to move).",
        "back_to_vote": "To candidates",
        "vote_result": "Vote result", "no_votes": "No votes.",
        "leader": "Most votes: <b>{v}</b>",
        "tie": "Tie: {v}",
        "btn_exile": "Exile: {v}", "btn_mayor": "Mayor cancelled the exile",
        "btn_no_exile": "Exile nobody",
        "dead_night": "You were killed tonight. You can stay and watch, but silently! 🤫",
        "dead_day": "The town voted you out. You can stay and watch, but silently! 🤫",
        "lucky_saved": "You were attacked tonight, but you got lucky! Luck won't help again.",
        "dm_check": "Check result: {v} — <b>{res}</b>",
        "dm_lawyer_ok": "You guessed right: {v} is Mafia! Now defend them.",
        "dm_lawyer_no": "Wrong: {v} is not Mafia.",
        "you_turned": "The first Mafia member has died. Now you are Mafia!",
        "turncoat_joined": "Turncoat {v} has joined your side!",
        "story_title": "Story to read aloud", "for_host": "For the host",
        "btn_broadcast": "Send story to all players", "btn_next": "Next",
        "auto_sent": "The story was sent to players.",
        "broadcast_done": "Sent to players: {n}",
        "reveal_role": "Role: {role}.", "reveal_team": "Team: {team}.",
        "note_kill_blocked": "the party host took a Mafia member — no kill",
        "note_immortal": "the Mafia attacked the Immortal: {v}",
        "note_saved": "the doctor saved: {v}",
        "note_guarded": "bodyguard {b} died protecting {v}",
        "note_lucky": "{v} survived thanks to luck",
        "note_redirected": "the driver redirected the attack from {v} to {b}",
        "note_check_mafia": "detective {d} checked {v}: Mafia",
        "note_check_town": "detective {d} checked {v}: not Mafia",
        "note_lawyer_ok": "lawyer {d} found the Mafia: {v}",
        "note_lawyer_no": "lawyer {d} guessed wrong: {v}",
        "note_turned": "turncoat {v} joined the Mafia",
        "note_mayor": "the Mayor cancelled the exile of {v}",
        "game_over": "Game over",
        "btn_rematch": "New game in this room",
        "rematch": "New round! Wait for your role.",
        "you_are_host": "You are the host! Your panel is below.",
        "owner_only": "This command is for the bot owner only.",
        "no_role": "You don't have a role yet.",
        "cancelled": "OK, nothing changed 🙂",
        "help_short": "Commands: /rooms — rooms, /profile — profile, /role — my role, "
                      "/leave — leave the room.",
        "profile": "Profile", "nick": "Nickname", "real_name": "Name", "gender": "Gender",
        "language": "Language", "registered": "Member since", "tenure": "Time with us",
        "points_total": "Total points", "points_last": "Points in last game",
        "games_played": "Games", "wins": "wins",
        "gender_m": "Male", "gender_f": "Female", "gender_none": "Not specified",
        "btn_nick": "Nickname", "btn_name": "Name", "btn_gender": "Gender", "btn_lang": "Language",
        "btn_photo": "Photo", "btn_games": "My games",
        "ask_nick": "Send your game nickname ({a}–{b} characters). Everyone will see it. Cancel: /cancel",
        "ask_name": "Send your real name. Only the host sees it. Cancel: /cancel",
        "ask_gender": "Choose your gender:",
        "ask_photo": "Send a photo in one message. Cancel: /cancel",
        "bad_nick": "The nickname must be {a}–{b} characters and not start with “/”. Try again: /profile",
        "bad_name": "That name doesn't work. Try again via /profile",
        "nick_after_game": "You can change your nickname after the game ends.",
        "nick_taken": "This nickname is taken by another player in the lobby. Pick another: /profile",
        "nick_saved": "Your nickname: <b>{v}</b>",
        "name_saved": "Your name: <b>{v}</b>",
        "gender_saved": "Gender: {v}",
        "lang_saved": "Language: English",
        "ask_lang": "Choose a language:",
        "photo_saved": "Photo saved!",
        "photo_deleted": "Photo deleted.",
        "delete_photo": "Delete photo",
        "photo_hint": "To change your profile photo, open /profile → Photo.",
        "no_games": "You haven't played any games yet.",
        "games_more": "…and {n} more",
    },
}


# Меню команд бота (бот ставит его сам при запуске, BotFather не нужен)
COMMANDS = {
    "ru": [("start", "Главное меню"), ("rooms", "Комнаты"), ("profile", "Мой профиль"),
           ("role", "Моя роль"), ("panel", "Панель ведущего"), ("leave", "Выйти из комнаты"),
           ("cancel", "Отменить ввод")],
    "en": [("start", "Main menu"), ("rooms", "Rooms"), ("profile", "My profile"),
           ("role", "My role"), ("panel", "Host panel"), ("leave", "Leave room"),
           ("cancel", "Cancel input")],
}

# ===========================================================================
# ТАТАРЧА (tt)
# ===========================================================================
LANG_NAMES["tt"] = "Татарча"
ROLE_NAMES["tt"] = {r: (n, n) for r, n in {
    "mafia": "Мафия", "framer": "Яла ягучы", "lawyer": "Адвокат", "doctor": "Табиб",
    "detective": "Детектив", "bodyguard": "Сакчы", "partyhost": "Мәҗлесче",
    "driver": "Таксист", "mayor": "Мэр", "immortal": "Үлемсез", "lucky": "Бәхетле",
    "bestfriend": "Иң якын дус", "turncoat": "Хыянәтче", "civilian": "Тыныч кеше",
}.items()}
TEAM_NAMES["tt"] = {"town": "🏘 Шәһәр", "mafia": "🔪 Мафия"}
PRESET_NAMES["tt"] = {"classic": "Классика", "extended": "Киңәйтелгән", "chaos": "Хаос", "custom": "Үзенеке"}
ROLE_DESC["tt"] = {
    "mafia": "Төнлә сез калган мафия белән бергә корбан сайлыйсыз. Көндез тыныч кеше булып кыланыгыз.",
    "framer": "Сез мафия өчен уйныйсыз. Һәр төндә уенчы сайлагыз: әгәр детектив аны шул төндә тикшерсә, "
              "«мафия» дип күрәчәк. Максатыгыз — детективларны бутау.",
    "lawyer": "Сез мафия өчен уйныйсыз, ләкин аның кем икәнен белмисез. Һәр төндә мафиозины табарга "
              "тырышыгыз. Тапсагыз — көндез аны яклагыз. Тапмасагыз — тикшергән кешене батырыгыз, чөнки "
              "ул тыныч кеше. Җиңүне санаганда сез мафия командасында.",
    "doctor": "Һәр төндә сез бер уенчыны дәвалыйсыз. Мафия аңа килсә, ул исән кала.",
    "detective": "Һәр төндә сез бер уенчыны тикшерәсез һәм аның мафия булу-булмавын беләсез.",
    "bodyguard": "Һәр төндә сез бер уенчыны саклыйсыз. Мафия аңа һөҗүм итсә, аның урынына сез һәлак буласыз.",
    "partyhost": "Һәр төндә сез бер уенчыны мәҗлескә алып китәсез — аның төнге гамәле үтәлми. "
                 "Мафиозины алып китсәгез, үтерү булмаячак.",
    "driver": "Һәр төндә сез ике уенчының урынын алмаштырасыз: берсенә юнәлтелгән һәрнәрсә икенчесенә эләгә. "
              "Коткарырга да, бутарга да мөмкин — акыл белән сайлагыз.",
    "mayor": "Көндез сезнең тавыш гади, ә кем икәнегез — сер. Уенда бер тапкыр тавыш бирүдән соң сез "
             "куып чыгаруны юкка чыгара аласыз. Алып баручы игълан иткәч, аңа әйтегез.",
    "immortal": "Мафия сезне төнлә үтерә алмый. Ә көндез куарга мөмкин.",
    "lucky": "Сезгә беренче төнге һөҗүм барып чыкмаячак. Аннан соң сез гади тыныч кеше. "
             "Көндез сезне теләсә кайчан куарга мөмкин.",
    "bestfriend": "Сез һәм иң якын дустыгыз — тыныч кешеләр, һәм икегез дә моны беләсез. Бергә булыгыз!",
    "turncoat": "Әлегә сез тыныч кеше. Ләкин беренче мафиози һәлак булгач, сез мафиягә күчәрсез "
                "һәм яңа союздашларыгызны белерсез.",
    "civilian": "Төнлә сез йоклыйсыз. Көндез мафияне эзләгез һәм акыл белән тавыш бирегез.",
}
STORIES["tt"] = {
    "night_header": ["🌅 <b>{r}-нче төннән соңгы иртә. Шәһәр уяна…</b>"],
    "day_header": ["🌆 <b>{r}-нче көн, кич. Тавыш бирү нәтиҗәләре</b>"],
    "kill": [
        "Төн томанлы булды. Шәһәр йоклады, ләкин барысы да түгел. Таң белән кешеләр {v} исемле "
        "уенчыны иске фонтан янында таптылар — мафия шәфкать белми.",
        "Сәгать өчне суккач, бер йортта ут сүнде. Иртән күршеләр аңладылар: {v} башка уянмаячак.",
        "Шәһәр яңгыр тавышы астында йоклап китте. Мафия корбанын сайлады, табиб өлгермәде. "
        "{v} уеннан мәңгегә китә.",
        "Ай болытлар артына яшеренде, тынлыкта ату тавышы яңгырады. Иртән билгеле булды: "
        "{v} мафия тарафыннан үтерелгән.",
        "Төнлә урамнар буйлап номерсыз кара машина узды. Ә иртән шәһәрдә бер кеше җитмәде: "
        "{v} эзсез юкка чыкты.",
    ],
    "bodyguard": [
        "Төнлә мафия ауга чыкты, ләкин үтерүчеләр юлында сакчы басып торды. {v} башка кешене "
        "үзе белән каплады һәм батыр булып һәлак булды.",
        "Караңгыда ату тавышы яңгырады, ләкин пуля кирәкле кешегә тимәде: {v} аркылы ташланды "
        "һәм үз гомере бәрабәренә кеше гомерен коткарды.",
    ],
    "saved": [
        "Төнлә мафия ауга чыкты, ләкин табиб тизрәк булды. Барысы да исән уянды — кемдер төнне "
        "тамчы астында үткәргән булса да. 💉",
        "Шәүләләр корбанның өенә якынлашты, ләкин бусагада инде табиб үз чемоданчыгы белән "
        "басып тора иде. Мафия буш кул белән китте.",
        "Бу төн кемнеңдер соңгысы булырга мөмкин иде. Ләкин табиб могҗиза кылды: барысы да исән!",
    ],
    "survived": [
        "Төнлә мафия һөҗүм итте, ләкин корбан… үлмәде генә. Шәһәр пышылдый: я могҗиза, "
        "я монда кемдер гади түгел.",
        "Үтерүчеләр эшләрен башкардылар, ләкин иртән аларның корбаны урамга исән-сау чыкты. "
        "Мафия аптырашта.",
    ],
    "quiet": [
        "Төн гаҗәп тыныч узды. Мафия посып ята… яки нәрсәдер уйлап таба. 🤔",
        "Шәһәр каты йоклады, хәтта мафия дә ял алган кебек. Барысы да исән — әлегә.",
        "Кайдадыр таңга кадәр музыка яңгырады, ә мафия эшкә чыкмады. Сәер төн булды.",
    ],
    "exile": [
        "Бәхәсләр кичкә кадәр басылмады. Ниһаять, шәһәр карар чыгарды: {v} куып чыгарылды.",
        "Тавыш бирү киеренке булды, ләкин күпчелек {v} исемле уенчыга күрсәтте. Карар кабул ителде.",
        "Шәһәр куркыныч янамаска булды: {v} уеннан китә.",
        "Гаепләүләр, акланулар, кычкырышлар… Ахырда кешеләр {v} исемле уенчыга каршы тавыш бирде.",
    ],
    "no_exile": [
        "Шикләр күп иде, ә дәлилләр аз. Кешеләр беркемне дә кумыйча өйләренә таралыштылар.",
        "Шәһәр килешә алмады. Бүген беркем дә уеннан китми… ләкин төн якын. 🌙",
    ],
    "mayor": [
        "Шәһәр {v} исемле уенчыны куарга карар иткән иде инде, ләкин соңгы мизгелдә мэриядән "
        "фәрман килде: куып чыгару юкка чыгарылды! Кем соң ул мэр? 🎩",
        "{v} инде шәһәр капкасы янында басып тора иде, мэр мөһере белән чапкын йөгереп килде. "
        "Хөкем юкка чыгарылды — {v} шәһәрдә кала.",
    ],
    "tie_revote": ["Тавышлар тигез бүленде, һәм шәһәр кабат тавыш бирергә булды."],
    "tie_rps": ["Тавышлар тигез бүленде, һәм язмышны «таш, кайчы, кәгазь» дуэле хәл итте:\n{x}\n{v} оттырды."],
    "tie_dice": ["Тавышлар тигез бүленде, һәм язмышны кубик хәл итте:\n{x}\nЧират {v} исемле уенчыга төште."],
    "tie_random": ["Тавышлар тигез бүленде, һәм чират {v} исемле уенчыга төште."],
    "win_town": ["🎉 <b>Тыныч кешеләр җиңде!</b> Бөтен мафия тотылды, шәһәр тыныч йокларга мөмкин."],
    "win_mafia": ["🔪 <b>Мафия җиңде!</b> Тыныч кешеләр бик аз калды — шәһәр хәзер мафия кулында."],
}
T["tt"] = {
    "btn_close_room": "Бүлмәне ябу", "close_yes": "Әйе, ябарга",
    "close_confirm": "{n} бүлмәсен ябаргамы? Анда уен барса, ул исәпкә алынмаячак.",
    "cant_close_yet": "Бүлмәне бер тәүлек хәрәкәтсез торгач кына ябып була.",
    "room_closed_by": "{v} {n} бүлмәсен япты.",
    "room_closed_idle": "{n} бүлмәсе бетерелде: анда бер атна буе бернәрсә дә булмады.",
    "room_idle_warning": "{n} бүлмәсе бер тәүлектән бетереләчәк: анда күптән бернәрсә дә булмый. "
                         "Саклап калу өчен төймәгә басыгыз.",
    "btn_keep_room": "Бүлмәне саклау", "room_kept": "Бүлмә сакланды!",
    "idle_for": "Хәрәкәтсез: {v}", "hours": ("сәгать", "сәгать"),
    "rooms_title": "Бүлмәләр", "room": "Бүлмә", "free_room": "Буш бүлмә",
    "no_rooms": "Әлегә бер бүлмә дә юк — буш бүлмәне ачыгыз!",
    "host": "Алып баручы", "no_host": "алып баручы юк", "watchers": "Тамашачылар",
    "invite": "Чакыру", "status_lobby": "җыелу", "status_over": "уен тәмам",
    "status_paused": "тукталыш — алып баручы юк",
    "btn_play": "Уйнарга", "btn_watch": "Карап кына торырга", "btn_my_role": "Минем роль",
    "btn_take_host": "Алып баручы булырга", "btn_release": "Алып баручылыктан китү",
    "btn_end_game": "Уенны тәмамлау", "btn_leave_room": "Бүлмәдән чыгу",
    "cant_leave_alive": "Сез барган уенда тере уенчы — уен беткәч кенә чыгып була.",
    "host_taken_already": "Бу бүлмәнең алып баручысы бар инде.",
    "cant_host_alive": "Сез барган уенда тере уенчы — алып баручы бары тик уеннан чыкканнар "
                       "яки тамашачылар гына була ала.",
    "new_host": "👑 {v} хәзер бу бүлмәнең алып баручысы.",
    "you_released": "Сез инде алып баручы түгел.",
    "host_released": "🙌 {v} алып баручы урынын бушатты. Аны теләсә кем ала ала.",
    "host_released_game": "⏸ {v} алып баручы урынын бушатты — уен туктатылды. "
                          "Алып баручы уеннан чыкканнар һәм тамашачылар була ала.",
    "host_taken_by_owner": "Бот хуҗасы алып баручы ролен үзенә алды.",
    "takehost_no_room": "Башта бүлмәгә керегез: /rooms",
    "game_started_watch": "Уен башланды! Сез тамашачы буларак карыйсыз.",
    "game_aborted": "{v} уенны тәмамлады. Ул исәпкә алынмады. Бүлмә яңадан җыелуга кайтты.",
    "end_confirm": "Уенны чыннан да тәмамларгамы? Ул исәпкә алынмаячак.",
    "end_yes": "Әйе, тәмамларга", "end_no": "Юк, кире кайтырга",
    "back_to_roles": "Рольләргә", "team": "Команда", "count": "Саны",
    "card_pair": "Пар булып санала: ике урын алып тора.",
    "set_vote_mode": "Тавыш бирү",
    "val_vote_mode_host": "алып баручы аша", "val_vote_mode_phones": "телефоннардан",
    "set_tie_default": "Тигезлектә гадәттә",
    "val_tie_default_nobody": "беркем дә", "val_tie_default_rps": "таш-кайчы-кәгазь",
    "val_tie_default_random": "кубик", "val_tie_default_revote": "кабат тавыш бирү",
    "set_show_names": "Исемнәр җәяләрдә",
    "btn_open_vote": "Тавыш бирүне ачу", "btn_close_vote": "Тавыш бирүне ябу",
    "btn_cancel_votes": "Тавышларны юкка чыгару",
    "vote_hint_host": "Кандидатны сайлагыз һәм аның өчен кем тавыш биргәнен билгеләгез. "
                      "Тавышны «Тавышларны юкка чыгару» аша гына үзгәртеп була.",
    "vote_hint_phones": "Уенчылар бот белән шәхси чатта тавыш бирә. Исәпне сез генә күрәсез.",
    "voted": "Тавыш бирделәр", "not_voted": "Әле тавыш бирмәделәр",
    "already_voted_host": "Бу уенчы тавыш биргән инде. Тавышны «Тавышларны юкка чыгару» бүлегендә "
                          "юкка чыгарып була.",
    "cancel_hint": "Юкка чыгару өчен тавышка басыгыз. Аннан соң уенчы яңадан тавыш бирә ала.",
    "ballot_title": "Тавыш бирү!", "ballot_hint": "Шәһәрдән кемне куарга? Тавыш яшерен.",
    "your_vote": "Сезнең тавыш: <b>{v}</b>",
    "your_vote_hint": "Тавышны үзгәртер өчен, башта аны юкка чыгарыгыз.",
    "btn_cancel_my_vote": "Тавышымны юкка чыгару",
    "already_voted": "Сез тавыш бирдегез инде. Үзгәртер өчен, тавышыгызны юкка чыгарыгыз.",
    "vote_closed": "Тавыш бирү ябылды.", "vote_not_open": "Хәзер тавыш бирү ябык.",
    "tie_choose": "Ничек хәл итәбез?",
    "tie_nobody": "Беркем дә китми", "tie_rps": "Таш, кайчы, кәгазь",
    "tie_random": "Кубик", "tie_revote": "Кабат тавыш бирү",
    "decided": "Китә: {v}",
    "rps_title": "Таш, кайчы, кәгазь", "rps_round": "раунд",
    "rps_prompt": "Тавыш бирүдә тигезлек! Көндәшләрегез: {v}. Оттырган кеше шәһәрдән китә. Сезнең чират:",
    "rps_chosen": "Сезнең сайлау: {v}. Көндәшләрне көтәбез…",
    "rps_expired": "Бу раунд инде актуаль түгел.",
    "rps_you_safe": "Сез дуэльдә җиңдегез һәм уенда каласыз!",
    "rps_you_lost": "Сез дуэльдә оттырдыгыз.",
    "rps_cancelled": "Алып баручы дуэльне туктатты.",
    "btn_rps_random": "Сайламаганнар өчен очраклы сайлау",
    "btn_rps_cancel": "Дуэльне туктату",
    "dice_title": "Тигезлек! Кубик ташлыйбыз:",
    "back": "Кире", "skip": "Беркем дә / калдыру", "auto": "авто", "pts": "балл",
    "years": ("ел", "ел"), "months": ("ай", "ай"), "days": ("көн", "көн"),
    "only_host": "Бу төймәләр алып баручы өчен генә",
    "lobby": "Лобби", "players": "Уенчылар", "nobody_yet": "әлегә беркем дә юк",
    "preset": "Рольләр җыелмасы", "will_drop": "уенчылар җитмәячәк: {roles}",
    "btn_roles": "Рольләр", "btn_settings": "Көйләүләр", "btn_players": "Уенчылар",
    "btn_deal": "Рольләрне тарату", "btn_refresh": "Яңарту",
    "kick_hint": "Уенчыны тамашачыларга күчерү өчен аңа басыгыз.",
    "kicked": "Алып баручы сезне тамашачыларга күчерде. Уйнау өчен бүлмәдә «Уйнарга» төймәсенә басыгыз.",
    "player_joined": "{v} кушылды (барлыгы: {n})",
    "player_left": "{v} бүлмәдән чыкты",
    "nick_changed": "{a} хәзер {b} дип атала",
    "roles_title": "Рольләр җыелмасы",
    "roles_hint": "Рольләр уенчылардан азрак булганда гына бот тыныч кешеләрне үзе өсти. "
                  "Уенчылар җитмәсә, артык рольләр автоматик рәвештә алына.",
    "mafia_auto": "Мафия: авто (4 уенчыга 1)",
    "settings_title": "Алып баручы көйләүләре",
    "settings_hint": "Үзгәртү өчен көйләүгә басыгыз.",
    "set_reveal": "Чыгучыларны ачу",
    "val_reveal_full": "роль", "val_reveal_team": "команда", "val_reveal_none": "юк",
    "set_doctor_self": "Табиб үзен дәвалый",
    "set_doctor_repeat": "Табиб бер кешене 2 төн рәттән дәвалый",
    "set_first_phase": "Уен башы",
    "val_first_phase_night": "төн", "val_first_phase_day": "танышу көне",
    "set_auto_broadcast": "Хикәяләрне автоматик җибәрү",
    "set_detective_dm": "Детективка нәтиҗә шәхси хәбәрдә",
    "set_lawyer_dm": "Адвокатка нәтиҗә шәхси хәбәрдә",
    "need_3": "Ким дигәндә 3 уенчы кирәк.",
    "roles_dealt": "Рольләр таратылды!",
    "dropped": "Уенчылар җитмәде, алынды: {roles}",
    "dm_failed": "Рольне җибәреп булмады: {v}. Алар ботта Start басарга тиеш.",
    "your_role": "Сезнең роль", "your_team": "Сезнең команда",
    "your_friend": "Иң якын дустыгыз: {v} — ул да тыныч кеше.",
    "keep_secret": "Бу хәбәрне беркемгә дә күрсәтмәгез!",
    "you_are_out": "Сез уеннан чыктыгыз.",
    "lucky_spent": "🍀 Бәхетегез инде кулланылды.",
    "lawyer_done": "✅ Сез мафияне таптыгыз инде — хәзер көндез аны яклагыз.",
    "night": "Төн", "mafia_team_kill": "Мафия",
    "night_hint": "⇒ — барлык сайлауларны исәпкә алып, алдан нәтиҗә.",
    "blocked": "мәҗлестә",
    "res_mafia": "МАФИЯ", "res_town": "мафия түгел", "res_right": "тапты", "res_wrong": "ялгышты",
    "pick_mafia": "Мафия кемне сайлады?",
    "pick_doctor": "кемне дәвалый?", "pick_detective": "кемне тикшерә?",
    "pick_lawyer": "кемне мафия дип саный?", "pick_bodyguard": "кемне саклый?",
    "pick_partyhost": "кемне мәҗлескә чакыра?", "pick_framer": "кемгә яла яга?",
    "pick_driver": "кемнәрне алмаштыра? (икесен сайлагыз)",
    "btn_view": "Составы", "btn_end_night": "Төнне тәмамлау",
    "day": "Көн", "alive": "Исәннәр",
    "intro_day": "Танышу көне", "intro_hint": "Уенчылар таныша. Бүген тавыш бирү юк.",
    "btn_start_night": "Төнне башлау",
    "vote_title": "Тавыш бирү",
    "who_voted_for": "Кем каршы тавыш бирде: <b>{v}</b>?",
    "voters_hint": "☑️ — шушы кандидат өчен, ▫️ — башка кандидат өчен (күчерү өчен басыгыз).",
    "back_to_vote": "Кандидатларга",
    "vote_result": "Тавыш бирү нәтиҗәсе", "no_votes": "Тавышлар юк.",
    "leader": "Иң күп тавыш: <b>{v}</b>", "tie": "Тигезлек: {v}",
    "btn_exile": "Куарга: {v}", "btn_mayor": "Мэр куып чыгаруны туктатты",
    "btn_no_exile": "Беркемне дә кумаска",
    "dead_night": "Бу төндә сезне үтерделәр. Калып карап торырга була, тик эндәшмичә! 🤫",
    "dead_day": "Шәһәр сезгә каршы тавыш бирде. Калып карап торырга була, тик эндәшмичә! 🤫",
    "lucky_saved": "Бу төндә сезгә һөҗүм иттеләр, ләкин бәхетегез бар икән! Башка бәхет ярдәм итмәс.",
    "dm_check": "Тикшерү нәтиҗәсе: {v} — <b>{res}</b>",
    "dm_lawyer_ok": "Сез таптыгыз: {v} — мафия! Хәзер аны яклагыз.",
    "dm_lawyer_no": "Ялгыштыгыз: {v} — мафия түгел.",
    "you_turned": "Беренче мафиози һәлак булды. Хәзер сез — мафия!",
    "turncoat_joined": "Хыянәтче {v} сезнең якка күчте!",
    "story_title": "Кычкырып уку өчен хикәя", "for_host": "Алып баручы өчен",
    "btn_broadcast": "Хикәяне барлык уенчыларга җибәрү", "btn_next": "Алга",
    "auto_sent": "Хикәя уенчыларга җибәрелде.",
    "broadcast_done": "Уенчыларга җибәрелде: {n}",
    "reveal_role": "Роль: {role}.", "reveal_team": "Команда: {team}.",
    "note_kill_blocked": "мәҗлесче мафиозины алып китте — үтерү юк",
    "note_immortal": "мафия үлемсезгә һөҗүм итте: {v}",
    "note_saved": "табиб коткарды: {v}",
    "note_guarded": "сакчы {b} һәлак булды, {v} кешесен саклап",
    "note_lucky": "{v} бәхет аркасында исән калды",
    "note_redirected": "таксист һөҗүмне {v} кешесеннән {b} кешесенә юнәлтте",
    "note_check_mafia": "детектив {d} тикшерде — {v}: мафия",
    "note_check_town": "детектив {d} тикшерде — {v}: мафия түгел",
    "note_lawyer_ok": "адвокат {d} мафияне тапты: {v}",
    "note_lawyer_no": "адвокат {d} ялгышты: {v}",
    "note_turned": "хыянәтче {v} мафиягә күчте",
    "note_mayor": "мэр {v} уенчысын куудан коткарды",
    "game_over": "Уен тәмам",
    "btn_rematch": "Бу бүлмәдә яңа уен",
    "rematch": "Шул ук бүлмәдә яңа уен! Ролегезне көтегез.",
    "you_are_host": "Сез — алып баручы! Панель түбәндә.",
    "owner_only": "Бу команда бот хуҗасы өчен генә.",
    "no_role": "Сезнең әлегә роль юк.",
    "cancelled": "Ярый, бернәрсә дә үзгәртмибез 🙂",
    "help_short": "Командалар: /rooms — бүлмәләр, /profile — профиль, /role — минем роль, "
                  "/leave — бүлмәдән чыгу.",
    "profile": "Профиль", "nick": "Ник", "real_name": "Исем", "gender": "Җенес",
    "language": "Тел", "registered": "Теркәлгән көн", "tenure": "Стаж",
    "points_total": "Барлык баллар", "points_last": "Соңгы уендагы баллар",
    "games_played": "Уеннар", "wins": "җиңү",
    "gender_m": "Ир-ат", "gender_f": "Хатын-кыз", "gender_none": "Күрсәтелмәгән",
    "btn_nick": "Ник", "btn_name": "Исем", "btn_gender": "Җенес", "btn_lang": "Тел",
    "btn_photo": "Фото", "btn_games": "Минем уеннар",
    "ask_nick": "Уен никегезне языгыз ({a}–{b} символ). Аны барлык уенчылар күрәчәк. Кире кагу: /cancel",
    "ask_name": "Чын исемегезне языгыз. Аны алып баручы гына күрә. Кире кагу: /cancel",
    "ask_gender": "Җенесегезне сайлагыз:",
    "ask_photo": "Фотоны бер хәбәр белән җибәрегез. Кире кагу: /cancel",
    "bad_nick": "Ник {a}–{b} символдан торырга һәм «/» белән башланмаска тиеш. Тагын бер тапкыр: /profile",
    "bad_name": "Исем туры килми. /profile аша яңадан карагыз",
    "nick_after_game": "Никны уен беткәч кенә үзгәртеп була.",
    "nick_taken": "Бу ник лоббида башка уенчыда инде. Башкасын сайлагыз: /profile",
    "nick_saved": "Сезнең ник: <b>{v}</b>", "name_saved": "Сезнең исем: <b>{v}</b>",
    "gender_saved": "Җенес: {v}", "lang_saved": "Тел: Татарча",
    "ask_lang": "Телне сайлагыз:",
    "photo_saved": "Фото сакланды!", "photo_deleted": "Фото бетерелде.",
    "delete_photo": "Фотоны бетерү",
    "photo_hint": "Профиль фотосын алмаштыру өчен /profile → Фото ачыгыз.",
    "no_games": "Сез әле бер уен да уйнамадыгыз.",
    "games_more": "…һәм тагын {n}",
}
COMMANDS["tt"] = [("start", "Төп меню"), ("rooms", "Бүлмәләр"), ("profile", "Минем профиль"),
                  ("role", "Минем роль"), ("panel", "Алып баручы панеле"),
                  ("leave", "Бүлмәдән чыгу"), ("cancel", "Кертүне туктату")]

# ===========================================================================
# ҚАЗАҚША (kk)
# ===========================================================================
LANG_NAMES["kk"] = "Қазақша"
ROLE_NAMES["kk"] = {r: (n, n) for r, n in {
    "mafia": "Мафия", "framer": "Жала жабушы", "lawyer": "Адвокат", "doctor": "Дәрігер",
    "detective": "Детектив", "bodyguard": "Оққағар", "partyhost": "Тойшыл",
    "driver": "Таксист", "mayor": "Әкім", "immortal": "Өлмейтін", "lucky": "Жолы болғыш",
    "bestfriend": "Ең жақын дос", "turncoat": "Сатқын", "civilian": "Бейбіт тұрғын",
}.items()}
TEAM_NAMES["kk"] = {"town": "🏘 Қала", "mafia": "🔪 Мафия"}
PRESET_NAMES["kk"] = {"classic": "Классика", "extended": "Кеңейтілген", "chaos": "Хаос", "custom": "Өзіндік"}
ROLE_DESC["kk"] = {
    "mafia": "Түнде сіз басқа мафиямен бірге құрбан таңдайсыз. Күндіз бейбіт тұрғын болып көрініңіз.",
    "framer": "Сіз мафия үшін ойнайсыз. Әр түні бір ойыншыны таңдаңыз: егер детектив оны сол түні "
              "тексерсе, «мафия» деп көреді. Мақсатыңыз — детективтерді шатастыру.",
    "lawyer": "Сіз мафия үшін ойнайсыз, бірақ олардың кім екенін білмейсіз. Әр түні мафиозиді табуға "
              "тырысыңыз. Тапсаңыз — күндіз оны қорғаңыз. Таппасаңыз — тексерген адамды батырыңыз, "
              "өйткені ол бейбіт тұрғын. Жеңісті санағанда сіз мафия командасындасыз.",
    "doctor": "Әр түні сіз бір ойыншыны емдейсіз. Мафия оған келсе, ол тірі қалады.",
    "detective": "Әр түні сіз бір ойыншыны тексеріп, оның мафия екенін не емес екенін білесіз.",
    "bodyguard": "Әр түні сіз бір ойыншыны күзетесіз. Мафия оған шабуыл жасаса, оның орнына сіз қаза табасыз.",
    "partyhost": "Әр түні сіз бір ойыншыны тойға алып кетесіз — оның түнгі әрекеті орындалмайды. "
                 "Мафиозиді алып кетсеңіз, өлтіру болмайды.",
    "driver": "Әр түні сіз екі ойыншының орнын ауыстырасыз: біреуіне бағытталғанның бәрі екіншісіне тиеді. "
              "Құтқаруға да, шатастыруға да болады — ақылмен таңдаңыз.",
    "mayor": "Күндіз сіздің дауысыңыз қарапайым, ал кім екеніңіз — құпия. Ойында бір рет дауыс беруден "
             "кейін қууды болдырмай аласыз. Жүргізуші жариялағанда оған айтыңыз.",
    "immortal": "Мафия сізді түнде өлтіре алмайды. Ал күндіз қууға болады.",
    "lucky": "Сізге жасалған алғашқы түнгі шабуыл сәтсіз болады. Одан кейін сіз қарапайым бейбіт "
             "тұрғынсыз. Күндіз сізді кез келген уақытта қууға болады.",
    "bestfriend": "Сіз және ең жақын досыңыз — бейбіт тұрғындарсыз, және екеуіңіз де мұны білесіздер. "
                  "Бірге болыңыздар!",
    "turncoat": "Әзірге сіз бейбіт тұрғынсыз. Бірақ алғашқы мафиози қаза тапқанда, сіз мафияға өтіп, "
                "жаңа одақтастарыңызды білесіз.",
    "civilian": "Түнде сіз ұйықтайсыз. Күндіз мафияны іздеп, ақылмен дауыс беріңіз.",
}
STORIES["kk"] = {
    "night_header": ["🌅 <b>{r}-түннен кейінгі таң. Қала оянуда…</b>"],
    "day_header": ["🌆 <b>{r}-күннің кеші. Дауыс беру қорытындысы</b>"],
    "kill": [
        "Түн тұманды болды. Қала ұйықтады, бірақ бәрі емес. Таң ата тұрғындар {v} деген ойыншыны "
        "ескі фонтанның жанынан тапты — мафия аяушылықты білмейді.",
        "Сағат үшті соққанда, бір үйдің жарығы сөнді. Таңертең көршілер түсінді: {v} енді оянбайды.",
        "Қала жаңбыр дыбысымен ұйықтап кетті. Мафия құрбанын таңдады, дәрігер үлгермеді. "
        "{v} ойыннан мәңгіге кетеді.",
        "Ай бұлттың артына жасырынды, тыныштықта атылған оқтың даусы шықты. Таңертең белгілі болды: "
        "{v} мафияның қолынан қаза тапты.",
        "Түнде көшелермен нөмірсіз қара көлік өтті. Ал таңертең қалада бір тұрғын жетіспеді: "
        "{v} із-түзсіз жоғалды.",
    ],
    "bodyguard": [
        "Түнде мафия аңға шықты, бірақ өлтірушілердің жолында оққағар тұрды. {v} басқа адамды "
        "өзімен қалқалап, батыр ретінде қаза тапты.",
        "Қараңғыда оқ атылды, бірақ ол көздеген адамға тимеді: {v} алдына атылып, өз өмірі есебінен "
        "біреудің өмірін сақтап қалды.",
    ],
    "saved": [
        "Түнде мафия аңға шықты, бірақ дәрігер жылдамырақ болды. Бәрі тірі оянды — біреу түнді "
        "тамшылатқыштың астында өткізгені анық болса да. 💉",
        "Көлеңкелер құрбанның үйіне жақындады, бірақ табалдырықта дәрігер өз сөмкесімен тұрған еді. "
        "Мафия құр қол кетті.",
        "Бұл түн біреу үшін соңғы болуы мүмкін еді. Бірақ дәрігер ғажайып жасады: бәрі тірі!",
    ],
    "survived": [
        "Түнде мафия шабуыл жасады, бірақ құрбан… жай ғана өлмеді. Қала сыбырлайды: не ғажайып, "
        "не мұнда біреу соншалықты қарапайым емес.",
        "Өлтірушілер өз ісін істеді, бірақ таңертең олардың құрбаны көшеге аман-есен шықты. "
        "Мафия абдырап қалды.",
    ],
    "quiet": [
        "Түн таңқаларлықтай тыныш өтті. Мафия жасырынып жатыр… немесе бір нәрсе ойлап жүр. 🤔",
        "Қала қатты ұйықтады, тіпті мафия да демалыс алған сияқты. Бәрі тірі — әзірге.",
        "Бір жерде таңға дейін музыка ойнады, ал мафия іске шықпады. Біртүрлі түн болды.",
    ],
    "exile": [
        "Даулар кешке дейін басылмады. Ақырында қала шешім шығарды: {v} қуылды.",
        "Дауыс беру шиеленісті болды, бірақ көпшілік {v} деген ойыншыны көрсетті. Шешім қабылданды.",
        "Қала тәуекелге бармауды шешті: {v} ойыннан кетеді.",
        "Айыптаулар, ақталулар, айқай… Соңында тұрғындар {v} деген ойыншыға қарсы дауыс берді.",
    ],
    "no_exile": [
        "Күдік көп болды, ал дәлел аз. Тұрғындар ешкімді қумай, үйлеріне тарады.",
        "Қала келісе алмады. Бүгін ешкім ойыннан кетпейді… бірақ түн жақын. 🌙",
    ],
    "mayor": [
        "Қала {v} деген ойыншыны қууды шешіп қойған еді, бірақ соңғы сәтте әкімдіктен жарлық келді: "
        "қуу болдырылмады! Әкім кім екен? 🎩",
        "{v} қала қақпасының алдында тұрған кезде әкімнің мөрі бар шабарман жүгіріп келді. "
        "Үкім болдырылмады — {v} қалада қалады.",
    ],
    "tie_revote": ["Дауыстар тең бөлінді, сондықтан қала қайта дауыс беруді шешті."],
    "tie_rps": ["Дауыстар тең бөлінді, ал тағдырды «тас, қайшы, қағаз» жекпе-жегі шешті:\n{x}\n{v} жеңілді."],
    "tie_dice": ["Дауыстар тең бөлінді, ал тағдырды кубик шешті:\n{x}\nЖеребе {v} деген ойыншыға түсті."],
    "tie_random": ["Дауыстар тең бөлінді, және жеребе {v} деген ойыншыға түсті."],
    "win_town": ["🎉 <b>Бейбіт тұрғындар жеңді!</b> Барлық мафия ұсталды, қала тыныш ұйықтай алады."],
    "win_mafia": ["🔪 <b>Мафия жеңді!</b> Бейбіт тұрғындар тым аз қалды — қала енді мафияның қолында."],
}
T["kk"] = {
    "btn_close_room": "Бөлмені жабу", "close_yes": "Иә, жабу",
    "close_confirm": "{n}-бөлмені жабу керек пе? Онда ойын жүріп жатса, ол есептелмейді.",
    "cant_close_yet": "Бөлмені бір тәулік әрекетсіз тұрғаннан кейін ғана жабуға болады.",
    "room_closed_by": "{v} {n}-бөлмені жапты.",
    "room_closed_idle": "{n}-бөлме жойылды: онда бір апта бойы ештеңе болмады.",
    "room_idle_warning": "{n}-бөлме бір тәуліктен кейін жойылады: онда көптен бері ештеңе болмай жатыр. "
                         "Сақтап қалу үшін батырманы басыңыз.",
    "btn_keep_room": "Бөлмені сақтау", "room_kept": "Бөлме сақталды!",
    "idle_for": "Әрекетсіз: {v}", "hours": ("сағат", "сағат"),
    "rooms_title": "Бөлмелер", "room": "Бөлме", "free_room": "Бос бөлме",
    "no_rooms": "Әзірге бірде-бір бөлме жоқ — бос бөлмені ашыңыз!",
    "host": "Жүргізуші", "no_host": "жүргізуші жоқ", "watchers": "Көрермендер",
    "invite": "Шақыру", "status_lobby": "жиналу", "status_over": "ойын аяқталды",
    "status_paused": "үзіліс — жүргізуші жоқ",
    "btn_play": "Ойнау", "btn_watch": "Тек көру", "btn_my_role": "Менің рөлім",
    "btn_take_host": "Жүргізуші болу", "btn_release": "Жүргізушіліктен бас тарту",
    "btn_end_game": "Ойынды аяқтау", "btn_leave_room": "Бөлмеден шығу",
    "cant_leave_alive": "Сіз жүріп жатқан ойындағы тірі ойыншысыз — ойын біткен соң ғана шыға аласыз.",
    "host_taken_already": "Бұл бөлменің жүргізушісі бар.",
    "cant_host_alive": "Сіз жүріп жатқан ойындағы тірі ойыншысыз — жүргізуші тек ойыннан шыққандар "
                       "немесе көрермендер бола алады.",
    "new_host": "👑 {v} енді осы бөлменің жүргізушісі.",
    "you_released": "Сіз енді жүргізуші емессіз.",
    "host_released": "🙌 {v} жүргізуші орнын босатты. Оны кез келген адам ала алады.",
    "host_released_game": "⏸ {v} жүргізуші орнын босатты — ойын тоқтатылды. "
                          "Жүргізуші ойыннан шыққандар мен көрермендер бола алады.",
    "host_taken_by_owner": "Бот иесі жүргізуші рөлін өзіне алды.",
    "takehost_no_room": "Алдымен бөлмеге кіріңіз: /rooms",
    "game_started_watch": "Ойын басталды! Сіз көрермен ретінде қарап отырсыз.",
    "game_aborted": "{v} ойынды аяқтады. Ол есептелмейді. Бөлме қайтадан жиналуға оралды.",
    "end_confirm": "Ойынды шынымен аяқтау керек пе? Ол есептелмейді.",
    "end_yes": "Иә, аяқтау", "end_no": "Жоқ, оралу",
    "back_to_roles": "Рөлдерге", "team": "Команда", "count": "Саны",
    "card_pair": "Жұп болып саналады: екі орын алады.",
    "set_vote_mode": "Дауыс беру",
    "val_vote_mode_host": "жүргізуші арқылы", "val_vote_mode_phones": "телефондардан",
    "set_tie_default": "Тең дауыста әдепкі",
    "val_tie_default_nobody": "ешкім", "val_tie_default_rps": "тас-қайшы-қағаз",
    "val_tie_default_random": "кубик", "val_tie_default_revote": "қайта дауыс беру",
    "set_show_names": "Есімдер жақшада",
    "btn_open_vote": "Дауыс беруді ашу", "btn_close_vote": "Дауыс беруді жабу",
    "btn_cancel_votes": "Дауыстарды болдырмау",
    "vote_hint_host": "Үміткерді таңдап, оған кім дауыс бергенін белгілеңіз. "
                      "Дауысты тек «Дауыстарды болдырмау» арқылы өзгертуге болады.",
    "vote_hint_phones": "Ойыншылар ботпен жеке чатта дауыс береді. Есепті тек сіз көресіз.",
    "voted": "Дауыс бергендер", "not_voted": "Әлі дауыс бермегендер",
    "already_voted_host": "Бұл ойыншы дауыс беріп қойған. Дауысты «Дауыстарды болдырмау» бөлімінде "
                          "болдырмауға болады.",
    "cancel_hint": "Болдырмау үшін дауысты басыңыз. Содан кейін ойыншы қайта дауыс бере алады.",
    "ballot_title": "Дауыс беру!", "ballot_hint": "Қаладан кімді қуамыз? Дауыс құпия.",
    "your_vote": "Сіздің дауысыңыз: <b>{v}</b>",
    "your_vote_hint": "Дауысты өзгерту үшін алдымен оны болдырмаңыз.",
    "btn_cancel_my_vote": "Дауысымды болдырмау",
    "already_voted": "Сіз дауыс беріп қойдыңыз. Өзгерту үшін дауысыңызды болдырмаңыз.",
    "vote_closed": "Дауыс беру жабылды.", "vote_not_open": "Қазір дауыс беру жабық.",
    "tie_choose": "Қалай шешеміз?",
    "tie_nobody": "Ешкім шықпайды", "tie_rps": "Тас, қайшы, қағаз",
    "tie_random": "Кубик", "tie_revote": "Қайта дауыс беру",
    "decided": "Шығады: {v}",
    "rps_title": "Тас, қайшы, қағаз", "rps_round": "раунд",
    "rps_prompt": "Дауыс беруде тең түсті! Қарсыластарыңыз: {v}. Жеңілген қаладан кетеді. Сіздің жүрісіңіз:",
    "rps_chosen": "Сіздің таңдауыңыз: {v}. Қарсыластарды күтеміз…",
    "rps_expired": "Бұл раунд енді өзекті емес.",
    "rps_you_safe": "Сіз жекпе-жекте жеңдіңіз және ойында қаласыз!",
    "rps_you_lost": "Сіз жекпе-жекте жеңілдіңіз.",
    "rps_cancelled": "Жүргізуші жекпе-жекті тоқтатты.",
    "btn_rps_random": "Таңдамағандар үшін кездейсоқ таңдау",
    "btn_rps_cancel": "Жекпе-жекті тоқтату",
    "dice_title": "Тең дауыс! Кубик лақтырамыз:",
    "back": "Артқа", "skip": "Ешкім / өткізу", "auto": "авто", "pts": "ұпай",
    "years": ("жыл", "жыл"), "months": ("ай", "ай"), "days": ("күн", "күн"),
    "only_host": "Бұл батырмалар тек жүргізушіге арналған",
    "lobby": "Лобби", "players": "Ойыншылар", "nobody_yet": "әзірге ешкім жоқ",
    "preset": "Рөлдер жиынтығы", "will_drop": "ойыншылар жетпейді: {roles}",
    "btn_roles": "Рөлдер", "btn_settings": "Баптаулар", "btn_players": "Ойыншылар",
    "btn_deal": "Рөлдерді тарату", "btn_refresh": "Жаңарту",
    "kick_hint": "Ойыншыны көрермендерге ауыстыру үшін оны басыңыз.",
    "kicked": "Жүргізуші сізді көрермендерге ауыстырды. Ойнау үшін бөлмеде «Ойнау» батырмасын басыңыз.",
    "player_joined": "{v} қосылды (барлығы: {n})",
    "player_left": "{v} бөлмеден шықты",
    "nick_changed": "{a} енді {b} деп аталады",
    "roles_title": "Рөлдер жиынтығы",
    "roles_hint": "Рөлдер ойыншылардан аз болса ғана бот бейбіт тұрғындарды өзі қосады. "
                  "Ойыншылар жетпесе, артық рөлдер автоматты түрде алынып тасталады.",
    "mafia_auto": "Мафия: авто (4 ойыншыға 1)",
    "settings_title": "Жүргізуші баптаулары",
    "settings_hint": "Ауыстыру үшін баптауды басыңыз.",
    "set_reveal": "Шыққандарды ашу",
    "val_reveal_full": "рөлі", "val_reveal_team": "командасы", "val_reveal_none": "жоқ",
    "set_doctor_self": "Дәрігер өзін емдейді",
    "set_doctor_repeat": "Дәрігер бір адамды 2 түн қатарынан емдейді",
    "set_first_phase": "Ойын басы",
    "val_first_phase_night": "түн", "val_first_phase_day": "танысу күні",
    "set_auto_broadcast": "Әңгімелерді автожіберу",
    "set_detective_dm": "Нәтиже детективке жеке хатта",
    "set_lawyer_dm": "Нәтиже адвокатқа жеке хатта",
    "need_3": "Кемінде 3 ойыншы қажет.",
    "roles_dealt": "Рөлдер таратылды!",
    "dropped": "Ойыншылар жетпеді, алынды: {roles}",
    "dm_failed": "Рөлді жіберу мүмкін болмады: {v}. Олар ботта Start басуы керек.",
    "your_role": "Сіздің рөліңіз", "your_team": "Сіздің командаңыз",
    "your_friend": "Ең жақын досыңыз: {v} — ол да бейбіт тұрғын.",
    "keep_secret": "Бұл хабарламаны ешкімге көрсетпеңіз!",
    "you_are_out": "Сіз ойыннан шықтыңыз.",
    "lucky_spent": "🍀 Сіздің жолыңыз пайдаланылып қойды.",
    "lawyer_done": "✅ Сіз мафияны тауып қойдыңыз — енді күндіз оны қорғаңыз.",
    "night": "Түн", "mafia_team_kill": "Мафия",
    "night_hint": "⇒ — барлық таңдауды ескергендегі алдын ала нәтиже.",
    "blocked": "тойда",
    "res_mafia": "МАФИЯ", "res_town": "мафия емес", "res_right": "тапты", "res_wrong": "қателесті",
    "pick_mafia": "Мафия кімді таңдады?",
    "pick_doctor": "кімді емдейді?", "pick_detective": "кімді тексереді?",
    "pick_lawyer": "кімді мафия деп санайды?", "pick_bodyguard": "кімді күзетеді?",
    "pick_partyhost": "кімді тойға шақырады?", "pick_framer": "кімге жала жабады?",
    "pick_driver": "кімдердің орнын ауыстырады? (екеуін таңдаңыз)",
    "btn_view": "Құрамы", "btn_end_night": "Түнді аяқтау",
    "day": "Күн", "alive": "Тірілер",
    "intro_day": "Танысу күні", "intro_hint": "Ойыншылар танысады. Бүгін дауыс беру жоқ.",
    "btn_start_night": "Түнді бастау",
    "vote_title": "Дауыс беру",
    "who_voted_for": "Кім қарсы дауыс берді: <b>{v}</b>?",
    "voters_hint": "☑️ — осы үміткер үшін, ▫️ — басқа үміткер үшін (ауыстыру үшін басыңыз).",
    "back_to_vote": "Үміткерлерге",
    "vote_result": "Дауыс беру қорытындысы", "no_votes": "Дауыстар жоқ.",
    "leader": "Ең көп дауыс: <b>{v}</b>", "tie": "Тең дауыс: {v}",
    "btn_exile": "Қуу: {v}", "btn_mayor": "Әкім қууды болдырмады",
    "btn_no_exile": "Ешкімді қумау",
    "dead_night": "Бұл түні сізді өлтірді. Қалып көруге болады, бірақ үнсіз! 🤫",
    "dead_day": "Қала сізге қарсы дауыс берді. Қалып көруге болады, бірақ үнсіз! 🤫",
    "lucky_saved": "Бұл түні сізге шабуыл жасалды, бірақ жолыңыз болды! Енді жол көмектеспейді.",
    "dm_check": "Тексеру нәтижесі: {v} — <b>{res}</b>",
    "dm_lawyer_ok": "Таптыңыз: {v} — мафия! Енді оны қорғаңыз.",
    "dm_lawyer_no": "Қателестіңіз: {v} — мафия емес.",
    "you_turned": "Алғашқы мафиози қаза тапты. Енді сіз — мафиясыз!",
    "turncoat_joined": "Сатқын {v} сіздің жағыңызға өтті!",
    "story_title": "Дауыстап оқуға арналған әңгіме", "for_host": "Жүргізуші үшін",
    "btn_broadcast": "Әңгімені барлық ойыншыларға жіберу", "btn_next": "Әрі қарай",
    "auto_sent": "Әңгіме ойыншыларға жіберілді.",
    "broadcast_done": "Ойыншыларға жіберілді: {n}",
    "reveal_role": "Рөлі: {role}.", "reveal_team": "Командасы: {team}.",
    "note_kill_blocked": "тойшыл мафиозиді алып кетті — өлтіру жоқ",
    "note_immortal": "мафия өлмейтінге шабуыл жасады: {v}",
    "note_saved": "дәрігер құтқарды: {v}",
    "note_guarded": "оққағар {b} қаза тапты, {v} қорғап",
    "note_lucky": "{v} жолы болып аман қалды",
    "note_redirected": "таксист шабуылды {v} дегеннен {b} дегенге бұрды",
    "note_check_mafia": "детектив {d} тексерді — {v}: мафия",
    "note_check_town": "детектив {d} тексерді — {v}: мафия емес",
    "note_lawyer_ok": "адвокат {d} мафияны тапты: {v}",
    "note_lawyer_no": "адвокат {d} қателесті: {v}",
    "note_turned": "сатқын {v} мафияға өтті",
    "note_mayor": "әкім {v} ойыншысын қуудан құтқарды",
    "game_over": "Ойын аяқталды",
    "btn_rematch": "Осы бөлмеде жаңа ойын",
    "rematch": "Сол бөлмеде жаңа ойын! Рөліңізді күтіңіз.",
    "you_are_host": "Сіз — жүргізушісіз! Панель төменде.",
    "owner_only": "Бұл команда тек бот иесіне арналған.",
    "no_role": "Сізде әзірге рөл жоқ.",
    "cancelled": "Жақсы, ештеңе өзгертпейміз 🙂",
    "help_short": "Командалар: /rooms — бөлмелер, /profile — профиль, /role — менің рөлім, "
                  "/leave — бөлмеден шығу.",
    "profile": "Профиль", "nick": "Ник", "real_name": "Аты", "gender": "Жынысы",
    "language": "Тіл", "registered": "Тіркелген күні", "tenure": "Өтілі",
    "points_total": "Барлық ұпай", "points_last": "Соңғы ойындағы ұпай",
    "games_played": "Ойындар", "wins": "жеңіс",
    "gender_m": "Ер", "gender_f": "Әйел", "gender_none": "Көрсетілмеген",
    "btn_nick": "Ник", "btn_name": "Аты", "btn_gender": "Жынысы", "btn_lang": "Тіл",
    "btn_photo": "Фото", "btn_games": "Менің ойындарым",
    "ask_nick": "Ойын нигіңізді жазыңыз ({a}–{b} таңба). Оны барлық ойыншылар көреді. Болдырмау: /cancel",
    "ask_name": "Шын атыңызды жазыңыз. Оны тек жүргізуші көреді. Болдырмау: /cancel",
    "ask_gender": "Жынысыңызды таңдаңыз:",
    "ask_photo": "Фотоны бір хабарламамен жіберіңіз. Болдырмау: /cancel",
    "bad_nick": "Ник {a}–{b} таңбадан тұруы және «/» белгісімен басталмауы керек. Қайтадан: /profile",
    "bad_name": "Бұл ат жарамайды. /profile арқылы қайталап көріңіз",
    "nick_after_game": "Никті ойын біткен соң өзгертуге болады.",
    "nick_taken": "Бұл ник лоббиде басқа ойыншыда бар. Басқасын таңдаңыз: /profile",
    "nick_saved": "Сіздің нигіңіз: <b>{v}</b>", "name_saved": "Сіздің атыңыз: <b>{v}</b>",
    "gender_saved": "Жынысы: {v}", "lang_saved": "Тіл: Қазақша",
    "ask_lang": "Тілді таңдаңыз:",
    "photo_saved": "Фото сақталды!", "photo_deleted": "Фото жойылды.",
    "delete_photo": "Фотоны жою",
    "photo_hint": "Профиль фотосын ауыстыру үшін /profile → Фото ашыңыз.",
    "no_games": "Сіз әлі бірде-бір ойын ойнаған жоқсыз.",
    "games_more": "…және тағы {n}",
}
COMMANDS["kk"] = [("start", "Басты мәзір"), ("rooms", "Бөлмелер"), ("profile", "Менің профилім"),
                  ("role", "Менің рөлім"), ("panel", "Жүргізуші панелі"),
                  ("leave", "Бөлмеден шығу"), ("cancel", "Енгізуді болдырмау")]

# ===========================================================================
# КЫРГЫЗЧА (ky)
# ===========================================================================
LANG_NAMES["ky"] = "Кыргызча"
ROLE_NAMES["ky"] = {r: (n, n) for r, n in {
    "mafia": "Мафия", "framer": "Жалаачы", "lawyer": "Адвокат", "doctor": "Дарыгер",
    "detective": "Детектив", "bodyguard": "Жан сакчы", "partyhost": "Тойчу",
    "driver": "Таксист", "mayor": "Мэр", "immortal": "Өлбөс", "lucky": "Бактылуу",
    "bestfriend": "Эң жакын дос", "turncoat": "Чыккынчы", "civilian": "Тынч тургун",
}.items()}
TEAM_NAMES["ky"] = {"town": "🏘 Шаар", "mafia": "🔪 Мафия"}
PRESET_NAMES["ky"] = {"classic": "Классика", "extended": "Кеңейтилген", "chaos": "Хаос", "custom": "Өзүңүкү"}
ROLE_DESC["ky"] = {
    "mafia": "Түнкүсүн сиз башка мафия менен бирге курмандыкты тандайсыз. Күндүз тынч тургун болуп көрүнүңүз.",
    "framer": "Сиз мафия үчүн ойнойсуз. Ар түнү бир оюнчуну тандаңыз: эгер детектив аны ошол түнү "
              "текшерсе, «мафия» деп көрөт. Максатыңыз — детективдерди адаштыруу.",
    "lawyer": "Сиз мафия үчүн ойнойсуз, бирок алар кимдер экенин билбейсиз. Ар түнү мафиозини табууга "
              "аракет кылыңыз. Тапсаңыз — күндүз аны коргоңуз. Таппасаңыз — текшерген адамды чөктүрүңүз, "
              "анткени ал тынч тургун. Жеңишти эсептегенде сиз мафиянын командасындасыз.",
    "doctor": "Ар түнү сиз бир оюнчуну дарылайсыз. Мафия ага келсе, ал тирүү калат.",
    "detective": "Ар түнү сиз бир оюнчуну текшерип, ал мафиябы же жокпу экенин билесиз.",
    "bodyguard": "Ар түнү сиз бир оюнчуну коргойсуз. Мафия ага кол салса, анын ордуна сиз каза табасыз.",
    "partyhost": "Ар түнү сиз бир оюнчуну тойго алып кетесиз — анын түнкү аракети аткарылбайт. "
                 "Мафиозини алып кетсеңиз, өлтүрүү болбойт.",
    "driver": "Ар түнү сиз эки оюнчунун ордун алмаштырасыз: бирөөсүнө багытталгандын баары экинчисине "
              "тиет. Куткарууга да, адаштырууга да болот — акыл менен тандаңыз.",
    "mayor": "Күндүз сиздин добушуңуз жөнөкөй, ал эми ким экениңиз — сыр. Оюнда бир жолу добуш берүүдөн "
             "кийин куугунду жокко чыгара аласыз. Алып баруучу жарыялаганда ага айтыңыз.",
    "immortal": "Мафия сизди түнкүсүн өлтүрө албайт. Ал эми күндүз кууп чыгууга болот.",
    "lucky": "Сизге жасалган биринчи түнкү кол салуу ийгиликсиз болот. Андан кийин сиз жөнөкөй тынч "
             "тургунсуз. Күндүз сизди каалаган убакта кууп чыгууга болот.",
    "bestfriend": "Сиз жана эң жакын досуңуз — тынч тургунсуздар, экөөңүз тең муну билесиздер. Бирге болгула!",
    "turncoat": "Азырынча сиз тынч тургунсуз. Бирок биринчи мафиози каза тапканда, сиз мафияга өтүп, "
                "жаңы шериктериңизди билесиз.",
    "civilian": "Түнкүсүн сиз уктайсыз. Күндүз мафияны издеп, акыл менен добуш бериңиз.",
}
STORIES["ky"] = {
    "night_header": ["🌅 <b>{r}-түндөн кийинки таң. Шаар ойгонууда…</b>"],
    "day_header": ["🌆 <b>{r}-күндүн кечи. Добуш берүүнүн жыйынтыгы</b>"],
    "kill": [
        "Түн тумандуу болду. Шаар уктады, бирок баары эмес. Таң атканда тургундар {v} деген оюнчуну "
        "эски фонтандын жанынан табышты — мафия аёону билбейт.",
        "Саат үчтү урганда, бир үйдүн жарыгы өчтү. Эртең менен коңшулар түшүнүштү: {v} мындан ары ойгонбойт.",
        "Шаар жамгырдын үнү менен уктап калды. Мафия курмандыгын тандады, дарыгер үлгүрбөдү. "
        "{v} оюндан түбөлүккө кетет.",
        "Ай булуттун артына жашынды, тынчтыкта ок үнү чыкты. Эртең менен белгилүү болду: "
        "{v} мафиянын колунан каза тапты.",
        "Түнү көчөлөр менен номурсуз кара машина өттү. Ал эми эртең менен шаарда бир тургун жетишпеди: "
        "{v} из-дайынсыз жоголду.",
    ],
    "bodyguard": [
        "Түнү мафия аңчылыкка чыкты, бирок киши өлтүргүчтөрдүн жолунда жан сакчы турду. {v} башка "
        "адамды өзү менен калкалап, баатыр катары каза тапты.",
        "Караңгыда ок атылды, бирок ал көздөгөн адамга тийбеди: {v} алдына ыргып, өз өмүрүнүн эсебинен "
        "бирөөнүн өмүрүн сактап калды.",
    ],
    "saved": [
        "Түнү мафия аңчылыкка чыкты, бирок дарыгер ылдамыраак болду. Баары тирүү ойгонушту — кимдир "
        "бирөө түнү тамчылаткычтын астында өткөргөнү анык болсо да. 💉",
        "Көлөкөлөр курмандыктын үйүнө жакындады, бирок босогодо дарыгер өз баштыгы менен турган эле. "
        "Мафия куру кол кетти.",
        "Бул түн кимдир бирөө үчүн акыркы болушу мүмкүн эле. Бирок дарыгер керемет жасады: баары тирүү!",
    ],
    "survived": [
        "Түнү мафия кол салды, бирок курмандык… жөн эле өлгөн жок. Шаар шыбырайт: же керемет, "
        "же бул жерде кимдир бирөө жөнөкөй эмес.",
        "Киши өлтүргүчтөр ишин бүтүрүштү, бирок эртең менен алардын курмандыгы көчөгө аман-эсен чыкты. "
        "Мафия эмне кыларын билбей калды.",
    ],
    "quiet": [
        "Түн таң калыштуу тынч өттү. Мафия жашынып жатат… же бир нерсе ойлоп жатат. 🤔",
        "Шаар катуу уктады, жада калса мафия да эс алып калгандай. Баары тирүү — азырынча.",
        "Бир жерде таң атканча музыка ойноду, ал эми мафия ишке чыккан жок. Кызык түн болду.",
    ],
    "exile": [
        "Талаш-тартыштар кечке чейин басылган жок. Акыры шаар чечим чыгарды: {v} кууп чыгарылды.",
        "Добуш берүү курч болду, бирок көпчүлүк {v} деген оюнчуну көрсөттү. Чечим кабыл алынды.",
        "Шаар тобокелге барбоону чечти: {v} оюндан кетет.",
        "Айыптоолор, актануулар, кыйкырыктар… Акыры тургундар {v} деген оюнчуга каршы добуш беришти.",
    ],
    "no_exile": [
        "Шектенүү көп болду, далил аз. Тургундар эч кимди куубай, үйлөрүнө тарашты.",
        "Шаар макулдаша алган жок. Бүгүн эч ким оюндан кетпейт… бирок түн жакын. 🌙",
    ],
    "mayor": [
        "Шаар {v} деген оюнчуну кууп чыгууну чечип койгон эле, бирок акыркы учурда мэриядан буйрук келди: "
        "куугун жокко чыгарылды! Мэр ким болду экен? 🎩",
        "{v} шаардын дарбазасынын алдында турганда мэрдин мөөрү бар чабарман чуркап келди. "
        "Өкүм жокко чыгарылды — {v} шаарда калат.",
    ],
    "tie_revote": ["Добуштар тең бөлүндү, ошондуктан шаар кайра добуш берүүнү чечти."],
    "tie_rps": ["Добуштар тең бөлүндү, ал эми тагдырды «таш, кайчы, кагаз» беттешүүсү чечти:\n{x}\n{v} жеңилди."],
    "tie_dice": ["Добуштар тең бөлүндү, ал эми тагдырды кубик чечти:\n{x}\nЧүчүкулак {v} деген оюнчуга түштү."],
    "tie_random": ["Добуштар тең бөлүндү, чүчүкулак {v} деген оюнчуга түштү."],
    "win_town": ["🎉 <b>Тынч тургундар жеңди!</b> Бардык мафия кармалды, шаар тынч уктай алат."],
    "win_mafia": ["🔪 <b>Мафия жеңди!</b> Тынч тургундар өтө аз калды — шаар эми мафиянын колунда."],
}
T["ky"] = {
    "btn_close_room": "Бөлмөнү жабуу", "close_yes": "Ооба, жабуу",
    "close_confirm": "{n}-бөлмөнү жабабызбы? Анда оюн жүрүп жатса, ал эсепке алынбайт.",
    "cant_close_yet": "Бөлмөнү бир сутка аракетсиз тургандан кийин гана жабууга болот.",
    "room_closed_by": "{v} {n}-бөлмөнү жапты.",
    "room_closed_idle": "{n}-бөлмө өчүрүлдү: анда бир жума бою эч нерсе болгон жок.",
    "room_idle_warning": "{n}-бөлмө бир суткадан кийин өчүрүлөт: анда көптөн бери эч нерсе болбой жатат. "
                         "Сактап калуу үчүн баскычты басыңыз.",
    "btn_keep_room": "Бөлмөнү сактоо", "room_kept": "Бөлмө сакталды!",
    "idle_for": "Аракетсиз: {v}", "hours": ("саат", "саат"),
    "rooms_title": "Бөлмөлөр", "room": "Бөлмө", "free_room": "Бош бөлмө",
    "no_rooms": "Азырынча бир да бөлмө жок — бош бөлмөнү ачыңыз!",
    "host": "Алып баруучу", "no_host": "алып баруучу жок", "watchers": "Көрүүчүлөр",
    "invite": "Чакыруу", "status_lobby": "чогулуу", "status_over": "оюн бүттү",
    "status_paused": "тыныгуу — алып баруучу жок",
    "btn_play": "Ойноо", "btn_watch": "Көрүү гана", "btn_my_role": "Менин ролум",
    "btn_take_host": "Алып баруучу болуу", "btn_release": "Алып баруучулуктан баш тартуу",
    "btn_end_game": "Оюнду бүтүрүү", "btn_leave_room": "Бөлмөдөн чыгуу",
    "cant_leave_alive": "Сиз жүрүп жаткан оюндагы тирүү оюнчусуз — оюн бүткөндөн кийин гана чыга аласыз.",
    "host_taken_already": "Бул бөлмөнүн алып баруучусу бар.",
    "cant_host_alive": "Сиз жүрүп жаткан оюндагы тирүү оюнчусуз — алып баруучу оюндан чыккандар "
                       "же көрүүчүлөр гана боло алат.",
    "new_host": "👑 {v} эми бул бөлмөнүн алып баруучусу.",
    "you_released": "Сиз мындан ары алып баруучу эмессиз.",
    "host_released": "🙌 {v} алып баруучунун ордун бошотту. Аны каалаган адам ала алат.",
    "host_released_game": "⏸ {v} алып баруучунун ордун бошотту — оюн тыныгууда. "
                          "Алып баруучу оюндан чыккандар жана көрүүчүлөр боло алат.",
    "host_taken_by_owner": "Боттун ээси алып баруучунун ролун өзүнө алды.",
    "takehost_no_room": "Адегенде бөлмөгө кириңиз: /rooms",
    "game_started_watch": "Оюн башталды! Сиз көрүүчү катары карап жатасыз.",
    "game_aborted": "{v} оюнду бүтүрдү. Ал эсепке алынбайт. Бөлмө кайра чогулууга кайтты.",
    "end_confirm": "Оюнду чын эле бүтүрөбүзбү? Ал эсепке алынбайт.",
    "end_yes": "Ооба, бүтүрүү", "end_no": "Жок, артка",
    "back_to_roles": "Ролдорго", "team": "Команда", "count": "Саны",
    "card_pair": "Жуп катары эсептелет: эки орун ээлейт.",
    "set_vote_mode": "Добуш берүү",
    "val_vote_mode_host": "алып баруучу аркылуу", "val_vote_mode_phones": "телефондордон",
    "set_tie_default": "Тең добушта демейки",
    "val_tie_default_nobody": "эч ким", "val_tie_default_rps": "таш-кайчы-кагаз",
    "val_tie_default_random": "кубик", "val_tie_default_revote": "кайра добуш берүү",
    "set_show_names": "Ысымдар кашаада",
    "btn_open_vote": "Добуш берүүнү ачуу", "btn_close_vote": "Добуш берүүнү жабуу",
    "btn_cancel_votes": "Добуштарды жокко чыгаруу",
    "vote_hint_host": "Талапкерди тандап, ага ким добуш бергенин белгилеңиз. "
                      "Добушту «Добуштарды жокко чыгаруу» аркылуу гана өзгөртүүгө болот.",
    "vote_hint_phones": "Оюнчулар бот менен жеке чатта добуш беришет. Эсепти сиз гана көрөсүз.",
    "voted": "Добуш бергендер", "not_voted": "Азырынча добуш бербегендер",
    "already_voted_host": "Бул оюнчу добуш берип койгон. Добушту «Добуштарды жокко чыгаруу» бөлүмүндө "
                          "жокко чыгарууга болот.",
    "cancel_hint": "Жокко чыгаруу үчүн добушту басыңыз. Андан кийин оюнчу кайра добуш бере алат.",
    "ballot_title": "Добуш берүү!", "ballot_hint": "Шаардан кимди кууйбуз? Добуш жашыруун.",
    "your_vote": "Сиздин добушуңуз: <b>{v}</b>",
    "your_vote_hint": "Добушту өзгөртүү үчүн адегенде аны жокко чыгарыңыз.",
    "btn_cancel_my_vote": "Добушумду жокко чыгаруу",
    "already_voted": "Сиз добуш берип койдуңуз. Өзгөртүү үчүн добушуңузду жокко чыгарыңыз.",
    "vote_closed": "Добуш берүү жабылды.", "vote_not_open": "Азыр добуш берүү жабык.",
    "tie_choose": "Кантип чечебиз?",
    "tie_nobody": "Эч ким чыкпайт", "tie_rps": "Таш, кайчы, кагаз",
    "tie_random": "Кубик", "tie_revote": "Кайра добуш берүү",
    "decided": "Чыгат: {v}",
    "rps_title": "Таш, кайчы, кагаз", "rps_round": "раунд",
    "rps_prompt": "Добуш берүүдө тең чыкты! Атаандаштарыңыз: {v}. Жеңилген шаардан кетет. Сиздин жүрүшүңүз:",
    "rps_chosen": "Сиздин тандооңуз: {v}. Атаандаштарды күтөбүз…",
    "rps_expired": "Бул раунд мындан ары актуалдуу эмес.",
    "rps_you_safe": "Сиз беттешүүдө жеңдиңиз жана оюнда каласыз!",
    "rps_you_lost": "Сиз беттешүүдө жеңилдиңиз.",
    "rps_cancelled": "Алып баруучу беттешүүнү токтотту.",
    "btn_rps_random": "Тандабагандар үчүн кокустук тандоо",
    "btn_rps_cancel": "Беттешүүнү токтотуу",
    "dice_title": "Тең добуш! Кубик ыргытабыз:",
    "back": "Артка", "skip": "Эч ким / өткөрүү", "auto": "авто", "pts": "упай",
    "years": ("жыл", "жыл"), "months": ("ай", "ай"), "days": ("күн", "күн"),
    "only_host": "Бул баскычтар алып баруучу үчүн гана",
    "lobby": "Лобби", "players": "Оюнчулар", "nobody_yet": "азырынча эч ким жок",
    "preset": "Ролдор топтому", "will_drop": "оюнчулар жетпейт: {roles}",
    "btn_roles": "Ролдор", "btn_settings": "Жөндөөлөр", "btn_players": "Оюнчулар",
    "btn_deal": "Ролдорду таратуу", "btn_refresh": "Жаңылоо",
    "kick_hint": "Оюнчуну көрүүчүлөргө которуу үчүн аны басыңыз.",
    "kicked": "Алып баруучу сизди көрүүчүлөргө которду. Ойноо үчүн бөлмөдө «Ойноо» баскычын басыңыз.",
    "player_joined": "{v} кошулду (бардыгы: {n})",
    "player_left": "{v} бөлмөдөн чыкты",
    "nick_changed": "{a} эми {b} деп аталат",
    "roles_title": "Ролдор топтому",
    "roles_hint": "Ролдор оюнчулардан аз болгондо гана бот тынч тургундарды өзү кошот. "
                  "Оюнчулар жетпесе, ашыкча ролдор автоматтык түрдө алынып салынат.",
    "mafia_auto": "Мафия: авто (4 оюнчуга 1)",
    "settings_title": "Алып баруучунун жөндөөлөрү",
    "settings_hint": "Которуу үчүн жөндөөнү басыңыз.",
    "set_reveal": "Чыккандарды ачуу",
    "val_reveal_full": "ролу", "val_reveal_team": "командасы", "val_reveal_none": "жок",
    "set_doctor_self": "Дарыгер өзүн дарылайт",
    "set_doctor_repeat": "Дарыгер бир адамды 2 түн катары менен дарылайт",
    "set_first_phase": "Оюндун башы",
    "val_first_phase_night": "түн", "val_first_phase_day": "таанышуу күнү",
    "set_auto_broadcast": "Окуяларды автожөнөтүү",
    "set_detective_dm": "Жыйынтык детективге жеке билдирүүдө",
    "set_lawyer_dm": "Жыйынтык адвокатка жеке билдирүүдө",
    "need_3": "Кеминде 3 оюнчу керек.",
    "roles_dealt": "Ролдор таратылды!",
    "dropped": "Оюнчулар жетпеди, алынды: {roles}",
    "dm_failed": "Ролду жөнөтүү мүмкүн болгон жок: {v}. Алар ботто Start басышы керек.",
    "your_role": "Сиздин ролуңуз", "your_team": "Сиздин командаңыз",
    "your_friend": "Эң жакын досуңуз: {v} — ал да тынч тургун.",
    "keep_secret": "Бул билдирүүнү эч кимге көрсөтпөңүз!",
    "you_are_out": "Сиз оюндан чыктыңыз.",
    "lucky_spent": "🍀 Сиздин бактыңыз колдонулуп бүткөн.",
    "lawyer_done": "✅ Сиз мафияны таптыңыз — эми күндүз аны коргоңуз.",
    "night": "Түн", "mafia_team_kill": "Мафия",
    "night_hint": "⇒ — бардык тандоолорду эске алгандагы алдын ала жыйынтык.",
    "blocked": "тойдо",
    "res_mafia": "МАФИЯ", "res_town": "мафия эмес", "res_right": "тапты", "res_wrong": "жаңылды",
    "pick_mafia": "Мафия кимди тандады?",
    "pick_doctor": "кимди дарылайт?", "pick_detective": "кимди текшерет?",
    "pick_lawyer": "кимди мафия деп эсептейт?", "pick_bodyguard": "кимди коргойт?",
    "pick_partyhost": "кимди тойго чакырат?", "pick_framer": "кимге жала жабат?",
    "pick_driver": "кимдердин ордун алмаштырат? (экөөнү тандаңыз)",
    "btn_view": "Курамы", "btn_end_night": "Түндү бүтүрүү",
    "day": "Күн", "alive": "Тирүүлөр",
    "intro_day": "Таанышуу күнү", "intro_hint": "Оюнчулар таанышат. Бүгүн добуш берүү жок.",
    "btn_start_night": "Түндү баштоо",
    "vote_title": "Добуш берүү",
    "who_voted_for": "Ким каршы добуш берди: <b>{v}</b>?",
    "voters_hint": "☑️ — ушул талапкер үчүн, ▫️ — башка талапкер үчүн (которуу үчүн басыңыз).",
    "back_to_vote": "Талапкерлерге",
    "vote_result": "Добуш берүүнүн жыйынтыгы", "no_votes": "Добуштар жок.",
    "leader": "Эң көп добуш: <b>{v}</b>", "tie": "Тең добуш: {v}",
    "btn_exile": "Кууп чыгуу: {v}", "btn_mayor": "Мэр куугунду жокко чыгарды",
    "btn_no_exile": "Эч кимди куубоо",
    "dead_night": "Бул түнү сизди өлтүрүштү. Калып көрүүгө болот, бирок үнсүз! 🤫",
    "dead_day": "Шаар сизге каршы добуш берди. Калып көрүүгө болот, бирок үнсүз! 🤫",
    "lucky_saved": "Бул түнү сизге кол салышты, бирок бактыңыз бар экен! Мындан ары бакыт жардам бербейт.",
    "dm_check": "Текшерүүнүн жыйынтыгы: {v} — <b>{res}</b>",
    "dm_lawyer_ok": "Таптыңыз: {v} — мафия! Эми аны коргоңуз.",
    "dm_lawyer_no": "Жаңылдыңыз: {v} — мафия эмес.",
    "you_turned": "Биринчи мафиози каза тапты. Эми сиз — мафиясыз!",
    "turncoat_joined": "Чыккынчы {v} силердин тарапка өттү!",
    "story_title": "Үн чыгарып окуу үчүн окуя", "for_host": "Алып баруучу үчүн",
    "btn_broadcast": "Окуяны бардык оюнчуларга жөнөтүү", "btn_next": "Андан ары",
    "auto_sent": "Окуя оюнчуларга жөнөтүлдү.",
    "broadcast_done": "Оюнчуларга жөнөтүлдү: {n}",
    "reveal_role": "Ролу: {role}.", "reveal_team": "Командасы: {team}.",
    "note_kill_blocked": "тойчу мафиозини алып кетти — өлтүрүү жок",
    "note_immortal": "мафия өлбөскө кол салды: {v}",
    "note_saved": "дарыгер куткарды: {v}",
    "note_guarded": "жан сакчы {b} каза тапты, {v} коргоп",
    "note_lucky": "{v} бактысы менен аман калды",
    "note_redirected": "таксист кол салууну {v} дегенден {b} дегенге бурду",
    "note_check_mafia": "детектив {d} текшерди — {v}: мафия",
    "note_check_town": "детектив {d} текшерди — {v}: мафия эмес",
    "note_lawyer_ok": "адвокат {d} мафияны тапты: {v}",
    "note_lawyer_no": "адвокат {d} жаңылды: {v}",
    "note_turned": "чыккынчы {v} мафияга өттү",
    "note_mayor": "мэр {v} оюнчусун куугундан куткарды",
    "game_over": "Оюн бүттү",
    "btn_rematch": "Ушул бөлмөдө жаңы оюн",
    "rematch": "Ошол эле бөлмөдө жаңы оюн! Ролуңузду күтүңүз.",
    "you_are_host": "Сиз — алып баруучусуз! Панель төмөндө.",
    "owner_only": "Бул команда боттун ээси үчүн гана.",
    "no_role": "Сизде азырынча рол жок.",
    "cancelled": "Макул, эч нерсе өзгөртпөйбүз 🙂",
    "help_short": "Командалар: /rooms — бөлмөлөр, /profile — профиль, /role — менин ролум, "
                  "/leave — бөлмөдөн чыгуу.",
    "profile": "Профиль", "nick": "Ник", "real_name": "Аты", "gender": "Жынысы",
    "language": "Тил", "registered": "Катталган күнү", "tenure": "Стаж",
    "points_total": "Бардык упай", "points_last": "Акыркы оюндагы упай",
    "games_played": "Оюндар", "wins": "жеңиш",
    "gender_m": "Эркек", "gender_f": "Аял", "gender_none": "Көрсөтүлгөн эмес",
    "btn_nick": "Ник", "btn_name": "Аты", "btn_gender": "Жынысы", "btn_lang": "Тил",
    "btn_photo": "Сүрөт", "btn_games": "Менин оюндарым",
    "ask_nick": "Оюн никиңизди жазыңыз ({a}–{b} белги). Аны бардык оюнчулар көрөт. Жокко чыгаруу: /cancel",
    "ask_name": "Чыныгы атыңызды жазыңыз. Аны алып баруучу гана көрөт. Жокко чыгаруу: /cancel",
    "ask_gender": "Жынысыңызды тандаңыз:",
    "ask_photo": "Сүрөттү бир билдирүү менен жөнөтүңүз. Жокко чыгаруу: /cancel",
    "bad_nick": "Ник {a}–{b} белгиден турушу жана «/» менен башталбашы керек. Кайра: /profile",
    "bad_name": "Бул ат туура келбейт. /profile аркылуу кайра аракет кылыңыз",
    "nick_after_game": "Никти оюн бүткөндөн кийин өзгөртүүгө болот.",
    "nick_taken": "Бул ник лоббиде башка оюнчуда бар. Башкасын тандаңыз: /profile",
    "nick_saved": "Сиздин никиңиз: <b>{v}</b>", "name_saved": "Сиздин атыңыз: <b>{v}</b>",
    "gender_saved": "Жынысы: {v}", "lang_saved": "Тил: Кыргызча",
    "ask_lang": "Тилди тандаңыз:",
    "photo_saved": "Сүрөт сакталды!", "photo_deleted": "Сүрөт өчүрүлдү.",
    "delete_photo": "Сүрөттү өчүрүү",
    "photo_hint": "Профилдин сүрөтүн алмаштыруу үчүн /profile → Сүрөт ачыңыз.",
    "no_games": "Сиз азырынча бир да оюн ойногон жоксуз.",
    "games_more": "…жана дагы {n}",
}
COMMANDS["ky"] = [("start", "Башкы меню"), ("rooms", "Бөлмөлөр"), ("profile", "Менин профилим"),
                  ("role", "Менин ролум"), ("panel", "Алып баруучунун панели"),
                  ("leave", "Бөлмөдөн чыгуу"), ("cancel", "Киргизүүнү жокко чыгаруу")]

# ===========================================================================
# БАШҠОРТСА (ba)
# ===========================================================================
LANG_NAMES["ba"] = "Башҡортса"
ROLE_NAMES["ba"] = {r: (n, n) for r, n in {
    "mafia": "Мафия", "framer": "Яла яғыусы", "lawyer": "Адвокат", "doctor": "Табип",
    "detective": "Детектив", "bodyguard": "Һаҡсы", "partyhost": "Байрамсы",
    "driver": "Таксист", "mayor": "Мэр", "immortal": "Үлемһеҙ", "lucky": "Бәхетле",
    "bestfriend": "Иң яҡын дуҫ", "turncoat": "Хыянатсы", "civilian": "Тыныс кеше",
}.items()}
TEAM_NAMES["ba"] = {"town": "🏘 Ҡала", "mafia": "🔪 Мафия"}
PRESET_NAMES["ba"] = {"classic": "Классика", "extended": "Киңәйтелгән", "chaos": "Хаос", "custom": "Үҙеңдеке"}
ROLE_DESC["ba"] = {
    "mafia": "Төндә һеҙ ҡалған мафия менән бергә ҡорбан һайлайһығыҙ. Көндөҙ тыныс кеше булып ҡыланығыҙ.",
    "framer": "Һеҙ мафия өсөн уйнайһығыҙ. Һәр төндә уйынсы һайлағыҙ: әгәр детектив уны шул төндә "
              "тикшерһә, «мафия» тип күрәсәк. Маҡсатығыҙ — детективтарҙы бутау.",
    "lawyer": "Һеҙ мафия өсөн уйнайһығыҙ, ләкин уның кем икәнен белмәйһегеҙ. Һәр төндә мафиозиҙы "
              "табырға тырышығыҙ. Тапһағыҙ — көндөҙ уны яҡлағыҙ. Тапмаһағыҙ — тикшергән кешене "
              "батырығыҙ, сөнки ул тыныс кеше. Еңеүҙе һанағанда һеҙ мафия командаһында.",
    "doctor": "Һәр төндә һеҙ бер уйынсыны дауалайһығыҙ. Мафия уға килһә, ул иҫән ҡала.",
    "detective": "Һәр төндә һеҙ бер уйынсыны тикшерәһегеҙ һәм уның мафия булыу-булмауын беләһегеҙ.",
    "bodyguard": "Һәр төндә һеҙ бер уйынсыны һаҡлайһығыҙ. Мафия уға һөжүм итһә, уның урынына һеҙ "
                 "һәләк булаһығыҙ.",
    "partyhost": "Һәр төндә һеҙ бер уйынсыны мәжлескә алып китәһегеҙ — уның төнгө ғәмәле үтәлмәй. "
                 "Мафиозиҙы алып китһәгеҙ, үлтереү булмаясаҡ.",
    "driver": "Һәр төндә һеҙ ике уйынсының урынын алмаштыраһығыҙ: береһенә йүнәлтелгән бөтә нәмә "
              "икенсеһенә эләгә. Ҡотҡарырға ла, бутарға ла мөмкин — аҡыл менән һайлағыҙ.",
    "mayor": "Көндөҙ һеҙҙең тауыш ғәҙәти, ә кем икәнегеҙ — сер. Уйында бер тапҡыр тауыш биреүҙән һуң "
             "ҡыуыуҙы кире ҡаға алаһығыҙ. Алып барыусы иғлан иткәс, уға әйтегеҙ.",
    "immortal": "Мафия һеҙҙе төндә үлтерә алмай. Ә көндөҙ ҡыуырға мөмкин.",
    "lucky": "Һеҙгә беренсе төнгө һөжүм барып сыҡмаясаҡ. Шунан һуң һеҙ ғәҙәти тыныс кеше. "
             "Көндөҙ һеҙҙе теләһә ҡасан ҡыуырға мөмкин.",
    "bestfriend": "Һеҙ һәм иң яҡын дуҫығыҙ — тыныс кешеләр, һәм икегеҙ ҙә быны беләһегеҙ. Бергә булығыҙ!",
    "turncoat": "Әлегә һеҙ тыныс кеше. Ләкин беренсе мафиози һәләк булғас, һеҙ мафияға күсәһегеҙ "
                "һәм яңы союздаштарығыҙҙы беләһегеҙ.",
    "civilian": "Төндә һеҙ йоҡлайһығыҙ. Көндөҙ мафияны эҙләгеҙ һәм аҡыл менән тауыш бирегеҙ.",
}
STORIES["ba"] = {
    "night_header": ["🌅 <b>{r}-се төндән һуңғы иртә. Ҡала уяна…</b>"],
    "day_header": ["🌆 <b>{r}-се көн, кис. Тауыш биреү һөҙөмтәләре</b>"],
    "kill": [
        "Төн томанлы булды. Ҡала йоҡланы, ләкин бөтәһе лә түгел. Таң менән кешеләр {v} исемле "
        "уйынсыны иҫке фонтан янында таптылар — мафия шәфҡәт белмәй.",
        "Сәғәт өстө һуҡҡас, бер өйҙә ут һүнде. Иртән күршеләр аңланы: {v} башҡа уянмаясаҡ.",
        "Ҡала ямғыр тауышы аҫтында йоҡлап китте. Мафия ҡорбанын һайланы, табип өлгөрмәне. "
        "{v} уйындан мәңгегә китә.",
        "Ай болоттар артына йәшеренде, тынлыҡта атыу тауышы яңғыраны. Иртән билдәле булды: "
        "{v} мафия тарафынан үлтерелгән.",
        "Төндә урамдар буйлап номерһыҙ ҡара машина үтте. Ә иртән ҡалала бер кеше етмәне: "
        "{v} эҙһеҙ юғалды.",
    ],
    "bodyguard": [
        "Төндә мафия һунарға сыҡты, ләкин үлтереүселәр юлында һаҡсы баҫып торҙо. {v} башҡа кешене "
        "үҙе менән ҡапланы һәм батыр булып һәләк булды.",
        "Ҡараңғыла атыу тауышы яңғыраны, ләкин пуля кәрәкле кешегә теймәне: {v} алдына ташланды "
        "һәм үҙ ғүмере хаҡына кеше ғүмерен ҡотҡарҙы.",
    ],
    "saved": [
        "Төндә мафия һунарға сыҡты, ләкин табип тиҙерәк булды. Бөтәһе лә иҫән уянды — кемдер төндө "
        "тамсы аҫтында үткәргән булһа ла. 💉",
        "Шәүләләр ҡорбандың өйөнә яҡынлашты, ләкин тупһала инде табип үҙ сумкаһы менән баҫып тора ине. "
        "Мафия буш ҡул менән китте.",
        "Был төн кемдеңдер һуңғыһы булыуы мөмкин ине. Ләкин табип мөғжизә ҡылды: бөтәһе лә иҫән!",
    ],
    "survived": [
        "Төндә мафия һөжүм итте, ләкин ҡорбан… үлмәне генә. Ҡала шыбырлай: йә мөғжизә, "
        "йә бында кемдер ябай түгел.",
        "Үлтереүселәр эштәрен башҡарҙы, ләкин иртән уларҙың ҡорбаны урамға иҫән-һау сыҡты. "
        "Мафия аптырашта.",
    ],
    "quiet": [
        "Төн ғәжәп тыныс үтте. Мафия боҫоп ята… йәки нимәлер уйлап таба. 🤔",
        "Ҡала ҡаты йоҡланы, хатта мафия ла ял алған кеүек. Бөтәһе лә иҫән — әлегә.",
        "Ҡайҙалыр таңға тиклем музыка яңғыраны, ә мафия эшкә сыҡманы. Сәйер төн булды.",
    ],
    "exile": [
        "Бәхәстәр кискә тиклем баҫылманы. Ниһайәт, ҡала ҡарар сығарҙы: {v} ҡыуып сығарылды.",
        "Тауыш биреү киҫкен булды, ләкин күпселек {v} исемле уйынсыны күрһәтте. Ҡарар ҡабул ителде.",
        "Ҡала хәүефкә бармаҫҡа булды: {v} уйындан китә.",
        "Ғәйепләүҙәр, аҡланыуҙар, ҡысҡырыштар… Аҙаҡта кешеләр {v} исемле уйынсыға ҡаршы тауыш бирҙе.",
    ],
    "no_exile": [
        "Шик күп ине, ә дәлилдәр әҙ. Кешеләр бер кемде лә ҡыумайынса өйҙәренә таралышты.",
        "Ҡала килешә алманы. Бөгөн бер кем дә уйындан китмәй… ләкин төн яҡын. 🌙",
    ],
    "mayor": [
        "Ҡала {v} исемле уйынсыны ҡыуырға ҡарар иткән ине инде, ләкин һуңғы мәлдә мэриянан фарман "
        "килде: ҡыуыу кире ҡағылды! Кем һуң ул мэр? 🎩",
        "{v} инде ҡала ҡапҡаһы янында баҫып тора ине, мэр мөһөрө менән сапҡын йүгереп килде. "
        "Хөкөм кире ҡағылды — {v} ҡалала ҡала.",
    ],
    "tie_revote": ["Тауыштар тигеҙ бүленде, һәм ҡала ҡабат тауыш бирергә булды."],
    "tie_rps": ["Тауыштар тигеҙ бүленде, һәм яҙмышты «таш, ҡайсы, ҡағыҙ» дуэле хәл итте:\n{x}\n{v} отолдо."],
    "tie_dice": ["Тауыштар тигеҙ бүленде, һәм яҙмышты кубик хәл итте:\n{x}\nСират {v} исемле уйынсыға төштө."],
    "tie_random": ["Тауыштар тигеҙ бүленде, һәм сират {v} исемле уйынсыға төштө."],
    "win_town": ["🎉 <b>Тыныс кешеләр еңде!</b> Бөтә мафия тотолдо, ҡала тыныс йоҡлай ала."],
    "win_mafia": ["🔪 <b>Мафия еңде!</b> Тыныс кешеләр бик әҙ ҡалды — ҡала хәҙер мафия ҡулында."],
}
T["ba"] = {
    "btn_close_room": "Бүлмәне ябыу", "close_yes": "Эйе, ябырға",
    "close_confirm": "{n} бүлмәһен ябырғамы? Унда уйын барһа, ул иҫәпкә алынмаясаҡ.",
    "cant_close_yet": "Бүлмәне бер тәүлек хәрәкәтһеҙ торғас ҡына ябып була.",
    "room_closed_by": "{v} {n} бүлмәһен япты.",
    "room_closed_idle": "{n} бүлмәһе юйылды: унда бер аҙна буйы бер нәмә лә булманы.",
    "room_idle_warning": "{n} бүлмәһе бер тәүлектән юйыласаҡ: унда күптән бер нәмә лә булмай. "
                         "Һаҡлап ҡалыу өсөн төймәгә баҫығыҙ.",
    "btn_keep_room": "Бүлмәне һаҡлау", "room_kept": "Бүлмә һаҡланды!",
    "idle_for": "Хәрәкәтһеҙ: {v}", "hours": ("сәғәт", "сәғәт"),
    "rooms_title": "Бүлмәләр", "room": "Бүлмә", "free_room": "Буш бүлмә",
    "no_rooms": "Әлегә бер бүлмә лә юҡ — буш бүлмәне асығыҙ!",
    "host": "Алып барыусы", "no_host": "алып барыусы юҡ", "watchers": "Тамашасылар",
    "invite": "Саҡырыу", "status_lobby": "йыйылыу", "status_over": "уйын тамам",
    "status_paused": "туҡталыш — алып барыусы юҡ",
    "btn_play": "Уйнарға", "btn_watch": "Ҡарап ҡына торорға", "btn_my_role": "Минең роль",
    "btn_take_host": "Алып барыусы булырға", "btn_release": "Алып барыусылыҡтан китеү",
    "btn_end_game": "Уйынды тамамлау", "btn_leave_room": "Бүлмәнән сығыу",
    "cant_leave_alive": "Һеҙ барған уйында тере уйынсы — уйын бөткәс кенә сығып була.",
    "host_taken_already": "Был бүлмәнең алып барыусыһы бар инде.",
    "cant_host_alive": "Һеҙ барған уйында тере уйынсы — алып барыусы уйындан сыҡҡандар йәки "
                       "тамашасылар ғына була ала.",
    "new_host": "👑 {v} хәҙер был бүлмәнең алып барыусыһы.",
    "you_released": "Һеҙ инде алып барыусы түгел.",
    "host_released": "🙌 {v} алып барыусы урынын бушатты. Уны теләһә кем ала ала.",
    "host_released_game": "⏸ {v} алып барыусы урынын бушатты — уйын туҡтатылды. "
                          "Алып барыусы уйындан сыҡҡандар һәм тамашасылар була ала.",
    "host_taken_by_owner": "Бот хужаһы алып барыусы ролен үҙенә алды.",
    "takehost_no_room": "Тәүҙә бүлмәгә инегеҙ: /rooms",
    "game_started_watch": "Уйын башланды! Һеҙ тамашасы булараҡ ҡарайһығыҙ.",
    "game_aborted": "{v} уйынды тамамланы. Ул иҫәпкә алынманы. Бүлмә яңынан йыйылыуға ҡайтты.",
    "end_confirm": "Уйынды ысынлап та тамамларғамы? Ул иҫәпкә алынмаясаҡ.",
    "end_yes": "Эйе, тамамларға", "end_no": "Юҡ, кире ҡайтырға",
    "back_to_roles": "Ролдәргә", "team": "Команда", "count": "Һаны",
    "card_pair": "Пар булып һанала: ике урын ала.",
    "set_vote_mode": "Тауыш биреү",
    "val_vote_mode_host": "алып барыусы аша", "val_vote_mode_phones": "телефондарҙан",
    "set_tie_default": "Тигеҙлектә ғәҙәттә",
    "val_tie_default_nobody": "бер кем дә", "val_tie_default_rps": "таш-ҡайсы-ҡағыҙ",
    "val_tie_default_random": "кубик", "val_tie_default_revote": "ҡабат тауыш биреү",
    "set_show_names": "Исемдәр йәйәләрҙә",
    "btn_open_vote": "Тауыш биреүҙе асыу", "btn_close_vote": "Тауыш биреүҙе ябыу",
    "btn_cancel_votes": "Тауыштарҙы кире алыу",
    "vote_hint_host": "Кандидатты һайлағыҙ һәм уның өсөн кем тауыш биргәнен билдәләгеҙ. "
                      "Тауышты «Тауыштарҙы кире алыу» аша ғына үҙгәртеп була.",
    "vote_hint_phones": "Уйынсылар бот менән шәхси чатта тауыш бирә. Иҫәпте һеҙ генә күрәһегеҙ.",
    "voted": "Тауыш бирҙеләр", "not_voted": "Әле тауыш бирмәнеләр",
    "already_voted_host": "Был уйынсы тауыш биргән инде. Тауышты «Тауыштарҙы кире алыу» бүлегендә "
                          "кире алып була.",
    "cancel_hint": "Кире алыу өсөн тауышҡа баҫығыҙ. Шунан һуң уйынсы яңынан тауыш бирә ала.",
    "ballot_title": "Тауыш биреү!", "ballot_hint": "Ҡаланан кемде ҡыуырға? Тауыш йәшерен.",
    "your_vote": "Һеҙҙең тауыш: <b>{v}</b>",
    "your_vote_hint": "Тауышты үҙгәртер өсөн, тәүҙә уны кире алығыҙ.",
    "btn_cancel_my_vote": "Тауышымды кире алыу",
    "already_voted": "Һеҙ тауыш бирҙегеҙ инде. Үҙгәртер өсөн тауышығыҙҙы кире алығыҙ.",
    "vote_closed": "Тауыш биреү ябылды.", "vote_not_open": "Хәҙер тауыш биреү ябыҡ.",
    "tie_choose": "Нисек хәл итәбеҙ?",
    "tie_nobody": "Бер кем дә китмәй", "tie_rps": "Таш, ҡайсы, ҡағыҙ",
    "tie_random": "Кубик", "tie_revote": "Ҡабат тауыш биреү",
    "decided": "Китә: {v}",
    "rps_title": "Таш, ҡайсы, ҡағыҙ", "rps_round": "раунд",
    "rps_prompt": "Тауыш биреүҙә тигеҙлек! Көндәштәрегеҙ: {v}. Отолған кеше ҡаланан китә. Һеҙҙең сират:",
    "rps_chosen": "Һеҙҙең һайлау: {v}. Көндәштәрҙе көтәбеҙ…",
    "rps_expired": "Был раунд инде актуаль түгел.",
    "rps_you_safe": "Һеҙ дуэлдә еңдегеҙ һәм уйында ҡалаһығыҙ!",
    "rps_you_lost": "Һеҙ дуэлдә отолдоғоҙ.",
    "rps_cancelled": "Алып барыусы дуэлде туҡтатты.",
    "btn_rps_random": "Һайламағандар өсөн осраҡлы һайлау",
    "btn_rps_cancel": "Дуэлде туҡтатыу",
    "dice_title": "Тигеҙлек! Кубик ташлайбыҙ:",
    "back": "Кире", "skip": "Бер кем дә / үткәреү", "auto": "авто", "pts": "балл",
    "years": ("йыл", "йыл"), "months": ("ай", "ай"), "days": ("көн", "көн"),
    "only_host": "Был төймәләр алып барыусы өсөн генә",
    "lobby": "Лобби", "players": "Уйынсылар", "nobody_yet": "әлегә бер кем дә юҡ",
    "preset": "Ролдәр йыйылмаһы", "will_drop": "уйынсылар етмәйәсәк: {roles}",
    "btn_roles": "Ролдәр", "btn_settings": "Көйләүҙәр", "btn_players": "Уйынсылар",
    "btn_deal": "Ролдәрҙе таратыу", "btn_refresh": "Яңыртыу",
    "kick_hint": "Уйынсыны тамашасыларға күсереү өсөн уға баҫығыҙ.",
    "kicked": "Алып барыусы һеҙҙе тамашасыларға күсерҙе. Уйнау өсөн бүлмәлә «Уйнарға» төймәһенә баҫығыҙ.",
    "player_joined": "{v} ҡушылды (барлығы: {n})",
    "player_left": "{v} бүлмәнән сыҡты",
    "nick_changed": "{a} хәҙер {b} тип атала",
    "roles_title": "Ролдәр йыйылмаһы",
    "roles_hint": "Ролдәр уйынсыларҙан әҙерәк булғанда ғына бот тыныс кешеләрҙе үҙе өҫтәй. "
                  "Уйынсылар етмәһә, артыҡ ролдәр автоматик рәүештә алына.",
    "mafia_auto": "Мафия: авто (4 уйынсыға 1)",
    "settings_title": "Алып барыусы көйләүҙәре",
    "settings_hint": "Үҙгәртеү өсөн көйләүгә баҫығыҙ.",
    "set_reveal": "Сыҡҡандарҙы асыу",
    "val_reveal_full": "роль", "val_reveal_team": "команда", "val_reveal_none": "юҡ",
    "set_doctor_self": "Табип үҙен дауалай",
    "set_doctor_repeat": "Табип бер кешене 2 төн рәттән дауалай",
    "set_first_phase": "Уйын башы",
    "val_first_phase_night": "төн", "val_first_phase_day": "танышыу көнө",
    "set_auto_broadcast": "Хикәйәләрҙе автоматик ебәреү",
    "set_detective_dm": "Детективҡа һөҙөмтә шәхси хәбәрҙә",
    "set_lawyer_dm": "Адвокатҡа һөҙөмтә шәхси хәбәрҙә",
    "need_3": "Кәм тигәндә 3 уйынсы кәрәк.",
    "roles_dealt": "Ролдәр таратылды!",
    "dropped": "Уйынсылар етмәне, алынды: {roles}",
    "dm_failed": "Ролде ебәреп булманы: {v}. Улар ботта Start баҫырға тейеш.",
    "your_role": "Һеҙҙең роль", "your_team": "Һеҙҙең команда",
    "your_friend": "Иң яҡын дуҫығыҙ: {v} — ул да тыныс кеше.",
    "keep_secret": "Был хәбәрҙе бер кемгә лә күрһәтмәгеҙ!",
    "you_are_out": "Һеҙ уйындан сыҡтығыҙ.",
    "lucky_spent": "🍀 Бәхетегеҙ инде файҙаланылды.",
    "lawyer_done": "✅ Һеҙ мафияны таптығыҙ инде — хәҙер көндөҙ уны яҡлағыҙ.",
    "night": "Төн", "mafia_team_kill": "Мафия",
    "night_hint": "⇒ — бөтә һайлауҙарҙы иҫәпкә алып, алдан һөҙөмтә.",
    "blocked": "мәжлестә",
    "res_mafia": "МАФИЯ", "res_town": "мафия түгел", "res_right": "тапты", "res_wrong": "яңылышты",
    "pick_mafia": "Мафия кемде һайланы?",
    "pick_doctor": "кемде дауалай?", "pick_detective": "кемде тикшерә?",
    "pick_lawyer": "кемде мафия тип һанай?", "pick_bodyguard": "кемде һаҡлай?",
    "pick_partyhost": "кемде мәжлескә саҡыра?", "pick_framer": "кемгә яла яға?",
    "pick_driver": "кемдәрҙе алмаштыра? (икәүһен һайлағыҙ)",
    "btn_view": "Составы", "btn_end_night": "Төндө тамамлау",
    "day": "Көн", "alive": "Иҫәндәр",
    "intro_day": "Танышыу көнө", "intro_hint": "Уйынсылар таныша. Бөгөн тауыш биреү юҡ.",
    "btn_start_night": "Төндө башлау",
    "vote_title": "Тауыш биреү",
    "who_voted_for": "Кем ҡаршы тауыш бирҙе: <b>{v}</b>?",
    "voters_hint": "☑️ — ошо кандидат өсөн, ▫️ — башҡа кандидат өсөн (күсереү өсөн баҫығыҙ).",
    "back_to_vote": "Кандидаттарға",
    "vote_result": "Тауыш биреү һөҙөмтәһе", "no_votes": "Тауыштар юҡ.",
    "leader": "Иң күп тауыш: <b>{v}</b>", "tie": "Тигеҙлек: {v}",
    "btn_exile": "Ҡыуырға: {v}", "btn_mayor": "Мэр ҡыуыуҙы кире ҡаҡты",
    "btn_no_exile": "Бер кемде лә ҡыумаҫҡа",
    "dead_night": "Был төндә һеҙҙе үлтерҙеләр. Ҡалып ҡарап торорға була, тик өндәшмәйенсә! 🤫",
    "dead_day": "Ҡала һеҙгә ҡаршы тауыш бирҙе. Ҡалып ҡарап торорға була, тик өндәшмәйенсә! 🤫",
    "lucky_saved": "Был төндә һеҙгә һөжүм иттеләр, ләкин бәхетегеҙ бар икән! Башҡа бәхет ярҙам итмәҫ.",
    "dm_check": "Тикшереү һөҙөмтәһе: {v} — <b>{res}</b>",
    "dm_lawyer_ok": "Таптығыҙ: {v} — мафия! Хәҙер уны яҡлағыҙ.",
    "dm_lawyer_no": "Яңылыштығыҙ: {v} — мафия түгел.",
    "you_turned": "Беренсе мафиози һәләк булды. Хәҙер һеҙ — мафия!",
    "turncoat_joined": "Хыянатсы {v} һеҙҙең яҡҡа күсте!",
    "story_title": "Ҡысҡырып уҡыу өсөн хикәйә", "for_host": "Алып барыусы өсөн",
    "btn_broadcast": "Хикәйәне бөтә уйынсыларға ебәреү", "btn_next": "Алға",
    "auto_sent": "Хикәйә уйынсыларға ебәрелде.",
    "broadcast_done": "Уйынсыларға ебәрелде: {n}",
    "reveal_role": "Роль: {role}.", "reveal_team": "Команда: {team}.",
    "note_kill_blocked": "байрамсы мафиозиҙы алып китте — үлтереү юҡ",
    "note_immortal": "мафия үлемһеҙгә һөжүм итте: {v}",
    "note_saved": "табип ҡотҡарҙы: {v}",
    "note_guarded": "һаҡсы {b} һәләк булды, {v} кешеһен һаҡлап",
    "note_lucky": "{v} бәхете арҡаһында иҫән ҡалды",
    "note_redirected": "таксист һөжүмде {v} кешеһенән {b} кешеһенә борҙо",
    "note_check_mafia": "детектив {d} тикшерҙе — {v}: мафия",
    "note_check_town": "детектив {d} тикшерҙе — {v}: мафия түгел",
    "note_lawyer_ok": "адвокат {d} мафияны тапты: {v}",
    "note_lawyer_no": "адвокат {d} яңылышты: {v}",
    "note_turned": "хыянатсы {v} мафияға күсте",
    "note_mayor": "мэр {v} уйынсыһын ҡыуыуҙан ҡотҡарҙы",
    "game_over": "Уйын тамам",
    "btn_rematch": "Был бүлмәлә яңы уйын",
    "rematch": "Шул уҡ бүлмәлә яңы уйын! Ролегеҙҙе көтөгөҙ.",
    "you_are_host": "Һеҙ — алып барыусы! Панель түбәндә.",
    "owner_only": "Был команда бот хужаһы өсөн генә.",
    "no_role": "Һеҙҙең әлегә роль юҡ.",
    "cancelled": "Ярай, бер нәмә лә үҙгәртмәйбеҙ 🙂",
    "help_short": "Командалар: /rooms — бүлмәләр, /profile — профиль, /role — минең роль, "
                  "/leave — бүлмәнән сығыу.",
    "profile": "Профиль", "nick": "Ник", "real_name": "Исем", "gender": "Енес",
    "language": "Тел", "registered": "Теркәлгән көнө", "tenure": "Стаж",
    "points_total": "Бөтә баллдар", "points_last": "Һуңғы уйындағы баллдар",
    "games_played": "Уйындар", "wins": "еңеү",
    "gender_m": "Ир-ат", "gender_f": "Ҡатын-ҡыҙ", "gender_none": "Күрһәтелмәгән",
    "btn_nick": "Ник", "btn_name": "Исем", "btn_gender": "Енес", "btn_lang": "Тел",
    "btn_photo": "Фото", "btn_games": "Минең уйындар",
    "ask_nick": "Уйын никтегеҙҙе яҙығыҙ ({a}–{b} символ). Уны бөтә уйынсылар күрәсәк. Кире ҡағыу: /cancel",
    "ask_name": "Ысын исемегеҙҙе яҙығыҙ. Уны алып барыусы ғына күрә. Кире ҡағыу: /cancel",
    "ask_gender": "Енесегеҙҙе һайлағыҙ:",
    "ask_photo": "Фотоны бер хәбәр менән ебәрегеҙ. Кире ҡағыу: /cancel",
    "bad_nick": "Ник {a}–{b} символдан торорға һәм «/» менән башланмаҫҡа тейеш. Тағы бер тапҡыр: /profile",
    "bad_name": "Исем тап килмәй. /profile аша яңынан ҡарағыҙ",
    "nick_after_game": "Никты уйын бөткәс кенә үҙгәртеп була.",
    "nick_taken": "Был ник лоббила башҡа уйынсыла бар инде. Башҡаһын һайлағыҙ: /profile",
    "nick_saved": "Һеҙҙең ник: <b>{v}</b>", "name_saved": "Һеҙҙең исем: <b>{v}</b>",
    "gender_saved": "Енес: {v}", "lang_saved": "Тел: Башҡортса",
    "ask_lang": "Телде һайлағыҙ:",
    "photo_saved": "Фото һаҡланды!", "photo_deleted": "Фото юйылды.",
    "delete_photo": "Фотоны юйыу",
    "photo_hint": "Профиль фотоһын алмаштырыу өсөн /profile → Фото асығыҙ.",
    "no_games": "Һеҙ әле бер уйын да уйнаманығыҙ.",
    "games_more": "…һәм тағы {n}",
}
COMMANDS["ba"] = [("start", "Төп меню"), ("rooms", "Бүлмәләр"), ("profile", "Минең профиль"),
                  ("role", "Минең роль"), ("panel", "Алып барыусы панеле"),
                  ("leave", "Бүлмәнән сығыу"), ("cancel", "Индереүҙе туҡтатыу")]


# Справка о ролях для всех (/roles)
T["ru"]["roles_guide"] = 'Роли в игре'
T["ru"]["roles_guide_hint"] = 'Нажмите на роль, чтобы прочитать, что она умеет.'
COMMANDS["ru"].insert(2, ("roles", 'Все роли'))
T["en"]["roles_guide"] = 'Roles in the game'
T["en"]["roles_guide_hint"] = 'Tap a role to read what it does.'
COMMANDS["en"].insert(2, ("roles", 'All roles'))
T["tt"]["roles_guide"] = 'Уендагы рольләр'
T["tt"]["roles_guide_hint"] = 'Роль турында уку өчен аңа басыгыз.'
COMMANDS["tt"].insert(2, ("roles", 'Барлык рольләр'))
T["kk"]["roles_guide"] = 'Ойындағы рөлдер'
T["kk"]["roles_guide_hint"] = 'Рөл туралы оқу үшін оны басыңыз.'
COMMANDS["kk"].insert(2, ("roles", 'Барлық рөлдер'))
T["ky"]["roles_guide"] = 'Оюндагы ролдор'
T["ky"]["roles_guide_hint"] = 'Рол жөнүндө окуу үчүн аны басыңыз.'
COMMANDS["ky"].insert(2, ("roles", 'Бардык ролдор'))
T["ba"]["roles_guide"] = 'Уйындағы ролдәр'
T["ba"]["roles_guide_hint"] = 'Роль тураһында уҡыу өсөн уға баҫығыҙ.'
COMMANDS["ba"].insert(2, ("roles", 'Бөтә ролдәр'))


# Вход на сайт (/web): код, чтобы связать аккаунт с сайтом или сбросить пароль.
# Для tt/kk/ky/ba тексты сообщения пока берутся из русского.
T["ru"]["web_site"] = "сайт игры"
T["ru"]["web_code"] = ("🌐 Код для сайта: <b><code>{code}</code></b>\n\n"
                       "Откройте {url}, выберите «Есть Telegram» и введите код. Он действует 10 минут.\n\n"
                       "С этим кодом можно связать аккаунт с сайтом или задать новый пароль. "
                       "Никому его не пересылайте.")
T["en"]["web_site"] = "the game website"
T["en"]["web_code"] = ("🌐 Website code: <b><code>{code}</code></b>\n\n"
                       "Open {url}, choose “I have Telegram” and enter the code. It works for 10 minutes.\n\n"
                       "Use it to link your account to the website or set a new password. "
                       "Don't forward it to anyone.")
for _lang, _label in [("ru", "Вход на сайт"), ("en", "Website login"), ("tt", "Сайтка керү"),
                      ("kk", "Сайтқа кіру"), ("ky", "Сайтка кирүү"), ("ba", "Сайтҡа инеү")]:
    COMMANDS[_lang].insert(-1, ("web", _label))
