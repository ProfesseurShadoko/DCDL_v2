from utils.message import Timer,Message


class C_Engine:
    """
    Attributes:
        compute_best:bool : if False, the first solution found is returned, else the shortest solution is returned
    Static Methods:
        solve(target:int,numbers:list[int])->(int,str) : returns the nearest result and a string of the operations to do
    
    Example:
        >>> result,solution = C_Engine.solve(987,[6,25,3,7,1,10])
        >>> print(result) # 987
        >>> print(solution)
        >>> # 25*6=150
        >>> # 150+1=151
        >>> # 151-10=141
        >>> # 141*7=987
    """
    
    memory:dict[str,(int,str)] = {}
    compute_best:bool = True # if False, the first solution found is returned, else the shortest solution is returned
    
    @staticmethod
    def _key(target:int,numbers:list[int])->str:
        """
        Returns:
            str: for {target=987,numbers=[6,25,3,7,1,10]} returns "987 1 3 6 7 10 25" (# unique key for a given target and numbers)
        """
        return f"{target} {' '.join([str(n) for n in sorted(numbers)])}"
    
    @staticmethod
    def _solve_memoized(numbers:list,target:int)->tuple[int,str]:
        """returns (result:int,solution:str)"""
        key = C_Engine._key(target,numbers)
        
        #let's not twice the same thing (this is O(1))
        if key in C_Engine.memory:
            return C_Engine.memory[key]
        
        #base case
        if len(numbers)==1:
            return numbers[0],""
        
        #let's find best result by searching over the cards
        best_result=numbers[0]
        
        for number in numbers:
            if abs(number-target)<abs(best_result-target):
                best_result=number
        best_solution=""
        
        for n1 in numbers.copy(): # super important ! else the rest will modify the list and shuffle it, the result will then be wrong !
            if best_result==target:
                if not C_Engine.compute_best:
                    break
            numbers.remove(n1)
            
            for n2 in numbers.copy():
                if best_result==target:
                    if not C_Engine.compute_best:
                        break
                numbers.remove(n2)
                
                n_max,n_min=max(n1,n2),min(n1,n2)
                
                for ope in ["+","-","//","*"]:
                    
                    if ope!="//" or n_max%n_min==0:
                        new_card = eval(f"{n_max}{ope}{n_min}")
                        
                        if new_card!=0 and not new_card in [n1,n2]:
                            numbers.append(new_card)
                            result,solution = C_Engine._solve_memoized(numbers,target)
                            
                            solution=f"{n_max}{ope}{n_min}={new_card}\n"+solution
                            
                            if abs(result-target)<=abs(best_result-target):
                                if abs(result-target) < abs(best_result-target) or len(solution) < len(best_solution):
                                    #une meilleure solution ou une solution plus courte
                                    
                                    best_result=result
                                    best_solution=solution
                                    
                            numbers.remove(new_card)
                
                numbers.append(n2)
            numbers.append(n1)
        
        C_Engine.memory[C_Engine._key(target,numbers)]=best_result,best_solution
        
        return best_result,best_solution.replace("//","/").replace("\n\n","\n")
    
    @staticmethod
    def solve(target:int,numbers:list[int])->tuple[int,str]:
        """
        Args:
            target (int): ex 987
            numbers (list[int]): ex [6,25,3,7,1,10]

        Returns:
            tuple[int,str]: ex (987,"25*6=150\n150+1=151\n151-10=141\n141*7=987")
        """
        Message("Calculs pour <"+str(target)+":"+"-".join([str(n) for n in numbers])+">")
        C_Engine.memory={}
        timer = Timer().start()
        result,solution = C_Engine._solve_memoized(numbers,target)
        Message(f"Solution trouvée après {timer.stop():.2f} s","OK")
        return result,solution


        
        
    
        