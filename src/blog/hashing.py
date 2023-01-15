from passlib.context import CryptContext

# `deprecated='auto'`で非推奨なアルゴリズムを除外している
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hash:
    @staticmethod
    def bcrypt(password: str) -> str:
        return pwd_context.hash(password)
