from abc import ABC, abstractmethod
from hashlib import new

class PaymentMethod(ABC):

    @abstractmethod
    def get_details(self):
        pass

    @abstractmethod
    def pay(self,amount):
        pass

class RazorpayCardPayment(PaymentMethod):

    def __init__(self, card_number, amount):
        self.card_number=card_number
        self.amount=amount

    def get_details(self):
        print(f"payment method RazorPayCard done via card number{self.card_number}")

    def pay(self,amount):
        self.amount=amount
        print(f"{self.amount} paid using RazorPayCard")
        return True


class RazorpayUPIPayment(PaymentMethod):

    def __init__(self, upi_id, amount):
        self.upi_id=upi_id
        self.amount=amount

    def get_details(self):
        print(f"payment method RazorPayUPI done via id :{self.upi_id}")

    def pay(self,amount):
        self.amount=amount
        print(f"{self.amount} paid using RazorPayUPI")
        return True



class StripeCardPayment(PaymentMethod):

    def __init__(self, card_number, amount):
        self.card_number=card_number
        self.amount=amount

    def get_details(self):
        print(f"payment method StripeCard done via id :{self.card_number} and amount ₹{self.amount}")

    def pay(self,amount):
        self.amount=amount
        print(f"{self.amount} paid using Stripe card")
        return True

class StripeUPIPayment(PaymentMethod):

    def __init__(self, upi_id, amount):
        self.upi_id=upi_id
        self.amount=amount

    def get_details(self):
        print(f"payment method StripeUPI done via id :{self.upi_id} and amount ₹{self.amount}")

    def pay(self,amount):
        self.amount=amount
        print(f"{self.amount} paid using StripeUPI payment")
        return True

class FactoryPaymentMethod(ABC):
    @abstractmethod
    def get_payment_object(cls,method_type,**kwargs):
        pass



class RazorpayFactory(FactoryPaymentMethod):

   
    Factory= {"card":RazorpayCardPayment,
              "upi":RazorpayUPIPayment}

        
    @classmethod
    def get_payment_object(cls,method_type):
        return  cls.Factory[method_type]

class StripepayFactory(FactoryPaymentMethod):
    Factory={"card":StripeCardPayment,
             "upi":StripeUPIPayment}

    @classmethod
    def get_payment_object(cls,method_type,**kwargs):
        return cls.Factory[method_type]

#Task3 

class Aggregator(ABC):

    @abstractmethod
    def call_get_payment_object(self,method_type,amount,**kwargs):
        pass

class RazorpayAggregator(Aggregator):

    def pay(self,amount):
        print(f"Payment of ₹{amount} done using Razorpay aggregator")
        return True
    def call_get_payment_object(cls,method_type,amount: int,**kwargs):
        processing_fee=(0.02)*float((amount))
        payment=RazorpayFactory()
        obj =payment.get_payment_object(method_type,**kwargs)(int(id),amount) # razorpayFactory-> RazorpayCardPayment or RazorpayUPIPayment-(id,amount)
        amount=float(amount)+float(processing_fee)
       
class StripeAggregator(Aggregator):
    def pay(self,amount):
        print(f"Payment of ₹{amount} done using Stripe aggregator")
        return True

    def call_get_payment_object(self,method_type,amount:int,**kwargs):
        processing_fee=(0.029)*float((amount))
        payment=StripepayFactory()# abc=123
        
        import pdb;pdb.set_trace()
        stripe =  payment.get_payment_object(method_type,**kwargs)(int(upi_id), amount)
        amount=float(amount)+float(processing_fee)
        stripe.pay(amount)

class AggregatorFactory:
    factory={
        "stripe":StripeAggregator,
        "razorpay":RazorpayAggregator
    }

    @classmethod
    def get_aggregator_object(cls,aggregator_name):
        return cls.factory[aggregator_name.lower()]
    
amount=input("Enter the amount: ")
print("Select aggregator : ")
print("razorpay and Stripe")
agg=str(input("Enter the choice : "))
method=str(input("card or upi :"))

card_num=None
upi_id=None
if method=="card":
    card_num=input("Enter card number:")
elif method=="upi":
    upi_id=input("Enter upi id : ")
new_payment=AggregatorFactory.get_aggregator_object(agg)
#new payment is a class razorpay agregator or stripe aggregator
payment_object= new_payment().call_get_payment_object(method,amount,card_number=card_num,upi_id=upi_id)