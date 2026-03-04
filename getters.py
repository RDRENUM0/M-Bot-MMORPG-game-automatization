import time
import re
import math
import undetected_chromedriver as uc

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException

# ====================== KONFIGURACJA DRIVERÓW =======================

def get_options():
    return uc.ChromeOptions()

def get_driver(options):
    return uc.Chrome(options=options)

def get_wait(driver, timeout=20):
    return WebDriverWait(driver, timeout)

# ====================== INFORMACJE O GRACZU =========================

def get_current_location(wait: WebDriverWait) -> str | None:
    try:
        element = wait.until(EC.presence_of_element_located((By.ID, "botloc")))
        return element.get_attribute("tip")
    except Exception as e:
        print(f"[Lokalizacja] Błąd: {e}")
        return None

def get_current_position(wait: WebDriverWait) -> tuple[int, int] | tuple[None, None]:
    """
    Zwraca pozycję (x, y) bohatera na podstawie zawartości elementu #botloc.
    Oczekuje na obecność przecinka (czyli pełną pozycję).
    """
    try:

        wait.until(EC.text_to_be_present_in_element((By.ID, "botloc"), ","))

        text = wait.until(EC.presence_of_element_located((By.ID, "botloc"))).text.strip()
        if not text:
            print("[Pozycja] Pusty tekst w #botloc.")
            return None, None

        parts = text.split(",")
        if len(parts) != 2:
            print(f"[Pozycja] Niepoprawny format: '{text}'")
            return None, None

        x, y = map(lambda s: int(s.strip()), parts)
        return x, y

    except ValueError:
        print("[Pozycja] Błąd: nie udało się przekonwertować pozycji na liczby całkowite.")
        return None, None
    except Exception as e:
        print(f"[Pozycja] Błąd ogólny: {e}")
        return None, None

def get_level(driver) -> int:
    el = driver.find_element(By.ID, "nick")
    text = el.text
    match = re.search(r"\((\d+)h\)", text)
    if match:
        return int(match.group(1))
    raise ValueError(f"Nie udało się znaleźć poziomu w tekście: {text}")

def get_profession(driver) -> str:
    el = driver.find_element(By.ID, "nick")
    tip = el.get_attribute("tip")
    match = re.search(r"Profesja:\s*(.*?)<br>", tip)
    if match:
        return match.group(1).strip()
    raise ValueError(f"Nie udało się znaleźć profesji w atrybucie tip: {tip}")

def get_current_health(wait: WebDriverWait) -> float | tuple[None, None]:
    try:
        element = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='life1'][@tip]")))
        content = element.get_attribute("tip")
        match = re.findall(r'\d+', content.replace(' ', ''))
        if len(match) == 2:
            return int(match[0]) / int(match[1]) * 100
        else:
            print(f"[Zdrowie] Błąd: nie znaleziono obu wartości w '{content}'")
            return None, None
    except Exception as e:
        print(f"[Zdrowie] Błąd: {e}")
        return None, None

# ====================== TORBY I EKWIPUNEK ==========================

def get_empty_bag_slots(wait: WebDriverWait) -> int | None:
    try:
        slots = sum(int(wait.until(EC.presence_of_element_located((By.ID, f"bs{i}"))).text.strip()) for i in range(3))
        return slots
    except ValueError:
        print("[Torby] Błąd: wartość nie jest liczbą.")
        return None
    except Exception as e:
        print(f"[Torby] Błąd: {e}")
        return None

# ====================== MAPA I OBIEKTY =============================

def extract_npc_name(tip_html):
    """Ekstrahuje nazwę NPC z atrybutu tip."""
    match = re.search(r"<b>(.*?)</b>", tip_html)
    return match.group(1).strip() if match else None

