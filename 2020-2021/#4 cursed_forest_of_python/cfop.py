from textwrap import dedent
from time import sleep
from sys import exit
from random import choices
import platform
import os

# list of enemy names and difficutly/rarity multipliers
e_names = {'Devil': 1, 'Ghoul': 1.1, 'Demon': 1.2, 'Drowner': 1.3, 'Wolf': 1.4, 'Mutant': 1.5, 'Wraith': 1.6, 'Cockatrice': 1.7, 'Skullhead': 1.8, 'Kikimore': 1.9, 'Wyvern': 1.95}

elements = ['Fire', 'Water', 'Earth', 'Air']
element_adv = {'Fire': ['Air'],
               'Air': ['Earth'],
               'Earth': ['Water'],
               'Water': ['Fire'],
               'Light': ['Fire', 'Air', 'Earth', 'Water']}
 
def nprint(s):
    print('\n' + s)

def ninput(s):
    return input('\n' + s + '\n\n>>> ').lower()

def c_understand():
    nprint("Sorry, I can't understand your answer. Try again")

def clear():
    if platform.system() == 'Windows':
        os.system('cls')

    else:
        os.system('clear')

def user_help():
    print(dedent(f"""
          +------------------------------------------------+
          |                 <-- LIGHT -->                  |
          |      FIRE -> AIR -> EARTH -> WATER -> FIRE     |
          +--------------------Commands--------------------+
          | > map: display map                             |
          | > move: change location                        | 
          | > store: move to store if in Main City         |
          |   > buy: purchase items in store               |
          | > attack: attack nearby enemy                  |
          | > loot: loot nearby chests                     | 
          | > inventory: display inventory                 |
          | > potion: use a potion to heal HP              | 
          | > equip: equip armor or sword                  | 
          | > upgrade: upgrade armor or sword              | 
          | > stats: display player statistics             | 
          | > leave: you will leave the game, pls stay :/  | 
          +------------------------------------------------+"""))

##########
# location: string (p.location)
# place: list (object Place)
##########
# returns m
# m will print player location and use a for loop to decide if place was discovered or not
def view_map(location):
    m_width = 50
    m = dedent(f"""
                +{'-'*m_width}+
                |{'THE CURSED FOREST OF PYTHON':^{m_width}}{'|':>1}
                +{'-'*m_width}+
                |{'CURRENT LOCATION: ' + location.name:^{m_width}}{'|':>1}
                +{'-'*m_width}+
                """)

    for place in places:
        m += f"|{place.name if place.discovered else 'UNDISCOVERED':^{m_width}}|\n"

        if place.stores and place.discovered:
            m +=  f"|{'Stores: ' + ', '.join([store.name for store in place.stores]):^{m_width}}|\n"

        m += f"|{'-'*m_width}+\n"

    print(m)

def calc_damage(receiving, dealing):
    # If player is taking damage
    if isinstance(receiving, Player):
        # Checking if player has armor
        if receiving.armor:
            # If enemy damage has advantage against player armor, double the damage
            if receiving.armor.element in element_adv[dealing.element]:
                # If the player's armor is stronger than the damage dealt, take no damage instead of healing the player lol
                if 2*dealing.damage-receiving.armor.defense <= 0:
                    nprint('Your enemy could not penetrate the defense of your armor. No damage was taken!')

                else:
                    receiving.hp -= 2*dealing.damage-receiving.armor.defense
                    nprint('Your armor is weak against your enemy. You took double the damage. Ouch!')

            # If player armor has advantage against enemy damaage, half the damage
            elif dealing.element in element_adv[receiving.armor.element]:
                # If the player's armor is stronger than the damage dealt, take no damage instead of healing the player lol
                if dealing.damage/2-receiving.armor.defense <= 0:
                    nprint('Your enemy could not penetrate the defense of your armor. No damage was taken!')

                else:
                    receiving.hp -= dealing.damage/2-receiving.armor.defense
                    nprint('The element in your armor reduced the damage!')

            # The player has armor but its not related to the enemy
            else:
                receiving.hp -= dealing.damage-receiving.armor.defense

        # The player has no armor
        else:
            receiving.hp -= dealing.damage

    # Player is dealing damage
    else:
        # If player weapon has advantage over enemy element, double the damage
        if receiving.element in element_adv[dealing.weapon.element]:
            receiving.hp -= 2*dealing.weapon.damage
            nprint('Your sword is strong against your enemy. You dealt double the damage!')

        # If enemy element has advantage over player weapon element, half the damage
        elif dealing.weapon.element in element_adv[receiving.element]:
            receiving.hp -= dealing.weapon.damage/2
            nprint('Your sword is weak against the enemy. You dealt half the damage!')

        else:
            receiving.hp -= dealing.weapon.damage

