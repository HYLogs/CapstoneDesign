class Observer:
    def notify(self) -> None:
        raise NotImplementedError("구현되지 않은 메소드입니다.")

class Subject:  
    def addObserver(self, observer:Observer) -> None:
        raise NotImplementedError("구현되지 않은 메소드입니다.")
    
    def removeObserver(self, observer:Observer) -> None:
        raise NotImplementedError("구현되지 않은 메소드입니다.")
    
    def notifyObservers(self) -> None:
        raise NotImplementedError("구현되지 않은 메소드입니다.")
    