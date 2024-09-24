#Bank class
class Bank:
    def __init__(self, bankName):
        self.bankName = bankName
        self.savingsDigits = 1001
        self.currentDigits = 2001
        self.accountList = [] #List for storing User's account objects.
        self.adminList = [] #List for storing admin's account objects.
        self.isBankrupt = False
        self.__loanBalance = 1000000
        self.loanState = True

    def createAccount(self, name, email, address, password, accountType, isAdmin = False):
        if isAdmin:
            # Create an admin account
            admin = Admin(name, email, address, password, self)
            self.adminList.append(admin)
            print(f"\nAdmin account created for {name}.")
            return True
        else:
            # Create a user account based on account type
            if accountType == 'savings':
                accountNumber = self.savingsDigits
                self.savingsDigits += 1 #incremented for next account number.
            elif accountType == 'current':
                accountNumber = self.currentDigits
                self.currentDigits += 1 #incremented for next account number.
            else:
                print('\n----> Invalid account type.')
                return False
            
            newAccount = User(name, email, address, password, accountType, accountNumber)
            self.accountList.append(newAccount)
            print(f'\n----> User acount created for {newAccount.name}. Account Number: {newAccount.accountNumber}')
            return True

    def viewAccounts(self):
        print(f'\n---> {self.bankName} Account Details: ')
        for account in self.accountList:
            print(f'Name: {account.name}.\nAccount Number: {account.accountNumber}.\nAccount Type: {account.accountType}.')
    
    def findAccount(self, accountNumber):
        for account in self.accountList:
            if account.accountNumber == accountNumber:
                return account

    def deleteUser(self, accountNumber):
        account = self.findAccount(accountNumber)
        if account:
            self.accountList.remove(account)
            print("\n----> Account was removed.")
        else:    
            print(f'\n----> No user was found with account number: {accountNumber}.')

    @property
    def TotalBalance(self):
        return sum(account.checkBalance for account in self.accountList)
    
    def loanFeatureState(self, state):
        if state == 'on':
            self.loanState = True
            print(f"\n----> Loan feature has been turned on.")
        else:
            self.loanState = False
            print(f"\n----> Loan feature has been turned off.")

    def declareBankrupt(self):
        self.isBankrupt = True

    def declareNotBankrupt(self):
        self.isBankrupt = False

    @property
    def LoanBalance(self):
        return self.__loanBalance
    
    @LoanBalance.setter
    def LoanBalance(self, amount):
        self.__loanBalance += amount

    def verifyUser(self, accountNumber, password):
        account = self.findAccount(accountNumber)
        if account:
            if password == account.getPassword:
                return account
            else:
                print('\n----> Incorrect password.')
        else:   
            print("\n----> No user found!")

    
    def verifyAdmin(self, email, password):
        for admin in self.adminList:
            if admin.email == email:
                if password == admin.getPassword:
                    return admin
                else:
                    print('\n----> Incorrect password.')
                    return
        print("\n----> No Admin found!")


#Person class
class Person:
    def __init__(self, name, email,  address):
        self.name = name
        self.email = email
        self.address = address

#Admin Class
class Admin(Person):
    def __init__(self, name, email, address, password, bankName):
        super().__init__(name, email, address)
        self.__passWord = password
        self.bankName = bankName

    def viewAccounts(self):
        self.bankName.viewAccounts()

    def deleteUser(self, accountNumber):
        self.bankName.deleteUser(accountNumber)

    def showTotalBalance(self):
        return self.bankName.TotalBalance

    def loanFeatureState(self, state):
        self.bankName.loanFeatureState(state)

    def declareBankrupt(self):
        self.bankName.declareBankrupt()

    def declareNotBankrupt(self):
        self.bankName.declareNotBankrupt()

    def showLoanBalance(self):
        return self.bankName.LoanBalance

    @property
    def getPassword(self):
        return self.__passWord


