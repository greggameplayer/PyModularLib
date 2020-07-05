import operator
from PyModularLib.FancyTable import FancyTable


class Filter:
    """
    classe représentant un filtre
    """
    def __init__(self, title):
        """
        initialisation
        :param title:
        """
        self.title = title

    def execute(self, content):
        """
        fonction permettant d'executer le filtre
        :param content:
        :return:
        """
        pass


class WordWrapFilter(Filter):
    """
    filtre permettant de découper l'entrée en ligne d'un nombre maximum de caractère donnée
    """
    def __init__(self, lineLength):
        super().__init__("WordWrapFilter")
        try:
            self.lineLength = int(lineLength)
        except ValueError:
            self.ValueError = True

    def execute(self, content):
        if hasattr(self, 'ValueError') and self.ValueError:
            return {'error': 'Invalid parameter type'}
        startint = 0
        stringtab = []
        content = content.replace('\n', '')
        for idx, val in enumerate(content):
            if idx % self.lineLength == 0:
                stringtab.append(content[startint:idx])
                startint = idx
            elif idx == len(content) - 1:
                stringtab.append(content[startint:])
        return {'message': '\n'.join(stringtab[1:])}


class BoxFilter(Filter):
    """
    filtre permettant de dessiner une boite autour de l'entrée texte
    """
    def __init__(self, color=""):
        super().__init__("BoxFilter")
        decorated = False
        for i in FancyTable.FancyTab:
            if color == i:
                self.color = color
                decorated = True
        if not decorated:
            self.color = ""

    def execute(self, content):
        stringtab = content.split('\n')
        result = []
        max_index, max_value = max(enumerate([len(i) for i in stringtab]), key=operator.itemgetter(1))

        result.append(self.color + '+-' + ''.join(['-' for i in range(max_value)]) + '-+' + FancyTable.CEND)

        for idx, val in enumerate(stringtab):
            formatStr = '{0: ^' + str(max_value) + '}'
            result.append(self.color + '| ' + FancyTable.CEND + formatStr.format(val) + self.color + ' |' + FancyTable.CEND)

        result.append(self.color + '+-' + ''.join(['-' for i in range(max_value)]) + '-+' + FancyTable.CEND)

        return {'message': '\n'.join(result)}


class EmailFilter(Filter):
    """
    filtre permettant de convertir l'entrée de texte en format mail avec le sujet, le destinataire, et l'envoyeur
    en argument
    """
    def __init__(self, sender, recipients, subject):
        super().__init__("EmailFilter")
        self.sender = sender
        self.recipients = recipients
        self.subject = subject

    def email_validation(self, x):
        a = 0
        y = len(x)
        dot = x.rfind(".")
        at = x.find("@")
        for i in range(0, at):
            if ('a' <= x[i] <= 'z') or ('A' <= x[i] <= 'Z'):
                a = a + 1
        if a > 0 and at > 0 and (dot - at) > 0 and (dot + 1) < y:
            return True
        else:
            return False

    def execute(self, content):
        if not self.email_validation(self.sender):
            return {'error': 'Invalid sender email'}

        if not self.email_validation(self.recipients):
            return {'error': 'Invalid recipient email'}

        return {
            'message': 'MAIL FROM: ' + self.sender + '\nRCPT TO: ' + self.recipients + '\nDATA\nSubject: ' \
                       + self.subject + '\n' + content}
