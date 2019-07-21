# -*- coding: utf-8 -*-

"""Search the Vue.js Documentation"""

from os import path
import urllib.parse
import html
from algoliasearch.search_client import SearchClient

from albertv0 import *

__iid__ = "PythonInterface/v0.2"
__prettyname__ = "Vue.js Docs"
__version__ = "0.1.0"
__trigger__ = "vue "
__author__ = "Rick West"
__dependencies__ = ["algoliasearch"]


client = SearchClient.create("BH4D9OD16A", "85cc3221c9f23bfbaa4e3913dd7625ea")
index = client.init_index("vuejs")


icon = "{}/icon.png".format(path.dirname(__file__))
google_icon = "{}/google.png".format(path.dirname(__file__))


def getSubtitle(hit):
    hierarchy = hit["hierarchy"]

    if hierarchy["lvl2"] is not None:
        return hierarchy["lvl2"]

    if hierarchy["lvl3"] is not None:
        return hierarchy["lvl3"]

    if hierarchy["lvl4"] is not None:
        return hierarchy["lvl4"]

    if hierarchy["lvl5"] is not None:
        return hierarchy["lvl5"]

    if hierarchy["lvl6"] is not None:
        return hierarchy["lvl6"]

    return None


def sortByLevel(el):
    return el["hierarchy"]["lvl0"]


def handleQuery(query):
    items = []

    if query.isTriggered:

        if not query.isValid:
            return

        if query.string.strip():
            search = index.search(query.string, {"hitsPerPage": 5})

            hits = search["hits"]

            if len(hits) is not 0:
                hits.sort(key=sortByLevel)

            for hit in hits:
                subtitle = getSubtitle(hit)

                if subtitle is not None:
                    subtitle = "[{}] - {}".format(hit["hierarchy"]["lvl0"], subtitle)
                else:
                    subtitle = "[{}]".format(hit["hierarchy"]["lvl0"])

                items.append(
                    Item(
                        id=__prettyname__,
                        icon=icon,
                        text=html.unescape(hit["hierarchy"]["lvl1"]),
                        subtext=html.unescape(subtitle),
                        actions=[
                            UrlAction("Open in the Vue.js Documentation", hit["url"])
                        ],
                    )
                )

            if len(items) == 0:
                term = "vue js {}".format(query.string)

                google = "https://www.google.com/search?q={}".format(
                    urllib.parse.quote(term)
                )

                items.append(
                    Item(
                        id=__prettyname__,
                        icon=google_icon,
                        text="Search Google",
                        subtext='No match found. Search Google for: "{}"'.format(term),
                        actions=[UrlAction("No match found. Search Google", google)],
                    )
                )

                items.append(
                    Item(
                        id=__prettyname__,
                        icon=icon,
                        text="Open Docs",
                        subtext="No match found. Open vuejs.org/guide...",
                        actions=[
                            UrlAction(
                                "Open the Vue.js Documentation",
                                "https://vuejs.org/guide",
                            )
                        ],
                    )
                )

        else:
            items.append(
                Item(
                    id=__prettyname__,
                    icon=icon,
                    text="Open Docs",
                    subtext="Open vuejs.org/guide...",
                    actions=[
                        UrlAction(
                            "Open the Vue.js Documentation", "https://vuejs.org/guide"
                        )
                    ],
                )
            )

    return items
