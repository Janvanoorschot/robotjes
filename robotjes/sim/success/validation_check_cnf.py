from .validation_compiler import ValidationCompiler

class ValidationCheckCNF:

    def __init__(self):
        self.preRunProgramExpression = []
        self.runWorldExpression = []
        self.postRunProgramExpression = []
        self.postRunWorldExpression = []
        self.postRunUsageExpression = []

    @staticmethod
    def fromMap(map):
        preRunProgramStr = map.get('preRunProgram', "")
        runWorldStr = map.get('runWorld', "")
        postRunProgramStr = map.get('postRunProgram', "")
        postRunWorldStr = map.get('postRunWorld', "")
        postRunUsageStr = map.get('postRunWorld', "")
        vcc = ValidationCheckCNF()
        vcc.preRunProgramExpression = ValidationCompiler.toCNFArray(preRunProgramStr)
        vcc.runWorldExpression = ValidationCompiler.toCNFArray(runWorldStr)
        vcc.postRunProgramExpression = ValidationCompiler.toCNFArray(postRunProgramStr)
        vcc.postRunWorldExpression = ValidationCompiler.toCNFArray(postRunWorldStr)
        vcc.postRunUsageExpression = ValidationCompiler.toCNFArray(postRunUsageStr)
        return vcc



