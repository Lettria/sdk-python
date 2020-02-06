from .sharedClass import SharedClass_A

class Base_entity(SharedClass_A):
        def __init__(self, name, data = None, document_level = True):
            self.document_level = document_level
            self.data = data
            self.name = name
        def __repr__(self):
            if 'source' in self.format(self.data)[0]:
                return str(self.format([[d['source'] for d in seq] for seq in self.data]))
            else:
                return str(self.format([d for d in self.data]))

        def print_formatted(self):
            length = 25
            d = {}
            seq = []
            print("{:15s}\t{:20s}\t".format('Type','Source'), end = '')
            for _seq in self.data:
                for _seq in self.data:
                    if _seq:
                        seq = _seq
                        break
            for d_ in seq:
                if d_:
                    d = d_
                    break
            if not d:
                return
            for key in d.keys():
                if key not in ['type', 'source']:
                    if isinstance(d[key], dict):
                        for k in d[key].keys():
                            print("{:12s}".format(k.capitalize()), end = '\t')
                            length += 16
                    else:
                        print("{:10s}".format(key.capitalize()), end = '\t')
                        length += 16
            print('')
            print('-' * length)
            for seq in self.data:
                for d in seq:
                    print("{:15.15s}\t{:20.20s}\t".format(d['type'].upper(), d['source']), end = '')
                    for key in d.keys():
                        if key not in ['type', 'source']:
                            if isinstance(d[key], dict):
                                for k in d[key].keys():
                                    if not isinstance(d[key][k], (str, float, int)):
                                        print("{:12.12s}".format(type(d[key][k]).__name__), end = '\t')
                                    else:
                                        print("{:12.12s}".format(str(d[key][k])), end = '\t')
                            else:
                                _field = d[key] if d[key] else 'None'
                                print("{:10}".format(_field), end = '\t')
                    if d:
                        print('')


class Person(Base_entity):
        def __init__(self, data = None, document_level = True):
            self.document_level = document_level
            self.data = data
            self.name = 'Person'
        def __repr__(self):
            return str(self.format([[d['source'] for d in seq] for seq in self.data]))
        def print_formatted(self):
            print("{:10s}\t{:10s}".format('Type','Source'))
            print('-' * 20)
            for seq in self.data:
                for d in seq:
                    print("{:10s}\t".format(d['type'].upper()), end = '')
                    print("{:10s}".format(d['source']))

class Location(Base_entity):
        def __init__(self, data = None, document_level = True):
            self.document_level = document_level
            self.data = data
            self.name = 'Location'
        def __repr__(self):
            return str(self.format([[d['source'] for d in seq] for seq in self.data]))
        def print_formatted(self):
            print("{:10s}\t{:10s}".format('Type','Source'))
            print('-' * 20)
            for seq in self.data:
                for d in seq:
                    print("{:10s}\t".format(d['type'].upper()), end = '')
                    print("{:10s}".format(d['source']))

class Date(Base_entity):
        def __init__(self, data = None, document_level = True):
            self.document_level = document_level
            self.data = data
            self.name = 'Date'
        def __repr__(self):
            return str(self.format([[d['source'] for d in seq] for seq in self.data]))
        def print_formatted(self):
            print("{:10s}\t{:20s}\t{:20s}\t{:20s}".format('Type','Source', 'ISO', 'timestamp'))
            print('-' * 70)
            for seq in self.data:
                for d in seq:
                    print("{:10s}\t".format(d['type'].upper()), end = '')
                    print("{:20.20s}\t{:20s}\t{:20s}".format(d['source'], d['value']['ISO'], str(d['value']['timestamp'])))

class Distance(Base_entity):
        def __init__(self, data = None, document_level = True):
            self.document_level = document_level
            self.data = data
            self.name = 'Distance'

        def __repr__(self):
            return str(self.format([[d['source'] for d in seq] for seq in self.data]))
        def print_formatted(self):
            print("{:10s}\t".format('Type'), end = '')
            print("{:10s}\t{:15s}\t{:15}\t{:15}".format('Source', 'Unit', 'Meter', 'Miles'))
            print('-' * 75)
            for seq in self.data:
                for d in seq:
                    print("{:10s}\t".format(d['type'].upper()), end = '')
                    print("{:10s}\t{:15s}\t{:15.10s}\t{:15.10s}".format(d['source'], d['value']['unit'], str(d['value']['meter']), str(d['value']['miles'])))

