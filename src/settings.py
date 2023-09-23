class SettingsLoader:
    def __init__(self):
        with open("settings.properties", 'r') as f:
            lines = f.readlines()
            if len(lines) < 1:
                f.close()
                raise ValueError("Invalid settings file")
            self.__type = lines[0].split('=')[1].strip()
            f.close()

    def get_type(self):
        return self.__type