def fight(p, enemy):
    turn = 1
    while True:
        # Player attacks first every turn
        # Calculates the element advantages
        # calc_damage(receiving, dealing)
        calc_damage(enemy, p)
        # Enemy attacks
        calc_damage(p, enemy)

        print(dedent(f"""
              +------+---------------+---------------+
              |{'Turn':^6}|{'Player HP':^15}|{f'{enemy.name} HP':^15}|
              +------+---------------+---------------+
              |{turn:^6}|{int(p.hp):^15}|{int(enemy.hp):^15}|
              +------+---------------+---------------+"""))

        if p.hp <= 0:
            nprint(f'You honestly suck, you died to a mere {enemy.name}. Start from scratch now')
            exit()

        if enemy.hp <= 0:
            nprint(f'Congratulations, you killed the {enemy.name}. You were rewarded {int(enemy.damage)*2} coins')
            p.location.enemies.remove(enemy)
            p.money += enemy.damage*4
            break

        ninput(f'Press "Enter" to continue to turn {turn+1}')
        turn += 1
        
        clear()

class Player():
    def __init__(self, location, money = 0):
        self.hp = 100
        self.weapon = ''
        self.armor = ''
        self.money = money
        self.inventory = []
        self.location = location

    def equip_armor(self):
        armors = []

        for item in self.inventory:
            if isinstance(item, Armor):
                armors.append(item)               

        if armors:
            nprint(f"Here are the armors you have:\n{''.join([str(armor) for armor in armors])}")

        else:
            nprint('You do not have any armor')
            return False

        while True:
            choice = ninput('Enter the name of the armor you want to equip. To cancel enter "0"')
            for armor in armors:
                if armor.name.lower() == choice:
                    # Removing current armor and adding to inventory if the player has any
                    if self.armor:
                        self.inventory.append(self.armor)

                    # Equiping new armor and removing it from the inventory
                    self.armor = armor
                    self.inventory.remove(armor)
                    nprint(f'You equipped {self.armor.name} succesfully')

                    return

                elif choice == '0':
                    return

            else:
                c_understand()

    def upgrade_armor(self):

        if self.armor:
            cost = 20*self.armor.level
        
            nprint(f'The cost to upgrade your current armor to level {self.armor.level+1} is: {cost} coins')

            if self.money < cost:
                nprint(f'You do not have enough money to upgrade your {self.armor.name} to level {self.armor.level+1}')
                return

            while True:
                sure = ninput(f'Would you like to upgrade your {self.armor.name}? 0: NO / 1: YES')

                if sure.isdigit():
                    if sure == '0':
                        return

                    elif sure == '1':
                        self.money -= cost
                        self.armor.level += 1
                        self.armor.defense *= self.armor.level*0.25+1

                        nprint(f'{cost} coins were removed from your inventory')
                        nprint(f'Your {self.armor.name} was upgraded to {self.armor.level}')
                        
                        return

                    else:
                        c_understand()
                        continue

                else:
                    c_understand()
                    continue

        else:
            nprint('You do not have any armor equipped')
            return False

    def equip_weapon(self):
        weapons = []
        for item in self.inventory:
            if isinstance(item, Weapon):
                weapons.append(item)

        if weapons:
            nprint(f"Here are the weapons you have:\n{''.join([str(weapon) for weapon in weapons])}")

        else:
            nprint('You do not have any weapons')
            return False

        while True:
            choice = ninput('Enter the name of the weapon you want to equip. To cancel enter "0"')
            for weapon in weapons:
                if weapon.name.lower() == choice:
                    # Removing current weapon and adding to inventory if the player has any
                    if self.weapon:
                        self.inventory.append(self.weapon)

                    # Equiping new weapon and removing it from the inventory
                    self.weapon = weapon
                    self.inventory.remove(weapon)
                    nprint(f'You equipped {self.weapon.name} succesfully')

                    return

                elif choice == '0':
                    return

            else:
                c_understand()

    def upgrade_weapon(self):
        if self.weapon:
            cost = 15*self.weapon.level

            nprint(f'The cost to upgrade your current weapon to level {self.weapon.level+1} is: {cost} coins')

            if self.money < cost:
                nprint(f'You do not have enough money to upgrade your {self.weapon.name} to level {self.weapon.level+1}')
                return

            while True:
                sure = ninput(f'Would you like to upgrade your {self.weapon.name}? 0: NO / 1: YES')
                if sure.isdigit():
                    if sure == '0':
                        return

                    elif sure == '1':
                        self.money -= cost
                        self.weapon.level += 1
                        self.weapon.damage *= self.weapon.level*0.25+1

                        nprint(f'{cost} coins were removed from your inventory')
                        nprint(f'Your {self.weapon.name} was upgraded to {self.weapon.level}')

                        return

                    else:
                        c_understand()
                        continue

                else:
                    c_understand()
                    continue
            
        else:
            nprint('You do not have any weapon equipped')
            return False

    def view_intentory(self):
        i_width = 25
        s = f"""
            +{'-'*i_width}+
            |{'Inventory':^{i_width}}|
            +---+{'-'*(i_width-4)}+"""

        item_n = 1
        for item in self.inventory:
            # Here I had to indent to the same level as s above, so that dedent works properly while I use dedent only once
            s += f"""
            |{item_n:^3}|{item.name:<{i_width-4}}|
            +---+{'-'*(i_width-4)}+"""

            item_n += 1

        # I did not use nprint here because then it would have two blank spaces on the top
        print(dedent(s))

    def __str__(self):
        # player table width
        p_width = 15
        # information column width
        inf_width = 9

        # This multiline string must be in the same identation level for Weapon.str and Armor.str
        # adding 1 to player stats line because of the extra column below
        s = dedent(f"""
                   +{'-'*(p_width+inf_width+1)}+
                   |{'Player Stats':^{p_width+inf_width+1}}|
                   +{'-'*inf_width}+{'-'*p_width}+
                   |{'HP':^{inf_width}}|{int(self.hp):^{p_width}}|
                   |{'Money':^{inf_width}}|{int(self.money):^{p_width}}|
                   +{'-'*inf_width}+{'-'*p_width}+""")

        if self.weapon:
            s += str(self.weapon)
        
        if self.armor:
            s += str(self.armor)

        return s

