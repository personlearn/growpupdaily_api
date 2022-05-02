import configparser;

def getConfig(section,key):
    cf=configparser.ConfigParser()
    cf.read("config.ini")
    value=cf.get(section,key)
    return value