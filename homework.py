class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:

        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:

        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: float = 1000.0
    MIN_IN_H: float = 60.0

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:

        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""

        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""

        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""

        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories()
                           )


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER: float = 18.0
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:

        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                 + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / self.M_IN_KM * self.duration * self.MIN_IN_H)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    CALORIES_WEIGHT_MULTIPLIER: float = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER: float = 0.029
    KMH_IN_MSEC: float = round(1000 / 3600, 3)
    CM_IN_M: float = 100.0

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:

        super().__init__(action, duration, weight)
        self.height = height

    def get_distance(self) -> float:

        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_spent_calories(self) -> float:
        duration_minutes = self.duration * self.MIN_IN_H
        height_in_metres = self.height / self.CM_IN_M
        speed_in_mps = self.get_mean_speed() * self.KMH_IN_MSEC

        return ((self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                + (speed_in_mps ** 2 / height_in_metres)
                * self.CALORIES_SPEED_HEIGHT_MULTIPLIER * self.weight)
                * duration_minutes)


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    MULTIPLIER_LENGTH_POOL: float = 1.1
    MULTIPLIER_COUNT_POOL: float = 2.0

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int,
                 ) -> None:

        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:

        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:

        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:

        return ((self.get_mean_speed() + self.MULTIPLIER_LENGTH_POOL)
                * self.MULTIPLIER_COUNT_POOL
                * self.weight * self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    training_types = {'SWM': Swimming,
                      'RUN': Running,
                      'WLK': SportsWalking}

    return training_types[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""

    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)

        main(training)
