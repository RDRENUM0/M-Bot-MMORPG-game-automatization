import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import npc
import getters
import functions
import map
from map import map_graph, cities
import navigation
import re
import time


def tp(driver, wait, where_tp):
    last_hero_x, last_hero_y = 0, 0
    npc_tip = "Zakonnik Planu Astralnego"
    

    tp_locations = {
        1: "Ithan",
        3: "Torneg",
        5: "Werbin",
        7: "Karka-han",
        9: "Eder",
        12: "Nithal",
        15: "Trupia Przełęcz",
        18: "Thuzal",
        22: "Liściaste Rozstaje"
    }
    
    current_hero_location = getters.get_current_location(wait)
    target_city = tp_locations.get(where_tp, "Unknown")

    if current_hero_location in cities:
        if current_hero_location == target_city:
            print(f"[TP] Już jesteśmy w docelowym mieście: {target_city}")
            return True
        else:
            try:
                xpath = f"//div[starts-with(@id, 'npc') and contains(@tip, '{npc_tip}')]"
                npc_element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))

                npc_x, npc_y = getters.get_npc_position(wait, npc_tip)
                if npc_x is None or npc_y is None:
                    print(f"[TP] Nie udało się uzyskać pozycji NPC '{npc_tip}'")
                    return False

                driver.execute_script("arguments[0].scrollIntoView(true);", npc_element)
                time.sleep(0.5)

                ActionChains(driver).move_to_element(npc_element).click().perform()
                print(f"[TP] Kliknięto NPC '{npc_tip}', czekam aż bohater podejdzie...")

                while True:
                    hero_x, hero_y = getters.get_current_position(wait)

                    if hero_x is None or hero_y is None:
                        print("[TP] Nie udało się uzyskać pozycji bohatera")
                        return False

                    if abs(npc_x - hero_x) <= 2 and abs(npc_y - hero_y) <= 1:
                        time.sleep(0.7)
                        print("[TP] Bohater blisko NPC, otwieram dialog...")
                        break

                    if functions.is_hero_moving(hero_x, hero_y, last_hero_x, last_hero_y):
                        time.sleep(0.5)
                    else:
                        ActionChains(driver).move_to_element(npc_element).click().perform()
                        time.sleep(0.5)

                    last_hero_x, last_hero_y = hero_x, hero_y

                ActionChains(driver).move_to_element(npc_element).click().perform()
                time.sleep(0.5)

                functions.click_dialog(wait, 1, driver)
                time.sleep(0.2)
                functions.click_dialog(wait, where_tp, driver)

                return True

            except Exception as e:
                print(f"[TP] Błąd przy klikaniu NPC '{npc_tip}': {str(e)}")
                return False
        
    else: 
        navigation.back_to_city(wait, driver)
        return tp(driver, wait, where_tp)


def sell_items_to_roan(driver, wait):
    """
    Sprzedaje przedmioty u NPC Roan w Ithan do skutku
    Procedura:
    1. Teleport do Ithan
    2. Znalezienie NPC Roan
    3. Otwarcie sklepu
    4. Sprzedaż przedmiotów z wszystkich toreb aż nie będzie więcej możliwości sprzedaży
    5. Zamknięcie sklepu
    """
    print("[SPRZEDAŻ] Rozpoczynam sprzedaż przedmiotów u Roana w Ithan")
    
    if not tp(driver, wait, 1):
        print("[SPRZEDAŻ] Błąd teleportu do Ithan")
        return False
    
    npc_name = "Sprzedawca Roan"
    try:
        print(f"[SPRZEDAŻ] Szukam NPC {npc_name}")
        xpath = f"//div[starts-with(@id, 'npc') and contains(@tip, '{npc_name}')]"
        npc_element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        
        npc_x, npc_y = getters.get_npc_position(wait, npc_name)
        if npc_x is None or npc_y is None:
            print(f"[SPRZEDAŻ] Nie udało się uzyskać pozycji NPC {npc_name}")
            return False
            
        print(f"[SPRZEDAŻ] Podchodzę do NPC {npc_name}")
        functions.div_click(npc_element.get_attribute("id"), wait, driver)
        
        for _ in range(10):
            hero_x, hero_y = getters.get_current_position(wait)
            if abs(npc_x - hero_x) <= 2 and abs(npc_y - hero_y) <= 1:
                break
            time.sleep(0.5)
        
        print("[SPRZEDAŻ] Otwieram sklep")
        functions.div_click(npc_element.get_attribute("id"), wait, driver)
        if not functions.click_dialog(wait, 1, driver):
            print("[SPRZEDAŻ] Nie udało się otworzyć sklepu")
            return False
        time.sleep(0.5)

    except Exception as e:
        print(f"[SPRZEDAŻ] Błąd podczas interakcji z NPC: {str(e)}")
        return False
    
    try:
        print("[SPRZEDAŻ] Rozpoczynam sprzedaż przedmiotów")
        
        previous_empty_slots = -1
        current_empty_slots = getters.get_empty_bag_slots(wait)
        max_attempts = 10
        attempts = 0
        
        while attempts < max_attempts:
            if current_empty_slots is None:
                print("[SPRZEDAŻ] Nie udało się sprawdzić ilości przedmiotów")
                break
                
            print(f"[SPRZEDAŻ] Próba sprzedaży {attempts + 1}/{max_attempts}")
            print(f"[SPRZEDAŻ] Wolne miejsca przed sprzedażą: {current_empty_slots}")
            
            previous_empty_slots = current_empty_slots
            
            for bag_num in [1, 2, 3]:
                try:
                    bag_element = wait.until(EC.element_to_be_clickable((By.ID, f"torba{bag_num}")))
                    ActionChains(driver).move_to_element(bag_element).click().perform()
                    print(f"[SPRZEDAŻ] Kliknięto torbę {bag_num}")
                    time.sleep(0.2)
                except Exception as e:
                    print(f"[SPRZEDAŻ] Błąd przy klikaniu torby {bag_num}: {str(e)}")
                    continue
            
            try:
                accept_button = wait.until(EC.element_to_be_clickable((By.ID, "shop_accept")))
                ActionChains(driver).move_to_element(accept_button).click().perform()
                print("[SPRZEDAŻ] Kliknięto przycisk akceptacji")
                time.sleep(0.5)
            except Exception as e:
                print(f"[SPRZEDAŻ] Błąd przy akceptacji sprzedaży: {str(e)}")
                break
            
            current_empty_slots = getters.get_empty_bag_slots(wait)
            
            if current_empty_slots == previous_empty_slots:
                print("[SPRZEDAŻ] Brak zmian w liczbie wolnych miejsc - kończę sprzedaż")
                break
                
            attempts += 1
        
        try:
            close_button = wait.until(EC.element_to_be_clickable((By.ID, "shop_close")))
            ActionChains(driver).move_to_element(close_button).click().perform()
            print("[SPRZEDAŻ] Zamknięto sklep")
            time.sleep(1)
        except Exception as e:
            print(f"[SPRZEDAŻ] Błąd przy zamykaniu sklepu: {str(e)}")

            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)
        
        return True
        
    except Exception as e:
        print(f"[SPRZEDAŻ] Krytyczny błąd podczas sprzedaży: {str(e)}")

        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)
        return False