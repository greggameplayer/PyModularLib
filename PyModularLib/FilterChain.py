from PyModularLib.Filters import Filter


class FilterChain:
    def __init__(self, filters, filtersGroups):
        self.filters = filters
        self.filtersGroups = filtersGroups

    def execute(self, content):
        result = {'message': content}
        for idx, filter in enumerate(self.filters):
            if hasattr(filter, 'get') and filter.get("group"):
                for idx, val in enumerate(self.filtersGroups):
                    if val == filter['group']:
                        for idxchild, filterchild in enumerate(self.filtersGroups[val]):
                            if isinstance(filterchild, Filter):
                                result = filterchild.execute(result['message'])
                                if result.get("error"):
                                    return result['error']
                            else:
                                return 'Thing entered at group index inside filters : ' + str(idx) +\
                                       '\nand filter index inside group : ' +\
                                       str(idxchild) + '\nisn\'t a filter'
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
