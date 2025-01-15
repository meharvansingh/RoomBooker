# For some reason GitHub hasn't updated my most recent changes even when I've pushed...
# The new changes completely changes how the program handles all the elements on the website

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up the WebDriver
driver = webdriver.Chrome()

try:
    # Open the booking page
    driver.get('https://cal.lib.uw.edu/spaces?lid=1450&gid=0&c=0')
    print("Webpage opened.")

    # Wait for the room names to be loaded
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'fc-cell-text'))
    )

    # Extract room names
    room_name_elements = driver.find_elements(By.CLASS_NAME, 'fc-cell-text')
    room_names = [elem.text.split(' ')[0] for elem in room_name_elements if 'Capacity' in elem.text]


    # Function to check room availability using JavaScript
    def check_availability_js():
        room_availability = {name: [] for name in room_names}

        # Loop through each room name to check for available slots
        for room_name in room_names:
            # Use JavaScript to get all elements with the 'fc-timeline-event' class for the specific room
            slot_elements = driver.execute_script(
                "return Array.from(document.querySelectorAll('.fc-timeline-event')).filter(e => e.getAttribute('title').includes(arguments[0]) && e.getAttribute('title').includes('Available'));",
                room_name
            )

            # Loop through the slot elements and store the availability in the dictionary
            for slot_element in slot_elements:
                title = slot_element.get_attribute('title').strip()
                room_availability[room_name].append(title)

        return room_availability


    # Check for availability on the current day
    availability = check_availability_js()

    # Output the availability data
    for room, slots in availability.items():
        if slots:
            available_count = len(slots)
            print(f'{room} has {available_count} available slots:')
            for slot in slots:
                print(f'  {slot}')
        else:
            print(f'{room} has no available slots.')

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # Uncomment the line below for debugging if you want to keep the browser open
    input("Press Enter to close the browser...")
    driver.quit()
