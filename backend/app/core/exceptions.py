class DefaultSecretError(ValueError):
    def __init__(self, variable_name: str) -> None:
        message = (
            f'{variable_name} 的值为 "changethis"，'
            "出于安全考虑，请至少在部署前修改该值。"
        )

        super().__init__(message)
