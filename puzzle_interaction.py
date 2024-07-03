from selenium.webdriver.common.by import By
import time

def access_puzzle_page(driver):
    driver.get('https://www.nytimes.com/games/connections')
    time.sleep(5)  # Wait for the page to load

def click_play_button(driver):
    try:
        play_button = driver.find_element(By.XPATH, '//button[contains(text(), "Play")]')
        play_button.click()
        time.sleep(5)  # Wait for the words to load
    except Exception as e:
        print(f"An error occurred while clicking the play button: {e}")

def extract_words(driver):
    try:
        labels = driver.find_elements(By.XPATH, '//label[contains(@class, "Card-module_label")]')
        if not labels:
            print("No labels found.")
            print(driver.page_source)  # Print the page source for debugging
            raise ValueError("No labels found")
        
        words = [label.text for label in labels]
        if not words:
            print("Labels found but no text extracted.")
            raise ValueError("No words found")
        
        print(f"Found words: {words}")
        return words
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

