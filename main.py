import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import getters
import functions
from map import map_graph, cities
import keyboard
import exp
import navigation
import presets
import time
import map
import npc

#------------------------------------DEKLARACJE----------------------------------------------------------------#

options = getters.get_options()

options.add_argument(r"--user-data-dir=C:\Users\Kacper\AppData\Local\Google\Chrome\User Data\Default")
options.add_argument(r"--profile-directory=Profile 1")

options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--start-maximized")
options.add_argument("--disable-extensions")
options.add_argument("--disable-infobars")

options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36")

driver = getters.get_driver(options)
wait = getters.get_wait(driver)

driver.get("https://www.margonem.pl")

#------------------------------------CO ROBI BOT----------------------------------------------------------------#

#------Otwarcie Strony

functions.open_game(driver)

functions.login_to_game(driver, wait)

#---------------

time.sleep(1)

###driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)

#mob_names = ["Brązowa mrówka tragarz", "Brązowa mrówka robotnica", "Brązowa mrówka żołnierz"]

#functions.find_and_interact_with_npcs(driver, mob_names)


#----------------- FUNKCJONOWANIE BOTA --------------------------

#presets.tp(driver, wait, 5)

exp_locations = [
    "Mrowisko",
    "Mrowisko p.1",
    "Mrowisko p.2",
    "Kopiec Mrówek p.2",
    "Kopiec Mrówek p.1",
    "Kopiec Mrówek"
]

#mob_names = ["Brązowa mrówka tragarz", "Brązowa mrówka robotnica", "Brązowa mrówka żołnierz"]
"""
lvl = getters.get_level(driver)
prof = getters.get_profession(driver)


print(lvl)
print(prof)

def print_doors():
    current_location = getters.get_current_location(wait)
    tips = getters.generate_graph_entry_from_doors(wait, current_location)
    print(tips)

print("Wciśnij 'o', aby wyświetlić dostępne przejścia...")

while True:
    if keyboard.is_pressed('o'):
        
        print_doors()

        time.sleep(2)

"""

###presets.sell_items_to_roan(driver, wait)
###presets.tp(driver, wait, 1)

#-------------------------------------------------------------------------------


if 1 == 0:
    for i in range(500000):


        time.sleep(1)

        functions.div_click('npc230430', wait, driver)

        time.sleep(2)

        functions.right_click_mob('npc230430', wait, driver)

for i in range(20):
    functions.all_data_getter_info(wait)
    time.sleep(1)




input("Naciśnij Enter, aby zamknąć...")
driver.quit()

