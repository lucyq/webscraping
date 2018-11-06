from bs4 import BeautifulSoup 
import requests 
import csv

def main():
  link = "https://projects.fivethirtyeight.com/2018-midterm-election-forecast/senate/massachusetts/";
  headers = {
    'User-Agent': 'Educational workshop',
    'From': 'your_email@gmail.com'
  }
  page = requests.get(link, headers=headers)
  soup = BeautifulSoup(page.content, 'html.parser')

  polls = soup.find_all('tr', {"class": "show"})

  table = []

  for p in polls:
    dates = p.find('td', {"class": "dates"}).text
    pollster = p.find('td', {"class": "pollster"}).text
    margin = p.find('td', {"class": "raw"}).text

    table.append([dates, pollster, margin])

  with open('election_data.csv', 'wb') as csvfile:
    wrtr = csv.writer(csvfile)
    wrtr.writerow(['date', 'pollster', 'margin'])
    for row in table:
      wrtr.writerow(row)


if __name__ == "__main__":
  main()