class Duration(Base_entity):
        def __init__(self, data = None, document_level = True):
            self.document_level = document_level
            self.data = data
            self.name = 'Duration'

        def __repr__(self):
            return str(self.format([[d['source'] for d in seq] for seq in self.data]))

class Frequency(Base_entity):
        def __init__(self, data = None, document_level = True):
            self.document_level = document_level
            self.data = data
            self.name = 'Frequency'
        def __repr__(self):
            return str(self.format([[d['source'] for d in seq] for seq in self.data]))

class Interval(Base_entity):
        def __init__(self, data = None, document_level = True):
            self.document_level = document_level
            self.data = data
            self.name = 'Interval'
        def __repr__(self):
            return str(self.format([[d['source'] for d in seq] for seq in self.data]))
        def print_formatted(self):
            print("{:10s}\t".format('Type'), end = '')
            print("{:20s}\t{:20s}\t{:20s}\t{:15s}\t{:15s}\t{:15s}".format('Source', 'Start', 'End', 'days', 'hours', 'minutes'))
            print('-' * 130)
            for seq in self.data:
                for d in seq:
                    print("{:10.10s}\t{:20.20s}\t".format(d['type'].upper(), d['source']), end = '')
                    if d['value']['start']:
                        print("{:20s}".format(d['value']['start']['ISO']), end = '\t')
                    else:
                        print("{:20s}".format(''), end = '\t')
                    if d['value']['end']:
                        print("{:20s}".format(d['value']['end']['ISO']), end = '\t')
                    else:
                        print("{:20s}".format(''), end = '\t')
                    if d['value']['duration']['start_end']:
                        print("{:15.5f}".format(d['value']['duration']['start_end']['days']), end = '\t')
                        print("{:15.5f}".format(d['value']['duration']['start_end']['hours']), end = '\t')
                        print("{:15.5f}".format(d['value']['duration']['start_end']['minutes']), end = '\t')
                    else:
                        print("{:15s}\t{:15s}\t{:15s}".format('', '', ''), end = '')
                    print('')

class Ip(Base_entity):
        def __init__(self, data = None, document_level = True):
            self.document_level = document_level
            self.data = data
            self.name = 'Ip'
        def __repr__(self):
            return str(self.format([[d['source'] for d in seq] for seq in self.data]))
        def print_formatted(self):
            print("{:10s}\t".format('Type'), end = '')
            print("{:10s}\t{:15s}\t{:15}\t{:25}".format('Source', 'Country', 'City', 'Organisation'))
            print('-' * 100)
            for seq in self.data:
                for d in seq:
                    print("{:10s}\t".format(d['type'].upper()), end = '')
                    print("{:10s}\t".format(d['source']), end = '')
                    if 'value' in d and d['value']:
                        print("{:15s}\t{:15s}\t{:25s}".format(d['value']['country'], d['value']['city'], d['value']['org']))
                    else:
                        print("{:15s}\t{:15s}\t{:25s}".format('None', 'None', 'None'))
class Ipv6(Base_entity):
        def __init__(self, data = None, document_level = True):
            self.document_level = document_level
            self.data = data
            self.name = 'Ipv6'
        def __repr__(self):
            return str(self.format([[d['source'] for d in seq] for seq in self.data]))

class Mail(Base_entity):
        def __init__(self, data = None, document_level = True):
            self.document_level = document_level
            self.data = data
            self.name = 'Mail'
        def __repr__(self):
            return str(self.format([[d['source'] for d in seq] for seq in self.data]))

class Mass(Base_entity):
        def __init__(self, data = None, document_level = True):
            self.document_level = document_level
            self.data = data
            self.name = 'Mass'
        def __repr__(self):
            return str(self.format([[d['source'] for d in seq] for seq in self.data]))

class Mass_by_volume(Base_entity):
        def __init__(self, data = None, document_level = True):
            self.document_level = document_level
            self.data = data
            self.name = 'Mass_by_volume'
        def __repr__(self):
            return str(self.format([[d['source'] for d in seq] for seq in self.data]))

class Mol(Base_entity):
        def __init__(self, data = None, document_level = True):
            self.document_level = document_level
            self.data = data
            self.name = 'Mol'
        def __repr__(self):
            return str(self.format([[d['source'] for d in seq] for seq in self.data]))

