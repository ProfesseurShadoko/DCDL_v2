
from datetime import datetime
from time import perf_counter

class Message:
    green = "\033[32m"
    red = "\033[31m"
    blue="\033[34m"
    reset = "\033[0m"
    lightblue = "\033[96m"
    color=blue
    active=True
    ignore = []
    
    _type_to_color = {
        "LOG":"blue",
        "ERROR":"red",
        "OK":"green"
    }
    
    def __init__(self,message:str,msg_type:str="LOG"):
        """

        Args:
            message (str): displayed message (after .upper() is applied)
            msg_type (str, optional): type of the message (must be one of the following: "LOG","OK","ERROR"). Defaults to "LOG".
        """
        
        self._set_color(msg_type)
        message = message.upper()
        msg_type = msg_type.replace("OK","OK ").replace("ERROR","ERR")
        
        if Message.active and not (msg_type in Message.ignore):
            print(f"{self.color}[{msg_type}]{self.reset} ~ {self.date_str()} --> \"{self.color}{message}{self.reset}\"")
    
    def _set_color(self,msg_type:str)->None:
        assert msg_type in self._type_to_color.keys(), f"Invalid message type {msg_type} (valid message types are {self._type_to_color.keys()})"
        self.color = self.__getattribute__(self._type_to_color[msg_type])
    
    @staticmethod
    def disable(disable:bool=True)->None:
        Message.active = not disable
        
    @staticmethod
    def date_str():
        return "["+datetime.now().strftime('%Y-%m-%d  %H:%M:%S')+"]"

class Timer:
    
    start_time:int=None
    stop_time:int=None
    
    def __init__(self):
        pass
    
    def start(self)->'Timer':
        self.stop_time = None
        self.start_time = perf_counter()
        return self
    
    def stop(self)->float:
        self.stop_time = perf_counter()
        return self.stop_time - self.start_time
    
    @property
    def time(self)->float:
        if self.stop_time is None:
            return perf_counter() - self.start_time
        else:
            return self.stop_time - self.start_time
    
        
    
    

if __name__=="__main__":
    Message("Starting something...")
    Message("Something went wrong!",msg_type="ERROR")
    Message("Starting from scratch",msg_type="LOG")
    Message("Work done!",msg_type="OK")