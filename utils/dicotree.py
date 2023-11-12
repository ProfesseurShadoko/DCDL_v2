
from utils.message import Message,Timer

class DicoTree:
    """
    ### Attributes:
        root (DicoNode): root of the tree
    
    ### Methods:
        add(word:str) -> None: adds word to the tree by recursively creating the next node, starting from self.root
        contains(word:str) -> bool: returns True if the requested word has been added to the dictionnary
        get_words() -> list[str]: returns the list of all words
        get_node(prefix:str) -> DicoNode or None: returns the node corresponding to the prefix, or None if it does not exist
        
    ### Static methods:
        from_file(filename:str) -> DicoTree: creates DicoTree from words in filename (format: one word per line)
        
    """
    root:'DicoNode'
    
    def __init__(self):
        self.root = DicoNode()
    
    def add(self,word:str) -> None:
        self.root.add(word)
    
    def contains(self,word:str) -> bool:
        return self.root.contains(word)
    
    def __contains__(self,word:str) -> bool:
        return self.contains(word)
    
    @staticmethod
    def from_string(file:str)->'DicoTree':
        Message(f"Initialisation du dictionnaire...")
        timer = Timer().start()
        
        d = DicoTree()
        file = file.split("\n")
        for line in file:
            if len(line)>0:
                d.add(line.strip())
            
        Message(f"Dictionnaire initialisé après {timer.time:.2f} s","OK")
        return d
        
        
class DicoNode:
    # description of class properties and methods and all
    """
    Attributes:
        children (list[DicoNode or None]): list of children nodes (one for each letter, so the length of the list is 26)
        is_valid (bool): True if node corresponds to a valid word
    
    Methods:
        add(word:str) -> None: adds word to the tree by recursively creating the next node
        contains(suffix:str) -> bool: returns True if the path defined by the letters of the suffix leads to a node corresponding to a valid word
    """
    
    children:list['DicoNode'] 
    is_valid:bool
    
    def __init__(self) -> None:
        self.children = [None]*26
        self.is_valid = False
    
    def add(self,word:str) -> None:
        """
        If the word is empty, then the node corresponds to a complete word, is_valid is set to True. 
        Otherwise, the first letter of the word is used to create the next node, and the rest of the word is added to this node.
        
        Args:
            word (str): lower case string (or empty string)
        """
        # if we add "" then it means that the node corresponds to a complete word
        if len(word) == 0:
            self.is_valid = True
            return
        
        # check if string is only letters and lower case
        assert word.isalpha() and word.islower(),f"Invalid word '{word}': must be only lower case letters"
        
        index = ord(word[0]) - ord('a')
        if self.children[index] is None:
            self.children[index] = DicoNode()
        self.children[index].add(word[1:])
        

    def contains(self,suffix:str)->bool:
        """
        Args:
            suffix (str): lower case string (or empty string)

        Returns:
            bool: True if the path defined by the letters of the suffix leads to a node corresponding to a valid word
        """
        if len(suffix)==0:
            return self.is_valid
        
        assert suffix.isalpha() and suffix.islower(),f"Invalid word '{suffix}': must be only lower case letters"
        
        index = ord(suffix[0]) - ord('a')
        
        if self.children[index] is None:
            return False
        else:
            return self.children[index].contains(suffix[1:])

    
    
    
    