from PyModularLib.Filters import Filter
import operator
import pyparsing

ops = {
    "<=": operator.le,
    "<": operator.lt,
    "==": operator.eq,
    "!=": operator.ne,
    ">": operator.gt,
    ">=": operator.ge
}


class FilterChain:
    """
    classe représentant une chaîne de différents filtres
    """
    def __init__(self, filters, filtersGroups):
        """
        initialisation
        :param filters:
        :param filtersGroups:
        """
        self.filters = filters
        self.filtersGroups = filtersGroups

    def execute(self, content):
        """
        fonction permettant d'éxecuter les filtres contenu dans l'instance de classe
        :param content:
        :return:
        """
        result = {'message': content}
        for idx, filter in enumerate(self.filters):
            if hasattr(filter, 'get') and filter.get("group"):
                result = self.executeCurrentFilters(filter['group'], result)
                if result.get("error"):
                    return result['error']
            elif hasattr(filter, 'get') and filter.get('condition'):
                result = self.executeConditionFilter(filter, result, idx)
                if result.get("error"):
                    return {'error': result['error']}
            else:
                if isinstance(filter, Filter):
                    result = filter.execute(result['message'])
                    if result.get("error"):
                        return result['error']
                else:
                    return 'Thing entered at filter index : ' + str(idx) + ' isn\'t a filter'
        return result['message']

    def addFilter(self, filter):
        self.filters.append(filter)

    def executeCurrentFilters(self, filters, result):
        """
        fonction permettant d'éxecuter les filtres du tableau passé
        :param filters:
        :param result:
        :return:
        """
        for idx, filter in enumerate(filters):
            if hasattr(filter, 'get') and filter.get("group"):
                result = self.executeGroupFilter(filter['group'], result)
                if result.get("error"):
                    return {'error': result['error']}
            elif hasattr(filter, 'get') and filter.get('condition'):
                result = self.executeConditionFilter(filter, result, idx)
                if result.get("error"):
                    return {'error': result['error']}
            else:
                if isinstance(filter, Filter):
                    result = filter.execute(result['message'])
                    if result.get("error"):
                        return {'error': result['error']}
                else:
                    return {'error': 'Thing entered at filter index : ' + str(idx) + ' isn\'t a filter'}
        return result

    def executeGroupFilter(self, filters, result):
        """
        fonction permettant d'éxecuter les filtres d'un groupe donné
        :param filters:
        :param result:
        :return:
        """
        for idxgrp, val in enumerate(self.filtersGroups):
            if val == filters:
                result = self.executeCurrentFilters(self.filtersGroups[val], result)
                if result.get("error"):
                    return result['error']
        return result

    def executeConditionFilter(self, filters, result, idx):
        """
        fonction permettant d'éxecuter les filtres de la condition donnée
        :param filters:
        :param result:
        :param idx:
        :return:
        """
        if filters['condition'].find('==') != -1 or \
                filters['condition'].find('>=') != -1 or \
                filters['condition'].find('<=') != -1 or \
                filters['condition'].find('<') != -1 or \
                filters['condition'].find('!=') != -1 or \
                filters['condition'].find('>') != -1:
            statementTab = (pyparsing.Word(pyparsing.alphas) + pyparsing.oneOf('== >= <= > <') +
                            pyparsing.Word(pyparsing.nums)).parseString(filters['condition'])
            if statementTab[0] == 'length':
                if ops[statementTab[1]](len(result['message']), int(statementTab[2])):
                    result = self.executeCurrentFilters(filters['valid'], result)
                    if result.get("error"):
                        return result['error']
                else:
                    if filters.get('invalid'):
                        result = self.executeCurrentFilters(filters['invalid'], result)
                        if result.get("error"):
                            return result['error']

            else:
                return {'error': 'Unknown ' + statementTab[0] + ' in condition entered in the filter at index : ' +
                                 str(idx)}
        else:
            return {'error': 'Missing operator in condition entered in the filter at index : ' + str(idx)}

        return result
