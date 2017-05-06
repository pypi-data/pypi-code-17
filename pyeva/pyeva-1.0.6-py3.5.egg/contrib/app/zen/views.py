import random

from eva.web import APIRequestHandler


class Zen(APIRequestHandler):

    zen = {
        "python": [
            "Beautiful is better than ugly.",
            "Explicit is better than implicit.",
            "Simple is better than complex.",
            "Complex is better than complicated.",
            "Flat is better than nested.",
            "Sparse is better than dense.",
            "Readability counts.",
            "Special cases aren't special enough to break the rules.",
            "Although practicality beats purity.",
            "Errors should never pass silently.",
            "Unless explicitly silenced.",
            "In the face of ambiguity, refuse the temptation to guess.",
            "There should be one-- and preferably only one --obvious way to do it.",
            "Although that way may not be obvious at first unless you're Dutch.",
            "Now is better than never.",
            "Although never is often better than *right* now.",
            "If the implementation is hard to explain, it's a bad idea.",
            "If the implementation is easy to explain, it may be a good idea.",
            "Namespaces are one honking great idea -- let's do more of those!",
        ],

        "github": [
            "Responsive is better than fast.",
            "It’s not fully shipped until it’s fast.",
            "Anything added dilutes everything else.",
            "Practicality beats purity.",
            "Approachable is better than simple.",
            "Mind your words, they are important.",
            "Speak like a human.",
            "Half measures are as bad as nothing at all.",
            "Encourage flow.",
            "Non-blocking is better than blocking.",
            "Favor focus over features.",
            "Avoid administrative distraction.",
            "Design for failure.",
            "Keep it logically awesome.",
        ],
    }

    def get(self):
        '''参考 https://api.github.com/zen
        '''

        t = self.get_argument('t', 'python')
        zen = self.zen.get(t, ['No news is good news.'])
        self.write(random.choice(zen))
