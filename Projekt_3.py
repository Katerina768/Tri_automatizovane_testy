from playwright.sync_api import sync_playwright
import pytest
from playwright.sync_api import Page


# Test 1: Ověření title stránky IKEA

def test_title_ikea(page: Page): 
    # Přechod na stránku https://www.ikea.com/cz/cs/
    page.goto("https://www.ikea.com/cz/cs/")

    # Získání obsahu <title> z hlavičky stránky
    title = page.title()

    # Ověření, že title odpovídá očekávanému textu
    # Pokud title nesouhlasí, test selže
    assert title == "Nábytek se švédskou tradicí pro každou domácnost - IKEA"


# Test 2: Odkliknutí cookies banneru

def test_cookies_ikea(page: Page):
    # Přechod na hlavní stránku IKEA
    page.goto("https://www.ikea.com/cz/cs/")
    
     # Najde tlačítko "Přijmout vše" 
    button = page.locator("#onetrust-accept-btn-handler")

    # Kliknutí na tlačítko, čímž se zavře cookies banner
    button.click()
    
   # Najde samotný banner (čtverec|) podle ID
    cookies_square = page.locator("#onetrust-banner-sdk")

    # Počká až banner zmizí (state="hidden") s timeoutem 6 sekund
    cookies_square.wait_for(state="hidden", timeout=6000)

    # Ověří, že banner již není viditelný
    assert not cookies_square.is_visible()


# Test 3: Otevření odkazu v patičce a ověření nadpisu

def test_open_popup_and_check_title(page: Page):
    # Otevře hlavní stránku IKEA a počká na úplné načtení
    page.goto("https://www.ikea.com/cz/cs/", wait_until="load")

    # Zavře cookies banner, pokud je viditelný-řjn tfg
    accept = page.locator("#onetrust-accept-btn-handler")
    if accept.is_visible():
        accept.click()

    # Najde odkaz "Kontakt a pomoc" v patičce a klikne na něj
    services_link = page.locator('footer a', has_text="Kontakt a pomoc")
    services_link.click()

    # Počká na načtení nové stránky
    page.wait_for_load_state("load")

    # Získá nadpis stránky přes evaluate
    heading = page.evaluate("() => document.querySelector('h1').innerText")
    
    # Ověří, že nadpis obsahuje "Kontakt a pomoc"
    assert "Kontakt a pomoc" in heading
