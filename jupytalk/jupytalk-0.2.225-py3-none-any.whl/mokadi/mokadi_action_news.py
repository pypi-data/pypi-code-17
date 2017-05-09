#-*- coding: utf-8 -*-
"""
@file
@brief Defines an action for Mokadi.
"""
from .mokadi_action import MokadiAction
from .mokadi_info import MokadiInfo
from .mokadi_exceptions import MokadiException
from .cognitive_services_helper import call_api_news
from .mokadi_helper import convert_into_days


class MokadiActionNews(MokadiAction):
    """
    Action. News.
    """

    def __init__(self, subkey, fLOG=None):
        """
        Constructor.

        @param      subkey      subscription key
        @param      fLOG        logging function
        """
        MokadiAction.__init__(self, fLOG=fLOG)
        self._subkey = subkey

    def can_do(self, interpreted, message):
        """
        Tells if the class can process the message.

        @param      interpreted     interpreted message
        @param      message         message
        @return                     true if the class can process the message
        """
        if len(interpreted) < 2:
            return False
        word = interpreted[1]
        for word in interpreted:
            if word[1] == ":news:":
                return True
        return False

    def process_interpreted_message(self, interpretation, message):
        """
        Process the interpreted message.

        @param      interpretation      interpretation
        @param      message             original message
        @return                         iterator on Info
        """
        done = False
        query = "NOT SET"

        # We assume
        has_news = any(_ for _ in interpretation if _[1] == ":news:")
        has_query = any(_ for _ in interpretation if _[1] == ":apropos:")
        if has_news:
            if has_query:
                for i in range(len(interpretation)):
                    if interpretation[i][1] == ":apropos:":
                        break
                if i == len(interpretation):
                    yield MokadiInfo("error", "", "Je n'ai pas compris ce qu'il fallait chercher.")
                    done = True
                    query = None
                else:
                    query = " ".join(_[0] for _ in interpretation[i + 1:-1])
            else:
                query = ""

            if query is not None:
                res = call_api_news(self._subkey, query)
                if len(res) == 0:
                    yield MokadiInfo("ok", "Aucun nouvelle n'a été trouvée à ce sujet.")
                    done = True
                if 'value' not in res or len(res["value"]) == 0:
                    yield MokadiInfo("ok", "La recherche '{0}' a abouti mais aucun résultat n'a été trouvé.".format(query))
                    done = True
                else:
                    displayed = 0
                    for val in res["value"]:
                        # Example of a news
                        # {'_type': 'News',
                        #  'readLink': 'https://api.cognitive.microsoft.com/api/v5/news/search?q=',
                        #  'value': [{'name': "Colombie : le bilan de la coulꥠde boue s'alourdit ࠲54 morts",
                        #             'url': 'http://www.bing.com/cr?IG=CEFF9C63FD7A4439B591261606484860&CID=3B75F5FD9A146DBF103CFFA49BF36C83&rd=1&h=Pu7c9WbgY9iMPFtyYtszuhDNymO92hG1vbCqLp0qUHw&v=1&r=http%3a%2f%2fwww.lepoint.fr%2fmonde%2fcolombie-le-bilan-de-la-coulee-de-boue-s-alourdit-a-254-morts-03-04-2017-2116711_24.php&p=DevEx,5019.1',
                        #             'image': {'thumbnail': {'contentUrl': 'https://www.bing.com/th?id=ON.08357B50C029DBC09D053826F9B22658&pid=News',
                        #                                     'width': 700, 'height': 304}},
                        #             'datePublished': '2017-04-03T10:33:00',
                        title = val["name"]
                        url = val["url"]
                        date = convert_into_days(val['datePublished'])
                        snippet = val.get("url", None)
                        yield MokadiInfo("ok", date + ". " + title, url=url, image=snippet)
                        displayed += 1
                    if displayed == 0:
                        yield MokadiInfo("ok", "La recherche '{0}' a abouti mais les résultats sont inattendus.".format(query))
                    done = True

        if not done:
            args = [message, len(interpretation),
                    interpretation, has_news, has_query, query]
            raise MokadiException(
                "Unable to interpret '{0}'\n{1} - {2}\nhas_news={3} has_query={4} query={5}.".format(*args))
