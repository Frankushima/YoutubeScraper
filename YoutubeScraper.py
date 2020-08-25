from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import pickle
import youtube_dl as ydl
import PySimpleGUI as sg

#TO DO:
# Make GUI
# Allow users to enter a playlist link or a list of song names to download
# Allow users to add their own tags to songs when searched (3D Audio, Offical, Audio only)
# Progress Bar

# Chrome WebDriver code
# Make it headless later

#Pickle this
folderPath = ''

try:
    pickle_in = open("path.pickle", "rb")
    userDict = pickle.load(pickle_in)

except FileNotFoundError:
    folderPath = 'downloads'

# folderPath = 'C:/Users/Frank/Downloads'
# folderPath = '/Users/frankYao/Downloads'

youtubeOptions = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'outtmpl': folderPath + '/%(title)s.%(ext)s',
}

def updateOptions(newPath):
    global youtubeOptions
    youtubeOptions = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': newPath + '/%(title)s.%(ext)s',
    }

def downloadSong(songTitle, tag):
    options = Options()
    options.binary_location = 'chromedriver.exe'
    options.headless = True

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

    ydl.YoutubeDL(youtubeOptions).download([str(songURL)])

def pickleVals():
    pickle_out = open("path.pickle", "wb")
    pickle.dump(folderPath, pickle_out)
    pickle_out.close()

# GUI

sg.theme('DarkAmber')    # Keep things interesting for your users

layout = [[sg.Input(key = '-FILE-',visible= False, enable_events= True ),sg.FolderBrowse(button_text='Browse Download Folder',button_color=('white', 'green'),font =("Times New Roman", 24))],
          [sg.Input(key='-IN-', do_not_clear= False, font =("Times New Roman", 24))],
          [sg.Text(text= 'Songs: ',font =("Times New Roman", 18)),sg.Text(size=(50,5),key= '-INPUTS-',font =("Times New Roman", 18))],
          [sg.Submit(button_text= 'Add Song', font =("Times New Roman", 24)),sg.Button(button_text= 'Download', button_color= ('white' ,'green'),font =("Times New Roman", 24)), sg.Exit(button_color= ('white', 'red'),font =("Times New Roman", 24))]]

window = sg.Window('Youtube Scraper', layout, resizable= True)

GUIInput = ''

while True:                         # The Event Loop
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        pickleVals()
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
        updateOptions(folderPath)

window.close()


# Parse into list of Strings

songList = GUIInput.split(',')

tag = 'audio'

for songTitle in songList:
    downloadSong(songTitle,tag)

pickleVals()