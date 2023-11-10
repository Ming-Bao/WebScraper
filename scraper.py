# Improvements: add write to output file while getting the html requests - removes 2 for each loops and a lot of memory

import requests
from bs4 import BeautifulSoup
import pypandoc

init_url = "https://novelfull.com/the-legendary-mechanic/chapter-1-rebirth.html"
chapters = []

# Recursively adds page content to chapters
# Recursion ends when the next chapter button is disabled
def save_chapter(url):
    next_url = url
    
    while (True):
        #if stop == 0: return
        print(next_url)
        # HTML request
        response = requests.get(next_url)
        html = response.text
        
        # Getting soup setup
        soup = BeautifulSoup(html, "html.parser")
        paragraphs = soup.find_all('p')
        next_chap = soup.find(id="next_chap")
        
        #create add new list in chapters and add content into list
        chapters.append([])
        for p in paragraphs:
            text = p.text
            
            # Don't push paragraphs that contains these
            if "Translator:" not in text and "Editor:" not in text and text != "" and "Copyright NovelFull.Com. All Rights Reserved" not in text:
                text = text.replace("<", "-")
                text = text.replace(">", "-")
                chapters[-1].append(text)
        
        # Makes the first part of the chapter the title
        chapters[-1][0] = "# " + chapters[-1][0]
        print('                                                                                                  end')
        
        # Check if this is the end 
        if 'disabled=' in str(next_chap): return
        
        # Next chapter is available so get the url
        next_url = "https://novelfull.com" + next_chap['href']

# Saves the book as an epub
def save_as_epub():
    # Creates a string to store the words
    out_string = ""
    
    # Pushed all the words into the main string and add paragraphs when necessary
    for paragraphs in chapters:
        for text in paragraphs:
            out_string = out_string+ text + "\n\n"

    # Outputs a markdown file of the book
    with open("output.md", "w", encoding="utf-8") as f:
        f.write(out_string)
    
    # Converts the markdown file into a epub using pandoc     
    output = pypandoc.convert_file("output.md", 'epub', outputfile="output.epub")
    assert output == ""
    
    # Print out book stats
    token = out_string.split()
    type = set(token)
    diversity = len(type)/len(token)
    
    print(f"type: {len(type)}     token: {len(token)}     diversity: {diversity}")
    
    

def init():
    save_chapter(init_url)
    save_as_epub()

init()