#User Class.
class User(Person):
    def __init__(self, name, email, address, password, accountType, accountNumber):
        super().__init__(name, email, address)
        self.__passWord = password
        self.accountType = accountType
        self.accountNumber = accountNumber
        self.__balance = 0
        self.transactions = [] #list for storing transaction history.
        self.loanCounter = 0
        self.loanAmount = 0

    def deposit(self, bankName, amount):
        if bankName.isBankrupt:
            print(f"\n----> Cannot deposit: {bankName.bankName} is bankrupt!")
        elif amount < 100:
            print(f"\n----> The minimum deposit amount is 100 taka.")
        else:
            self.__balance += amount #deposit done.
            self.transactions.append(f'Deposit : {amount}') #added the transaction in the transactions history. 
            print(f'\n----> {amount} taka was successfully deposited into your account.')

    def withdraw(self, bankName, amount):
        if bankName.isBankrupt:
            print(f"\n----> Cannot withdraw: {bankName.bankName} is bankrupt!")
        elif amount > self.__balance:
            print("\n----> Withdrawal failed: Insufficient funds in your account.")
        elif amount < 100:
            print(f"\n----> The minimum withdrawal amount is 100 taka.")
        else:
            self.__balance -= amount #withdraw done.
            self.transactions.append(f'Withdraw : {amount}') #added the transaction in the transactions history. 
            print(f"\n----> {amount} taka was successfully withdrawn.")

    @property
    def checkBalance(self):
        return self.__balance
    
    @property
    def getPassword(self):
        return self.__passWord

    def viewTransactions(self):
        print('\n-------Transaction History-------')
        for transac in self.transactions:
            print(f'{transac} Taka')

    def takeLoan(self, bankName, amount):
        if bankName.isBankrupt:
            print(f"\n----> Cannot take loan: {bankName.bankName} is bankrupt!")
        elif bankName.loanState == False:
            print(f"\n----> Loan facility is currently turned off.")
        elif self.loanCounter == 2:
            print(f'\n----> Sorry! Your loan-taking limit has been reached.')
        elif amount > bankName.LoanBalance: 
             print(f"\n----> Sorry! The bank doesn't have enough funds to provide this loan.")
        elif amount > 10000:
            print(f"\n----> Sorry! The maximum loan amount is 10,000 taka.")
        else:
            self.loanAmount +=  amount # Added to the user's loan balance.
            self.__balance += amount # Added to the user's current balance.
            bankName.LoanBalance += (-amount) # Deducted amount from bank's laon balance.
            self.transactions.append(f'Loan : {amount}') # Added loan transaction to history.
            self.loanCounter += 1  # Increment loan counter for the user
            print(f'\n----> {amount} taka as loan was added to your account.')

    def transferMoney(self, bankName, accountNumber, amount):
        if bankName.isBankrupt:
            print(f"\n----> Cannot transfer money: {bankName.bankName} is bankrupt!")
            return

        account = bankName.findAccount(accountNumber)
        if account:
            if amount > self.__balance:
                print(f"\n----> Insufficient balance for this transaction.")
            elif amount < 100:
                print(f"\n----> The minimum transferable amount is 100 taka.")
            else:
                self.__balance -= amount # Deduct from current user's balance.
                account.__balance += amount # Deposit to the recipient's account.
                self.transactions.append(f'Send Money: {amount}') # transaction added to history in sender's account.
                account.transactions.append(f'Received Money: {amount}') # transaction added to history in receiver's account.
                print(f"\n----> {amount} taka was successfully transferred to account {accountNumber}.")
        else:
            print(f"\n----> Account {accountNumber} not found.")

        

#main test program runs from here.
#creating bank object.
ektaBank = Bank("Ekta Bank")

