from playwright.sync_api import sync_playwright
import time
import pyautogui

def join_teams_meeting(meeting_url, duration):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)

        # Allow mic and camera by default
        context = browser.new_context(
            permissions=["microphone", "camera"]
        )

        page = context.new_page()
        print(" Opening Teams meeting link...")
        page.goto(meeting_url)
        page.wait_for_timeout(3000)

        # Step 0: Handle potential browser alert/pop-up using pyautogui
        time.sleep(3)  # wait for alert to appear
        print(" Looking for popup cancel button using pyautogui...")

        # Move to expected coordinates (adjust based on your screen)
        cancel_button_x, cancel_button_y = 1050, 300  #  change these as per your screen
        pyautogui.moveTo(cancel_button_x, cancel_button_y, duration=1)
        pyautogui.click()
        print(" Clicked Cancel on popup (via pyautogui)")

        # Step 1: Click "Continue on this browser"
        try:
            page.click("text='Continue on this browser'", timeout=10000)
            print(" Clicked 'Continue on this browser'")
        except Exception as e:
            print(" Could not find 'Continue on this browser':", e)

        page.wait_for_timeout(8000)

        # Step 2: Enter name in input
        try:
            page.fill("input[data-tid='prejoin-display-name-input']", "Shashank")
            print("] Entered name.")
        except Exception as e:
            print(" Failed to enter name:", e)

        time.sleep(4)

        # Step 3: Click Join now
        try:
            page.click("button:has-text('Join now')")
            print(" Joined the meeting.")
        except Exception as e:
            print(" Failed to click 'Join now':", e)

        print(f" Staying in meeting for {duration // 60} minutes...")
        time.sleep(duration)

        browser.close()

if __name__ == "__main__":
    url = input("Paste full Teams meeting URL: ").strip()
    duration = int(input("Enter meeting duration (in minutes): ")) * 60
    join_teams_meeting(url, duration)
