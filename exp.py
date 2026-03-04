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
import navigation
import presets
import time
import map
import npc


exp_areas = {
    "Mrówki": {
        "locations": [

            "Mrowisko", "Mrowisko p.1", "Mrowisko p.2",
            "Kopiec Mrówek", "Kopiec Mrówek p.1", "Kopiec Mrówek p.2"

        ],

        "mob_names": [
            "Brązowa mrówka tragarz",
            "Brązowa mrówka robotnica",
            "Brązowa mrówka żołnierz"
        ],

        "level_range": (19, 22)
    },
    "Niedźwiedzie, Nietoperze": {
        "locations": [
            
            "Dziewicza Knieja",           
            "Siedlisko Nietoperzy p.1",
            "Siedlisko Nietoperzy p.2",
            "Siedlisko Nietoperzy p.3 - sala 1",
            "Siedlisko Nietoperzy p.3 - sala 2",
            "Siedlisko Nietoperzy p.4",
            "Siedlisko Nietoperzy p.5"],

        "mob_names": [
            "Niedźwiedź szary",
            "Niedźwiedź czarny",
            "Niedźwiedź brunatny",
            "Gacek Szary"
        ],
        "level_range": (23, 26)
    },
    "Demony": {

        "locations": [
 
            "Przeklęta Strażnica",
            "Przeklęta Strażnica p.1",
            "Przeklęta Strażnica p.2",
            "Przeklęta Strażnica - podziemia p.1 s.2",
            "Przeklęta Strażnica - podziemia p.2 s.2",
            
        ],

        "mob_names": [

            "Mały demon",
            "Nieznośny demon",
            "Pomniejszy demon",
            "Paskudny demon",
            "Dokuczliwy bies",
            "Kąśliwy demon"
        ],

        "level_range": (27, 30)
    },
}

def match_expo(lvl: int) -> dict | None:
    for name, data in exp_areas.items():
        min_lvl, max_lvl = data["level_range"]
        if min_lvl <= lvl <= max_lvl:
            return {
                "name": name,
                "locations": data["locations"],
                "mob_names": data["mob_names"]
            }
    return None

def exp(driver, wait):

    lvl = getters.get_level(driver)


    expo = match_expo(lvl)
    if not expo:
        print(f"[EXP] Nie znaleziono expowiska dla poziomu {lvl}")
        return

    current_location = getters.get_current_location(driver) 

    if current_location in expo["locations"]:

        print(f"[EXP] Już jesteś w odpowiednim expowisku: {current_location}")

    else:

        target_location = expo["locations"][0]

        print(f"[EXP] Przemieszczam się do {target_location}...")

        navigation.go_to_location(wait, driver, target_location)

        print(f"[EXP] Dotarto do {target_location}")

    print(f"[EXP] Rozpoczynam ekspienie w: {expo['name']}")

    exp_mechanics(driver, wait, expo["mob_names"], expo["locations"])

