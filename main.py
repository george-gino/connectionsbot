from driver_setup import setup_driver
from puzzle_interaction import access_puzzle_page, click_play_button, extract_words
from word_analysis import solve_connections, debug_similarity

def main():
    driver = setup_driver()
    try:
        access_puzzle_page(driver)
        click_play_button(driver)
        words = extract_words(driver)
        print(f"Found words: {words}")

        debug_similarity(words)
        
        groups = solve_connections(words)
        print(f"Solved groups: {groups}")
    
    finally:
        driver.quit()

if __name__ == "__main__":
    main()


