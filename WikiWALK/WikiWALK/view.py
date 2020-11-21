from django.shortcuts import render

from WikiWALK.models import Link
import pymysql
import pickle
import random
def startGame(req):
    global conn, cur, conn_meta, cur_meta
    conn_meta = pymysql.connect(host='localhost',
                              user='root',
                              port=3306,
                              password='aad',
                              db='Data',
                              cursorclass=pymysql.cursors.DictCursor)
    cur_meta = conn_meta.cursor()
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
    # res = createGameState(startLink)
    # return render(req, "index.html", {"InitialLink": startLink, "Link": res, "EndLink": endLink, "CurrentLink": startLink})

    return nextLink(req, startLink)
    # res = createGameState(startLink)
    # return render(req, "index.html", {"CurrentLink": startLink, "Link": res})


def createGameState(currentLink):
    query = "SELECT * FROM `%s`" % (currentLink)
    cur.execute(query)
    res = cur.fetchall()
    return res


def nextLink(req, next_link):
    if req.POST.get('suggested_link'):
        print(req.POST.get('suggested_link'))
        print(next_link)
        query = """INSERT INTO Suggestions (from_link, to_link) VALUES("%s", "%s")"""%(next_link, req.POST.get('suggested_link'))
        cur_meta.execute(query)
        conn_meta.commit()
    if next_link == endLink:
        return render(req, "gameOver.html")
    res = createGameState(next_link)
    return render(req, "index.html", {"CurrentLink": next_link, "Link": res, "InitialLink": startLink, "EndLink": endLink})