class Place():
    def __init__(self, name, tier, chests, stores, story):
        self.name = name
        self.tier = tier
        self.enemies = []
        self.chests = chests
        self.stores = stores
        self.discovered = False
        self.story = story

    def generate_enemies(self):
        for i in range(int(self.tier)):
            enemy = choices(list(e_names.keys()), weights=[2-value for value in e_names.values()])[0]
            element = choices(elements)[0]
            self.enemies.append(Enemy(enemy, 17*self.tier*e_names[enemy], 3.3*self.tier*e_names[enemy], element))

    def display_chests(self):
        # Used to check if there are chests available
        unopened = []
        for chest in self.chests:
            if not chest.opened:
                unopened.append(chest)

        if not unopened:
            nprint('There is nothing to loot here')
            return False

        else:
            nprint('These are the chests available')
            # Not using nprint here because then there would be 2 spaces before the chests
            print(f"{''.join([str(chest) for chest in self.chests])}")
            return True

    def display_stores(self):
        store_width = 30
        # store number width
        stn_width = 3
        s = f"""
             +{'-'*(store_width+stn_width+1)}+
             |{'Store in ' + self.name:^{(store_width+stn_width+1)}}|
             +{'-'*stn_width}+{'-'*store_width}+"""

        x = 1
        for store in self.stores:
            # this string has to match the indentation of the string above for dedent to work
            s += f"""
             |{x:^{stn_width}}|{store.name:^{store_width}}|"""

        # not using nprint to avoid the additional space that the multine string has
        print(dedent(s) + f"\n+{'-'*stn_width}+{'-'*store_width}+")


    def __str__(self):
        # width of the Place table
        p_width = 25 if not len(self.enemies) else len(self.enemies)*7+25
        # width of the information column
        inf_width = 9
        s = f"""
            +{'-'*p_width}+
            |{self.name:^{p_width}}|
            +{'-'*inf_width}+{'-'*(p_width-inf_width-1)}+
            |{'Tier':^{inf_width}}|{self.tier:^{p_width-inf_width-1}}|
            |{'Enemies':^{inf_width}}|{', '.join(enemy.name for enemy in self.enemies) if self.enemies else 'None':^{p_width-inf_width-1}}|
            |{'Loot':^{inf_width}}|{len(self.chests):^{p_width-inf_width-1}}|
            +{'-'*inf_width}+{'-'*(p_width-inf_width-1)}+"""

        return dedent(s)
        
