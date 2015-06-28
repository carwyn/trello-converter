
import sys
import json
import dominate
from dominate.tags import *
from dominate.util import raw
from markdown import Markdown

def main():
    
    f = open(sys.argv[1])
    board = json.load(f)

    labels = {lab['id']: lab for lab in board['labels']}
    members = {mem['id']: mem for mem in board['members']}
    lists = {lis['id']: lis for lis in board['lists']}
    cards = {card['id']: card for card in board['cards']}
    cards_by_list = {card['idList']: card for card in board['cards']}
    actions = {action['id']: action for action in board['actions']}
    checklists = {check['id']: check for check in board['checklists']}

    # Markdown renderer.
    md = Markdown()

    title = "Exported Trello Board: " + board['name']

    doc = dominate.document(title=title)

    with doc:
        h1(title)
        
        with div(id="members"):
            h2("Trello Board Members")
            with ul():
                for m in board['members']:
                    li("{} ({})".format(m['fullName'], m['username']))

        with div(id="lists"):
            h2("Trello Lists")
            with ul():
                for l in board['lists']:
                    li("{}".format(l['name']))

        with div(id="cards"):
            h2("Trello Cards")
            for c in board['cards']:
                with div(cls="card"):
                    h3(c['name'])

                    with div(cls="cardmembers"):
                        h4("Members")
                        with ul():
                            for m in c['idMembers']:
                                li(members[m]['fullName'])

                    with div(cls="cardlabels"):
                        h4("Labels")
                        with ul():
                            for l in c['idLabels']:
                                li(labels[l]['name'])

                    with div(cls="carddesc"):
                        h4("Description")
                        div(raw((md.reset().convert(c['desc']))))

                    with div(cls="cardactivity"):
                        h4("Activity")



    print(doc)

if __name__ == '__main__':

    if len(sys.argv) == 2:
        main()
    else:
        print("Usage: ", sys.argv[0], "<Trello JSON File>")
        sys.exit(2)
