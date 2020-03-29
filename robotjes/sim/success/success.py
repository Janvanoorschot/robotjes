from .validation_check_cnf import ValidationCheckCNF


class Success:

    def __init__(self, validationCheckMap, hintRulesMap):
        self.validationCheckMap = validationCheckMap
        self.hintRulesMap = hintRulesMap
        self.validationCNF = ValidationCheckCNF.fromMap(self.validationCheckMap)

    @staticmethod
    def from_json(json):
        validationCheck = {}
        hintRules = {}
        if json and 'validationCheck' in json:
            validationCheck = json['validationCheck']
        if json and 'hintRules' in json:
            hintRules = json['hintRules']
        return Success(validationCheck, hintRules)
