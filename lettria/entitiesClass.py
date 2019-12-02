from .sharedClass import SharedClass

class Person(SharedClass):
        def __init__(self, data = None):
            self.data = data
        def __repr__(self):
            return [d['source'] for d in self.data]
        def print_formatted(self):
            print("{:10s}\t{:10s}".format('Type','Source'))
            print('-' * 20)
            for d in self.data:
                print("{:10s}\t".format(d['type'].upper()), end = '')
                print("{:10s}".format(d['source']))

class Location(SharedClass):
        def __init__(self, data = None):
            self.data = data
        def __repr__(self):
            return [d['source'] for d in self.data]
        def print_formatted(self):
            print("{:10s}\t{:10s}".format('Type','Source'))
            print('-' * 20)
            for d in self.data:
                print("{:10s}\t".format(d['type'].upper()), end = '')
                print("{:10s}".format(d['source']))

class Date(SharedClass):
        def __init__(self, data = None):
            self.data = data
        def __repr__(self):
            return [d['source'] for d in self.data]
        def print_formatted(self):
            print("{:10s}\t{:10s}\t{:20s}\t{:20s}".format('Type','Source', 'ISO', 'timestamp'))
            print('-' * 70)
            for d in self.data:
                print("{:10s}\t".format(d['type'].upper()), end = '')
                print("{:10s}\t{:20s}\t{:20s}".format(d['source'], d['value']['ISO'], str(d['value']['timestamp'])))

class Distance(SharedClass):
        def __init__(self, data = None):
            self.data = data
        def __repr__(self):
            return [d['source'] for d in self.data]
        def print_formatted(self):
            print("{:10s}\t".format('Type'), end = '')
            print("{:10s}\t{:15s}\t{:15}\t{:15}".format('Source', 'Unit', 'Meter', 'Miles'))
            print('-' * 75)
            for d in self.data:
                print("{:10s}\t".format(d['type'].upper()), end = '')
                print("{:10s}\t{:15s}\t{:15.10s}\t{:15.10s}".format(d['source'], d['value']['unit'], str(d['value']['meter']), str(d['value']['miles'])))

class Duration(SharedClass):
        def __init__(self, data = None):
            self.data = data
        def __repr__(self):
            return [d['source'] for d in self.data]

class Electric_power(SharedClass):
        def __init__(self, data = None):
            self.data = data
        def __repr__(self):
            return [d['source'] for d in self.data]

class Hex_color(SharedClass):
        def __init__(self, data = None):
            self.data = data
        def __repr__(self):
            return [d['source'] for d in self.data]

class Frequency(SharedClass):
        def __init__(self, data = None):
            self.data = data
        def __repr__(self):
            return [d['source'] for d in self.data]

class Interval(SharedClass):
        def __init__(self, data = None):
            self.data = data
        def __repr__(self):
            return [d['source'] for d in self.data]
        def print_formatted(self):
            print("{:10s}\t".format('Type'), end = '')
            print("{:10s}\t{:20s}\t{:20s}\t{:15s}\t{:15s}\t{:15s}".format('Source', 'Start', 'End', 'days', 'hours', 'minutes'))
            print('-' * 120)
            for d in self.data:
                print("{:10s}\t".format(d['type'].upper()), end = '')
                print("{:10s}\t{:20s}\t{:20s}\t{:15.8s}\t{:15.8s}\t{:15.8s}".format(\
                    d['source'], d['value']['start']['ISO'], d['value']['end']['ISO'],\
                    str(d['value']['duration']['start_end']['days']),\
                    str(d['value']['duration']['start_end']['hours']),\
                    str(d['value']['duration']['start_end']['minutes'])))