def exp_mechanics(driver, wait, mob_names, locations):
    from getters import get_collisions
    import time
    import keyboard
    from selenium.webdriver.common.by import By
    from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException

    direction = 1
    index = 0
    last_attack_time = 0
    attack_cooldown = 2
    stuck_threshold = 3
    location_change_timeout = 15
    max_location_attempts = 2
    safe_distance = 3 

    while True:
        if keyboard.is_pressed("q"):
            print("[EXP] Przerwano ekspienie przez użytkownika (q).")
            return

        if not (0 <= index < len(locations)):
            direction *= -1
            index += direction
            continue

        current_exp_location = locations[index]
        print(f"[EXP] Przemieszczam się do lokalizacji: {current_exp_location}")
        
        location_changed = False
        for attempt in range(1, max_location_attempts + 1):
            start_time = time.time()
            navigation.go_to_location(wait, driver, current_exp_location)
            
            while time.time() - start_time < location_change_timeout:
                if keyboard.is_pressed("q"):
                    print("[EXP] Przerwano ekspienie przez użytkownika (q).")
                    return
                    
                current_location = getters.get_current_location(wait)
                if current_location == current_exp_location:
                    print(f"[EXP] Dotarto do: {current_exp_location}")
                    location_changed = True
                    break
                time.sleep(0.5)
            
            if location_changed:
                break
            else:
                print(f"[EXP] Nie udało się zmienić lokacji (próba {attempt}/{max_location_attempts})")
                if attempt < max_location_attempts:

                    direction *= -1
                    index += direction
                    current_exp_location = locations[index]
                    print(f"[EXP] Próbuję alternatywnej trasy do: {current_exp_location}")

        if not location_changed:
            print(f"[EXP] Krytyczny błąd: nie udało się dotrzeć do {current_exp_location}")
            print("[EXP] Wracam do najbliższego miasta...")
            navigation.back_to_city(wait, driver)
            continue

        while True:
            if keyboard.is_pressed("q"):
                print("[EXP] Przerwano ekspienie przez użytkownika (q).")
                return

            health = getters.get_current_health(wait)
            if health is not None and health < 30:
                print(f"[EXP] Niskie HP ({health}%), wracam do miasta!")
                navigation.back_to_city(wait, driver)
                break

            empty_slots = getters.get_empty_bag_slots(wait)
            if empty_slots is not None and empty_slots <= 1:
                print(f"[EXP] Mało miejsca w torbach ({empty_slots}), wracam do miasta!")
                navigation.back_to_city(wait, driver)
                break

            collisions = get_collisions(driver)
            hero_x, hero_y = getters.get_current_position(wait)
            
            mob_dict = {}
            for _ in range(3):
                if keyboard.is_pressed("q"):
                    print("[EXP] Przerwano ekspienie przez użytkownika (q).")
                    return
                    
                result = getters.get_mob_locations(driver, mob_names, wait)
                if result and len(result) == 3 and result[0]:
                    mob_dict, _, _ = result
                    break
                time.sleep(0.5)

            if not mob_dict:
                print(f"[EXP] Brak mobów w {current_exp_location}, zmiana lokacji.")
                break

            closest = getters.get_closest_mob(mob_dict, hero_x, hero_y, collisions=collisions)
            if not closest:
                print("[EXP] Nie znaleziono dostępnych mobów — możliwe kolizje.")
                break

            mob_coords, mob_id = closest
            mob_x, mob_y = mob_coords

            current_time = time.time()
            if current_time - last_attack_time < attack_cooldown:
                time.sleep(attack_cooldown - (current_time - last_attack_time))
                continue

            try:

                try:
                    mob_element = wait.until(EC.presence_of_element_located((By.ID, mob_id)))
                except (StaleElementReferenceException, NoSuchElementException):
                    print(f"[EXP] Mob {mob_id} zniknął, szukam nowego")
                    continue


                functions.div_click(mob_id, wait, driver)
                last_attack_time = time.time()


                stuck_counter = 0
                last_hero_pos = (hero_x, hero_y)
                attack_success = False
                
                for _ in range(20):
                    if keyboard.is_pressed("q"):
                        print("[EXP] Przerwano ekspienie przez użytkownika (q).")
                        return

                    current_hero_x, current_hero_y = getters.get_current_position(wait)
                    
                    if (abs(mob_x - current_hero_x) <= safe_distance and 
                        abs(mob_y - current_hero_y) <= 1 and 
                        current_hero_y != mob_y + 1):
                        
                        try:

                            mob_element = driver.find_element(By.ID, mob_id)
                            functions.right_click_mob(driver, mob_element)
                            print(f"[EXP] Zaatakowano moba {mob_id} na pozycji {mob_coords}")
                            attack_success = True
                            break
                        except StaleElementReferenceException:
                            print("[EXP] Mob zniknął przed atakiem")
                            break
                        except Exception as e:
                            print(f"[EXP] Błąd podczas ataku prawym przyciskiem: {e}")

                            try:
                                ActionChains(driver).move_to_element(mob_element).click().perform()
                                print("[EXP] Użyto lewego przycisku jako awaryjnego")
                                attack_success = True
                                break
                            except:
                                print("[EXP] Błąd również przy lewym przycisku")
                                break

                    if (current_hero_x == last_hero_pos[0] and 
                        current_hero_y == last_hero_pos[1]):
                        stuck_counter += 1
                        if stuck_counter > stuck_threshold:
                            print("[EXP] Bohater się nie rusza — pomijam moba.")
                            break

                        try:
                            functions.div_click(mob_id, wait, driver)
                        except:
                            print("[EXP] Błąd przy ponownym kliknięciu moba")
                            break
                    else:
                        stuck_counter = 0
                    
                    last_hero_pos = (current_hero_x, current_hero_y)
                    time.sleep(0.3)

                if not attack_success:
                    continue

                time.sleep(0.5)

            except Exception as e:
                print(f"[EXP] Krytyczny błąd podczas ataku: {e}")
                print("[EXP] Próbuję odzyskać kontrolę...")
                time.sleep(2)

                try:
                    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)
                except:
                    pass
                continue

        index += direction