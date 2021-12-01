from typing import Any, Union
from os import mkdir
import sqlite3


class AsyncDataBaseConnector:
    def __init__(self, path_to_db: str = "./", db_prefix: str = "db") -> None:
        self.name: str = path_to_db
        self.__db_prefix: str = db_prefix
        for path in self.name.split('/'):
            try:
                mkdir(path)
            except FileExistsError:
                pass
            except PermissionError:
                pass
            except OSError:
                pass
        self.__conn = sqlite3.connect(self.name)
        print(f"получено соединение к базе данных. Путь до неё: {self.name}")

    async def __check_subject(self, user_id: Any, subject: str) -> Union[None, int]:
        """
        if count of subject names in db is 0, return None,
        if him is 1 then return True,
        if him > 1, then return 1
        :param user_id:
        :param subject:
        :return:
        """
        cursor = self.__conn.cursor()
        try:
            subjects: list = [elem for elem in cursor.execute(
                f"""
                SELECT * FROM {self.__db_prefix}_{user_id}
                WHERE subjects = {subject.lower()}
                """
            )]
        except sqlite3.OperationalError:
            print("ой, с базой данных что-то пошло не так")
        else:
            if not subjects:
                return
            elif len(subjects) == 1:
                return True
            elif len(subjects) > 1:
                return 1

    async def add_user(self, user_id: Any, *args) -> Union[None, int]:
        """
        add user to database

        if error with adding: return 1, else return None
        :param user_id:
        :return:
        """
        cursor = self.__conn.cursor()
        try:
            cursor.execute(
                f"""
                CREATE TABLE {self.__db_prefix}_{user_id}
                (subject text, score text)
                """
            )
        except sqlite3.OperationalError:
            print(
                (
                    f"таблица {self.__db_prefix}_{user_id} "
                    "в базе данных {self.name} уже была создана"
                )
            )
            return 1
        self.__conn.commit()
        print(
            (
                f"создана новая таблица {self.__db_prefix}_{user_id} в "
                "базе данных {self.name}"
            )
        )

    async def add_subject_to_user(self, user_id: Any, subject: str, scores: str = "", *args) -> Union[None, int]:
        """
        if error with adding or databse then return 1, else None
        :param user_id:
        :param subject:
        :param scores:
        :return:
        """
        cursor = self.__conn.cursor()
        try:
            subj_res = await self.__check_subject(user_id=user_id, subject=subject)
            if subj_res and type(subj_res) == bool:
                cursor.execute(
                    f"""
                    INSERT INTO {self.__db_prefix}_{user_id}
                    VALUES ("{subject.lower()}", "{scores.lower()}")
                    """
                )
            else:
                return 1
        except sqlite3.OperationalError:
            print(
                (
                    "что-то пошло не так с добавлением пользователю"
                    f" {user_id} предмета"
                )
            )
            return 1
        self.__conn.commit()
        print(
            (
                f"к пользователю {user_id}"
                f" добавлен предмет {subject} и оценки {scores}"
            )
        )

    async def add_scores_to_subject(self, user_id: Any, subject: str, scores: str = "", *args) -> Union[None, int]:
        """
        аналог "!дописать"
        """
        cursor = self.__conn.cursor()
        try:
            subj_res = await self.__check_subject(user_id=user_id, subject=subject)
            if subj_res and type(subj_res) == bool:
                subjects: list = [elem for elem in cursor.execute(
                    f"""
                    SELECT * FROM {self.__db_prefix}_{user_id}
                    WHERE subjects = {subject.lower()}
                    """
                )][0]
            else:
                return 1
            '''
            subjects = cursor.execute(
                f"""
                SELECT * FROM {self.db_prefix}_{user_id}
                WHERE subjects = {subject.lower()}
                """
            )
            '''
        except sqlite3.OperationalError:
            print(
                (
                    "что-то пошло не так с получением пользователя"
                    f" {user_id} предмета {subject}"
                )
            )
            return 1
        else:
            if subjects:
                subjects[1] += scores.lower()
            try:
                cursor.execute(
                    f"""
                    UPDATE {self.__db_prefix}_{user_id}
                    SET subject = {subjects[0]},
                        score = {subjects[1]}
                    """
                )
            except sqlite3.OperationalError:
                print((
                    "что-то пошло не так с обновлением пользователю"
                    f" {user_id} предмета {subject}"
                    )
                )
            self.__conn.commit()
            print(
                (
                    f"данные пользователя {user_id} по предмету "
                    f"{subject} обновлены"
                )
            )

    async def clean_subject(self, user_id: Any, subject: str, *args) -> Union[None, int]:
        """
        "!очистить"
        """
        cursor = self.__conn.cursor()
        try:
            subjects: list = [elem for elem in cursor.execute(
                f"""
                SELECT * FROM {self.__db_prefix}_{user_id}
                WHERE subjects = {subject.lower()}
                """
            )][0]
            '''
            subjects = cursor.execute(
                f"""
                SELECT * FROM {self.db_prefix}_{user_id}
                WHERE subjects = {subject.lower()}
                """
            )
            '''
        except sqlite3.OperationalError:
            print(
                (
                    "что-то пошло не так с получением пользователя"
                    f" {user_id} предмета {subject}"
                )
            )
            return 1
        else:
            if subjects:
                subjects[1] = ""
            try:
                cursor.execute(
                    f"""
                    UPDATE {self.__db_prefix}_{user_id}
                    SET subject = {subjects[0]},
                        score = {subjects[1]}
                    """
                )
            except sqlite3.OperationalError:
                print((
                    "что-то пошло не так с обновлением пользователю"
                    f" {user_id} предмета {subject}"
                    )
                )
                return 1
            self.__conn.commit()
            print(
                (
                    f"данные пользователя {user_id} по предмету "
                    f"{subject} обновлены"
                )
            )

    async def clean_all_users_subjects(self, user_id: Any, *args) -> Union[None, int]:
        """
        "!стереть_всё"
        """
        cursor = self.__conn.cursor()
        try:
            cursor.execute(
                f"""
                DELETE FROM {self.__db_prefix}_{user_id}
                """
            )
        except sqlite3.OperationalError:
            print((
                "что-то пошло не так с удалением данных пользователя"
                f" {user_id}"
                )
            )
            return 1
        self.__conn.commit()

    async def __calculate_scores(self, scores: str) -> float:
        """
        calculate average of scores
        :param scores:
        :return:
        """
        filtered_scores: list = str(
            filter(
                lambda string: str(string).isdigit(),
                scores
            )
        ).split()
        result: float = sum(
            map(
                lambda string: int(string),
                filtered_scores
            )
        )/len(filtered_scores)
        return result

    async def now_score(self, user_id: Any, subject: str, *args) -> Union[float, None]:
        cursor = self.__conn.cursor()
        try:
            subjects: Union[list, tuple] = [elem for elem in cursor.execute(
                f"""
                SELECT * FROM {self.__db_prefix}_{user_id}
                WHERE subjects = {subject.lower()}
                """
            )][0]
        except sqlite3.OperationalError:
            print(
                (
                    "что-то пошло не так с получением пользователя"
                    f" {user_id} предмета {subject}"
                )
            )
            return
        else:
            if subjects:  # подразумевается, что оценки будут разделены пробелом
                result: float = await self.__calculate_scores(scores=subjects[1])
                # pass  # тут у меня уже заканчиваются силы над логикой бота Т_Т
                # я понял, что сделать, во
                return result
            else:
                print("то-то пошло не так с получением оценок")
                return

    async def predict_scores(self, user_id: Any, subject: str, predict_scores: str, *args) -> Union[float, None]:
        cursor = self.__conn.cursor()
        try:
            subjects: Union[list, tuple] = [elem for elem in cursor.execute(
                f"""
                SELECT * FROM {self.__db_prefix}_{user_id}
                WHERE subjects = {subject.lower()}
                """
            )][0]
        except sqlite3.OperationalError:
            print(
                (
                    "что-то пошло не так с получением пользователя"
                    f" {user_id} предмета {subject}"
                )
            )
            return
        else:
            if subjects:
                result: float = await self.__calculate_scores(scores=subjects[1]+predict_scores)
                return result
            else:
                print("то-то пошло не так с получением оценок")
                return

    async def all_subjects_with_scores_as_dict(self, user_id: Any, *args) -> Union[dict, None]:
        cursor = self.__conn.cursor()
        try:
            subjects: Union[list, tuple] = [elem for elem in cursor.execute(
                f"""
                SELECT * FROM {self.__db_prefix}_{user_id}
                """
            )]
        except sqlite3.OperationalError:
            print(f"что-то пошло не так с получением всех предметов и их оценок у юзера {user_id}")
            return
        else:
            result: dict = {
                key: self.__calculate_scores(value) for key, value in subjects
            }
            return result
