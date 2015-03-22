#!/usr/bin/env python

import copy, os, re, sqlite3, string, urllib
from bs4 import BeautifulSoup, NavigableString, Tag

DOCUMENTS_DIR = os.path.join('Microformats2.docset', 'Contents', 'Resources', 'Documents')
MICROFORMATS_DIR = os.path.join('microformats.org/wiki')

db = sqlite3.connect('Microformats2.docset/Contents/Resources/docSet.dsidx')
cur = db.cursor()

try: cur.execute('DROP TABLE searchIndex;')
except: pass
cur.execute('CREATE TABLE searchIndex(id INTEGER PRIMARY KEY, name TEXT, type TEXT, path TEXT);')
cur.execute('CREATE UNIQUE INDEX anchor ON searchIndex (name, type, path);')

# build search index and tables of contents
for filename in os.listdir(os.path.join(DOCUMENTS_DIR, MICROFORMATS_DIR)):
    path = os.path.join(DOCUMENTS_DIR, MICROFORMATS_DIR, filename)
    if os.path.isdir(path):
        # skip directories
        continue

    page = open(os.path.join(DOCUMENTS_DIR, MICROFORMATS_DIR, filename)).read()

    soup = BeautifulSoup(page, 'html5lib')

    # add each Microformat2 guide
    title = soup.find('h1', { 'class' : 'entry-title' } ).text.strip()

    if len(title) > 0:
        path = os.path.join(MICROFORMATS_DIR, filename)
        if (re.search('^h-.*', title)) :
            type = 'Object'
        else:
            type = 'Guide'
        cur.execute('INSERT OR IGNORE INTO searchIndex(name, type, path) VALUES (?,?,?)', (title, type, path))
        print 'title: %s, type: %s, path: %s' % (title, type, path)

    # strip unecessary HTML like sidebar, header and footer
    sidebar = soup.find(id='sidebar')
    if (sidebar):
        sidebar.extract()

    toc = soup.find(id='toc')
    if (toc):
        toc.extract()

    header = soup.find(class_='header')
    if (header):
        header.extract()

    contentControls = soup.find(id='content-controls')
    if (contentControls):
        contentControls.extract()

    lastModified = soup.find(class_='last-modified')
    if (lastModified):
        lastModified.extract()

    [t.extract() for t in soup('script')]

    dashStyle = soup.find(id='dash-style')

    if not (dashStyle):
        style = soup.new_tag('style', type='text/css', id='dash-style')
        style.append('.content { width: 100%; }');
        soup.head.append(style)

    # support table of contents by adding dash <a> tags for each header in the file
    for tag in soup.find_all(class_='mw-headline'):
        dashAnchor = tag.find('a', class_='dashAnchor')
        if dashAnchor:
            continue

        text = tag.text.strip()

        #print 'adding toc tag for section: %s' % text
        name = '//apple_ref/cpp/Section/' + urllib.quote(text, '')
        dashAnchor = BeautifulSoup('<a name="%s" class="dashAnchor"></a>' % name).a
        tag.insert(0, dashAnchor)

    fp = open(os.path.join(DOCUMENTS_DIR, MICROFORMATS_DIR, filename), 'w')
    fp.write(str(soup))
    fp.close()
db.commit()
db.close()
