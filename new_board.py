from bs4 import BeautifulSoup
import requests

board =    [[0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0]]

def new_bo(board=board):
    board =    [[0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0]]
    source  =requests.get('https://www.sudokuweb.org/').text
    soup = BeautifulSoup(source, 'lxml')
    table = soup.table

    for tr in table.find_all('tr'):
        if(len(tr['id'])==4):
            i = 0
        else:
            i = int(tr['id'][4])
        for span in tr.find_all('span', class_='sedy'):
            if span is not None:
                if(len(span.parent['id']) == 5):
                    j = 0
                elif(len(span.parent['id']) == 6):
                    j = int(span.parent['id'][5])
                else:
                    j = int(span.parent['id'][5])*10 + int(span.parent['id'][6])
                j %= 9
                board[i][j] = int(span.text)
    return board
