from glob import glob
import utils
import os
import oscm
import json
import requests
import urllib

endpoint_url = "http://52.34.230.77:9123/backend/"
put = "put/?"
get = "get/?"
SOFTWARE_CONFIG_NAME = "package.oscm"


def app_list_filter(item):
    return not (str(item).startswith(".") or str(item) == "node_modules")


def generate(initial=True):
    # get system config
    app_list = [p[:-1] for p in glob('*/')]
    app_list = filter(app_list_filter, app_list)
    for app in app_list:
        app_ret = Application()
        app_ret.resolve(app)
        utils.add_section(app)
        utils.set_property(app_ret.name, "version", app_ret.version)
        if len(app_ret.extras.keys()) > 0:
            for key in app_ret.extras.keys():
                utils.set_property(app_ret.name, key,
                                   app_ret.extras.get(key, ""))
    return {"code": 1}


def determine_version(app):
    application = get_app(app)


def fetch_conf_dict(f_name):
    ret = {}
    f = open(f_name, "r")
    f_lines = map(lambda x: list(x.strip().split(",")), f.readlines())
    for i in f_lines:
        ret[str(i[0])] = str(i[1])
    return ret


def get_app(name):
    pass


def eclipseVersion(name):
    v_path = os.path.join(os.getcwd(), name, ".eclipseproduct")
    if not os.path.isfile(v_path):
        return "0"
    else:
        return filter(lambda x: x[0] == "version",
                      map(lambda x: x.strip().split("="),
                          open(v_path, "r").readlines()))[0][1]
        # return str(list(filter( lambda a: a[0] == "version" , list(map(lambda x: x.strip().split("="),open(v_path,"r").readlines()))))[1])


def intellijVersion(name):
    return "0"


def perforceVersion(name):
    return "0"


def studioVersion(name):
    return "0"


class Application:
    """A class specifying what application it is"""
    applist = ["eclipse", "intellij", "perforce", "android_studio"]
    appVersionFinder = {
        "eclipse": eclipseVersion,
        "intellij": intellijVersion,
        "perforce": perforceVersion,
        "android_studio": studioVersion
    }

    def __init__(self):
        self.name = ""
        self.version = "0"
        self.is_custom = False
        self.url = None
        self.cmd = None
        self.extras = {}

    def set_version(self, version):
        self.version = version

    def resolve_version(self, name):
        self.version = self.appVersionFinder.get(self.name, lambda x: "0")(name)

    def resolve(self, name):
        global endpoint_url, put
        endpoint = endpoint_url + put
        a = list(filter(lambda x: x in name, self.applist))
        if len(a) > 0:
            self.name = a[0]
            self.resolve_version(name)
            if self.name == "eclipse":
                self.url = "http://archive.eclipse.org/technology/epp/downloads/release/helios/SR2/eclipse-jee-helios-SR2-macosx-cocoa-x86_64.tar.gz"
                if str(raw_input(
                        'Do you want to add plugins to the eclipse folder?(Y/n)')).lower() == "y":
                    s = str(raw_input(
                        "Enter the plugin zip URLs separated by commas (,):"))
                    if len(s) > 0:
                        self.extras["plugins"] = s
            params = {"name": self.name, "version": self.version,
                      "os": utils.get_os(), "arch": utils.get_arch(),
                      "url": self.url}
            params = dict((k, v) for k, v in params.items() if v.lower() != 'n')
            response = requests.get(
                "%s%s" % (endpoint, urllib.urlencode(params)))
        else:
            conf_file = os.path.join(os.getcwd(), name, SOFTWARE_CONFIG_NAME)
            if os.path.isfile(conf_file):
                con = fetch_conf_dict(conf_file)
                self.is_custom = True
                self.custom_conf = con
                self.name = con['name']
                self.version = con['version']
                self.url = con['url']
                self.cmd = con['cmd']
                add_custom_soft_conf(con)
                params = {"name": self.name, "version": self.version,
                          "os": utils.get_os(), "arch": utils.get_arch(),
                          "command": self.cmd, "url": self.url,
                          "tag": con.get('tag', 'n')}
                params = dict(
                    (k, v) for k, v in params.items() if v.lower() != 'n')
                response = requests.get(
                    "%s%s" % (endpoint, urllib.urlencode(params)))
            else:
                oscm.call_command('addsoftware')
                result = None
                with open("my_file", 'r') as f:
                    try:
                        result = json.load(f)
                    # if the file is empty the ValueError will be thrown
                    except ValueError:
                        result = {}
                self.is_custom = True
                self.name = result['name']
                self.version = result['version']
                self.url = result.get('url', '')
                self.cmd = result.get('cmd', '')


if __name__ == "__main__":
    generate()