class Store():
    def __init__(self, name, stock):
        self.name = name
        self.stock = stock

    def buy_item(self):
        clear()
        while True:
            print(self)
            sure = ninput("What item would you like to buy? 0: CANCEL / 1: ITEM ONE / 2: ITEM TWO...")

            if sure.isdigit():
                if (int(sure) < 0) or (int(sure) > len(self.stock)):
                    clear()
                    c_understand()
                    continue

                elif sure == '0':
                    clear()
                    nprint(f'You left the store. You are now in {p.location.name}')
                    return

                else:
                    if p.money < self.stock[int(sure)-1].price:
                        clear()
                        nprint(f'You do not have enough money to buy the {self.stock[int(sure)-1]}')
                        continue

                    else:
                        clear()
                        # Charging the player
                        p.money -= self.stock[int(sure)-1].price
                        # Adding the item to the player's inventory
                        p.inventory.append(self.stock[int(sure)-1])

                        nprint(f'You succesfully bought the item {self.stock[int(sure)-1].name}. {self.stock[int(sure)-1].price} coins were removed from your inventory')
                        
                        # Removing the item from the stock
                        self.stock.remove(self.stock[int(sure)-1])

            else:
                clear()
                c_understand()
                continue

    def __str__(self):
        # number column width
        n_width = 3
        # item column width
        it_width = 20
        # price column width
        p_width = 6
        # I had to add two to the self.name line because of the two + that are present because of the extra tables
        s = f"""
            +{'-'*(n_width+it_width+p_width+2)}+
            |{self.name:^{(n_width+it_width+p_width+2)}}|
            +{'-'*n_width}+{'-'*it_width}+{'-'*p_width}+
            |{'#':^{n_width}}|{'Item':^{it_width}}|{'Price':^{p_width}}|
            +{'-'*n_width}+{'-'*it_width}+{'-'*p_width}+"""

        i = 0
        for item in self.stock:
            i += 1
            # I had to match the same identation as s
            s += f"""
            |{i:^{n_width}}|{item.name:^{it_width}}|{item.price:^{p_width}}|"""

        if self.stock:
            return dedent(s) + f"\n+{'-'*n_width}+{'-'*it_width}+{'-'*p_width}+"

        else:
            return "Sorry, this store's stock is currently empty"


class Enemy():
    def __init__(self, name, hp, damage, element):
        self.name = name
        self.hp = hp
        self.damage = damage
        self.element = element

    def __str__(self):
        # enemy table width
        e_width = 20
        # width of the stat column
        st_width = 9
        # add 1 to the self.name expression because of the extra column below
        # the index of each enemy is added when printing them
        # Here i used the index function, but in other __str__ functions I used a loop to add the number of such object
        return dedent(f"""
                      +{'-'*(e_width+1)}+
                      |{self.name + ' #' + str(p.location.enemies.index(self)+1):^{e_width+1}}|
                      +{'-'*st_width}+{'-'*(e_width-st_width)}+
                      |{'Damage':^{st_width}}|{int(self.damage):^{e_width-st_width}}|
                      |{'HP':^{st_width}}|{int(self.hp):^{e_width-st_width}}|                     
                      |{'Element':^{st_width}}|{self.element:^{e_width-st_width}}|
                      +{'-'*st_width}+{'-'*(e_width-st_width)}+""")

class Weapon():
    def __init__(self, name, element, price=30):
        self.name = name
        self.level = 1
        self.damage = 5
        self.element = element
        self.price = price

    def __str__(self):
        # weapon table width
        w_width = 15
        # info column width
        inf_width = 9
        # Adding one to the name expression because of the extra column below
        s = f"""
            +{'-'*(w_width+inf_width+1)}+
            |{'WEAPON':^{w_width+inf_width+1}}|
            +{'-'*(w_width+inf_width+1)}+
            |{self.name:^{w_width+inf_width+1}}|
            +{'-'*inf_width}+{'-'*w_width}+
            |{'Level':^{inf_width}}|{self.level:^{w_width}}|
            |{'Damage':^{inf_width}}|{self.damage:^{w_width}}|
            |{'Element':^{inf_width}}|{self.element:^{w_width}}|
            +{'-'*inf_width}+{'-'*w_width}+"""
        return dedent(s)
           
