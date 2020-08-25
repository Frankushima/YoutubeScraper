from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from pytube import YouTube
import PySimpleGUI as sg

#TO DO:
# Make GUI
# Allow users to enter a playlist link or a list of song names to download
# Allow users to add their own tags to songs when searched (3D Audio, Offical, Audio only)
# Progress Bar

# Chrome WebDriver code
# Make it headless later

def downloadSong(songTitle, tag):
    options = Options()
    options.binary_location = 'chromedriver.exe'

    driver = webdriver.Chrome()
    driver.get('https://www.youtube.com')
    assert 'YouTube' in driver.title

    searchBar = driver.find_element_by_xpath("//div[@id='search-input']/input[@id='search']")
    searchBar.send_keys(songTitle,' ', tag , Keys.ENTER)

    actions = ActionChains(driver)
    title = driver.find_element_by_xpath("//a[@id='video-title']/yt-formatted-string[@class='style-scope ytd-video-renderer']")
    actions.click(title)
    actions.perform()

    # replace line 301 in pytube3 in extract.py
    # with: parse_qs(formats[i].get("cipher") or formats[i].get("signatureCipher")) for i, data in enumerate(formats)
    # otherwise this breaks
    songURL = driver.current_url.__str__()
    driver.close()

    yt = YouTube(songURL)
    global folderPath
    yt.streams.filter(only_audio= True, subtype= 'mp4')[0].download(folderPath)

# GUI

#Pickle this
folderPath = 'C:/Users/Frank/Downloads'
# folderPath = '/Users/frankYao/Downloads'

sg.theme('DarkAmber')    # Keep things interesting for your users

layout = [[sg.Input(key = '-FILE-',visible= False, enable_events= True),sg.FileBrowse(button_text='Browse Download Folder',button_color=('white', 'green'))],
          [sg.Input(key='-IN-', do_not_clear= False)],
          [sg.Text(text= 'Songs: '),sg.Text(key= '-INPUTS-')],
          [sg.Submit(button_text= 'Add Song'),sg.Button(button_text= 'Download', button_color= ('white' ,'green')), sg.Exit(button_color= ('white', 'red'))]]

window = sg.Window('Youtube Scraper', layout, resizable= True)

GUIInput = ''

while True:                         # The Event Loop
    event, values = window.read()
    print(event, values)
    if event == sg.WIN_CLOSED or event == 'Exit':
        raise SystemExit(0)
    elif event == 'Add Song':
        if GUIInput == '':
            GUIInput += values['-IN-']
        else:
            GUIInput += ', ' + values['-IN-']
        window['-INPUTS-'].update(GUIInput)
    elif event == 'Download':
        break
    elif event == '-FILE-':
        folderPath = values['-FILE-']

window.close()


# Parse into list of Strings

songList = GUIInput.split(',')

tag = 'audio'

for songTitle in songList:
    downloadSong(songTitle,tag)