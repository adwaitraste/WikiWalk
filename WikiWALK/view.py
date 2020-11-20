from django.shortcuts import render

from WikiWALK.models import Link
import pymysql


def startGame(req):
    global conn, cur
    conn = pymysql.connect(host='4.tcp.ngrok.io',
                              user='root',
                              port=17891,
                              password='aad',
                              db='Links',
                              cursorclass=pymysql.cursors.DictCursor)
    cur = conn.cursor()
    startLink = 'Chess'
    res = createGameState(startLink)
    return render(req, "index.html", {"CurrentLink": startLink, "Link": res})


def createGameState(currentLink):
    query = "SELECT * FROM `%s`" % (currentLink)
    cur.execute(query)
    res = cur.fetchall()
    return res


def nextLink(req, next_link):
    res = createGameState(next_link)
    return render(req, "index.html", {"CurrentLink": next_link, "Link": res})
