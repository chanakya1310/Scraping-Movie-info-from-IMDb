import requests
from bs4 import BeautifulSoup
import os
import threading
def extraction1(url):
    imdb_page=requests.get(url)
    imdb_soup=BeautifulSoup(imdb_page.content,'html.parser')

    try:
        step1=imdb_soup.find("td")
        link_to_next_page=step1.find("a")
        link3=link_to_next_page.get("href")
        #print(link_to_next_page.get("href"))
    except AttributeError:
        print("Out of Scope")

    return link3

def extraction2(url):
    movie_page=requests.get(url)
    movie_soup=BeautifulSoup(movie_page.content,'html.parser')
    topics=[]
    dict={}
    try:
        overall=movie_soup.find_all("div",{"class":"credit_summary_item"})

        headers = [elem.find_all("h4") for elem in overall]

        for i in headers:
            topics.append(i[0].text)
        x=0
        all=[]
        t=0
        
        for i in overall:
            x=0
            t+=1
            different=[]
            #print(i.find_all("a"))
            for j in i.find_all("a"):
                different.append(j.text)
                x+=1
            all.append(different)
            
        for i in range(0,t):
            a=len(all[i])
            if(len(all[i])>1):
                a=a-1
            b=all[i]
            dict.update({topics[i]:b[0:a]})
        print("The full Cast and Crew of the movie is\n",dict)
    
    except AttributeError:
        print("out of scope")
    print()
    return dict


def extraction3(url):
    movie_page=requests.get(url)
    movie_soup=BeautifulSoup(movie_page.content,"html.parser")
    try:
        summary=movie_soup.find_all("div",{"class":"summary_text"})
        summary=summary[0].text
        print("The summary of the movie is:",summary)
    except AttributeError:
        print("out of scope")
    print()

def extraction4(url):
    movie_page=requests.get(url)
    movie_soup=BeautifulSoup(movie_page.content,"html.parser")
    try:
        rating=movie_soup.find_all("span",{"itemprop":"ratingValue"})[0].text
        print("The rating of the movie is(out of 10)",rating)

    except AttributeError:
        print("out of scope")
    print()

def extraction5(url):
    movie_page=requests.get(url)
    movie_soup=BeautifulSoup(movie_page.content,"html.parser")
    try:
        running_time=movie_soup.find_all("time")[0].text
        print("The running time of the movie is",running_time)

    except AttributeError:
        print("Out of scope")
    print()

def extraction6(url):
    movie_page=requests.get(url)
    movie_soup=BeautifulSoup(movie_page.content,"html.parser")
    try:
        release_year=movie_soup.find_all("span",{"id":"titleYear"})[0].text
        print("The movie was released in: ",release_year)
    
    except AttributeError:
        print("Out of scope")
    print()


if __name__ == "__main__":
    print("The ID of the main process is {}".format(os.getpid()))

    movie=input("Enter the movie for which you want to get information: ")
    movie=movie.lower()
    movie=movie.split()
    movie = ("+").join(movie)
    #print(movie)

    url="https://www.imdb.com/find?q="
    url1=url+movie

    #print(url1)
    link3=extraction1(url1)

    url2="https://www.imdb.com"
    url3="?ref_=fn_al_tt_1"

    final_url=url2+link3+url3

    #This url will be the final url from which we will extract the neccessary things 
    #like ratings cast etc...

    print("The final URL is",final_url)
    print()

    t1=threading.Thread(target=extraction2,args=[final_url])
    #extraction2 is for scraping the directors,writers and cast of the film.

    t2=threading.Thread(target=extraction3,args=[final_url])
    #extraction3 is for scrapping the summary.

    t3=threading.Thread(target=extraction4,args=[final_url])
    #extraction4 is for scrapping the rating.

    t4=threading.Thread(target=extraction5,args=[final_url])
    #extraction5 is for scraping the running time

    t5=threading.Thread(target=extraction6,args=[final_url])
    #extraction6 is used for scraping the year in which film was released.

    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()

    t1.join()
    t2.join()
    t3.join()
    t4.join()
    t5.join()