class Armor():
    def __init__(self, name, element, price=30):
        self.name = name
        self.level = 1
        self.defense = 2
        self.element = element
        self.price = price

    def __str__(self):
        # armor table width
        a_width = 15
        # info column width
        inf_width = 9
        # Adding one to the name expression because of the extra column below
        s = f"""
            +{'-'*(a_width+inf_width+1)}+
            |{'ARMOR':^{a_width+inf_width+1}}|
            +{'-'*(a_width+inf_width+1)}+
            |{self.name:^{a_width+inf_width+1}}|
            +{'-'*inf_width}+{'-'*a_width}+
            |{'Level':^{inf_width}}|{self.level:^{a_width}}|
            |{'Defense':^{inf_width}}|{int(self.defense):^{a_width}}|
            |{'Element':^{inf_width}}|{self.element:^{a_width}}|
            +{'-'*inf_width}+{'-'*a_width}+"""
        return dedent(s)

class Potion():
    def __init__(self, price):
        self.name = 'Health Potion'
        self.price = price

    def use_potion(self):
        if p.hp == 100:
            nprint('Your HP is already at 100')
        
        else:
            p.inventory.remove(self)

            p.hp += 50
            if p.hp > 100:
                p.hp = 100

            nprint(f'You healed 50 points of HP, your current HP is: {int(p.hp)}')

    def __str__(self):
        return f'{self.name}'

class Chest():
    def __init__(self, items, money):
        self.items = items
        self.money = money
        self.opened = False

    def looting(self):
        if not self.opened:
            self.opened = True
            for item in self.items:
                p.inventory.append(item)

            p.money += self.money

            nprint(f"The items: {', '.join(item.name for item in self.items)} and {self.money} coins were added to your inventory")

        else:
            nprint("You already looted this chest. Don't be greedy")

    def __str__(self):
        if self.money >= 0:
            self.type = 'Wooden'

        if self.money >= 20:
            self.type = 'Metal'

        if self.money >= 40:
            self.type = 'Silver'

        if self.money >= 60:
            self.type = 'Golden'

        if self.money >= 80:
            self.type = 'Platinum'
        
        if self.money >= 100:
            self.type = 'Legendary'

        chest_width = 15
        s = f"""
            +{'-'*(chest_width)}+
            |{self.type + ' Chest #' + str(p.location.chests.index(self)+1):^{chest_width}}|
            +{'-'*chest_width}+"""

        return dedent(s)

# Generating all weapons
fire_sword = Weapon('Fire Sword', 'Fire')
air_sword = Weapon('Air Sword', 'Air')
earth_sword = Weapon('Earth Sword', 'Earth')
water_sword = Weapon('Water Sword', 'Water')
light_sword = Weapon('Light Sword', 'Light', 200)

# Generating all armors
fire_armor = Armor('Fire Armor', 'Fire')
air_armor = Armor('Air Armor', 'Air')
earth_armor = Armor('Earth Armor', 'Earth')
water_armor = Armor('Water Armor', 'Water')
light_armor = Armor('Light Armor', 'Light', 200)

# Generating chests
chest_1 = Chest([fire_armor], 10)
chest_2 = Chest([air_armor], 20)
chest_3 = Chest([earth_armor], 30)
chest_4 = Chest([water_armor], 40)

# Generating all places
deep_if_valley = Place('Deep If Valley', 1, [chest_1], [],
"""This place is so deep and vast, it is hard to comprehend which turn leads to where.
This almost seems like a stacked maze, and after every IF has been executed, you already forgot what the condition was.""")

no_comment_zone = Place('No Comment Zone', 2, [chest_2], [],
"""This place is empty, so empty that it is heartbreaking to look at.
The only reason why the creator of this game knows how to navigate this is because he was here when it was written.
However, for any new visitors, it is impossible to understand this 100 character line with a one-line if and one-line for loop.""")

bad_variable_name = Place('Bad Variable Name', 3, [chest_3], [],
"""N? n? x? i and j? What do they even mean? What values do they hold?
All these variables have the worst possible name!!!!!
"THE NUMBERS MASON! WHAT DO THEY MEAN?""")

