from textwrap import wrap

import nltk
from PyQt5.QtWidgets import QDialog
from nltk.help import upenn_tagset

from gui.gen.tags_help import Ui_TagsHelp


class TagsHelp(QDialog, Ui_TagsHelp):
    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)
        self.textBrowser.setText(self.getText())

    @staticmethod
    def getText():
        tagdict = nltk.data.load('help/tagsets/upenn_tagset.pickle')
        tags = sorted(tagdict)
        tagsStrings = []
        for tag in tags:
            entry = tagdict[tag]
            defn = [tag + ": " + entry[0]]
            examples = wrap(entry[1], width=75, initial_indent="    ", subsequent_indent="    ")
            tagsStrings.append("\n".join(defn + examples))
        return "\n".join(tagsStrings)


def showTagsHelp(parent):
    dialog = TagsHelp(parent)
    if dialog.exec_():
        return dialog.result()


if __name__ == '__main__':
    upenn_tagset()
