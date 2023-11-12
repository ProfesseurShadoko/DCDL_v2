import random as rd
from utils.message import Timer

######################
# CREATE LETTRES SET #
######################

vowls_multiplicity = {
    "a":165,
    "e":386,
    "i":160,
    "o":146,
    "u":135,
    "y":8,
}

vowls = []
for letter, multiplicity in vowls_multiplicity.items():
    for _ in range(multiplicity):
        vowls.append(letter)

consonants_multiplicity = {
    "b":28,
    "c":50,
    "d":71,
    "f":34,
    "g":26,
    "h":23,
    "j":7,
    "k":2,
    "l":95,
    "m":50,
    "n":138,
    "p":55,
    "q":22,
    "r":111,
    "s":130,
    "t":98,
    "v":31,
}

consonants = []
for letter, multiplicity in consonants_multiplicity.items():
    for _ in range(multiplicity):
        consonants.append(letter)


class Generator:
    """
    Class that allows the generation of random numbers and letters turns
    
    >>> Generator.next(Generator.LETTRES,vowls=4) # "tnlkeoamsa"
    >>> Generator.next(Generator.CHIFFRES) # "111 8 25 1 5 2 8"
    """
    
    _vowls = vowls
    _consonants = consonants
    _numbers = [i for i in range(1,11)]*2 + [25,50,75,100]
    
    CHIFFRES=0
    LETTRES=1
    
    @staticmethod
    def next(typ:int,vowls:int=5)->str:
        rd.shuffle(Generator._numbers)
        rd.shuffle(Generator._vowls)
        rd.shuffle(Generator._consonants)
        
        match typ:
            case Generator.CHIFFRES:
                target = rd.randint(100,999)
                return f"{target} {' '.join([str(c) for c in Generator._numbers[:6]])}"
            
            case Generator.LETTRES:
                assert 3 <= vowls and vowls <= 7, f"Invalid number of vowls, does not respect 2<{vowls}<8"
                out = Generator._vowls[:vowls]+Generator._consonants[:10-vowls]
                rd.shuffle(out)
                return "".join(out)

if __name__=="__main__":
    
    print(Generator.next(Generator.LETTRES,4))
    print(Generator.next(Generator.CHIFFRES))

                
        
        