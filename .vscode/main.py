from io import StringIO
import requests
from bs4 import BeautifulSoup
from csv import writer
import pandas as pd
import time
from collections import Counter
from matplotlib import pyplot as plot
import numpy as np



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

#clear_vasel_list()
#get_vasel_top_list()


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

def genre_search(text_file_in, text_file_out):
    
    #reads the games from the top board game .txt files
    with open(text_file_in) as in_file:
        contents = in_file.readlines()
        for content in contents:
            content = content.replace(" ", "+")
            content = content.rstrip()
            #print(content)
            #get the game ID number for BGG API
            game_url = ('https://boardgamegeek.com/xmlapi2/search?query={}&type=boardgame&exact=1'.format(content))
            print(game_url)
            response1 = requests.get(game_url)
            src1 = response1.content
            soup1 = BeautifulSoup(src1, 'html.parser')
            links1 = soup1.find_all('item')
            time.sleep(0.5)
            #print(links1)
            for link1 in links1:
                game_id = link1.get('id')
                time.sleep(.5)
                print(game_id)
            #use the obtained game id to search for its stat page
                game_id_url = ('https://boardgamegeek.com/xmlapi2/thing?id={}&stats=1').format(game_id)
                print(game_id_url)
                response2 = requests.get(game_id_url)
                time.sleep(.1)
                src2 = response2.content
                soup2 = BeautifulSoup(src2, 'html.parser')
                #scrapes the game categories and dumps them into designated file
                links2 = soup2.find_all(type="boardgamecategory")
                for link2 in links2:
                    game_categories = link2.get('value')
                    time.sleep(.5)
                    out_file = open(text_file_out, "a") 
                    out_file.write(game_categories)
                    out_file.write('\n')
                    time.sleep
                    out_file.close()
    
        in_file.close()

#genre_search("Quinn_list.txt", 'Quinn_cat_list2.txt')

def compile_data(cat_file_in1, cat_file_in2, name1, name2):
    with open(cat_file_in1) as in_file1:
        categories_list1 = [line.strip() for line in in_file1]
        in_file1.close()
        print(categories_list1)
        compiled_cats1 = (Counter(categories_list1))
    
    with open(cat_file_in2) as in_file2:
        categories_list2 = [line.strip() for line in in_file2]
        in_file2.close()
        #print(cat_list)
        compiled_cats2 = (Counter(categories_list2))
        
        df1 = pd.DataFrame.from_dict(compiled_cats1, orient='index')
        df2 = pd.DataFrame.from_dict(compiled_cats2, orient='index')
        fig = plot.figure()
 

        df1.plot.bar(color='red', ax=fig.gca(), position=0, width=0.3)
        df2.plot.bar(color='blue', ax=fig.gca(), position=1, width=0.3)
        plot.legend([name1, name2])
        plot.xlabel('Categories', fontsize=16)
        plot.ylabel('Occurences', fontsize=16)

        

        
        plot.show()
      
              
            

compile_data("Vasel_cat_list.txt", "Quinn_cat_list.txt", "Vasel", "Quinn")