class Money(Base_entity):
        def __init__(self, data = None, document_level = True):
            self.document_level = document_level
            self.data = data
            self.name = 'Money'
        def __repr__(self):
            return str(self.format([[d['source'] for d in seq] for seq in self.data]))

class Ordinal(Base_entity):
        def __init__(self, data = None, document_level = True):
            self.document_level = document_level
            self.data = data
            self.name = 'Ordinal'
        def __repr__(self):
            return str(self.format([[d['source'] for d in seq] for seq in self.data]))

class Percent(Base_entity):
        def __init__(self, data = None, document_level = True):
            self.document_level = document_level
            self.data = data
            self.name = 'Percent'
        def __repr__(self):
            return str(self.format([[d['source'] for d in seq] for seq in self.data]))

class Phone(Base_entity):
        def __init__(self, data = None, document_level = True):
            self.document_level = document_level
            self.data = data
            self.name = 'Phone'
        def __repr__(self):
            return str(self.format([[d['source'] for d in seq] for seq in self.data]))

class Pressure(Base_entity):
        def __init__(self, data = None, document_level = True):
            self.document_level = document_level
            self.data = data
            self.name = 'Pressure'
        def __repr__(self):
            return str(self.format([[d['source'] for d in seq] for seq in self.data]))

class Set(Base_entity):
        def __init__(self, data = None, document_level = True):
            self.document_level = document_level
            self.data = data
            self.name='Set'
        def __repr__(self):
            return str(self.format([[d['source'] for d in seq] for seq in self.data]))

class Speed(Base_entity):
        def __init__(self, data = None, document_level = True):
            self.document_level = document_level
            self.data = data
            self.name = 'Speed'
        def __repr__(self):
            return str(self.format([[d['source'] for d in seq] for seq in self.data]))
        def print_formatted(self):
            print("{:10s}\t".format('Type'), end = '')
            print("{:10s}\t{:15s}\t{:15}\t{:15}".format('Source', 'Unit', 'km/h', 'm/s'))
            print('-' * 75)
            for seq in self.data:
                for d in seq:
                    print("{:10s}\t".format(d['type'].upper()), end = '')
                    print("{:10s}\t{:15s}\t{:15.8s}\t{:15.8s}".format(d['source'], d['value']['unit'], str(d['value']['km/h']), str(d['value']['m/s'])))


class Strength(Base_entity):
        def __init__(self, data = None, document_level = True):
            self.document_level = document_level
            self.data = data
            self.name = 'Strength'
        def __repr__(self):
            return str(self.format([[d['source'] for d in seq] for seq in self.data]))

class Surface(Base_entity):
        def __init__(self, data = None, document_level = True):
            self.document_level = document_level
            self.data = data
            self.name = 'Surface'
        def __repr__(self):
            return str(self.format([[d['source'] for d in seq] for seq in self.data]))

class Surface_tension(Base_entity):
        def __init__(self, data = None, document_level = True):
            self.document_level = document_level
            self.data = data
            self.name = 'Surface_tension'
        def __repr__(self):
            return str(self.format([[d['source'] for d in seq] for seq in self.data]))

class Temperature(Base_entity):
        def __init__(self, data = None, document_level = True):
            self.document_level = document_level
            self.data = data
            self.name = 'Temperature'
        def __repr__(self):
            return str(self.format([[d['source'] for d in seq] for seq in self.data]))

class Time(Base_entity):
        def __init__(self, data = None, document_level = True):
            self.document_level = document_level
            self.data = data
            self.name = 'Time'
        def __repr__(self):
            return str(self.format([[d['source'] for d in seq] for seq in self.data]))

class Url(Base_entity):
        def __init__(self, data = None, document_level = True):
            self.document_level = document_level
            self.data = data
            self.name = 'URL'
        def __repr__(self):
            return str(self.format([[d['source'] for d in seq] for seq in self.data]))

class Voltage(Base_entity):
        def __init__(self, data = None, document_level = True):
            self.document_level = document_level
            self.data = data
            self.name = 'Voltage'
        def __repr__(self):
            return str(self.format([[d['source'] for d in seq] for seq in self.data]))

class Volume(Base_entity):
        def __init__(self, data = None, document_level = True):
            self.document_level = document_level
            self.data = data
            self.name = 'Volume'
        def __repr__(self):
            return str(self.format([[d['source'] for d in seq] for seq in self.data]))
