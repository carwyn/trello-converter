
import sys
import json
import dominate
from dominate.tags import *
from dominate.util import raw
from markdown import Markdown

def main():
    
    f = open(sys.argv[1])
    js = json.load(f)

    # Markdown renderer.
    md = Markdown()

    title = "Exported Trello Board: " + js['name']

    doc = dominate.document(title=title)

    with doc:
        h1(title)
        
        with div(id="members"):
            h2("Trello Board Members")
            with ul():
                for m in js['members']:
                    li("{} ({})".format(m['fullName'], m['username']))

        with div(id="lists"):
            h2("Trello Lists")
            with ul():
                for l in js['lists']:
                    li("{}".format(l['name']))

        with div(id="cards"):
            h2("Trello Cards")
            for c in js['cards']:
                with div():
                    h3(c['name'])
                    div(raw((md.reset().convert(c['desc']))))


    print(doc)

if __name__ == '__main__':

    if len(sys.argv) == 2:
        main()
    else:
        print("Usage: ", sys.argv[0], "<Trello JSON File>")
        sys.exit(2)