class Ip(SharedClass):
        def __init__(self, data = None):
            self.data = data
        def __repr__(self):
            return [d['source'] for d in self.data]
        def print_formatted(self):
            print("{:10s}\t".format('Type'), end = '')
            print("{:10s}\t{:15s}\t{:15}\t{:25}".format('Source', 'Country', 'City', 'Organisation'))
            print('-' * 100)
            for d in self.data:
                print("{:10s}\t".format(d['type'].upper()), end = '')
                print("{:10s}\t{:15s}\t{:15s}\t{:25s}".format(d['source'], d['value']['country'], d['value']['city'], d['value']['org']))

class Ipv6(SharedClass):
        def __init__(self, data = None):
            self.data = data
        def __repr__(self):
            return [d['source'] for d in self.data]

class Light_intensity(SharedClass):
        def __init__(self, data = None):
            self.data = data
        def __repr__(self):
            return [d['source'] for d in self.data]

class Mail(SharedClass):
        def __init__(self, data = None):
            self.data = data
        def __repr__(self):
            return [d['source'] for d in self.data]

class Mass(SharedClass):
        def __init__(self, data = None):
            self.data = data
        def __repr__(self):
            return [d['source'] for d in self.data]

class Mass_by_volume(SharedClass):
        def __init__(self, data = None):
            self.data = data
        def __repr__(self):
            return [d['source'] for d in self.data]

class Mol(SharedClass):
        def __init__(self, data = None):
            self.data = data
        def __repr__(self):
            return [d['source'] for d in self.data]

class Money(SharedClass):
        def __init__(self, data = None):
            self.data = data
        def __repr__(self):
            return [d['source'] for d in self.data]

class Ordinal(SharedClass):
        def __init__(self, data = None):
            self.data = data
        def __repr__(self):
            return [d['source'] for d in self.data]

class Percent(SharedClass):
        def __init__(self, data = None):
            self.data = data
        def __repr__(self):
            return [d['source'] for d in self.data]

class Phone(SharedClass):
        def __init__(self, data = None):
            self.data = data
        def __repr__(self):
            return [d['source'] for d in self.data]

class Pressure(SharedClass):
        def __init__(self, data = None):
            self.data = data
        def __repr__(self):
            return [d['source'] for d in self.data]

class Set(SharedClass):
        def __init__(self, data = None):
            self.data = data
        def __repr__(self):
            return [d['source'] for d in self.data]

class Speed(SharedClass):
        def __init__(self, data = None):
            self.data = data
        def __repr__(self):
            return [d['source'] for d in self.data]
        def print_formatted(self):
            print("{:10s}\t".format('Type'), end = '')
            print("{:10s}\t{:15s}\t{:15}\t{:15}".format('Source', 'Unit', 'km/h', 'm/s'))
            print('-' * 75)
            for d in self.data:
                print("{:10s}\t".format(d['type'].upper()), end = '')
                print("{:10s}\t{:15s}\t{:15.8s}\t{:15.8s}".format(d['source'], d['value']['unit'], str(d['value']['km/h']), str(d['value']['m/s'])))


class Strength(SharedClass):
        def __init__(self, data = None):
            self.data = data
        def __repr__(self):
            return [d['source'] for d in self.data]

class Surface(SharedClass):
        def __init__(self, data = None):
            self.data = data
        def __repr__(self):
            return [d['source'] for d in self.data]

class Surface_tension(SharedClass):
        def __init__(self, data = None):
            self.data = data
        def __repr__(self):
            return [d['source'] for d in self.data]

class Temperature(SharedClass):
        def __init__(self, data = None):
            self.data = data
        def __repr__(self):
            return [d['source'] for d in self.data]

class Time(SharedClass):
        def __init__(self, data = None):
            self.data = data
        def __repr__(self):
            return [d['source'] for d in self.data]

class Url(SharedClass):
        def __init__(self, data = None):
            self.data = data
        def __repr__(self):
            return [d['source'] for d in self.data]

class Voltage(SharedClass):
        def __init__(self, data = None):
            self.data = data
        def __repr__(self):
            return [d['source'] for d in self.data]

class Volume(SharedClass):
        def __init__(self, data = None):
            self.data = data
        def __repr__(self):
            return [d['source'] for d in self.data]
