from random import (
    random,
    choice,
    randint,
)

from .character import Character


class CharHandler:

    def __init__(self, char: Character):
        self.char = char

    # Helpers

    @classmethod
    def add_common(cls, value: dict, title: str, points: int, stuck_on_match: bool = False):
        # Skip if self.char has higher-level advantage/disadv/perk
        if abs(title in value and value[title]) > abs(points):
            if stuck_on_match:
                value[title] += points
            return

        value[title] = points

    @classmethod
    def roll_easy(cls):
        lvl_rand = random()
        if lvl_rand < 0.35:
            lvl = 1
        elif lvl_rand < 0.6:
            lvl = 2
        elif lvl_rand < 0.85:
            lvl = 3
        elif lvl_rand < 0.95:
            lvl = 4
        else:
            lvl = 5

        return lvl

    @classmethod
    def roll_medium(cls):
        lvl_rand = random()
        if lvl_rand < 0.45:
            lvl = 1
        elif lvl_rand < 0.7:
            lvl = 2
        elif lvl_rand < 0.95:
            lvl = 3
        else:
            lvl = 4

        return lvl

    @classmethod
    def roll_hard(cls):
        lvl_rand = random()
        if lvl_rand < 0.55:
            lvl = 1
        elif lvl_rand < 0.85:
            lvl = 2
        else:
            lvl = 3

        return lvl

    @classmethod
    def roll_very_hard(cls):
        lvl_rand = random()
        if lvl_rand < 0.75:
            lvl = 1
        elif lvl_rand < 0.95:
            lvl = 2
        else:
            lvl = 3

        return lvl

    def add_advantage(self, title: str, points: int, stuck_on_match: bool = False):
        self.add_common(
            value=self.char.advantages,
            title=title,
            points=points,
            stuck_on_match=stuck_on_match
        )

    def add_disadvantage(self, title: str, points: int, stuck_on_match: bool = False):
        self.add_common(
            value=self.char.disadvantages,
            title=title,
            points=points,
            stuck_on_match=stuck_on_match
        )

    def add_perk(self, title: str, points: int, stuck_on_match: bool = False):
        self.add_common(
            value=self.char.perks,
            title=title,
            points=points,
            stuck_on_match=stuck_on_match
        )

    def add_skill(self, title: str, complexity: str, attribute: str, level: int):
        if title not in self.char.skills:
            roll = random()
            if roll < 0.35:
                initial = -4
            elif roll < 0.75:
                initial = -3
            elif roll < 0.85:
                initial = -2
            elif roll < 0.95:
                initial = -1
            else:
                initial = 0

            self.char.skills[title] = [complexity, attribute, initial]

        self.char.skills[title][2] += level

    def add_description(self, title: str):
        self.char.descriptions.append(title)

    def increase_st(self):
        self.char.st += 1

    def increase_dx(self):
        self.char.dx += 1

    def increase_iq(self):
        self.char.iq += 1

    def increase_ht(self):
        self.char.ht += 1

    def add_wealth(self, level_mod: int):
        new_level = self.char.wealth_level + level_mod
        if -3 <= new_level <= 4:
            self.char.wealth_level = new_level

    # Handlers

    def sport_jumping_long(self):
        if random() < 0.9:
            self.increase_st()
        if random() < 0.5:
            self.add_skill("Акробатика", self.char.SKILL_HARD, "DX", self.roll_hard())
        if random() < 0.05:
            self.increase_ht()

        if random() < 0.85:
            self.add_skill("Спорт", self.char.SKILL_MEDIUM, "DX", self.roll_medium())

    def sport_jumping_high(self):
        if random() < 0.65:
            self.increase_st()
        if random() < 0.25:
            self.add_advantage("Мягкое падение", 10)
        if random() < 0.25:
            self.add_skill("Акробатика", self.char.SKILL_HARD, "DX", self.roll_hard())
        if random() < 0.05:
            self.increase_ht()

    def sport_running_marathon(self):
        if random() < 0.95:
            self.increase_ht()
        if random() < 0.1:
            self.increase_dx()
        if random() < 0.15:
            self.add_advantage("Крепкий", 5)
        if random() < 0.03:
            self.add_advantage("Повышенное перемещение", 5, stuck_on_match=True)
        if random() < 0.4:
            self.add_skill("Бег", self.char.SKILL_HARD, "HT", self.roll_hard())

        if random() < 0.85:
            self.add_skill("Спорт", self.char.SKILL_MEDIUM, "DX", self.roll_medium())

    def sport_running_shuttle(self):
        if random() < 0.8:
            self.increase_dx()
        if random() < 0.35:
            self.increase_ht()
        if random() < 0.05:
            self.add_advantage("Крепкий", 5)

        speed_increase = random()
        if speed_increase < 0.03:  # 3%
            self.add_advantage("Повышенное перемещение", 5, stuck_on_match=True)
        elif speed_increase < 0.07:  # 4%
            self.add_advantage("Повышенная скорость", 5, stuck_on_match=True)

        if random() < 0.4:
            self.add_skill("Бег", self.char.SKILL_HARD, "HT", self.roll_hard())

    def sport_skip_it(self):
        if random() < 0.2:
            self.increase_iq()

        roll = random()
        if roll < 0.01:
            self.add_disadvantage("Горбун", -10)
        elif roll < 0.02:  # 1%
            self.add_disadvantage("Хромой", -10)
        elif roll < 0.08:  # 5%
            self.add_disadvantage("Мелкие физические недостатки", -1)
        elif roll < 0.18:  # 10%
            self.add_disadvantage("Лень", -10)
        elif roll < 0.2:  # 2%
            self.add_disadvantage("Низкая самооценка", -10)

    def sport_watching(self):
        if random() < 0.4:
            self.add_disadvantage("Внимательный", -1)

        roll = random()
        if roll < 0.01:
            self.add_disadvantage("Горбун", -10)
        elif roll < 0.02:  # 1%
            self.add_disadvantage("Хромой", -10)
        elif roll < 0.05:  # 3%
            self.add_disadvantage("Мелкие физические недостатки", -1)
        elif roll < 0.1:  # 5%
            self.add_disadvantage("Скромный", -1)
        elif roll < 0.12:  # 2%
            self.add_disadvantage("Нерешительность", -10)
        elif roll < 0.16:  # 4%
            self.add_disadvantage("Лень", -10)
        elif roll < 0.2:  # 4%
            self.add_disadvantage("Низкая самооценка", -10)

        roll = random()
        if roll < 0.1:
            self.add_perk("Прежде, чем что-то делать, нужно разработать план", -2)
        elif roll < 0.2:
            self.add_perk("Наблюдая за профессионалом, можно чему-то научиться", -1)

    def sport_betting(self):
        if random() < 0.55:
            self.add_disadvantage("Расточительство", -5)
        if random() < 0.05:
            self.add_disadvantage("Внимательный", -1)

        roll = random()
        if roll < 0.01:
            self.add_disadvantage("Горбун", -10)
        elif roll < 0.02:  # 1%
            self.add_disadvantage("Хромой", -10)
        elif roll < 0.05:  # 3%
            self.add_disadvantage("Мелкие физические недостатки", -1)
        elif roll < 0.07:  # 2%
            self.add_advantage("Удача", 15)
        elif roll < 0.15:  # 8%
            self.add_disadvantage("Самоуверенность", -5)
        elif roll < 0.2:  # 5%
            self.add_disadvantage("Невезение", -10)
        elif roll < 0.25:  # 5%
            self.add_wealth(1)
        elif roll < 0.32:  # 7%
            self.add_wealth(-1)
        elif roll < 0.45:  # 13%
            self.add_skill("Азартные игры", self.char.SKILL_MEDIUM, "IQ", self.roll_medium())

        if random() < 0.15:
            roll_level = random()
            if roll_level < 0.1:
                level = 5
            elif roll < 0.3:
                level = 4
            elif roll < 0.6:
                level = 3
            elif roll < 0.8:
                level = 2
            else:
                level = 1

            self.add_disadvantage("Долги", -1 * level, stuck_on_match=True)

        roll = random()
        if roll < 0.1:
            self.add_perk("Деньги всегда нужно во что-то вкладывать", -2)
        elif roll < 0.2:
            self.add_perk("Кто не рискует, тот не пьет шампанского", -1)

    def sport_managing(self):
        if random() < 0.45:
            self.add_skill("Лидерство", self.char.SKILL_MEDIUM, "IQ", self.roll_medium())

        if random() < 0.1:
            self.add_wealth(1)

        if random() < 0.35:
            self.add_advantage("Харизма", 5, stuck_on_match=True)
            if random() < 0.2:
                self.add_advantage("Харизма", 5, stuck_on_match=True)

        if random() < 0.15:
            self.add_advantage("Голос", 10)
        if random() < 0.15:
            self.add_skill("Публичное выступление", self.char.SKILL_MEDIUM, "IQ", self.roll_medium())

        roll = random()
        if roll < 0.1:
            self.add_perk("Я готов найти другого, чтобы сделал за меня мою работу", -1)
        elif roll < 0.2:
            self.add_perk("Чем больше людей в команде, тем большего она сможет достичь", -1)

    def camping_patrol(self):
        if random() < 0.9:
            level = self.roll_easy()
            sense = choice([
                "Обостренный слух",
                "Обостренное зрение",
            ])
            self.add_advantage(sense, 2 * level, stuck_on_match=True)

        if random() < 0.35:
            level = randint(0, 3) + randint(1, 2)
            self.add_advantage("Адаптация к темноте", level, stuck_on_match=True)

        if random() < 0.25:
            self.add_disadvantage("Внимательный", -1)

        if random() < 0.1:
            self.add_advantage("Боевые рефлексы", 15)

        if random() < 0.3:
            self.add_skill("Наблюдение", self.char.SKILL_MEDIUM, "Per", self.roll_medium())

        if random() < 0.3:
            self.add_skill("Скрытность", self.char.SKILL_MEDIUM, "DX", self.roll_medium())

    def camping_hunting(self):
        if random() < 0.35:
            self.add_skill("Скрытность", self.char.SKILL_MEDIUM, "DX", self.roll_medium())
        if random() < 0.15:
            self.add_skill("Соколиная охота", self.char.SKILL_MEDIUM, "IQ", self.roll_medium())
        if random() < 0.3:
            self.add_skill("Следопыт", self.char.SKILL_MEDIUM, "Per", self.roll_medium())
        if random() < 0.25:
            self.add_skill("Выживание", self.char.SKILL_MEDIUM, "Per", self.roll_medium())

        roll = random()
        if roll < 0.25:
            self.add_skill("Лук", self.char.SKILL_MEDIUM, "DX", self.roll_medium())
        elif roll < 0.35:
            self.add_skill("Копье", self.char.SKILL_MEDIUM, "DX", self.roll_medium())
        elif roll < 0.6:
            self.add_skill("Метание оружия (Копье)", self.char.SKILL_EASY, "DX", self.roll_easy())

        if random() < 0.25:
            self.add_skill("Ловушки", self.char.SKILL_MEDIUM, "IQ", self.roll_medium())

        if random() < 0.15:
            self.add_disadvantage("Одиночка ", -5)

    def camping_storytelling(self):
        if random() < 0.35:
            self.add_advantage("Харизма", 5, stuck_on_match=True)
            if random() < 0.2:
                self.add_advantage("Харизма", 5, stuck_on_match=True)

        if random() < 0.2:
            self.add_advantage("Голос", 10)

        if random() < 0.1:
            self.add_skill("Лидерство", self.char.SKILL_MEDIUM, "IQ", self.roll_medium())
        if random() < 0.15:
            self.add_skill("Выступление", self.char.SKILL_MEDIUM, "IQ", self.roll_medium())
        if random() < 0.15:
            self.add_skill("Публичное выступление", self.char.SKILL_MEDIUM, "IQ", self.roll_medium())
        if random() < 0.15:
            self.add_skill("Артистизм", self.char.SKILL_MEDIUM, "IQ", self.roll_medium())
        if random() < 0.2:
            self.add_skill("Пение", self.char.SKILL_EASY, "HT", self.roll_easy())

        roll = random()
        if roll < 0.15:
            self.add_disadvantage("Общительный", -5)
        elif roll < 0.25:  # 10%
            self.add_disadvantage("Легко понять", -10)
        elif roll < 0.3:  # 5%
            self.add_disadvantage("Лень", -10)
        elif random() < 0.35:  # 5%
            self.add_disadvantage("Вечеринки", -5)

    def camping_camping(self):
        if random() < 0.25:
            self.add_skill("Выживание", self.char.SKILL_MEDIUM, "Per", self.roll_medium())
        if random() < 0.25:
            self.add_skill("Повар", self.char.SKILL_MEDIUM, "IQ", self.roll_medium())
        if random() < 0.15:
            self.add_skill("Математика", self.char.SKILL_HARD, "IQ", self.roll_hard())
            self.add_skill("Инженерия", self.char.SKILL_HARD, "IQ", self.roll_hard())

        roll = random()
        if roll < 0.15:
            self.add_disadvantage("Трудоголик", -5)
        elif roll < 0.25:
            self.add_disadvantage("Вечеринки", -5)
        elif roll < 0.3:
            self.add_disadvantage("Кодекс чести", -5)
        elif roll < 0.35:
            self.add_disadvantage("Чувство долга", -5)
        elif roll < 0.45:
            self.add_advantage("Эмпатия", 5)

        roll = random()
        if roll < 0.1:
            self.add_perk("Если не я, то кто?", -2)
        elif roll < 0.2:
            self.add_perk("Лучше сделать самому, чем довериться кому-то", -2)

    def camping_managing(self):
        if random() < 0.25:
            self.add_disadvantage("Лень", -10)
        if random() < 0.25:
            self.add_disadvantage("Самоуверенность", -5)

        if random() < 0.25:
            self.add_skill("Лидерство", self.char.SKILL_MEDIUM, "IQ", self.roll_medium())
        if random() < 0.15:
            self.add_skill("Выживание", self.char.SKILL_MEDIUM, "Per", self.roll_medium())
        if random() < 0.15:
            self.add_skill("Артистизм", self.char.SKILL_MEDIUM, "IQ", self.roll_medium())
        if random() < 0.15:
            self.add_skill("Заговаривание зубов", self.char.SKILL_MEDIUM, "IQ", self.roll_medium())

        if random() < 0.05:
            self.add_advantage("Голос", 10)

        roll = random()
        if roll < 0.1:
            self.add_perk("Почему я?!", -2)
        elif roll < 0.2:
            self.add_perk("Зачем что-то делать самому, можно же поручить!", -2)

    def own_things_physical(self):
        roll = random()
        if roll < 0.4:
            self.increase_st()
        elif roll < 0.8:
            self.increase_ht()
        elif roll < 0.95:
            self.increase_dx()

        if random() < 0.3:
            self.add_skill("Акробатика", self.char.SKILL_HARD, "DX", self.roll_hard())
        if random() < 0.3:
            self.add_skill("Бег", self.char.SKILL_HARD, "HT", self.roll_hard())
        if random() < 0.15:
            self.add_skill("Плавание", self.char.SKILL_EASY, "HT", self.roll_easy())
        if random() < 0.05:
            self.add_skill("Лазание", self.char.SKILL_MEDIUM, "DX", self.roll_medium())
        if random() < 0.15:
            self.add_skill("Спорт", self.char.SKILL_MEDIUM, "DX", self.roll_medium())

        roll = random()
        if roll < 0.2:
            self.add_skill("Драка", self.char.SKILL_EASY, "DX", self.roll_easy())
        elif roll < 0.23:  # 3%
            self.add_skill("Каратэ", self.char.SKILL_HARD, "DX", self.roll_hard())
        elif roll < 0.26:  # 3%
            self.add_skill("Дзюдо", self.char.SKILL_HARD, "DX", self.roll_hard())

    def own_things_learning(self):
        pass

    def own_things_playing(self):
        pass

    def own_things_discussing(self):
        pass

    def own_things_busy(self):
        pass

    def own_things_meditation(self):
        pass

    def own_things_art(self):
        pass

    def own_things_mixed(self):
        pass

    def own_things_nothing(self):
        pass

    def own_things_not_your_business(self):
        pass


