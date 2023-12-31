class InfoMessage:
    def __init__(self,
                 training_type,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f"Тип тренировки: {self.training_type}; "
                f"Длительность: {self.duration:.3f} ч.; "
                f"Дистанция: {self.distance:.3f} км; "
                f"Ср. скорость: {self.speed:.3f} км/ч; "
                f"Потрачено ккал: {self.calories:.3f}.")

    """Информационное сообщение о тренировке."""


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000
    H_IN_M = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        """Получить дистанцию в км."""
        return distance

    def get_mean_speed(self) -> float:
        mean_speed = self.get_distance() / self.duration
        """Получить среднюю скорость движения."""
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ):
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        calories = ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                     * self.get_mean_speed()
                     + self.CALORIES_MEAN_SPEED_SHIFT)
                    * self.weight / self.M_IN_KM * self.duration * self.H_IN_M)
        """Получить количество затраченных калорий."""
        return calories

    """Тренировка: бег."""
    pass


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(self, action: int, duration: int, weight: int, height: int):
        super().__init__(action, duration, weight)
        self.height = height

    KH_IN_MS = 0.278
    SM_IN_M = 100
    CALORIES_WEIGHT_MULTIPLIER = 0.035
    CALORIES_MEAN_SPEED_MULTIPLIER = 2
    CALORIES_WEIGHT_BRACKETS_MULTIPLIER = 0.029

    def get_spent_calories(self) -> float:
        mean_speed = self.get_mean_speed() * self.KH_IN_MS
        height_in_meters = self.height / self.SM_IN_M

        calories = ((self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                     + (mean_speed ** self.CALORIES_MEAN_SPEED_MULTIPLIER
                        / height_in_meters)
                     * self.CALORIES_WEIGHT_BRACKETS_MULTIPLIER * self.weight)
                    * self.duration * self.H_IN_M)

        return calories


class Swimming(Training):
    def __init__(self, action: int, duration: float, weight: float,
                 length_pool: float, count_pool: float):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    LEN_STEP = 1.38
    MEAN_SPEED_ADDEND = 1.1
    SPENT_CALORIES_F_MULTIPLIER = 2
    """Тренировка: плавание."""
    pass

    def get_mean_speed(self) -> float:
        mean_speed = (self.length_pool * self.count_pool / self.M_IN_KM
                      / self.duration)
        return mean_speed

    def get_spent_calories(self) -> float:
        calories = ((self.get_mean_speed()
                     + self.MEAN_SPEED_ADDEND)
                    * self.SPENT_CALORIES_F_MULTIPLIER
                    * self.weight * self.duration)
        return calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    types = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}
    return types[workout_type](*data)


def main(training: Training) -> None:
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
