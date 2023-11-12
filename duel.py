from c_engine import C_Engine
from l_engine import L_Engine
from generator import Generator
from utils.message import Message
from utils._dcdl_dico_str import file
import random as rd

class DuelGenerator:
    
    CHIFFRES = 0
    LETTRES = 1
    CALCUL = 2
    
    state = 1
    
    all_words = file.split("\n")
    all_words10 = [w for w in all_words if len(w)==10]
    
    operations = "+-x:"
    
    @staticmethod
    def chiffres()->str:
        sol = ""
        target = 0
        res = -1
        
        Message("Recherche d'un coup de chiffres intéressant...")
        
        i=-1
        while sol.count("=")<5 or res!=target: # 5 may be too long to compute and too hard to find afterwards, maybe 4 is better
            i+=1
            print("\tProcessing"+"."*(i%4)+" "*4,end="\r",flush=True)
            chiffres = Generator.next(Generator.CHIFFRES)
            target = int(chiffres.split()[0])
            res,sol = C_Engine.solve(target,[int(n) for n in chiffres.split()[1:]])
        print(" "*50)
        Message("Coup de chiffres obtenu !")
        return chiffres
    
    @staticmethod
    def lettres()->str:
        sol=[]
        
        Message("Recherche d'un coup de lettres intéressant...")
        while len(sol)!=1:
            word = rd.choice(DuelGenerator.all_words10)
            _,sol = L_Engine.solve(word)
            
        Message("Coup de lettres obtenu !")
        return sol[0]
    
    @staticmethod
    def _get_default_calcul()->str:
        Message("Generation d'opérations à effectuer...")
        x1 = rd.randint(100,1000)
        previous_op = ""
        previous_number=-1
        out = f"(((({x1}"
        
        n = 0 # we perform in total 5 calculations
        maxit = 50 # we stop after 1000 iterations
        
        while n < 5:
            
            maxit -= 1
            if maxit<0:
                return DuelGenerator._get_default_calcul() # we restart
            if x1==0:
                return DuelGenerator._get_default_calcul() # we restart
            
            op = rd.choice(DuelGenerator.operations)
            
            if op==previous_op:
                continue
            
            
            match op:
                case "+":
                    # check operation is nice #
                    if x1>=800: # don't increase x1 if x1 too high
                        continue
                    if x1 <=100 and x1 >= 10: # if x1 low, we prefer to do other operations
                        continue
                    
                    # choose x2 #
                    x2 = rd.randint(100,1000-x1) # x1 + x2 <= 1000 & x2 >= 100
                    
                    # check that we aren't using the same number twice in a row
                    if x2==previous_number:
                        continue
                    previous_number = x2
                    
                    # update #
                    x1 += x2
                    out += f"{op}{x2})"
                    n += 1
                    previous_op = op
                    
                    
                case "-":
                    # check operation is nice #
                    if x1<=60: # don't decrease x1 if x1 too low and prefer other operations
                        continue
                    
                    # choose x2 #
                    x2 = rd.randint(30,x1) # we don't want negative results / we don't want x2 too low
                    # OK because x1 > 60
                    
                    # check that we aren't using the same number twice in a row
                    if x2==previous_number:
                        continue
                    previous_number = x2
                    
                    x1 -= x2
                    out += f"{op}{x2})"
                    n += 1
                    previous_op = op
                
                case "x":
                    # check operation is nice #
                    if x1>=300: # don't increase x1 if already high
                        continue
                    
                    x2 = rd.randint(2,1000//x1) # x1*x2<=1000
                    # OK because x1 < 300 => 1000//x1 >= 3
                    
                    # check that we aren't using the same number twice in a row
                    if x2==previous_number:
                        continue
                    previous_number = x2
                    
                    x1 *= x2
                    out += f"{op}{x2})"
                    n += 1
                    previous_op = op
                
                case ":":
                    # check operation is nice #
                    if x1<=30: # else the division is not interesting
                        continue
                    
                    divisors = [i for i in range(2,100) if x1%i==0] # don't want divisors above 100 else we know instantly that res is 1
                    if len(divisors)==0:
                        continue
                    
                    x2 = rd.choice(divisors)
                    # OK because previous check
                    
                    # check that we aren't using the same number twice in a row
                    if x2==previous_number:
                        continue
                    previous_number = x2
                    
                    x1 //= x2
                    out += f"{op}{x2})"
                    n += 1
                    previous_op = op
        
        return out[:-1] # remove the last parenthesis
    
    @staticmethod
    def calculs()->tuple:
        """
        Returns:
            tuple: result (int), operations (str)
        """
        calculs = ""
        Message("Recherche d'un calcul intéressant...")
        found = False
        
    
        while not found:
            
            calculs = DuelGenerator._get_default_calcul()
            # let's check that the calculations are not too easy or too weird #
            
            conditions = [
                calculs.count("+")<3,
                calculs.count("-")<3,
                calculs.count("x")<3,
                calculs.count(":")<3,
                calculs.count("+")>0,
                calculs.count("-")>0,
                (calculs.count("x")+calculs.count(":"))>=2,
            ]
            #print(conditions)
            found = all(conditions)
        
        Message("Calcul intéressant trouvé !","OK")
            
        return calculs
    
    @staticmethod
    def next()->str:
        """
        Class that allows the generation of random duels. Starts with calculations, then letters, then numbers, and loops after that
        
        >>> DuelGenerator.next() # "((((913-431)+445):3)+519):6"
        >>> DuelGenerator.next() # "medicament"
        >>> DuelGenerator.next() # "449 10 2 5 4 7 25"
        """
        DuelGenerator.state+=1
        match DuelGenerator.state%3:
            case DuelGenerator.CHIFFRES:
                print(f"{Message.red}La recherche d'un coup de chiffres peut prendre quelques secondes...{Message.reset}")
                return DuelGenerator.chiffres()
            case DuelGenerator.LETTRES:
                return DuelGenerator.lettres()
            case DuelGenerator.CALCUL:
                return DuelGenerator.calculs()
        
        
        
        
        

if __name__=="__main__":
    Message.ignore = ["LOG","OK "]
    
    for _ in range(5):
        DuelGenerator.chiffres()
        print()
    
        