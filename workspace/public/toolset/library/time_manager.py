from datetime import date, datetime


class TimeManager:
    def generate_current_iso8601_date(self) -> str:
        return date.today().strftime("%Y-%m-%d")

    def generate_current_year(self) -> str:
        return datetime.now().year


singleton = TimeManager()
