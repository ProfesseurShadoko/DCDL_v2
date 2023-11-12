import os
from utils.message import Message
from api import API
import random as rd

# CREATE EXE FILE #
# pyinstaller --onefile --icon=utils/DCDL_logo.ico shell.py

Message.ignore = ["LOG","OK "]

shell_help = f"""
{Message.lightblue}

Bienvenue dans la console DCDL ! Voici quelques commandes pour l'utiliser :

>>> <10 lettres> : résoudre le coup de lettres correspondant
>>> <cible> <nbr1> <nbr2> ... : résoudre le compte correspondant (les nombres doivent être séparés par des espaces !)
>>> <mot> : vérifier si le mot est dans le dictionnaire DCDL (remarque : un mot de 10 lettres sera considéré comme un coup de lettres à résoudre, mais si le mot est valide, il apparaîtra dans la solution)
>>> -c ou c : propose un coup de chiffres aléatoire
>>> -l ou l : propose un coup de lettres aléatoire, avec un nombre de voyelles aléatoires
>>> -d ou d : propose un duel (calcul mental, 10 lettres à trouver ou coup de chiffres difficile)
>>> -s ou s : donne la solution au précédent duel ou coup de chiffres ou de lettres aléatoires proposé par le programme
>>> -q ou q : quitter le programe

Bon jeu !

{Message.reset}
"""



class ExitShell(Exception):
    pass

class Shell:
    
    cached_solution = ""
    
    def __init__(self):
        os.system("cls")
        print(shell_help)
    
    def run(self):
        try:
            while True:
                self.loop()
        except ExitShell:
            Message("Programme terminé","OK")
            return
        except KeyboardInterrupt:
            Message.ignore = []
            Message("Traitement de la requête interrompu","LOG")
            Message.ignore = ["LOG","OK "]
            self.run()
        except:
            Message("Une erreur fatale s'est produite. Vérifier la validité de la requête.","ERROR")
            self.run()
    
    def quit(self)->None:
        raise ExitShell()
    
    # COMPUTE SHELL RESPONSE #
    def get_random_l(self)->str:
        return API.random(API.LETTRES,rd.choice([3,3,4,4,4,5,5,5,5,6,6,7]))
    
    def get_response_l(self,lettres:str,typ:int=None,res:int=None,sol:str=None)->str:
        if typ is None and res is None and sol is None:
            typ,res,sol = API.solve(lettres)
            
        assert typ==API.LETTRES, "Wrong type of solution, should be letters"
        return f"J'ai {Message.green}{res}{Message.reset} lettres avec : " + " ".join(sol)
    
    def get_random_c(self)->str:
        return API.random(API.CHIFFRES)
    
    def get_response_c(self,chiffres,typ:int=None,res:int=None,sol:str=None)->str:
        if typ is None and res is None and sol is None:
            typ,res,sol = API.solve(chiffres)
            
        assert typ==API.CHIFFRES, "Wrong type of solution, should be numbers"
        target = int(chiffres.split(" ")[0])
        
        out = f"Le compte est bon ! Voici comment il fallait procéder pour obtenir {Message.green}{res}{Message.reset} : \n\n" if res==target\
            else f"Il n'était pas possible de faire mieux que {Message.red}{res}{Message.reset}. Voici comment il fallait procéder :\n\n"
        out += "\n".join("|\t"+ line for line in sol.split("\n")[:-1])
        return out
    
    def get_response_v(self,mot:str,typ:int=None,res:bool=None,sol:str=None)->str:
        if typ is None and res is None and sol is None:
            typ,res,sol = API.solve(mot)
            
        assert typ==API.VERIFICATION, "Wrong type of solution, should be verification"
        return f"'{Message.green}{sol}{Message.reset}' est un mot valide !" if res else f"'{Message.red}{sol}{Message.reset}' n'est pas un mot valide !"
    
    def handle_duel(self,duel:str)->None:
        if "(" in duel:
            
            # COMPUTE STEP-BY-STEP SOLUTION #
            evaluable_duel = duel.replace("x","*").replace(":","//")
            res = eval(evaluable_duel)
            # this is calculation step by step
            duel_steps = duel.replace("(","").split(")")
            evaluable_duel_steps = evaluable_duel.replace("(","").split(")")
            
            n_next = eval(evaluable_duel_steps[0])
            solution = f"{duel_steps[0]}={n_next}\n"
            
            for step in range(1,5):
                n_previous = n_next
                n_next = eval(f"{n_previous}{evaluable_duel_steps[step]}")
                solution += f"{n_previous}{duel_steps[step]}={n_next if step != 4 else Message.green+str(n_next)+Message.reset}\n"
            
            Shell.cached_solution = f"Il fallait trouver {Message.green}{res}{Message.reset} !\n\n"+"\n".join(["|\t"+step for step in solution.split("\n")[:-1]])
            
            # DISPLAY PROBLEM #
            print(f"\n{Message.lightblue}Effectuer les opérations suivantes :{Message.reset}\n")
            print("\t"+duel)
            return
        
        else:
            typ,res,sol = API.solve(duel)
            
            match typ:
                case API.LETTRES:
                    print(f"{Message.lightblue}Trouver l'unique mot de 10 lettres avec le tirage suivant :{Message.reset}\n")
                    letters = list(duel.upper())
                    rd.shuffle(letters)
                    print("\t"+" ".join(letters))
                    Shell.cached_solution = self.get_response_l(duel,typ,res,sol)
                    
                case API.CHIFFRES:
                    print(f"{Message.lightblue}Trouver le bon compte pour le tirage suivant :{Message.reset}\n")
                    print("\t",duel[:3]," =>",duel[3:])
                    Shell.cached_solution = self.get_response_c(duel,typ,res,sol)
    
    # DISPLAY #
    def display_cached_solution(self)->None:
        if len(Shell.cached_solution)==0:
            Message("Aucun duel, coup de chiffres ou de lettres aléatoire présent dans l'historique","ERROR")
        else:
            print(Shell.cached_solution)
            
            
    # MAIN LOOP #    
    def loop(self)->None:
        
        msg = input(f"\n{Message.lightblue}>>> ")
        print(Message.reset)
        
        # QUIT #
        if "quit()" in msg or "exit()" in msg or "-q"in msg or msg.strip()=="q":
            return self.quit()
        
        if len(msg.replace(" ",""))==0:
            return None
        
        # RANDOM GENERATION #
        if msg.strip().replace("-","")=="l":
            lettres = self.get_random_l()
            Shell.cached_solution = self.get_response_l(lettres)

            return print("\t",
                " ".join(
                    list(
                        lettres.upper()
                    )
                )
            )
        
        if msg.strip().replace("-","")=="c":
            chiffres = API.random(API.CHIFFRES)
            Shell.cached_solution = self.get_response_c(chiffres)
            return print("\t",chiffres[:3]," =>",chiffres[3:])
        
        if msg.strip().replace("-","")=="d":
            duel = API.duel()
            return self.handle_duel(duel)
        
        if msg.strip().replace("-","")=="s":
            return self.display_cached_solution()
        
        # SOLVER #        
        response = API.solve(msg)
        
        if response is None:
            return
        
        typ,res,sol = response
        
        match typ:
            case API.CHIFFRES:
                return print(self.get_response_c(msg,typ,res,sol))
                
            case API.LETTRES:
                return print(self.get_response_l(msg,typ,res,sol))
                
            case API.VERIFICATION:
                return print(self.get_response_v(msg,typ,res,sol))
    
    
        
    

if __name__=="__main__":
    Shell().run()