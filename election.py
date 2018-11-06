from bs4 import BeautifulSoup 
import requests 
import csv

def main():
  link = "https://projects.fivethirtyeight.com/2018-midterm-election-forecast/senate/massachusetts/";
  page = requests.get(link)
  soup = BeautifulSoup(page.content, 'html.parser')

  table_rows = soup.find_all('tr', {"class": "show"})

  for r in table_rows:
    dates = r.find('td', {"class": "dates"}).text
    pollster = r.find('td', {"class": "pollster"}).text
    margin = r.find('td', {"class": "raw"}).text





if __name__ == "__main__":
  main()