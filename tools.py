class TimeConverter:
    @staticmethod
    def convertTime(seconds):
        return seconds%60, int(seconds/60), int((seconds/60)/60)