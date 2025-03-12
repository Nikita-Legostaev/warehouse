from fastapi import HTTPException, status


class BaseException(HTTPException):
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail: str = ""

    def __init__(self, detail: str | None = None):
        final_detail = detail or self.detail
        super().__init__(status_code=self.status_code, detail=final_detail)


class CannotAddDataToDatabase(BaseException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Не удалось добавить запись"


class CannotDeleteDataFromDatabase(BaseException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Не удалось удалить запись"


class NotFoundException(BaseException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Запись не найдена"


class RollNotFoundError(BaseException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Рулон не найден"


class ValidationError(BaseException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Ошибка валидации данных"


class FilterError(BaseException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Ошибка фильтрации объектов"


class ConnectionError(BaseException):
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    detail = "Ошибка подключения к базе данных"


class StatisticsError(BaseException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Ошибка при получении статистики"
