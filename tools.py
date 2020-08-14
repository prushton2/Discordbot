class TimeConverter:
    @staticmethod
    def convertTime(timeInSeconds):
        seconds = timeInSeconds%60

        hours = int(timeInSeconds/60/60)

        minutes = int(timeInSeconds/60) - int(int(timeInSeconds/60/60)*60)

        return seconds, minutes, hours