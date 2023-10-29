import re
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.chrome.options import Options

# Create Chrome options with the incognito flag
chrome_options = Options()
# chrome_options.add_argument("--incognito")

# Initialize the Chrome WebDriver
chrome = webdriver.Chrome(options = chrome_options)

URL = 'https://in.i.mi.com/note/h5#/'
NOTES_PER_VIEW = 10
ELEMENTS_TO_SCROLL = 5

# headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 5.1.1; SM-G928X Build/LMY47X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.83 Mobile Safari/537.36'}
# req = requests.get(URL, headers=headers)

def collect_notes(start_index:int):
    elements = chrome.find_elements(by=By.CLASS_NAME,value='note-item-3E9te')
    print("🐍 File: mi-notes-export/index.py | Line: 33 | undefined ~ elements",elements, len(elements))
    for index in range(0, ELEMENTS_TO_SCROLL):
        print("🐍 File: mi-notes-export/index.py | Line: 26 | collect_notes ~ index",index)
        element = elements[index]
        element.click()
        sleep(7)
        note = chrome.find_element(by=By.ID, value="u1")
        with open(f'notes/note_{start_index+index}.txt', 'w') as file:
            file.write(note.text)
            print("Notes Added", f"note_{start_index+index}.txt")


def get_total_notes_count():
    note_count_element = chrome.find_element(by=By.CLASS_NAME, value="note-count-select-1nzNf")
    print("🐍 File: mi-notes-export/index.py | Line: 37 | get_total_notes_count ~ note_count_element",note_count_element)
    res = re.search(r'(\d+)', note_count_element.text)
    if res is None:
        return 0
    return int(res.group(1))

def scroll_given_elements(starting_element_index):
    parent_elem = chrome.find_element(by=By.CLASS_NAME, value="note-list-items-2ID3T")
    pixel = (starting_element_index+ELEMENTS_TO_SCROLL+3-1) * 93
    chrome.execute_script(f"arguments[0].scrollTop ={pixel};", parent_elem)
    print(f"scrolled {starting_element_index + 5} items")



# Open Chrome and visit the page
chrome.get(URL)
sleep(5)
input("Please log in manually, and press Enter when you're done...")
print("process resumed")
sleep(2)
# title_class_name= input("TitleClass name: " )
# print("🐍 File: mi-notes-export/index.py | Line: 29 | undefined ~ title_class_name",title_class_name)
try:
    # notes_class_name = input("NotesClass name: " ) # note-content-1u7XQ
    # print("🐍 File: mi-notes-export/index.py | Line: 31 | undefined ~ notes_class_name",notes_class_name)
    total_notes_count = get_total_notes_count()
    print("🐍 File: mi-notes-export/index.py | Line: 61 | undefined ~ total_notes_count",total_notes_count)
    if total_notes_count ==0:
        exit()
    # total_scroll_cycle = total_notes_count// NOTES_PER_VIEW

    for start_index in range(0,total_notes_count, ELEMENTS_TO_SCROLL):
        print("🐍 File: mi-notes-export/index.py | Line: 68 | undefined ~ start_index",start_index)
        try:
            collect_notes(start_index)
        except Exception as e:
          print('An exception occurred', e)
          input("wait")
          collect_notes(start_index)
        scroll_given_elements(start_index)



except Exception as e:
    print("🐍 File: mi-notes-export/index.py | Line: 41 | undefined ~ e",e)
    print('An exception occurred')

input("Enter to terminate")
# driver.execute_script("arguments[0].scrollIntoView(true);", liElement);
chrome.quit()
