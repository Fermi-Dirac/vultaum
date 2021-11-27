import pyautogui as pag
import pydirectinput as pdi
import time
from vultaum import locations as loc
from vultaum import setup_logger, imgroot, pathjoin

logger = setup_logger(__name__)

kin_path = r'..\imgs\builder\kinetic1.png'
laser_path = r'..\imgs\builder\laser1.png'
shields = r'..\imgs\builder\shields1.png'
armor = r'..\imgs\builder\armor1.png'

def press(key, wait=0.25, *args, **kwargs):
    if wait <= 0:
        return pdi.press(key, *args,**kwargs)
    else:
        pdi.press(key, *args, **kwargs)
        time.sleep(wait)

def console_command(cmd, close=True):
    press('`')
    pag.write(cmd)
    press('return')
    if close:
        press('`')

def click_img(imgpath, confidence=0.9, *args, **kwargs):
    return pdi.click(*pag.center(pag.locateOnScreen(imgpath, confidence=confidence)), *args, **kwargs)

def load_savegame(saveslot=0, wait=True):
    pdi.press('escape', interval=0.5)
    for _ in range(4):
        menu = pag.locateOnScreen(pathjoin(imgroot, 'mainmenu.png'), confidence=0.9)
        if menu is None:
            logger.debug("Menu not found! trying again")
            time.sleep(0.25)
            pdi.press('escape')
        else:
            break
    click_img(pathjoin(imgroot, 'loadgame.png'), interval=0.25)
    pdi.click(*loc.load_list[saveslot])
    time.sleep(0.25)
    pdi.click(*loc.load_selected)
    logger.debug("Re-Loading Save...")
    if wait:
        for _ in range(60):
            time.sleep(0.25)
            menu = pag.locateOnScreen(pathjoin(imgroot, 'paused.png'), confidence=0.9)
            if menu is None:
                logger.debug("Paused icon not found! Waiting...")
            else:
                logger.info("Game reloaded!")
                break


def repeat_save(saveslot=0, reps=10, output_dir=None):
    for repi in range(reps):
        load_savegame(saveslot)
        logger.debug(f"Now on rep {repi}")
        console_command('ai')
        pdi.press('space', interval=0.5)
        pdi.press('=', interval=0.5)
        pdi.press('=', interval=0.5)
        logger.info("Waiting for combat, 60sec timeout")
        for i in range(120):
            time.sleep(0.5)
            report = pag.locateOnScreen(pathjoin(imgroot, 'battle', 'combatreport.png'), confidence=0.9)
            if report is None:
                pass
            else:
                logger.debug("Found!")
                pdi.click(*pag.center(report))
                if output_dir is None:
                    pag.screenshot(fr'Combat report {repi:04d}.png', region=loc.combat_report)
                else:
                    pag.screenshot(pathjoin(output_dir, fr'Combat report {repi:04d}.png'), region=loc.combat_report)
                break

def design_corvette(name='default', loadout=None):
    if loadout is None:
        loadout = {'weapons': [kin_path, kin_path, kin_path],
                   'armor': [armor, armor, armor]}
    build_locations = {}
    delay = 0.1
    pdi.press('f9', interval=delay)
    pdi.click(*loc.new_design, interval=delay)
    click_img(r'builder\new_corvette.png', interval=0.5)
    pdi.click(*loc.vette_type, interval=delay)
    pdi.click(*pag.center(pag.locateOnScreen(r'..\imgs\builder\corvette_interceptor.png', confidence=0.9)),
              interval=0.5)
    all_small_weap = [pag.center(weap) for weap in
                      pag.locateAllOnScreen(r'..\imgs\builder\smallweap.png', confidence=0.9)]
    all_small_defense = [pag.center(util) for util in
                         pag.locateAllOnScreen(r'..\imgs\builder\smallarmor.png', confidence=0.9)]
    all_small_a = [pag.center(util) for util in pag.locateAllOnScreen(r'..\imgs\builder\util_a.png', confidence=0.9)]
    print(all_small_weap, all_small_defense, all_small_a)

    pdi.click(*all_small_weap[0])  # Show all weapons
    for weap_path in set(loadout['weapons']):
        build_locations[weap_path] = pag.center(pag.locateOnScreen(weap_path, confidence=0.9))
    # Build weapons
    for small, weap_path in zip(all_small_weap, loadout['weapons']):
        pdi.click(*build_locations[weap_path], interval=0.1)
        pdi.click(*small, interval=0.2)
    pdi.move(None, 100)
    time.sleep(1)
    pdi.rightClick(None, interval=1)
    pdi.click(*all_small_defense[0], interval=0.5)  # Show util armor
    for util_path in set(loadout['armor']):
        build_locations[util_path] = pag.center(pag.locateOnScreen(util_path, confidence=0.9))

    # Build armor
    for util, armor_path in zip(all_small_defense, loadout['armor']):
        pdi.click(*build_locations[armor_path], interval=0.1)
        pdi.click(*util, interval=0.1)
    pdi.move(None, 100)
    time.sleep(1)
    pdi.rightClick(None, interval=0.2)

    # Save it
    pdi.click(*pag.center(pag.locateOnScreen(r'..\imgs\builder\ship_rename.png', confidence=0.9)), interval=0.5)
    time.sleep(1)
    pdi.write(f'ship1', interval=0.1)
    pdi.click(*pag.center(pag.locateOnScreen(r'..\imgs\builder\save_design.png', confidence=0.9)), interval=0.5)

# print("Going to stellaris")
# time.sleep(1)
# pag.moveTo(500,500)
# pag.click()
# pdi.press('space')
# print("Escaping")
# pdi.press('esc')
# menu = pag.locateOnScreen(r'imgs\mainmenu.png', confidence=0.9)
# print(menu)
# if menu is None:
#     pag.press('esc')
# pag.click(pag.locateOnScreen(r'imgs\loadgame.png', confidence=0.9))
