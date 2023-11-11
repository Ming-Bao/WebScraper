import requests
from bs4 import BeautifulSoup
import pypandoc

init_url = "https://novelfull.com/the-legendary-mechanic/chapter-1-rebirth.html"
# chapters = []

# Recursively adds page content to chapters
# Recursion ends when the next chapter button is disabled
def save_chapter(url):
    next_url = url
    count = 100
    
    # Outputs a markdown file of the book
    with open("output.md", "w", encoding="utf-8") as f:
        while (True):
            #count -= 1 
            print(next_url)
            
            # List that stores the data that needs to be written to the markdown file
            push_string = []
            
            # HTML request
            response = requests.get(next_url)
            html = response.text
            
            # Getting soup setup
            soup = BeautifulSoup(html, "html.parser")
            paragraphs = soup.find_all('p')
            next_chap = soup.find(id="next_chap")
            
            for p in paragraphs:
                text = p.text
                
                # Don't push paragraphs that contains these
                if "Translator:" not in text and "Editor:" not in text and text != "" and "Copyright NovelFull.Com. All Rights Reserved" not in text:
                    text = text.replace("<", "-")
                    text = text.replace(">", "-")
                    push_string.append(text + "\n\n")
            
            # Makes the first part of the chapter the title
            push_string[0] = "# " + push_string[0]
            for text in push_string:
                f.write(text)
            
            print('                                                                                                  end')
            
            # Check if this is the end 
            if 'disabled=' in str(next_chap): return
            
            # Next chapter is available so get the url
            next_url = "https://novelfull.com" + next_chap['href']

# Saves the book as an epub
def save_as_epub():
    # Converts the markdown file into a epub using pandoc     
    output = pypandoc.convert_file("output.md", 'epub', outputfile="output.epub")
    assert output == ""
    
    

def init():
    save_chapter(init_url)
    save_as_epub()

init()