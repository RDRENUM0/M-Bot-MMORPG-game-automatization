import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
"""
functions.go_to_door_tip("Dolina Rozbójników", wait, driver)

functions.go_to_door_tip("Mokradła", wait, driver)

functions.go_to_door_tip("Fort Eder", wait, driver)

functions.go_to_door_tip("Eder", wait, driver)
"""


"""

time.sleep(1)
functions.div_click_npc_tip( "Zakonnik Planu Astralnego", wait, driver)
time.sleep(1)
functions.click_dialog(wait, 1, driver)
functions.click_dialog(wait, 3, driver)
"""






"""
def print_doors():
    current_location = getters.get_current_location(wait)
    tips = getters.generate_graph_entry_from_doors(wait, current_location)
    print(tips)

print("Wciśnij 'o', aby wyświetlić dostępne przejścia...")

# Główna pętla
while True:
    if keyboard.is_pressed('o'):
        
        print_doors()
        # Dodaj małe opóźnienie, żeby nie spamowało po jednym wciśnięciu
        time.sleep(2)
"""