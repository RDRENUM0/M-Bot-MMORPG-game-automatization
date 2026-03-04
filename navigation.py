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
import presets
import time
import map
import npc

def back_to_city(wait, driver):
    current_location = getters.get_current_location(wait)

    path = map.find_closest_city(current_location, map_graph, cities)

    for location in path:
        functions.go_to_door_tip(location, wait, driver)

def go_to_location(wait, driver, destination):
    current_location = getters.get_current_location(wait)

    path = map.find_path(current_location, map_graph, cities, destination)

    for location in path:
        functions.go_to_door_tip(location, wait, driver)