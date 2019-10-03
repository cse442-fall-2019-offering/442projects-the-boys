class User:
    def __init__(self,prof):
        self.prof = prof





    def addExpense(self, expense):
        if expense.profitOrLoss == True:
            expense.total = expense.total + expense.amount
        else:
            expense.total = expense.total - expense.amount

