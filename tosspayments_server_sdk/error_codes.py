class ErrorCodes:
    """토스페이먼츠 에러 코드 상수"""

    # API KEY ERRORS
    # https://docs.tosspayments.com/reference/using-api/api-keys#api-키-에러
    INVALID_CLIENT_KEY = "INVALID_CLIENT_KEY"
    INVALID_API_KEY = "INVALID_API_KEY"
    UNAUTHORIZED_KEY = "UNAUTHORIZED_KEY"
    INCORRECT_BASIC_AUTH_FORMAT = "INCORRECT_BASIC_AUTH_FORMAT"

    class Groups:
        """에러 코드 그룹들"""

        AUTH = {
            "INVALID_CLIENT_KEY",  # 400
            "INVALID_API_KEY",  # 400
            "UNAUTHORIZED_KEY",  # 401
            "INCORRECT_BASIC_AUTH_FORMAT",  # 401
        }

        # 나중에 추가될 그룹들
        # PAYMENT = {
        #     "ALREADY_CANCELED_PAYMENT",
        #     "PAYMENT_NOT_FOUND",
        #     "INSUFFICIENT_BALANCE"
        # }

    # ============= 편의 메서드들 =============
    @classmethod
    def is_auth_error(cls, error_code: str) -> bool:
        return error_code in cls.Groups.AUTH
