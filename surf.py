import requests
import csv

from bs4 import BeautifulSoup
# Making a GET request\microsoft\pyright\blob\main\docs\configuration.md
r = requests.get('https://surfcamp.it/europa/')


# print status code
#print(r)

# Parsing the HTML
soup = BeautifulSoup(r.content, 'html.parser')

# Print the contents of the main tag
#main_tag = soup.find('main')
#print(main_tag.contents)

elenco = soup.find('div', class_='risultatoPack')
if(elenco is None): 
    print("error elenco")
    exit()

grid_tag = elenco.find('div', class_='grid')
if(grid_tag is None): 
    print("error grid")
    exit()
#print(grid_tag)
# Find the grid items
list_item = grid_tag.findAll('div',class_='grid-item')
if(list_item is None): 
    print("error grid")
    exit()
i=0
#dizionario conterrà tutti i dati utili [nome prezzo link]
dizionario={}
for item in list_item:
   
    dataList=item.findAll('h2')
    if(dataList is None): 
        print("error dataList")
        exit()
    dataTextList=[]
    #lista con nome e prezzo
    for data in dataList:
        dataTextList.append(data.text)
    #aggiungo il link alla lista
    dataTextList.append(item.find('a',href=True)['href'])

    dizionario[i]=dataTextList
    i=i+1

#print(dizionario)
if (dizionario.values() is None):
    print('error dictionary')
    exit()


#apri link
value=dizionario[0]
link=value[2]

r=requests.get(link)
soup = BeautifulSoup(r.content, 'html.parser')
sx=soup.find('div',class_='parteSx')

first=sx.find('p')
next=first.find_next_siblings('p')
description=[first.text]
for paragraph in next:
    description.append(paragraph.text)
#print (description)
i=0
#table for prices
tables=sx.findAll('table')
for table in tables:
    rows = table.find_all('tr')

    # Extract the data from each row and store it in a list
    data = []
    

    data.append([dizionario[i][0].strip().replace(' ','')]) #il nome
    for row in rows:
        titles=row.find_all('th')
        titles = [title.text.strip().replace(' ','') for title in titles]

        data.append(titles)

        cols = row.find_all('td')
        cols = [col.text.strip().replace(' ','') for col in cols]
        while(len(cols)>4):
            cols.pop()
        data.append(cols)

    #write on table excell
    with open('output.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data)

   

    reader = csv.reader(open('t.csv', 'r'))
    reader1 = csv.reader(open('output.csv', 'r'))
    

    lr=list(reader)
    lr1=list(reader1)

    writer2 = csv.writer(open('t.csv', 'w'))

    for x in range(len(lr)):
        writer2.writerow(lr[x]+lr1[x])









 




