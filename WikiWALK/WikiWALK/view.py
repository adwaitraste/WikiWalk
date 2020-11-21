from django.shortcuts import render

from WikiWALK.models import Link
import pymysql
import pickle
import random

def startGame(req):
    global conn, cur
    conn = pymysql.connect(host='0.tcp.ngrok.io',
                              user='root',
                              port=10361,
                              password='aad',
                              db='Links',
                              cursorclass=pymysql.cursors.DictCursor)
    cur = conn.cursor()
    # res = createGameState(startLink)
    return render(req, "play.html", {})

def newGame(req):
    global startLink, endLink
    with open("table_names.pickle", 'rb') as handle:
        b = pickle.load(handle)
    links = list(b.keys())
    startnumber = random.randint(0, 200)
    endnumber = random.randint(0, 200)
    tslink = links[startnumber]
    telink = links[endnumber]
    print(tslink)
    print(type(links))
    print(telink)
    startLink = 'Chess' #Replace with links[startnumber]
    endLink = 'India'  #Replace with links[endnumnber]
    res = createGameState(startLink)
    return render(req, "index.html", {"InitialLink": startLink, "Link": res, "EndLink": endLink, "CurrentLink": startLink})

def createGameState(currentLink):
    query = "SELECT * FROM `%s`" % (currentLink)
    cur.execute(query)
    res = cur.fetchall()
    return res


def nextLink(req, next_link):
    if next_link == endLink:
        return render(req, "gameOver.html")
    res = createGameState(next_link)
    return render(req, "index.html", {"CurrentLink": next_link, "Link": res, "InitialLink": startLink, "EndLink": endLink})
