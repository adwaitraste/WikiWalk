from django.shortcuts import render
from WikiWALK.config import hostname, port
from WikiWALK.models import Link
import pymysql
import pickle
import random
def startGame(req):
    global conn, cur, conn_meta, cur_meta, b, links
    conn_meta = pymysql.connect(host=hostname,
                              user='root',
                              port=port,
                              password='aad',
                              db='Data',
                              cursorclass=pymysql.cursors.DictCursor)
    cur_meta = conn_meta.cursor()
    conn = pymysql.connect(host=hostname,
                              user='root',
                              port=port,
                              password='aad',
                              db='Links',
                              cursorclass=pymysql.cursors.DictCursor)
    cur = conn.cursor()
    with open("table_names.pickle", 'rb') as handle:
        b = pickle.load(handle)
    links = list(b.keys())
    # res = createGameState(startLink)
    return render(req, "home.html", {})

def newGame(req):
    global startLink, endLink, lastLink
    
    startnumber = random.randint(0, len(links)-1)
    endnumber = random.randint(0, len(links)-1)
    tslink = links[startnumber]
    telink = links[endnumber]
    print(tslink)
    print(type(links))
    print(telink)
    startLink = tslink #Replace with links[startnumber]
    endLink = telink  #Replace with links[endnumnber]

    startLink = "Chess" #Replace with links[startnumber]
    endLink = "Chess problems"  #Replace with links[endnumnber]
    lastLink = startLink

    possible_tasks = [["Chess", "Norway"], ["Analysis of algorithms", "Bellman–Ford algorithm"]]

    task_no = random.randint(0, len(possible_tasks)-1)


    startLink = possible_tasks[task_no][0] #Replace with links[startnumber]
    endLink = possible_tasks[task_no][1] #Replace with links[endnumnber]
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
    import WikiWALK.config
    if WikiWALK.config.lastLink == None:
        WikiWALK.config.lastLink = startLink
    if WikiWALK.config.lastLink != next_link:
        query = """INSERT INTO Paths (from_link, int_link, to_link) VALUES("%s", "%s", "%s")"""%(WikiWALK.config.lastLink, next_link, endLink)
        cur_meta.execute(query)
        conn_meta.commit()
        WikiWALK.config.lastLink = next_link
        
    peak_link = next_link
    if req.POST.get('suggested_link'):
        print(req.POST.get('suggested_link'))
        print(next_link)
        query = """INSERT INTO Suggestions (from_link, to_link) VALUES("%s", "%s")"""%(next_link, req.POST.get('suggested_link'))
        cur_meta.execute(query)
        conn_meta.commit()
    if req.POST.get('embed_link'):
        print(req.POST.get('embed_link'))
        peak_link = req.POST.get('embed_link')
        # return render(req, "index.html", {"CurrentLink": next_link, "Link": res, "InitialLink": startLink, "EndLink": endLink, "PeakLink": peak_link})

    if next_link == endLink:
        WikiWALK.config.lastLink = None
        return render(req, "gameOver.html")
    res = createGameState(next_link)
    res_temp = []
    for c in res:
        # print(c)
        # break
        tmp = c["LinkName"][0]
        tmp = tmp.capitalize()
        tmp2 = c["LinkName"]
        tmp2=tmp+tmp2[1:]
        c["LinkName"] = tmp2 
        if c["LinkName"] in b:
            res_temp.append(c)

    res = res_temp

    # print(res)
    return render(req, "index.html", {"CurrentLink": next_link, "Link": res, "InitialLink": startLink, "EndLink": endLink, "PeakLink": peak_link})

def aboutus_page(req):
    return render(req, "aboutUs.html")

def play_page(req):
    return render(req, "play.html")

def open_source_db(req):
    query = "SELECT * from Paths"
    cur_meta.execute(query)
    res = cur_meta.fetchall()
    data = []
    for row in res:
        data.append([row["from_link"], row["int_link"], row["to_link"]])
    data.reverse()
    return render(req, "openSourceDB.html", {"data": data})