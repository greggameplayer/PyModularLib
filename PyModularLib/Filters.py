import operator


class Filter:
    def __init__(self, title):
        self.title = title

    def execute(self, content):
        pass


class WordWrapFilter(Filter):
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
    def __init__(self):
        super().__init__("BoxFilter")

    def execute(self, content):
        stringtab = content.split('\n')
        result = []
        max_index, max_value = max(enumerate([len(i) for i in stringtab]), key=operator.itemgetter(1))

        result.append('+-' + ''.join(['-' for i in range(max_value)]) + '-+')

        for idx, val in enumerate(stringtab):
            formatStr = '{0: ^' + str(max_value) + '}'
            result.append('| ' + formatStr.format(val) + ' |')

        result.append('+-' + ''.join(['-' for i in range(max_value)]) + '-+')

        return {'message': '\n'.join(result)}


class EmailFilter(Filter):
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
            'message': 'MAIL FROM: ' + self.sender + '\nRCPT TO: ' + self.recipients + '\nDATA\nSubject: '\
                       + self.subject + '\n' + content}