def get_all_npcs_on_map(wait) -> list[dict]:
    """
    Zwraca listę wszystkich NPC na mapie w formie słowników zawierających:
    - 'id': identyfikator elementu DOM
    - 'name': czysta nazwa z atrybutu 'tip'
    - 'position': współrzędne w siatce (x, y)
    """
    from selenium.webdriver.support import expected_conditions as EC

    npcs = []
    try:
        elements = wait.until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[starts-with(@id, 'npc')]"))
        )

        for el in elements:
            try:
                id_ = el.get_attribute("id")
                tip_raw = el.get_attribute("tip")
                name = extract_npc_name(tip_raw) if tip_raw else None
                x, y = get_element_position(el)

                if id_ and name is not None and x is not None and y is not None:
                    npcs.append({
                        'id': id_,
                        'name': name,
                        'position': (x // 32, y // 32)
                    })

            except Exception as inner_e:
                print(f"[get_all_npcs_on_map] Błąd dla pojedynczego NPC: {inner_e}")

    except Exception as e:
        print(f"[get_all_npcs_on_map] Błąd ogólny: {e}")

    return npcs

    
def generate_graph_entry_from_doors(wait, current_location: str) -> str:
    try:
        _, tips = get_all_doors_on_map(wait)
        tips = [tip.strip() for tip in tips if tip.strip()]
        if not tips:
            print(f"[Graf] Brak przejść dla lokalizacji: {current_location}")
            return ""
        
        neighbors_str = ", ".join(f'"{tip}"' for tip in tips)
        graph_line = f'"{current_location}": [{neighbors_str}],'

        return graph_line
    except Exception as e:
        print(f"[Graf] Błąd generowania grafu: {e}")
        return ""


def get_all_doors_on_map(wait) -> tuple[list[str], list[str]]:
    try:
        elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[starts-with(@id, 'gw')]")))
        ids, tips = [], []
        for el in elements:
            ids.append(el.get_attribute("id"))
            tips.append(el.get_attribute("tip") or "")
        return ids, tips
    except Exception as e:
        print(f"[Drzwi] Błąd: {e}")
        return [], []

def get_element_position(element) -> tuple[int, int]:
    style = element.get_attribute("style")
    x = int(re.search(r"left:\s*(\d+)px", style).group(1)) if "left" in style else 0
    y = int(re.search(r"top:\s*(\d+)px", style).group(1)) if "top" in style else 0
    return x, y

# ====================== MOBY I ANALIZA POZYCJI =====================

def get_mob_locations(driver, mob_names: list[str], wait: WebDriverWait):

    mob_data = []
    if not mob_names:
        print("[Moby] Lista mobów jest pusta.")
        return {}, [], []

    mob_names_lower = [mob.lower() for mob in mob_names]
    print(f"[Moby] Szukam: {', '.join(mob_names)}")
    
    npc_elements = driver.find_elements(By.CLASS_NAME, "npc")
    hero_x, hero_y = get_current_position(wait)

    for el in npc_elements:
        for _ in range(5):
            try:
                tip_html = el.get_attribute("tip")
                if not tip_html:
                    break
                match = re.search(r"<b>(.*?)</b>", tip_html)
                if match:
                    name = match.group(1).strip()
                    if name.lower() in mob_names_lower:
                        px, py = get_element_position(el)
                        mob_x, mob_y = round(px / 32), round(py / 32)
                        npc_id = el.get_attribute("id")
                        mob_data.append(((mob_x, mob_y), npc_id))
                break
            except StaleElementReferenceException:
                time.sleep(0.1)
                continue
            except Exception as e:
                print(f"[Moby] Inny błąd przy pobieraniu tip: {e}")
                break

    if not mob_data:
        print("[Moby] Nie znaleziono.")
    else:
        print(f"[Moby] Znaleziono: {len(mob_data)}")

    mob_data.sort(key=lambda item: abs((item[0][0] - hero_x)) + abs((item[0][1] - hero_y)))

    mob_dict = {coords: npc_id for coords, npc_id in mob_data}
    mob_x = [coords[0] for coords, _ in mob_data]
    mob_y = [coords[1] for coords, _ in mob_data]

    return mob_dict, mob_x, mob_y


def get_closest_mob(mob_dict, hero_x, hero_y, collisions):
    if not mob_dict:
        return None

    closest = None
    min_distance = float('inf')

    for (mob_x, mob_y), mob_id in mob_dict.items():
        if collisions and is_path_blocked(hero_x, hero_y, mob_x, mob_y, collisions):
            continue

        distance = abs(hero_x - mob_x) + abs(hero_y - mob_y)
        if distance < min_distance:
            min_distance = distance
            closest = ((mob_x, mob_y), mob_id)

    return closest

def is_path_blocked(hero_x, hero_y, mob_x, mob_y, collisions):

    if not collisions:
        return False

    if hero_x == mob_x:
        for y in range(min(hero_y, mob_y) + 1, max(hero_y, mob_y)):
            if (hero_x, y) in collisions:
                return True
    elif hero_y == mob_y:
        for x in range(min(hero_x, mob_x) + 1, max(hero_x, mob_x)):
            if (x, hero_y) in collisions:
                return True
    return False


def get_collisions(driver):
    collisions = []
    try:
        elements = driver.find_elements(By.CLASS_NAME, "blokady")
        for el in elements:
            style = el.get_attribute("style")
            top_match = re.search(r"top:\s*(\d+)px", style)
            left_match = re.search(r"left:\s*(\d+)px", style)
            if top_match and left_match:
                top = int(top_match.group(1))
                left = int(left_match.group(1))
                y = top // 32
                x = left // 32
                collisions.append((x, y))
    except Exception as e:
        print(f"Błąd podczas zbierania kolizji: {e}")
    return collisions

def get_npc_position(wait, npc_name):
    """
    Zwraca pozycję (x, y) pierwszego NPC o podanej nazwie (z tip).
    """
    try:

        elements = wait._driver.find_elements(By.CLASS_NAME, "npc")

        for element in elements:
            try:
                tip_html = element.get_attribute("tip")
                if not tip_html:
                    continue

                match = re.search(r"<b>(.*?)</b>", tip_html)
                if not match:
                    continue

                name = match.group(1).strip()
                if name.lower() == npc_name.strip().lower():
                    x, y = get_element_position(element)
                    if x is not None and y is not None:
                        return x // 32, y // 32
                    else:
                        print(f"[get_npc_position] Nie udało się pobrać pozycji elementu dla '{name}'")
                        return None, None

            except StaleElementReferenceException:
                continue

        print(f"[get_npc_position] Nie znaleziono NPC o nazwie '{npc_name}'")
        return None, None

    except Exception as e:
        print(f"[get_npc_position] Błąd ogólny: {e}")
        return None, None