last_store = Store('Light Shop', [light_sword, light_armor])
def_func_in_func = Place('Def Func in Func', 4, [chest_4], [last_store],
"""You stare in utter horror at such a horrific sight, and your puny brain hurts the more you look at this.
There is a function being defined inside the definition of another function!
However, the end is near, and you have finally reached the last stage. It will not be easy to beat it, though!
If you do beat it, there is a huge reward waiting for you! Or, if you have the money, you can just buy it lol.""")

# generating potions

# health potions used in testing
potion_1_test = Potion(25)
potion_2_test = Potion(25)
# health potions in Main City Store
potion_1 = Potion(25)
potion_2 = Potion(25)
potion_3 = Potion(25)
potion_4 = Potion(25)
potion_5 = Potion(25)

main_city_store = Store('Main City Store', [air_sword, earth_sword, water_sword, potion_1, potion_2, potion_3, potion_4, potion_5])
main_city = Place('Main City', 0, [], [main_city_store],
"""This is where your journey begins.
This place is safe and has no monsters, and there is also a place for you to buy different items.
Consider this your home, and come here whenever you are in the need of supplies.
Remember that you found a Fire Sword? You don't, well your memory is foggy, but there is a Fire Sword in your inventory.
To buy these supplies you must start moving downwards through the dreadful Dark Forest of Python and defeat monsters!""")

places = [main_city, deep_if_valley, no_comment_zone, bad_variable_name, def_func_in_func]

# Generating player
clear()
nprint('Playing in testing mode will give you all the items and 1000 coins from the beginning')
while True:
    testing = ninput("Do you want to enjoy the game's full potential or simply test? 1: PLAY NORMALLY / 2: TEST")

    if testing.isdigit():
        if testing == '1':
            p = Player(main_city)
            p.inventory.append(fire_sword)
            break

        elif testing == '2':
            p = Player(main_city, money=1000)
            p.inventory.append(fire_sword)
            p.inventory.append(water_sword)
            p.inventory.append(earth_sword)
            p.inventory.append(air_sword)
            p.inventory.append(fire_armor)
            p.inventory.append(water_armor)
            p.inventory.append(earth_armor)
            p.inventory.append(air_armor)
            p.inventory.append(light_armor)
            p.inventory.append(light_sword)
            p.inventory.append(potion_1_test)
            p.inventory.append(potion_2_test)
            break

        else:
            c_understand()
            continue

    else:
        c_understand()
        continue

clear()

# Create Story line
nprint(f"""WELCOME TO THE CURSED FOREST OF PYTHON
{'-'*38}
This is a RPG game, but for a programmer it would be more of a horror game.
Each level represents practices that should never be done, and include horrible monsters for you to defeat.
Advance from stage to stage, and do not forget to use the best weapon and armor against your enemy.
GOOD LUCK!""")

ninput('Press "Enter" to continue')

