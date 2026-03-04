import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import npc
import getters
from map import map_graph, cities
import re

import time

def open_game(driver):
    try:
    
        login_link = driver.find_element(By.XPATH, "//a[text()='Zaloguj się na Stronie Głównej']")
        login_link.click()
        time.sleep(2)

    except Exception as e:
        print(f"Nie udało się kliknąć linku: {e}")

def login_to_game(driver, wait):
    enter_game_button = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='c-btn enter-game' and text()='Wejdź do gry']")))

    driver.execute_script("arguments[0].click();", enter_game_button)

def div_click(id, wait, driver):
    try:
        div_element = wait.until(EC.presence_of_element_located((By.ID, id)))

        ActionChains(driver).move_to_element(div_element).click().perform()

        print(f"Kliknięto element '{id}' za pomocą ActionChains.")
        time.sleep(1.5)

    except Exception as e:
        print(f"Błąd podczas próby kliknięcia elementu '{id}' ActionChains: {e}")

def div_click_npc_tip(npc_tip, wait, driver):
    
    try:

        xpath = f"//div[starts-with(@id, 'npc') and contains(@tip, '{npc_tip}')]"
        
        npc_element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        
        driver.execute_script("arguments[0].scrollIntoView(true);", npc_element)
        time.sleep(0.5)
        
        ActionChains(driver).move_to_element(npc_element).click().perform()
        
        print(f"Kliknięto NPC o nazwie '{npc_tip}'")
        return True
        
    except Exception as e:
        print(f"Błąd podczas próby kliknięcia NPC '{npc_tip}': {str(e)}")
        return False

def div_click_tip(door_tip, wait, driver):

    try:

        xpath = f"//div[starts-with(@class, 'gw') and @tip='{door_tip}']"

        door_element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))

        ActionChains(driver).move_to_element(door_element).click().perform()

        print(f"Próba kliknięcia drzwi do '{door_tip}' za pomocą ActionChains.")


    except Exception as e:
        print(f"Błąd podczas próby kliknięcia drzwi do '{door_tip}': {e}")

def click_dialog(wait, dialog_number, driver):
    try:

        xpaths = [
            f"//li[contains(@onclick, '0.{dialog_number}')]",
            f"//li[contains(@onclick, '0.{dialog_number}')]"
        ]
        

        for xpath in xpaths:
            try:
                dialog_option = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
                driver.execute_script("arguments[0].scrollIntoView(true);", dialog_option)
                time.sleep(0.3)

                ActionChains(driver).move_to_element(dialog_option).click().perform()
                print(f"Kliknięto opcję dialogową nr {dialog_number}")
                return True
            except:
                continue
                
        print(f"Nie znaleziono opcji dialogowej nr {dialog_number}")
        return False
        
    except Exception as e:
        print(f"Błąd podczas klikania dialogu {dialog_number}: {str(e)}")
        return False

def all_data_getter_info(wait):

    x, y = getters.get_current_position(wait)
    location = getters.get_current_location(wait)
    health = getters.get_current_health(wait)
    empty_bag_slots = getters.get_empty_bag_slots(wait)

    door_ids, door_tips = getters.get_all_doors_on_map(wait)

    npc_ids, npc_tips = getters.get_all_npcs_on_map(wait)

    print(f"jesteś na pozycji {x}, {y} - w lokalizacji {location}, twój poziom hp to {health}%, wolnych miejsc w torbach: {empty_bag_slots}, dostępne przejścia to {door_tips}, ich dane to {door_ids}, dostępni na mapie npc to {npc_tips}, a ich id to {npc_ids}")

    return x, y, location, health, empty_bag_slots, door_ids, door_tips, npc_ids, npc_tips

def go_to_door_id(door_id, wait, driver):
    div_click(door_id, wait, driver)

def go_to_door_tip(door_tip, wait, driver):

    div_click_tip(door_tip, wait, driver)

    last_x = 0
    last_y = 0


    while True:

        location = getters.get_current_location(wait)



        if(location == door_tip):
            time.sleep(1)
            print(f"udalo sie przejsc do {door_tip}")
            break

        else:
            time.sleep(1)
            print("czekanko")

        x, y = getters.get_current_position(wait)

        

        if(last_x == x and last_y == y):
            go_to_door_tip(door_tip, wait, driver)
            print("Ostatnie pozycje są takie same, ponowienie przejścia")
        else:

            last_x, last_y = x, y
            continue
            

def right_click_mob(driver, mob):

    actions = ActionChains(driver)
    actions.context_click(mob).perform()



def is_hero_moving(hero_x, hero_y, last_hero_x, last_hero_y):
    
    return hero_x != last_hero_x or hero_y != last_hero_y

