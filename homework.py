class InfoMessage:
    """Informative message about the training."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float,
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        """Get informative message about the training as a string."""
        message = (f'Тип тренировки: {self.training_type}; '
                   f'Длительность: {self.duration:.3f} ч.; '
                   f'Дистанция: {self.distance:.3f} км; '
                   f'Ср. скорость: {self.speed:.3f} км/ч; '
                   f'Потрачено ккал: {self.calories:.3f}.')
        return message


class Training:
    """Training base class."""

    M_IN_KM = 1000
    LEN_STEP = 0.65

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Get the distance in km."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Get the mean speed."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Get the number of calories burnt."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Get an informative message about the training."""
        message = InfoMessage(training_type=self.__class__.__name__,
                              duration=self.duration,
                              distance=self.get_distance(),
                              speed=self.get_mean_speed(),
                              calories=self.get_spent_calories()
                              )
        return message


class Running(Training):
    """Training sub-class: Running."""

    COEFF_CALORIES_CALCULATION_1 = 18
    COEFF_CALORIES_CALCULATION_2 = 20

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        """Get the number of calories burnt while running."""

        mean_speed = super().get_mean_speed()
        duration_minutes = self.duration * 60
        calories = ((self.COEFF_CALORIES_CALCULATION_1
                    * mean_speed - self.COEFF_CALORIES_CALCULATION_2)
                    * self.weight
                    / self.M_IN_KM * duration_minutes)
        return calories


class SportsWalking(Training):
    """Training sub-class: Jogging."""

    COEFF_CALORIES_CALCULATION_1 = 0.035
    EXP_CALORIES_CALCULATION = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.heigth = height

    def get_spent_calories(self) -> float:
        """Get the number of calories burnt wlile jogging."""

        mean_speed = super().get_mean_speed()
        duration_minutes = self.duration * 60
        calories = ((self.COEFF_CALORIES_CALCULATION_1 * self.weight
                    + (mean_speed**self.EXP_CALORIES_CALCULATION
                     // self.heigth)) * duration_minutes)
        return calories


class Swimming(Training):
    """Training sub-class: Swimming."""

    LEN_STEP = 1.38
    COEFF_CALORIES_CALCULATION_1 = 1.1
    COEFF_CALORIES_CALCULATION_2 = 2

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

    def get_spent_calories(self) -> float:
        """Get the number of calories burnt while swimming."""

        mean_speed = self.get_mean_speed()
        calories = ((mean_speed + self.COEFF_CALORIES_CALCULATION_1)
                    * self.COEFF_CALORIES_CALCULATION_2 * self.weight)
        return calories

    def get_mean_speed(self) -> float:
        """Get the mean speed while swimming."""
        duration_minutes = self.duration
        mean_speed = (self.length_pool * self.count_pool
                      / self.M_IN_KM / duration_minutes)
        return mean_speed


AVAILABLE_TRAININGS = {'RUN': Running,
                       'WLK': SportsWalking,
                       'SWM': Swimming}


def read_package(workout_type: str, data: list) -> Training:
    """Get the data from the sensors."""

    if workout_type not in AVAILABLE_TRAININGS:
        raise NameError(f'Unknown Training {workout_type}')
    return AVAILABLE_TRAININGS[workout_type](*data)


def main(training: Training) -> None:
    """Main function, prints results of the training in the terminal."""

    info = training.show_training_info()
    result_message = info.get_message()
    print(result_message)


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
