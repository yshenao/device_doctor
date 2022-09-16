from application.apps.testpoint.db.dal import DBProxy
import json


class Rule(object):
    def __init__(self):
        self.MysqlClient = DBProxy()
        rules = self.MysqlClient.get_rule_ids()
        rule_ids = []
        for r in rules:
            rule_ids.append(r.rule_id)
        self.rule_ids = json.dumps(rule_ids)
