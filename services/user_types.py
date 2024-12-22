from services.features import translitirate

class Column:
    def __init__(self, name, type, other = ''):
        self.name = name
        self.column_name = translitirate(name)
        self.type = type
        self.type_name = self._get_type_name(type)
        self.other = other

    def __str__(self):
        return f'column_{self.column_name}_{self.type}'

    def _get_type_name(self, type):
        match type:
            case 'int':
                return 'INT'
            case 'text':
                return 'TEXT'
            case 'char', num:
                return f'CHAR({num})'
