class ExtractClass:
    def get_date_items(self):
        return self.get_by_filter('type', 'date')

    def get_distance_items(self):
        return self.get_by_filter('type', 'distance')

    def get_duration_items(self):
        return self.get_by_filter('type', 'duration')

    def get_electric_power_items(self):
        return self.get_by_filter('type', 'electric power')

    def get_hex_color_items(self):
        return self.get_by_filter('type', 'hex color')

    def get_interval_items(self):
        return self.get_by_filter('type', 'interval')

    def get_ip_items(self):
        return self.get_by_filter('type', 'ip')

    def get_ipv6_items(self):
        return self.get_by_filter('type', 'ipv6')

    def get_light_intensity_items(self):
        return self.get_by_filter('type', 'light intensity')

    def get_mail_items(self):
        return self.get_by_filter('type', 'mail')

    def get_mass_items(self):
        return self.get_by_filter('type', 'mass')

    def get_mass_by_volume_items(self):
        return self.get_by_filter('type', 'mass by volume')

    def get_mol_items(self):
        return self.get_by_filter('type', 'mol')

    def get_money_items(self):
        return self.get_by_filter('type', 'money')

    def get_ordinal_items(self):
        return self.get_by_filter('type', 'ordinal')

    def get_percent_items(self):
        return self.get_by_filter('type', 'percent')

    def get_phone_items(self):
        return self.get_by_filter('type', 'phone')

    def get_pressure_items(self):
        return self.get_by_filter('type', 'pressure')

    def get_set_items(self):
        return self.get_by_filter('type', 'set')

    def get_speed_items(self):
        return self.get_by_filter('type', 'speed')

    def get_strength_items(self):
        return self.get_by_filter('type', 'strength')

    def get_surface_items(self):
        return self.get_by_filter('type', 'surface')

    def get_surface_tension_items(self):
        return self.get_by_filter('type', 'surface tension')

    def get_temperature_items(self):
        return self.get_by_filter('type', 'temperature')

    def get_time_items(self):
        return self.get_by_filter('type', 'time')

    def get_url_items(self):
        return self.get_by_filter('type', 'url')

    def get_voltage_items(self):
        return self.get_by_filter('type', 'voltage')

    def get_volume_items(self):
        return self.get_by_filter('type', 'volume')

    def get_happiness_items(self):
        return self.get_by_filter('type', 'happiness')

    def get_sadness_items(self):
        return self.get_by_filter('type', 'sadness')

    def get_fear_items(self):
        return self.get_by_filter('type', 'fear')

    def get_disgust_items(self):
        return self.get_by_filter('type', 'disgust')

    def get_anger_items(self):
        return self.get_by_filter('type', 'anger')

    def get_surprise_items(self):
        return self.get_by_filter('type', 'surprise')

    def get_judgement_items(self):
        return self.get_by_filter('type', 'judgement')
