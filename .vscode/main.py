import requests
from bs4 import BeautifulSoup
from csv import writer
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


#PATH = "C:\Program Files (x86)\chromedriver.exe"
#driver = webdriver.Chrome(PATH)     

#clears the file of any prior content
def clear_vasel_list():
    file = open("Vasel_list.txt", "w")
    file.close()

#pulls Tom Vasel's 2021 top 100 boardgames list and writes it to its own file
def get_vasel_top_list():
    i = 0
   
    for i in range (91):
        vasel_range_one = (i+10)
        vasel_range_two = (i+1)
        vasel_top_index = ('{}-{}'.format(vasel_range_one, vasel_range_two))
        vasel_url = ('https://www.dicetower.com/game-video/tom-vasels-top-100-games-all-time-2021-{}'.format(vasel_top_index))
        response1 = requests.get(vasel_url)
        src1 = response1.content
        soup1 = BeautifulSoup(src1, 'html.parser')
        links = soup1.find_all(class_='gt_title')
        for link in links:
            if "" in link.text:
                file = open("Vasel_list.txt", "a") 
                file.write(str(link.text))
                file.write('\n')
                file.close()
                #print(link.text)
                i += 10
                get_vasel_top_list


#get_vasel_top_list()
#clear_vasel_list()

#clears the file of any prior content
def clear_quinn_list():
    file = open("Quinn_list.txt", "w")
    file.close()

#pulls Quinn's 2021 top 139 boardgames list and writes it to its own file
def get_quinn_top_list():
    quinn_url = ('https://www.shutupandsitdown.com/videos/quinns-walks-you-through-his-game-collection/')
    response2 = requests.get(quinn_url)
    src2 = response2.content
    soup2 = BeautifulSoup(src2, 'html.parser')
    links = soup2.find_all('strong')
    for link in links:
        if "" in link.text:
            file = open("Quinn_list.txt", "a") 
            file.write(str(link.text))
            file.write('\n')
            file.close()
            #print(link.text)

#get_quinn_top_list()
#clear_quinn_list()

#merges items in common from input files into seperate file 
def merge_top_lists(source_file1, source_file2, merged_file):
    with open(source_file1, 'r') as file1:
        with open(source_file2, 'r') as file2:
            same = set(file1).intersection(file2)
            same.discard('the')
            #same.discard('\n')

    with open(merged_file, 'w') as file_out:
        for line in same:
            file_out.write(line)

#merge_top_lists('Vasel_list.txt', 'Quinn_list.txt', 'Vasel_Quinn_list.txt')

def genre_search(text_file):
    
    #file = open(text_file, "r")
    #line = file.readline()
    #while line = True:
        #body = {'q':line}
        #con = requests.get('https://boardgamegeek.com/advsearch/boardgame', params=body)
        #print (con.text)

    #body = {'q':text_file}
    #con = requests.get('https://boardgamegeek.com/advsearch/boardgame', data=body)
    #print(con.text)

    #get the game ID number for BGG API
    genre_index = ('{}'.format("gloomhaven"))
    game_url = ('https://boardgamegeek.com/xmlapi2/search?query={}&type=boardgame&exact=1'.format(genre_index))
    response1 = requests.get(game_url)
    src1 = response1.content
    soup1 = BeautifulSoup(src1, 'html.parser')
    links1 = soup1.find_all('item')
    for link1 in links1:
        game_id = link1.get('id')
    
    #use the obtained game id to search for its stat page
    game_id_url = ('https://boardgamegeek.com/xmlapi2/thing?id={}&stats=1').format(game_id)
    print(game_id_url)
    response2 = requests.get(game_id_url)
    src2 = response2.content
    soup2 = BeautifulSoup(src2, 'html.parser')
    links2 = soup2.find_all(type="boardgamecategory")
    for link2 in links2:
        game_categories = link2.get('value')
        print(game_categories)
    

        
    

    #opens Boardgamegeek title search, searches for a title, and then clicks the appropriate page link
    #driver.get('https://boardgamegeek.com/advsearch/boardgame')
    
    #search = driver.find_element_by_name("q")
    #search.send_keys("kemet")
    #search.send_keys(Keys.RETURN)
    #driver.find_element_by_link_text("Kemet").click()
    
    #locates the game's genre
    #time.sleep(5)
    #a_list = driver.find_element_by_xpath("//div[@class='feature-description']/span/a")
    #print(a_list.text)
    #driver.quit()
 
    

genre_search("kemet")