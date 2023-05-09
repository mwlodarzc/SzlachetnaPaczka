from configparser import ConfigParser


def config(filename="database.ini", section="postgresql"):
    parser = ConfigParser()
    parser.read(filename)
    if not parser.has_section(section):
        raise AttributeError(f"Section{section} is not found in the {filename}")
    params = parser.items(section)
    return {param[0]: param[1] for param in params}