def create_handlers_for(char: Character):
    handler = CharHandler(char)

    return {
        "sport_jumping_long": handler.sport_jumping_long,
        "sport_jumping_high": handler.sport_jumping_high,
        "sport_running_marathon": handler.sport_running_marathon,
        "sport_running_shuttle": handler.sport_running_shuttle,
        "sport_skip_it": handler.sport_skip_it,
        "sport_watching": handler.sport_watching,
        "sport_betting": handler.sport_betting,
        "sport_managing": handler.sport_managing,

        "camping_patrol": handler.camping_patrol,
        "camping_hunting": handler.camping_hunting,
        "camping_storytelling": handler.camping_storytelling,
        "camping_camping": handler.camping_camping,
        "camping_managing": handler.camping_managing,

        "own_things_physical": handler.own_things_physical,
        "own_things_learning": handler.own_things_learning,
        "own_things_playing": handler.own_things_playing,
        "own_things_discussing": handler.own_things_discussing,
        "own_things_busy": handler.own_things_busy,
        "own_things_meditation": handler.own_things_meditation,
        "own_things_art": handler.own_things_art,
        "own_things_mixed": handler.own_things_mixed,
        "own_things_nothing": handler.own_things_nothing,
        "own_things_not_your_business": handler.own_things_not_your_business,
    }
