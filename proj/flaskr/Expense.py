class Expense:
    def __init__(self, amount, date, profitOrLoss, total):
        self.amount = amount
        self.date = date
        self.profitOrLoss = profitOrLoss


    def setAmount(self, a):
        self.amount = a

    def getAmount(self):
        return self.amount

    def setDate(self,d):
        self.date = d

    def getDate(self):
        return self.date

    def setProfitOrLoss(self, p):
        self.profitOrLoss = p

    def getProfitOrLoss(self):
        self.profitOrLoss

