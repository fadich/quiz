
class Character:
    BASE_ATTRIBUTE_VALUE = 10
    DEFAULT_COST_PER_ST = 10
    DEFAULT_COST_PER_DX = 20
    DEFAULT_COST_PER_IQ = 20
    DEFAULT_COST_PER_HT = 10

    SKILL_EASY = 0
    SKILL_MEDIUM = 1
    SKILL_HARD = 2
    SKILL_VERY_HARD = 3

    WEALTH_BY_LEVEL = {
        -3: ("Нищий", -25),
        -2: ("Бедный", -15),
        -1: ("Небогатый", -10),
        0: ("Средний", 0),
        1: ("Обеспеченный", 10),
        2: ("Богатый", 20),
        3: ("Очень богатый", 30),
        4: ("Жутко богатый", 50),
    }

    def __init__(self):
        self.st = self.BASE_ATTRIBUTE_VALUE
        self.dx = self.BASE_ATTRIBUTE_VALUE
        self.iq = self.BASE_ATTRIBUTE_VALUE
        self.ht = self.BASE_ATTRIBUTE_VALUE

        self.cost_per_st = self.DEFAULT_COST_PER_ST
        self.cost_per_dx = self.DEFAULT_COST_PER_DX
        self.cost_per_iq = self.DEFAULT_COST_PER_IQ
        self.cost_per_ht = self.DEFAULT_COST_PER_HT

        self.advantages = {}  # {"Adv-1": 10, "Adv-2": 15, ...}
        self.disadvantages = {}  # {"Dis-1": -10, "Dis-2": -5, ...}
        self.perks = {}  # {"Perk-1": 1, "Perk-2": 3, ...}
        self.skills = {}  # {"Skill-1": ["hard", "DX", 2], "Skill-2": ["easy", "IQ", -1], ...}
        self.descriptions = set()  # {"Item-1", "Item-2", ...}

        self.wealth_level = 0

    @property
    def st_cost(self):
        return (self.st - self.BASE_ATTRIBUTE_VALUE) * self.cost_per_st

    @property
    def dx_cost(self):
        return (self.dx - self.BASE_ATTRIBUTE_VALUE) * self.cost_per_dx

    @property
    def iq_cost(self):
        return (self.iq - self.BASE_ATTRIBUTE_VALUE) * self.cost_per_iq

    @property
    def ht_cost(self):
        return (self.ht - self.BASE_ATTRIBUTE_VALUE) * self.cost_per_ht

    @property
    def attributes_cost(self):
        return sum([
            self.st_cost,
            self.dx_cost,
            self.iq_cost,
            self.ht_cost,
        ])

    @property
    def advantages_cost(self):
        return sum(self.advantages.values())

    @property
    def disadvantages_cost(self):
        return sum(self.disadvantages.values())

    @property
    def perks_cost(self):
        return sum(self.perks.values())

    @property
    def skills_cost(self):
        return sum(map(lambda x: self.get_skill_cost(x[0], x[2]), self.skills.values()))

    @property
    def wealth(self):
        return self.WEALTH_BY_LEVEL[self.wealth_level]

    @property
    def total_points(self):
        return sum([
            self.attributes_cost,
            self.advantages_cost,
            self.disadvantages_cost,
            self.perks_cost,
            self.skills_cost,
        ])

    @classmethod
    def get_skill_cost(cls, complexity: int, level: int):
        level += complexity
        if level < 0:
            cost = 0
        elif level == 0:
            cost = 1
        elif level == 1:
            cost = 2
        elif level == 2:
            cost = 4
        elif level == 3:
            cost = 8
        else:
            cost = 12 + 4 * abs(4 - level)

        return cost

    def print(self):
        def format_common(title: str, variable: dict):
            if len(variable):
                frmt = ';\n-  '.join(map(lambda x: f"{x[0]} [{x[1]}]", variable.items()))
                print(f"{title}:\n-  {frmt}.")

        def format_skills(title: str):
            if len(self.skills):
                frmt = ';\n-  '.join(map(
                    lambda x: f"{x[0]}, {x[1][1]}{x[1][2]:+} [{self.get_skill_cost(x[1][0], x[1][2])}]",
                    self.skills.items())
                )
                print(f"{title}:\n-  {frmt}.")

        if self.wealth_level < 0:
            self.disadvantages[f"Богатство: {self.wealth[0]}"] = self.wealth[1]
        elif self.wealth_level > 0:
            self.advantages[f"Богатство: {self.wealth[0]}"] = self.wealth[1]

        print()
        print(f"====" * 15)
        print(f"Аттрибуты [{self.attributes_cost}]")
        print(f"ST: {self.st} [{self.st_cost}]")
        print(f"DX: {self.dx} [{self.dx_cost}]")
        print(f"IQ: {self.iq} [{self.iq_cost}]")
        print(f"HT: {self.ht} [{self.ht_cost}]")

        format_common(f"Преимущества [{self.attributes_cost}]", self.advantages)
        format_common(f"Недостатки [{self.disadvantages_cost}]", self.disadvantages)
        format_common(f"Причуды [{self.perks_cost}]", self.perks)
        format_skills(f"Умения [{self.skills_cost}]")

        if self.descriptions:
            print(f"====" * 15)
            frmt = ';\n-  '.join(self.descriptions)
            print(f"Прочее:\n-  {frmt}.")

        print(f"====" * 15)
        print(f"Очков портачено ~≈ {self.total_points} ≈~")
        print(f"====" * 15)
