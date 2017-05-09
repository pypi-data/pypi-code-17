#-*- coding: utf-8 -*-
"""
@file
@brief Defines an action for Mokadi.
"""
import datetime
import os
from .mokadi_action import MokadiAction
from .mokadi_info import MokadiInfo
from .mokadi_exceptions import MokadiException
from .cognitive_services_helper import call_api_emotions
from .mokadi_picture import take_picture
from PIL import Image, ImageDraw


class MokadiActionEmotion(MokadiAction):
    """
    Action. Emotion. Takes a picture and analyses it.
    """

    def __init__(self, subkey, folder, fLOG=None):
        """
        Constructor.

        @param      subkey      subscription key
        @param      folder      where to save the picture (must exist)
        @param      fLOG        logging function
        """
        MokadiAction.__init__(self, fLOG=fLOG)
        self._subkey = subkey
        self._folder = folder

        if not os.path.exists(folder):
            raise FileNotFoundError(folder)

    def can_do(self, interpreted, message):
        """
        Tells if the class can process the message.

        @param      interpreted     interpreted message
        @param      message         message
        @return                     true if the class can process the message
        """
        if len(interpreted) < 2:
            return False
        for word in interpreted:
            if word[1] == ":emotion:":
                return True
        return False

    def get_picture_name(self):
        """
        return a picture name
        """
        dt = datetime.datetime.now()
        name = "camera-%04d-%02d-%02dT%02d-%02d-%02d" % (dt.year, dt.month, dt.day,
                                                         dt.hour, dt.minute, dt.second)
        final = os.path.join(self._folder, name + ".png")
        i = 0
        while os.path.exists(final):
            i += 1
            final = os.path.join(self._folder, "%s.%d.png" % (name, i))
        return final

    def process_interpreted_message(self, interpretation, message):
        """
        Process the interpreted message.

        @param      interpretation      interpretation
        @param      message             original message
        @return                         iterator on Info
        """
        filename = self.get_picture_name()
        self.fLOG(
            "[MokadiActionEmotion.process_interpreted_message] create ", filename)
        take_picture(filename)
        if not os.path.exists(filename):
            yield MokadiInfo("error", "", "Aucune photo n'a pas pu être prise. Je ne peux pas en dire plus.")
            done = False
        res = call_api_emotions(self._subkey, filename)
        self.fLOG("[MokadiActionEmotion.process_interpreted_message] ", res)
        if len(res) == 0:
            yield MokadiInfo("error", "", "Aucun résultat. Veuillez recommencer.")
            done = True
        elif "error" in res:
            yield MokadiInfo("error", "", res["message"])
            done = True
        else:
            img = Image.open(filename)
            draw = ImageDraw.Draw(img)
            new_filename = os.path.splitext(filename)[0] + ".emotion.png"
            # [{'faceRectangle': {'height': 198, 'left': 268, 'top': 191, 'width': 198},
            done = True
            if len(res) > 1:
                yield MokadiInfo("ok", "Vous êtes plusieurs...")
                done = False

                for i, el in enumerate(res):
                    score, emotion = self.analyse_emotion(el["scores"])
                    rect = el["faceRectangle"]
                    self.fLOG(
                        "[MokadiActionEmotion.process_interpreted_message] ", el)
                    draw.rectangle([rect["left"], rect["top"], rect["left"] + rect["width"], rect["top"] + rect["height"]],
                                   outline=(255, 255, 0))
                    if i == 0:
                        numero = "Le premier"
                    else:
                        numero = "Le suivant"
                    if score == 0:
                        yield MokadiInfo("ok", numero + " " + "Je ne sais pas.")
                    elif score < 0.5:
                        yield MokadiInfo("ok", "Dur dur. Dans le doute, " + numero + " " + emotion)
                    elif score < 0.8:
                        yield MokadiInfo("ok", "J'hésite. " + numero + " " + emotion)
                    else:
                        yield MokadiInfo("ok", numero + " " + emotion)

            else:
                for el in res:
                    score, emotion = self.analyse_emotion(el["scores"])
                    rect = el["faceRectangle"]
                    self.fLOG(
                        "[MokadiActionEmotion.process_interpreted_message] ", el)
                    draw.rectangle([rect["left"], rect["top"], rect["left"] + rect["width"], rect["top"] + rect["height"]],
                                   outline=(255, 255, 0))
                    if score == 0:
                        yield MokadiInfo("ok", "Je ne sais pas.")
                    elif score < 0.5:
                        yield MokadiInfo("ok", "Dur dur. Dans le doute, tu " + emotion)
                    elif score < 0.8:
                        yield MokadiInfo("ok", "J'hésite. Tu " + emotion)
                    else:
                        yield MokadiInfo("ok", "Tu " + emotion)

            img.save(new_filename)
            yield MokadiInfo("ok", image=new_filename)

        if not done:
            raise MokadiException(
                "Unable to interpret '{0}'\n{1}".format(interpretation, message))

    def analyse_emotion(self, scores):
        """
        Returns the emotion as text.

        @param      scores  dictionary
        @return             string

        Example for *scores*:

        ::

            'scores': {'anger': 0.000243422386, 'contempt': 0.00207486819,
                       'disgust': 2.390567e-05, 'fear': 2.512976e-07,
                       'happiness': 3.5321933e-05, 'neutral': 0.9925101,
                       'sadness': 0.00510106329, 'surprise': 1.10992869e-05}}]

        """
        traduction = {'anger': 'est en colère',
                      'contempt': 'est content',
                      'disgust': "est dégoûté",
                      'fear': "a peur",
                      'happiness': 'est heureux',
                      'neutral': 'est difficile à lire',
                      'sadness': 'est triste',
                      'surprise': 'est surpris'}
        strong = [traduction[k] for k, v in scores.items() if v > 0.8]
        weak = [traduction[k] for k, v in scores.items() if v > 0.5]
        if len(strong) > 0:
            return 0.8, " et ".join(strong)
        elif len(weak) > 0:
            return 0.5, " et ".join(weak)
        else:
            tri = [(v, k) for k, v in scores.items()]
            ans = max(tri)
            return ans[0], traduction[ans[1]]
