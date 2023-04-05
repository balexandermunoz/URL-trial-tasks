from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import random
import time

links = [
    "https://graceful-sunburst-78f35d.netlify.app/www.classcentral.com/index.html",
    "https://ammardab3an99.github.io/",
    "https://heartfelt-lollipop-736861.netlify.app/",
    "https://radiant-hummingbird-697a83.netlify.app/",
    "http://trialserver.rf.gd/trial6/www.classcentral.com/index.html",
    "https://class-central.vercel.app/www.classcentral.com/index.html",
    "https://5dcookie.github.io/",
    "https://www.census2011.co.in/city.php#:~:text=Here%20are%20the%20details%20of,%2D%203%2C124%2C458%2C%20Jaipur%20%2D%203%2C046%2C163",
    "https://umair1814.github.io/",
    "na.co",
    "https://www.httrack.com/",
    "https://www.classcentral.com/",
    "https://sinistersup.github.io/classcentral-hindi/",
    "https://omarkhalifa97.github.io/khalifaaaz.github.io/",
    "https://df0a.github.io/",
    "http://miguel-hindi-classcentral.s3-website-us-east-1.amazonaws.com/",
    "https://classcentral-scrape-hindi.vercel.app/",
    "https://testclass01.000webhostapp.com/www.classcentral.com/index.html",
    "https://mike-brown5.github.io/AllStars-Scrapped-Site/",
    "https://ubadeakkad.github.io/",
    "https://www.dqlab.id/",
    "https://drive.google.com/drive/folders/1eLU2AQ80bn89gYNC2HEIbrKswVzdj0qC?usp=sharing",
    "https://www.mediafire.com/folder/ktcts50c9o1up/Class_Central_-Website_translation",
    "https://www.facebook.com/",
    "http://daniel1uno.byethost31.com/",
    "http://mihir.testing-phase.com/",
    "http://grsmuche.vh109.hosterby.com/",
    "https://a58-mohiuddin.github.io/developer_trial_task/web_translate.html",
    "https://datta07.github.io/classcentralclone/",
    "https://venerable-froyo-7f3b1e.netlify.app/university/cornell.html",
    "https://muhammederenaslan.github.io/codingallstars/",
    "https://exosmotic-bay.000webhostapp.com/",
    "https://interviewdeneme123.000webhostapp.com/",
    "http://classcent.infinityfreeapp.com/",
    "https://codingallstarttest0000.on.drv.tw/www.teeest.blog/",
    ]

correct_url = "https://www.classcentral.com/"

def set_driver():
    options = Options()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
        )
    return driver
    
def check_webpage(url):
    driver = set_driver()
    driver.get(url)
    driver.maximize_window()
    
    # check if is the correct webpage:
    if not check_is_correct_webpage(driver):
        driver.close()
        return "FAIL"
        
    # Check if all text is in hindi:
    if not check_text_hindi(driver):
        driver.close()
        return "FAIL"
    
    if not check_resolution_images(driver):
        driver.close()
        return "FAIL"
    
    if not check_translate_inner_pages(url, driver):
        driver.close()
        return "FAIL"
    
    # Check the plegable menus
    if not check_plegable_menus(driver):
        driver.close()
        return "FAIL"
    
    # If pass all tests:
    driver.close()
    return "PASS"
    
    
def check_is_correct_webpage(driver):
    classcentral_logos = driver.find_elements(
        "xpath",
        "//nav[contains(@class,'cmpt-nav')]//i[contains(@class, 'symbol-classcentral-navy')]"
        )

    # Check if has the classcentral logo: 
    if not classcentral_logos:
        return False
    return True
   
    
def check_text_hindi(curr_driver):
    time.sleep(1)
    classcentral_text_elements = curr_driver.find_elements(
        "xpath",
        "//*[contains(text(), '')]"
        )
    time.sleep(1)
    webpage_text = [el.text for el in classcentral_text_elements[:200] 
                    if el.text.strip()]
    number_fails = 0
    for text in webpage_text[:100]:
        clean_text = ''.join(e for e in text 
                             if e.isalpha() and char_is_hindi(e))
        if number_fails > 4:
            return False
        if not clean_text:
            number_fails += 1
    return True
    
    
def char_is_hindi(character):
    if u'\u0900' <= character <= u'\u097f':
        return True
    else:
      return False
  
      
def check_plegable_menus(driver):
    # First dropdown menu: 
    dropdown_elements = driver.find_elements(
        "xpath",
        "//div[contains(@class,'margin-right-small large-up-margin-right-medium')]"
        )
    for dropdown_el in dropdown_elements:
        dropdown_el.click()
        nav_el_class = driver.find_elements(
            "xpath",
            "//nav[contains(@class,'main-nav-dropdown')]"
            )[0].get_attribute('class')
        if not 'is-open' in nav_el_class:
            return False
    return True


def check_translate_inner_pages(base_link, driver):
    base_link = base_link.split('.', 1)[0]
    anchor_elements = driver.find_elements("xpath", "//a")
    links = [anchor.get_attribute('href') for anchor in anchor_elements
             if base_link in anchor.get_attribute('href')]
    random_links = random.sample(links, 5)
    for link in random_links:
        link_driver = set_driver()
        link_driver.get(link)
        link_driver.maximize_window()
        if not check_text_hindi(link_driver):
            return False
        link_driver.close()
        time.sleep(1)
    return True
 
 
def check_resolution_images(driver):
    img_elements = driver.find_elements(
        "xpath",
        "//img[contains(@alt, 'Never stop learning.')]"
        )
    for image in img_elements:
        if image.size['width'] < 300 or image.size['height'] < 250:
            return False
    return True
 
 
for link in links[3:]:
    print(check_webpage(link))