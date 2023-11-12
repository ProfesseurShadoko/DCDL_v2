
from c_engine import C_Engine
from l_engine import L_Engine
from generator import Generator
from utils.message import Message
from duel import DuelGenerator


class API:
    
    letters = "abcdefghijklmnopqrstuvwxyz"
    
    CHIFFRES=0
    LETTRES=1
    VERIFICATION=2
    
    @staticmethod
    def solve(request:str)->tuple:
        """
        The function first verifies that the request is valid (contains only spaces and either some lower case lettres without accents or numbers)
        Then it infers what that of operation it has to do (calculate, find a word or verify a word)
        Finally, it returns accordingly:
        - (API.CHIFFRES,result:int,operations:str)
        - (API.LETTRES,score:int,word:str)
        - (API.VERIFICATION,validity:bool,initial_word:str)
        
        Args:
            request (str): request

        Returns:
            tuple: (int,int,str) or None if invalid request
        """
        
        Message("Traitement de la requête : "+request,"LOG")
        request = request.strip().lower()
        special_chars = API.special_chars(request)
        if len(special_chars)>0:
            Message("Caractères invalides : "+special_chars,"ERROR")
            return
        
        # check if input corresponds to numbers
        if all(char.isdigit() for char in request.replace(" ","")):
            target = int(request.split(" ")[0])
            numbers = [int(n) for n in request.split(" ")[1:]]
            if len(numbers)>0:
                return (API.CHIFFRES,*C_Engine.solve(target,numbers))
            else:
                Message("Requête invalide, seul le compte cible a pu être identifié","ERROR")
                return
        
        
        elif all([char.lower() in API.letters for char in request.replace(" ","")]):
            request = request.replace(" ","")
            
            if len(request)==10:
                return (API.LETTRES,*L_Engine.solve(request.replace(" ","")))
            else:
                return (API.VERIFICATION,L_Engine.dicotree.contains(request),request)
        
        else:
            Message("La requête comporte à la fois chiffres et lettres","ERROR")
    
    
    @staticmethod
    def special_chars(request:str)->str:
        """
        Returns:
            str: all characters that are neither numbers or letters. Empty string "" if no special chars
        """
        numbers_in_request = [int(n) for n in request if n.isdigit()]
        for n in numbers_in_request:
            request = request.replace(str(n),"")
        
        invalid = [char for char in request if not char.lower() in f"{API.letters} "]
        return "".join(invalid)
    
    @staticmethod
    def random(typ:int,vowls:int=5)->str:
        """
        Args:
            typ (int): API.CHIFFRES or API.LETTRES
            vowls (int, optional): use in case typ=API.LETTRES. Defaults to 5. Sets the number of vowls of the ouptut (2<vowls<8)

        Returns:
            str: string of random turn adapted to API.solve(...)
        
    >>> API.random(API.LETTRES,vowls=4) # "tnlkeoamsa"
    >>> API.random(API.CHIFFRES) # "111 8 25 1 5 2 8"
        """
        return Generator.next(typ,vowls)
    
    @staticmethod
    def duel()->str:
        """
        >>> DuelGenerator.next() # "((((913-431)+445):3)+519):6"
        >>> DuelGenerator.next() # "medicament"
        >>> DuelGenerator.next() # "449 10 2 5 4 7 25"
        """
        return DuelGenerator.next()
    
    


        