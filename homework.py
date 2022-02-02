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
        message = ('Тип тренировки: ' + self.training_type + '; '
                   + 'Длительность: ' + '{:.3f}'.format(self.duration)
                   + ' ч.; ' + 'Дистанция: '
                   + '{:.3f}'.format(self.distance) + ' км; '
                   + 'Ср. скорость: ' + '{:.3f}'.format(self.speed)
                   + ' км/ч; ' + 'Потрачено ккал: '
                   + '{:.3f}'.format(self.calories) + '.')
        return message


class Training:
    """Training base class."""

    M_IN_KM = 1000   # meters in kilometer
    LEN_STEP = 0.65  # basic length of the step for every training ex. Swimming

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
        message = InfoMessage(self.__class__.__name__,
                              self.duration,
                              self.get_distance(),
                              self.get_mean_speed(),
                              self.get_spent_calories()
                              )
        return message


class Running(Training):
    """Training sub-class: Running."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        """Get the number of calories burnt while running."""

        COEFF_1 = 18
        COEFF_2 = 20

        mean_speed = super().get_mean_speed()
        duration_minutes = self.duration * 60
        calories = ((COEFF_1 * mean_speed - COEFF_2) * self.weight
                    / self.M_IN_KM * duration_minutes)
        return calories


class SportsWalking(Training):
    """Training sub-class: Jogging."""

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

        COEFF_1 = 0.035
        EXP = 2

        mean_speed = super().get_mean_speed()
        duration_minutes = self.duration * 60
        calories = ((COEFF_1 * self.weight + (mean_speed**EXP // self.heigth))
                    * duration_minutes)
        return calories


class Swimming(Training):
    """Training sub-class: Swimming."""

    LEN_STEP = 1.38

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
        COEFF_1 = 1.1
        COEFF_2 = 2
        mean_speed = self.get_mean_speed()
        calories = (mean_speed + COEFF_1) * COEFF_2 * self.weight
        return calories

    def get_mean_speed(self) -> float:
        """Get the mean speed while swimming."""
        duration_minutes = self.duration
        mean_speed = (self.length_pool * self.count_pool
                      / self.M_IN_KM / duration_minutes)
        return mean_speed


def read_package(workout_type: str, data: list) -> Training:
    """Get the data from the sensors."""

    available_trainings = {'RUN': Running,
                           'WLK': SportsWalking,
                           'SWM': Swimming}
    if workout_type not in available_trainings:
        raise NameError('Unknown Trainign')
    else:
        return available_trainings[workout_type](*data)


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
