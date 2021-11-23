from dataclasses import dataclass
from typing import ClassVar


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        """Отправить сообщение о тренировке."""
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


@dataclass
class Training:
    """Базовый класс тренировки."""

    action: int
    duration: float
    weight: float
    M_IN_KM: ClassVar[int] = 1000
    LEN_STEP: ClassVar[int] = 0.65

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        self.distance = self.action * self.LEN_STEP / self.M_IN_KM
        return self.distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        self.mean_spead = self.get_distance() / self.duration
        return self.mean_spead

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError("Subclasses should implement this!")

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__, self.duration,
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories()
                           )


@dataclass
class Running(Training):
    """Тренировка: бег."""

    action: int
    duration: float
    weight: float

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        COEFF_RUN_SPEED: int = 18
        COEFF_RUN_CORRECT: int = 20
        spent_calories = ((COEFF_RUN_SPEED * self.get_mean_speed()
                          - COEFF_RUN_CORRECT) * self.weight
                          / self.M_IN_KM * self.duration * 60)
        return spent_calories


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    action: int
    duration: float
    weight: float
    height: float

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        COEFF_WLK_WEIGHT = 0.035
        COEFF_WLK_SPEED = 0.029
        spent_calories = ((COEFF_WLK_WEIGHT * self.weight
                          + (self.get_mean_speed() ** 2
                           // self.height)
                          * COEFF_WLK_SPEED * self.weight)
                          * self.duration * 60)
        return spent_calories


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""

    action: int
    duration: float
    weight: float
    length_pool: float
    count_pool: int
    LEN_STEP: ClassVar[float] = 1.38

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        self.mean_spead = (self.length_pool * self.count_pool
                           / self.M_IN_KM / self.duration)
        return self.mean_spead

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coeff_calorie_swm_1: float = 1.1
        coeff_calorie_swm_2: int = 2
        self.spent_calories = ((self.get_mean_speed() + coeff_calorie_swm_1)
                               * coeff_calorie_swm_2 * self.weight)
        return self.spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_type = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}
    if workout_type in training_type:
        return training_type[workout_type](*data)
    else:
        raise ValueError('Accept only "SWM", "RUN", "WLK" values')


def main(training: Training) -> str:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
