from . import ROBO_SEMANTICS, ROBO_LANGUAGE


class Success:

    def __init__(self, engine, validationCheckMap, hintRulesMap):
        self.engine = engine
        self.validationCheckMap = validationCheckMap
        self.hintRulesMap = hintRulesMap

    @staticmethod
    def from_json(json, engine):
        validationCheck = {}
        hintRules = {}
        if json and 'validationCheck' in json:
            validationCheck = json['validationCheck']
        if json and 'hintRules' in json:
            hintRules = json['hintRules']
        return Success(engine, validationCheck, hintRules)

    def beforeRun(self):
        pass

    def afterRun(self):
        # parseResult = lang.parseString(line)
        # expr = parseResult[0]
        # result = expr.eval(world, sem)
        pass


    def isSuccess(self):
        return True

    def getHints(self):
        return {
            "premise": "not beacon(2,13)",
            "value": "hint.auto.beaconInWrongSpot",
            "type": "world",
            "x": -1,
            "y": -1
        }