#user function.
def userFucntion(user):
    while True:
        print('\n---------Welcome to your account---------')
        print('1. Deposit.')
        print('2. Withdraw.')
        print('3. Check Balance.')
        print('4. View Transactions.')
        print('5. Take Loan.')
        print('6. Transfer Money.')
        print('7. Exit.')

        choice = input('Enter your choice: ')

        if choice == '1':
            amount = int(input('Enter amount: '))
            user.deposit(ektaBank, amount) 
        elif choice == '2':
            amount = int(input('Enter amount: '))
            user.withdraw(ektaBank, amount)
                
        elif choice == '3':
            print('\n----> Account balance:', user.checkBalance)
        elif choice == '4':
            user.viewTransactions()
        elif choice == '5':
            amount = int(input('Enter amount: '))
            user.takeLoan(ektaBank, amount)
        elif choice == '6':
            accountNumber = int(input('Enter account number: '))
            amount = int(input('Enter amount: '))
            user.transferMoney(ektaBank, accountNumber, amount)
        elif choice == '7':
            break
        else:
            print("\n----> Invalid input!")

#admin function.
def adminFunction(admin):
    while True:
        print('\n---------Welcome to admin panel---------')
        print('1. Delete User Account.')
        print('2. View Accounts.')
        print('3. View Total Balance Of the Bank.')
        print('4. View Total Loan Balance Of the Bank.')
        print('5. Turn on or off the laon feature.')
        print('6. Declare bank as bankrupt.')
        print('7. Declare bank as not bankrupt.')
        print('8. Exit.')

        choice = input('Enter your choice: ')

        if choice == '1':
            accountNumber = int(input('Enter account number: '))
            admin.deleteUser(accountNumber)
        elif choice == '2':
            admin.viewAccounts()
        elif choice == '3':
            print('\n----> Bank Total balance:', admin.showTotalBalance())
        elif choice == '4':
            print('\n----> Bank Total Loan balance:', admin.showLoanBalance())
        elif choice == '5':
            state = input('Enter state (on/off): ').lower()
            admin.loanFeatureState(state)
        elif choice == '6':
            admin.declareBankrupt()
        elif choice == '7':
            admin.declareNotBankrupt()
        elif choice == '8':
            break
        else:
            print("----> Invalid input!")

#Log in fucntion.
def logIn():
    print("\n---> Please Login.")
    print("1. As Admin.")
    print("2. As User.")
    print('3. Return to main page.')
    choice = input("\nEnter your choice: ")

    if choice == '1':
        email = input("Enter email: ")
        password = input("Enter password: ")

        admin =  ektaBank.verifyAdmin(email,password)
        
        if admin:
            adminFunction(admin)
        return
    elif choice == '2':
        accountNumber = int(input("Enter account number: "))
        password = input("Enter password: ")

        user =  ektaBank.verifyUser(accountNumber, password)
        
        if user:
            userFucntion(user)
        return
    elif choice == '3':
        return
    else:
        print('\n----> Invalid input!')

#main function
while True:
    print(f"\n--------Welcome to {ektaBank.bankName}--------")
    print('\n1. Create account as admin.')
    print('2. Create account as user.')
    print('3. Login.')
    print('4. Exit.')
    choice = input('Enter your choice: ')

    if choice == '1':
        #create an admin account.
        name = input('Enter your name: ')
        address = input('Enter your address: ')
        email = input('Enter you email: ')
        password = input('Enter password: ')

        #create an admin account.
        if ektaBank.createAccount(name, email, address, password, None, True):
            #go to login page.
            logIn()
    elif choice == '2':
        #create a user account and call to login --> user function.
        name = input('Enter your name: ')
        address = input('Enter your address: ')
        email = input('Enter you email: ')
        password = input('Enter password: ')
        accountType = input('Enter account type(savings/current): ').lower()
        
        #create an user account.
        if ektaBank.createAccount(name, email, address, password, accountType):
            #got to login page.
            logIn()
    elif choice == '3':
        #call login function.
        logIn()
    elif choice == '4':
        print(f'\n--------Thanks for banking with {ektaBank.bankName}.--------')
        break
    else:
        print('\n----> Wrong input! Choose again.')