while True:
    if not p.location.enemies:
        p.location.generate_enemies()

        if p.location.discovered and p.location.enemies:
            nprint('NO!!! New monsters appeared')

    if not p.location.discovered:
        p.location.discovered = True
        nprint(p.location.story)

    print(p.location)

    while True:
        action = ninput('What would you like to do? Type "help" if you are uncertain')

        if action == 'help':
            user_help()
            continue

        elif action == 'leave':
            nprint("Please don't leave :(")

            while True:
                sure = ninput(f"Are you sure you want to leave the Cursed Forest of Python? 0: NO / 1: YES")

                if sure == '0':
                    nprint('Pheww, thank you for staying')
                    continue

                elif sure == '1':
                    nprint('Fine...')
                    exit()

                else:
                    c_understand()
                    continue

        elif action == 'inventory':
            if p.inventory:
                p.view_intentory()
                continue

            else:
                nprint('Sorry, your inventory is empty')
                continue

        elif action == 'stats':
            print(p)
            continue

        elif action == 'map':
            view_map(p.location)
            continue

        elif action == 'potion':
            for item in p.inventory:
                if isinstance(item, Potion):
                    item.use_potion()
                    break

            else:
                nprint('Sorry, you do not have any potions in your inventory')
                continue

        elif action == 'equip':
            while True:
                sure = ninput('Would you like to equip a weapon or armor? 1: WEAPON / 2: ARMOR / 0: CANCEL')

                if sure == '1':
                    if not p.equip_weapon():
                        continue

                    break

                elif sure == '2':
                    if not p.equip_armor():
                        continue

                    break

                elif sure == '0':
                    break

                else:
                    c_understand()
                    continue

            continue

        elif action == 'upgrade':
            while True:
                sure = ninput('What would you like to upgrade? 1: WEAPON / 2: ARMOR / 0: CANCEL')

                if sure.isdigit():
                    if sure == '1':
                        if p.upgrade_weapon():
                            break

                        else:
                            continue
                    elif sure == '2':
                        if p.upgrade_armor():
                            break

                        else:
                            continue

                    elif sure == '0':
                        break

                else:
                    c_understand()
                    continue

        elif action == 'move':
            while True:
                sure = ninput(f"Do you want to move up or down? 1: UP / 2: DOWN / 0: CANCEL")
                if sure == '1':
                    if p.location == places[0]:
                        nprint('Sorry, you are already at the highest point of the map. Try moving to the down.')
                        continue

                    else:
                        nprint(f"Moving to {places[places.index(p.location)-1].name if places[places.index(p.location)-1].discovered else 'UNDISCOVERED'}...")
                        sleep(2)
                        p.location = places[places.index(p.location)-1]
                        clear()
                        break

                elif sure == '2':
                    if p.location == places[-1]:
                        nprint('Sorry, you are already at the lowest point of the map. Try moving to the up.')
                        continue

                    else:
                        nprint(f"Moving to {places[places.index(p.location)+1].name if places[places.index(p.location)+1].discovered else 'UNDISCOVERED'}...")
                        sleep(2)
                        p.location = places[places.index(p.location)+1]
                        clear()
                        break

                elif sure == '0':
                    nprint('Okay, be lazy then. You are staying on the same spot')
                    break

                else:
                    c_understand()                
                    continue
        
            break

        elif action == 'attack':
            if p.location.enemies:
                nprint("You've entered the combat zone. These are the enemies nearby")
                print(''.join([str(enemy) for enemy in p.location.enemies]))

                if not p.weapon:
                    nprint('WARNING!!! You do not have a weapon')
                    nprint('You cannot attack without a weapon. Please check your inventory for one')
                    nprint(f'You have left the combat zone. You are now in {p.location.name}')
                    break

                if not p.armor:
                    nprint('WARNING!!! You do not have any armor')


                while True:
                    sure = ninput('Which enemy would you like to attack? 0: CANCEL / 1: FIRST ENEMY / 2: SECOND ENEMY...')
                    if sure.isdigit():
                        if int(sure) > len(p.location.enemies) or int(sure) < 0:
                            c_understand()
                            continue

                        elif sure == '0':
                            nprint("You're such a coward!")
                            break

                        else:
                            clear()
                            fight(p, p.location.enemies[int(sure)-1])
                            break

                    else:
                        c_understand()
                        continue

            else:
                nprint('There are no enemies nearby')

        elif action == 'loot':
            if p.location.enemies:
                nprint('You can only loot when all enemis are dead')

            else:
                if p.location.display_chests():
                    while True:
                        sure = ninput('Which chest would you like to loot? 0: CANCEL / 1: FIRST CHEST / 2: SECOND CHEST...')

                        if sure.isdigit():
                            if (int(sure) < 0) or (int(sure) > len(p.location.chests)):
                                c_understand()
                                continue

                            elif sure == '0':
                                nprint('You deided to leave the treasure behind.')
                                break

                            else:
                                p.location.chests[int(sure)-1].looting()
                                break

                        else:
                            c_understand()
                            continue
                    
                continue

        elif action == 'store':
            if not p.location.stores:
                nprint('You look around and see no stores nearby')
                continue

            else:
                nprint(f"These are the stores available at {p.location.name}: ")

                p.location.display_stores()

                while True:
                    sure = ninput('Which store would you like to enter? 0: CANCEL / 1: FIRST STORE / 2: SECOND STORE...')

                    if sure.isdigit():
                        if (int(sure) < 0) or (int(sure) > len(p.location.stores)):
                            c_understand()
                            continue

                        elif sure == '0':
                            break

                        else:
                            p.location.stores[int(sure)-1].buy_item()
                            break

                    else:
                        c_understand()
                        continue

        else:
            c_understand()
            continue

        continue

    continue