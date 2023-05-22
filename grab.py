from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
prefs = {  # this list can be summarized as "I want to load the website w/o CSS or JS"
    "profile.default_content_setting_values": {
        "cookies": 2,
        "plugins": 2,
        "popups": 2,
        "geolocation": 2,
        "notifications": 2,
        "auto_select_certificate": 2,
        "fullscreen": 2,
        "mouselock": 2,
        "mixed_script": 2,
        "media_stream": 2,
        "media_stream_mic": 2,
        "media_stream_camera": 2,
        "protocol_handlers": 2,
        "ppapi_broker": 2,
        "automatic_downloads": 2,
        "midi_sysex": 2,
        "push_messaging": 2,
        "ssl_cert_decisions": 2,
        "metro_switch_to_desktop": 2,
        "protected_media_identifier": 2,
        "app_banner": 2,
        "site_engagement": 2,
        "durable_storage": 2,
    }
}
options.add_experimental_option("prefs", prefs)
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
driver = webdriver.Chrome(options=options)

driver.get("https://escapefromtarkov.fandom.com/wiki/Quests")  # the link :)
driver.implicitly_wait(5)  # supposedly, waiting is handy, 5 seconds worked

driver.execute_script(  # gets rid of that annoying popup but this isn't exactly needed
    """
   var l = document.getElementsByClassName("notifications-placeholder")[0];
   l.parentNode.removeChild(l);
"""
)

hrefs = []
vendors = [
    "Prapor",
    "Therapist",
    "Skier",
    "Peacekeeper",
    "Mechanic",
    "Ragman",
    "Jaeger",
]
for v in vendors:
    classOfRow = (
        "wikitable " + v + "-content"
    )  # the class of the table at the time of writing

    elements = driver.find_elements(
        By.XPATH,
        "//table[@class='"
        + classOfRow
        + "']/tbody/tr/th[1]/b/a",  # looks a little dirty but this points directly to the links for the sub pages
    )
    for e in elements:
        hrefs.append(
            e.get_attribute("href")
        )  # I've always found Pythons lists neat, not as neat as Lua does it though
for page in hrefs:
    driver.get(page)
    data = driver.execute_script(
        """return document.getElementsByClassName('mw-parser-output')[0].outerHTML"""
    )  # point to the content and grab it

    with open(
        "b/" + page.split("/")[4] + ".html", "w", encoding="utf-8"
    ) as file:  # yes, I did name the folder 'b', grab the page name, append .html...
        file.write(data)  # then write the file

print("GOODBYE")  # wanted a nice message to tell me it was done
driver.close()
driver.quit()