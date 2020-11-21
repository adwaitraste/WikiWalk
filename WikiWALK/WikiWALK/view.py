from django.shortcuts import render

from WikiWALK.models import Link
import pymysql


def startGame(req):
    global conn, cur, startLink, endLink, conn_meta, cur_meta
    conn = pymysql.connect(host='localhost',
                              user='root',
                              port=3306,
                              password='aad',
                              db='Links',
                              cursorclass=pymysql.cursors.DictCursor)
    cur = conn.cursor()

    conn_meta = pymysql.connect(host='localhost',
                              user='root',
                              port=3306,
                              password='aad',
                              db='Data',
                              cursorclass=pymysql.cursors.DictCursor)
    cur_meta = conn_meta.cursor()

    startLink = 'Chess'
    endLink = 'India'
    
    return nextLink(req, startLink)
    # res = createGameState(startLink)
    # return render(req, "index.html", {"CurrentLink": startLink, "Link": res})


def createGameState(currentLink):
    query = "SELECT * FROM `%s`" % (currentLink)
    cur.execute(query)
    res = cur.fetchall()
    return res


def nextLink(req, next_link):

    peak_link = next_link.replace(" ", "_")

    if req.POST.get('suggested_link'):
        print(req.POST.get('suggested_link'))
        print(next_link)
        query = """INSERT INTO Suggestions (from_link, to_link) VALUES("%s", "%s")"""%(next_link, req.POST.get('suggested_link'))
        cur_meta.execute(query)
        conn_meta.commit()
    
    if req.POST.get('embed_link'):
        print(req.POST.get('embed_link'))
        peak_link = req.POST.get('embed_link').replace(" ", "_")
    if next_link == endLink:
        return render(req, "gameOver.html")
    res = createGameState(next_link)
    return render(req, "index.html", {"CurrentLink": next_link, "Link": res, "peakLink": peak_link})
