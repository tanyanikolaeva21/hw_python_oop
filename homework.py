from dataclasses import dataclass
from typing import Dict, Tuple


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке: тип тренировки, время тренировки
    в ч., дистанция в км, скорость км/ч, затраченные калории в Ккал."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        """Получаем сообщение."""
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    HOUR_IN_MIN: int = 60

    def __init__(
            self,
            action: float,
            duration: float,
            weight: float
    ) -> None:
        """action - количество шагов (гребков), duration -
        время тренировки в ч., weightв - вес спортсмена."""
        self.action = action
        self.duration = duration
        self.weight = weight

    def duration_in_min(self) -> float:
        """Перевод времени тренировки в минуты"""
        return (self.duration * self.HOUR_IN_MIN)

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return (self.action * self.LEN_STEP / self.M_IN_KM)

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.get_distance() / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            self.__class__.__name__, self.duration, self.get_distance(),
            self.get_mean_speed(), self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    COEFF_CALORIE_1: int = 18
    COEFF_CALORIE_2: int = 20

    def get_spent_calories(self) -> float:
        return ((self.COEFF_CALORIE_1
                * self.get_mean_speed() - self.COEFF_CALORIE_2)
                * self.weight / self.M_IN_KM
                * self.duration_in_min()
                )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    COEFF_CALORIE_3: float = 0.035
    COEFF_CALORIE_4: float = 0.029
    COEFF_CALORIE_5: int = 2

    def __init__(
            self,
            action: float,
            duration: float,
            weight: float,
            height: float
    ) -> None:
        """height - рост."""
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return ((self.COEFF_CALORIE_3 * self.weight + (self.get_mean_speed()
                ** self.COEFF_CALORIE_5 // self.height) * self.COEFF_CALORIE_4
                * self.weight) * self.duration_in_min()
                )


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    COEFF_CALORIE_6: float = 1.1
    COEFF_CALORIE_7: int = 2

    def __init__(
            self,
            action: float,
            duration: float,
            weight: float,
            length_pool: float,
            count_pool: int
    ) -> None:
        """length_pool - длина бассейна в м., count_pool- кол-во раз,
        которые проплыл бассейн спортсмен"""
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:

        return ((self.get_mean_speed() + self.COEFF_CALORIE_6)
                * self.COEFF_CALORIE_7 * self.weight)


def read_package(workout_type: str, data: list):
    """Прочитать данные полученные от датчиков."""

    training_type: Dict[str, Tuple[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type not in training_type:
        raise ValueError('Неизвестный тип тренировки' + ' ' + workout_type)
    return training_type[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""

    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180])
    ]
    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
