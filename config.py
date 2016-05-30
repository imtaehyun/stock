import configparser

config_file_name = "config.dat"

class StockConfig:

    def __init__(self):
        self.config = configparser.ConfigParser()

    def save(self, **kwargs):
        user = kwargs['user']
        server = kwargs['server']

        if user:
            self.config.add_section("User")
            self.config.set("User", "id", user['id'])
            self.config.set("User", "pwd", user['pwd'])
            self.config.set("User", "certpwd", user['certpwd'])
            self.config.set("User", "acctpwd", user['acctpwd'])

        if server:
            self.config.add_section("Server")
            self.config.set("Server", "host", server['host'])
            self.config.set("Server", "port", str(server['port']))
            self.config.set("Server", "type", str(server['type']))

        with open(config_file_name, "w") as configfile:
            self.config.write(configfile)
            print("config 파일 작성")

    def load(self):
        user = {}
        server = {}

        if self.config.read(config_file_name):
            # config 파일이 존재하는 경우
            user["id"] = self.config["User"]["id"]
            user["pwd"] = self.config["User"]["pwd"]
            user["certpwd"] = self.config["User"]["certpwd"]
            user["acctpwd"] = self.config["User"]["acctpwd"]

            server["host"] = self.config["Server"]["host"]
            server["port"] = int(self.config["Server"]["port"])
            server["type"] = int(self.config["Server"]["type"])
        else:
            # config 파일이 존재하지 않는 경우
            user["id"] = ""
            user["pwd"] = ""
            user["certpwd"] = ""
            user["acctpwd"] = ""

            server["host"] = "demo.ebestsec.co.kr"
            server["port"] = 20001
            server["type"] = 0

        return {
            "user": user,
            "server": server
        }
