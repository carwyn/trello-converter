
import sys
import json
import dominate
from collections import defaultdict
from dominate.tags import *
from dominate.util import raw
from markdown import Markdown

def main():
    
    with open(sys.argv[1], encoding='utf-8') as f:
        board = json.load(f)

    # Build indexes into the JSON structure.
    labels = {lab['id']: lab for lab in board['labels']}
    members = {mem['id']: mem for mem in board['members']}
    lists = {lis['id']: lis for lis in board['lists']}
    cards = {card['id']: card for card in board['cards']}
    actions = {action['id']: action for action in board['actions']}
    checklists = {check['id']: check for check in board['checklists']}

    # Grouped collections of things.
    cards_by_list = defaultdict(list)

    for card in board['cards']:
        cards_by_list[card['id']].append(card)

    comments_by_card = defaultdict(list)

    for com in (c for c in board['actions'] if c['type'] == 'commentCard'):
        comments_by_card[com['data']['card']['id']].append(com)

    # Markdown renderer.
    md = Markdown()

    title = "Exported Trello Board: " + board['name']
    doc = dominate.document(title=title)

    with doc:
        h1(title)
        hr()
        
        with div(id="members"):
            h2("Trello Board Members")
            with ul():
                for m in board['members']:
                    li("{} (@{})".format(m['fullName'], m['username']))
        hr()

        with div(id="lists"):
            h2("Trello Lists")
            with ul():
                for l in board['lists']:
                    li("{}".format(l['name']))
        hr()

        with div(id="cards"):
            h2("Trello Cards")
            for c in board['cards']:
                with div(cls="card"):
                    h3("Card Title: {}".format(c['name']))

                    with dl(classmethod="carddetails"):
                        dt("Last Activity:")
                        dd(c['dateLastActivity'])
                        dt("Trello List:")
                        dd(lists[c['idList']]['name'])
                        if c['due']:
                            dt("Due Date:")
                            dd(c['due'])

                    if c['desc']:
                        h4("Card Description:")
                        with div(cls="carddesc"):
                            div(raw((md.reset().convert(c['desc']))))

                    if c['idMembers']:
                        with div(cls="cardmembers"):
                            h4("Card Members:")
                            with ul():
                                for m in c['idMembers']:
                                    li(members[m]['fullName'])

                    if c['idLabels']:
                        with div(cls="cardlabels"):
                            h4("Card Labels:")
                            with ul():
                                for l in c['idLabels']:
                                    li(labels[l]['name'])
                    
                    for cid in c['idChecklists']:
                        clist = checklists[cid]
                        with div(cls="checklist"):
                            h4("Checklist: {}".format(clist['name']))
                            with ul():
                                for item in clist['checkItems']:
                                    li("{} ({})".format(item['name'],item['state']))

                    if comments_by_card[c['id']]:
                        with div(cls="comments"):
                            h4("Card Comments:")
                            for com in comments_by_card[c['id']]:
                                with div(cls='cardcomment'):
                                    full = com['memberCreator']['fullName']
                                    user = com['memberCreator']['username']
                                    date = com['date']
                                    tup = (full, user, date)
                                    h4("{} ({}) : {}".format(*tup))
                                    md.reset()
                                    raw((md.convert(com['data']['text'])))

                # Line under each card.
                hr()


    with open(sys.argv[2], 'w', encoding='utf-8') as outfile:
        outfile.write(str(doc))

if __name__ == '__main__':

    if len(sys.argv) == 3:
        main()
    else:
        print("Usage: ", sys.argv[0], "[Trello JSON File] [Output File]")
        sys.exit(2)
