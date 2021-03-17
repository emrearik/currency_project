# Libraries were added to get exchange rate
from xml.etree.ElementTree import parse
from urllib.request import urlopen

# Currency rate is taken from TCMB website and parsed XML.
def fetchXMLData(index):
    url = "https://www.tcmb.gov.tr/kurlar/today.xml"
    response = urlopen(url)
    xmldoc = parse(response)
    root = xmldoc.getroot()
    currencyName, forexBuying ,forexSelling,crossRateOther = root[index][1].text,root[index][3].text,root[index][4].text,root[index][8].text
    return {
        "currencyName": currencyName,
        "forexBuying": forexBuying,
        "forexSelling": forexSelling,
        "crossRateOther": crossRateOther
    }

# The TurkishLira class was defined
class TurkishLira:
    
    # Money,piece,banknotes,currency that include were created constructor.
    # Money variable was sended to structure of constructor

    def __init__(self, money):
        self.banknotes = [{"name": "Itri", "price": 100}, {"name": "Fatma Aliye Topuz", "price": 50},
                        {"name": "Cahit Arf", "price": 10}]
        self.money = money
        self.piece = 0
        self.moneyCurrency = "TL"
    
    # A temporary value equal to money was created.All banknotes are visited, and the number of banknotes were calculated.
    # IMPORTANT: Out of banknot list values are not calculated.
    def calculate(self,bank):
        temp = self.money
        for i in range(len(bank)):
            if (temp // bank[i]["price"] != 0):
                self.piece = temp // bank[i]["price"]
                temp %= bank[i]["price"]
                print(f'{self.piece} {bank[i]["name"]} ', end="")
        print()

    # Calculate function is called, and results is printed the screen.    
    def printCurrency(self):
        print(f'\n-Your Anahtar result {self.money} {self.moneyCurrency} is:')
        for j in range(len(self.banknotes)):
            if (self.money // self.banknotes[j]["price"] != 0):
                self.calculate(self.banknotes[j::])

# UsDollar class extends from the TurkishLira class.The constructor variables is changed.
class UsDollar(TurkishLira):
    def __init__(self, money):
        super(UsDollar, self).__init__(money)
        self.banknotes = [{"name": "Independence Hall", "price": 100}, {"name": "United States Capitol", "price": 50},
                        {"name": "U.S. Treasury", "price": 10}]
        self.moneyCurrency = "USD"

# Euro class extends from the TurkishLira class.The constructor variables is changed.
class Euro(TurkishLira):
    def __init__(self, money):
        super(Euro, self).__init__(money)
        self.banknotes = [{"name": "Modern 20th century", "price": 500}, {"name": "Baroque & Rococo", "price": 100},
                        {"name": "Romanesque", "price": 10}]
        self.moneyCurrency = "EURO"

# Special functions work to catch errors.
class InvalidSelection(Exception):
    pass
class InvalidCurrency(Exception):
    pass
class InvalidObject(Exception):
    pass
class InvalidAmount(Exception):
    pass

# The function uses to the print results.
def printAllMoney(turkishLira,euro,usDollar):
    turkishLira.printCurrency()
    euro.printCurrency()
    usDollar.printCurrency()

# The stages occur in this function.
def process(selection):
    euroData = fetchXMLData(3)
    dollarData = fetchXMLData(0)
    # Exchange rates are rounded to the nearest number.
    euroTLCurrency = round(float(euroData["forexSelling"]), 2)
    dollarTLCurrency = round(float(dollarData["forexSelling"]), 2)
    euroDollarCurrency = round(float(euroData["crossRateOther"]), 2)
    
    # Transactions for currency selection.
    if(selection ==1):
        try:
             currency = str(input("Please Enter Currency (TL,EURO,USD):"))
             if(currency.upper()=="TL" or currency.upper()=="EURO" or currency.upper()=="USD"):
                try:
                    amount = int(input("Please Enter the Amount:"))
                    if(amount<0):
                        raise InvalidAmount("InvalidAmount")
                except InvalidAmount:
                    print("Please enter the positive value.")
             else:
                amount=-1
                raise InvalidCurrency("InvalidCurrency")
        except InvalidCurrency:
            print("Please enter one of the TL, EURO, USD values.")

        if(amount>0):
            # Transactions for TL selection.
            if(currency.upper()== "TL"):
                turkishLira = TurkishLira(amount)
                euro = Euro(round(float(amount/euroTLCurrency)))
                usDollar = UsDollar(round(float(amount/ dollarTLCurrency)))

                printAllMoney(turkishLira,euro,usDollar)
            # Transactions for EURO selection.
            elif (currency.upper() == "EURO"):
                euro = Euro(amount)
                turkishLira = TurkishLira(round(float(amount * euroTLCurrency)))
                usDollar = UsDollar(round(float(amount * euroDollarCurrency)))

                printAllMoney(turkishLira, euro, usDollar)
            # Transactions for USD selection.
            elif (currency.upper() == "USD"):
                usDollar = UsDollar(amount)
                turkishLira = TurkishLira(round(float(amount * dollarTLCurrency)))
                euro = Euro(round(float(amount / euroDollarCurrency)))

                printAllMoney(turkishLira,euro,usDollar)
        else:
            False

    # Transactions for goods selection.
    elif (selection ==2):
        index = -1
        # Object list is create. Static variables are add.
        objectList = [{"objectName": "CAR", "objectPrice": 30000}, {"objectName": "PLANE", "objectPrice": 45000},
                      {"objectName": "DOOR", "objectPrice": 3000},
                      {"objectName": "NOTEBOOK", "objectPrice": 7500},
                      {"objectName": "PENCIL", "objectPrice": 1000}]

        print("Object List:", end= " ")
        for i in range(len(objectList)):
            print(f"{objectList[i]['objectName']} {objectList[i]['objectPrice']}TL",end=" ")

        try:
            # It is calculated according to the entered object.
            object = input("\nPlease Enter Object:")
            for k in range(len(objectList)):
                if (objectList[k]["objectName"]==object.upper()):
                    index = k
            if(index!=-1):
                print(f"The value of a {objectList[index]['objectName']} is {objectList[index]['objectPrice']}")
                turkishLira = TurkishLira(objectList[index]["objectPrice"])
                euro = Euro(round(float(objectList[index]["objectPrice"] / euroTLCurrency)))
                usDollar = UsDollar(round(float(objectList[index]["objectPrice"] / dollarTLCurrency)))

                printAllMoney(turkishLira, euro, usDollar)
            else:
                raise InvalidObject("InvalidObject")
        except InvalidObject:
            print("You made a wrong object.")


# MAIN FUNCTION
if __name__ == '__main__':
    # The loop is created.
    while True:
        print("*************************")
        print("Please select your option\n1 for Currency \n2 for Goods")

        # From the user is asked to choose. Depending on the selection, it goes to the process function.
        try:
            selection = int(input('Selection: '))
            if (selection == 1 or selection == 2):
                 process(selection)
            else:
                 raise InvalidSelection("InvalidSelection")
        except ValueError:
            print("Please enter integer variable.")
        except InvalidSelection:
            print("You made a wrong choice. Please choose 1 or 2 number.")
