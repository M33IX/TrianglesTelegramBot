from dataclasses import dataclass
import math


@dataclass
class Triangle:
    sideA: float
    sideB: float
    sideC: float
    angleA: float
    angleB: float
    angleC: float

    def __init__(self, sideA: float, sideB: float, sideC: float) -> None:
        self.sideA = sideA
        self.sideB = sideB
        self.sideC = sideC
        if not self.isPossible():
            raise Exception("Треугольник с данными сторонами не может существовать")
        self.angleA, self.angleB, self.angleC = self.calculateAngles()
    
    def isPossible(self) -> bool:
        """Проверка треугольнка на возможность его существования"""
        return ((self.sideA + self.sideB >= self.sideC) and (self.sideA + self.sideC >= self.sideB) and (self.sideB + self.sideC >= self.sideA))
    
    def calculateAngles(self) -> tuple[float, float, float]:
        """Вычисляет углы треугольника по его сторонам"""
        angleA = math.degrees(math.acos((self.sideB**2 + self.sideC**2 - self.sideA**2) / (2 * self.sideB * self.sideC)))
        angleB = math.degrees(math.acos((self.sideA**2 + self.sideC**2 - self.sideB**2) / (2 * self.sideA * self.sideC)))
        angleC = math.degrees(math.acos((self.sideA**2 + self.sideB**2 - self.sideC**2) / (2 * self.sideA * self.sideB)))
        return (angleA, angleB, angleC)
    
    def perimeter(self) -> float:
        """Вычисляет периметр треугольника"""
        return self.sideA + self.sideB + self.sideC
    
    def type(self) -> str:
        """Возвращает тип тругольника"""
        result = ""
        if self.sideA == self.sideB == self.sideC:
            result = "Равносторонний и"
        elif self.sideA == self.sideB or self.sideA == self.sideC or self.sideB == self.sideC:
            result = "Равнобедренный и"
        else: 
            result = "Разносторонний и "
        
        if int(self.angleA) < 90 and int(self.angleB) < 90 and int(self.angleC) < 90:
            result += "остроугольный треугольник"
        elif int(self.angleA == 90) or int(self.angleB == 90) or int(self.angleC == 90):
            result += "прямоугольный треугольник"
        else:
            result += "тупоугольный треугольник"
        return result
    
    def area(self) -> float:
        """Вычисляет площадь треугольника"""
        s = self.perimeter() / 2
        return math.sqrt(s * (s - self.sideA) * (s - self.sideB) * (s - self.sideC))
    
    def heights(self) -> tuple[float, float, float]:
        """Вычилсяет высоты треугольника"""
        area = self.area()
        heightA = 2 * area / self.sideA
        heightB = 2 * area / self.sideB
        heightC = 2 * area / self.sideC
        return (heightA, heightB, heightC)
    
    def medians(self) -> tuple[float, float, float]:
        """Вычилсяет медианы треугольника"""
        medianA = 0.5 * math.sqrt(2 * self.sideB**2 + 2 * self.sideC**2 - self.sideA**2)
        medianB = 0.5 * math.sqrt(2 * self.sideA**2 + 2 * self.sideC**2 - self.sideB**2)
        medianC = 0.5 * math.sqrt(2 * self.sideA**2 + 2 * self.sideB**2 - self.sideC**2)
        return(medianA, medianB, medianC)
    
    def bisectrix(self) -> tuple[float, float, float]:
        """Вычилсяет биссектрисы треугольника"""
        s = self.area() / 2
        bisectorA = (2 / (self.sideB + self.sideC)) * math.sqrt(self.sideB * self.sideC * s * (s - self.sideA))
        bisectorB = (2 / (self.sideA + self.sideC)) * math.sqrt(self.sideA * self.sideC * s * (s - self.sideB))
        bisectorC = (2 / (self.sideA + self.sideB)) * math.sqrt(self.sideA * self.sideB * s * (s - self.sideC))
        return (bisectorA, bisectorB, bisectorC)
