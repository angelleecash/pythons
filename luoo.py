#!/usr/bin/python
__author__ = 'chenliang'
import urllib2
import os
import cgi
import os.path
import time

def getFilePath(category):
    return "luoo_category_" + str(category)

form = cgi.FieldStorage()
# Get data from fields
category = form.getvalue('category')
# category = "ost"
# categoryFilePath = getFilePath(category)


def parseLink(line):
    l = line

    hrefStart = l.index('"') + 1
    hrefEnd = l.index('"', hrefStart)

    href = l[hrefStart:hrefEnd]

    start = l.index(">") + 1
    end = l.index('<', start)

    title = l[start:end]

    return title, href

def comp(x, y):
    xLike = int(x[7])
    yLike = int(y[7])

    if xLike < yLike:
        return -1
    elif xLike > yLike:
        return 1
    else:
        return 0

categories = ["inside", "folk", "metal", "britpop", "electronic", "ambient", "pop", "china", "psychedelic", "punk", "world", "hardcore", "jazz", "hip-hop", "classical", "ost"]

# queues = {}

# for category in categories:
#     queues[category] = Queue.Queue()
results = {}


def processCategory(category):
    guessPageCount = 20
    allItems = []
    itemMap = {}

    for page in range(1, guessPageCount):
        url = "http://www.luoo.net/tag/" + category + "?p=" + str(page)
        response = urllib2.urlopen(url)
        html = response.read()
        htmlContent = str(html).split("\n")
        count = 0
        matched = False
        lineno = 1

        currentItem = []

        for line in htmlContent:
            count += 1
            line = line.lstrip()
            line = line.rstrip()

            if line == '<div class="meta rounded clearfix">':
                matched = True
                lineno = 1
                currentItem = []
            else:
                if line == '</div>':
                    if matched:
                        matched = False

                        if len(currentItem) > 0 and not currentItem[0] in itemMap:
                            allItems.append(currentItem)
                            itemMap[currentItem[0]] = 1
                        currentItem = []
                else:
                    if matched :
                        lineno += 1
                        currentItem.append(line)

    allItems.sort(cmp=comp, reverse=True)
    result = []
    for i in range(0, min(len(allItems), 10)):
        link = allItems[i][0]
        like = allItems[i][7]
        title, href = parseLink(link)
        result.append([title, like, href])
    results[category] = result
    saveCategoriesToFile(result, category)

SEPARATOR = "*"

def saveCategoriesToFile(result, category):
    file = open(getFilePath(category), "w")
    for item in result:
        file.write(SEPARATOR.join(item) + "\n")


def loadCategoriesFromFile(category):
    file = open(getFilePath(category), "r")
    result = []
    for line in file:
        result.append(line.split(SEPARATOR))
    results[category] = result



# for category in categories:
#     t = threading.Thread(target=processCategory, args=(category,))
#     t.start()
#     # t.join()

# url = self.request.GET



def isCategoryDataUpToDate(category):
    categoryFilePath = getFilePath(category)
    if not os.path.isfile(categoryFilePath):
        return False

    diff = int(time.time() - os.path.getctime(categoryFilePath))
    if diff < 24*60*60:
        return True
    else :
        return False

if isCategoryDataUpToDate(category):
    loadCategoriesFromFile(category)
else:
    processCategory(category)

# for category, queue in queues.iteritems():
#     results[category] = queue.get()

print """Content-Type: text/html;charset=UTF-8\n"""
print "<html>"
print "<head>"
print "<meta charset=\"UTF-8\">"
print "</head>"
print "<body>"

for category, ranks in results.iteritems():
    print "<h1>" + category + "</h1>"

    print "<table>"
    allItems = ranks

    for i in allItems:
        print "<tr>"
        title, like, href = i[:]
        print "<td><a href=\""+ href+ "\">"+ title + "(" + str(like) + ")</a></td>"
        print "</tr>"

    print "</table>"


print "</body>"
print "</html>"




