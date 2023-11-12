from utils.message import Timer,Message
from utils.dicotree import DicoTree,DicoNode
from utils._dcdl_dico_str import file

class L_Engine:
    """
    Static methods:
        solve(letters:str)->(int,list[str]) : returns the score and the list of words with highest score after about 4ms
    
    Example:
        >>> score,words = L_Engine.solve("drenlanted")
        >>> print(score) # 8
        >>> print(words) # ['etendard','lanterne']
        
    """
    
    dicotree = DicoTree.from_string(file)
    
    letters:list[str]
    current_node:DicoNode
    current_word:str
    remaining:list[bool]
    best_words:list[str]
    
    def __init__(self,letters:str):
        
        assert len(letters)==10 and letters.isalpha() and letters.islower(),f"Invalid set of letters '{letters}': must be exactly 10 lower case letters"
        self.letters = list(letters)
        self.letters.sort()
        self.remaining = [True]*len(self.letters)
        self.current_word = ""
        self.current_node = self.dicotree.root
        self.all_words = []
    
    def run(self)->'L_Engine':
        
        # look at the current word
        if self.current_node.is_valid:
            self.all_words.append(self.current_word)
        
        # look at the possible next words
        for i in range(len(self.letters)):
            if self.remaining[i]:
                char = self.letters[i]
                if self.current_node.children[ord(char)-ord('a')] is not None:
                    self.remaining[i]=False
                    self.current_word+=char
                    parent_node = self.current_node
                    self.current_node = self.current_node.children[ord(char)-ord('a')]
                    
                    self.run()
                    
                    self.current_node = parent_node
                    self.remaining[i]=True
                    self.current_word = self.current_word[:-1]
        return self
    
    @staticmethod
    def solve(letters:str)->tuple[int,list[str]]:
        Message("Recherche pour <"+letters+">")
        timer = Timer().start()
        all_words = L_Engine.get_all_words(letters)
        best_words = [w for w in all_words if len(w)==max([len(w) for w in all_words])]
        timer.stop()
        Message(f"Solution trouvée en {timer.time*1000:.2f} ms","OK")
        return len(best_words[0]),best_words
    
    @staticmethod
    def get_all_words(letters:str)->list[str]:
        out = L_Engine(letters).run()
        return list(set(out.all_words))
    
    


if __name__=="__main__":
    print(L_Engine.dicotree.contains("etendard"))
    score,words = L_Engine.solve("drenlanted")
    print(score,words)