from typing import Any, Union
from os import mkdir
import sqlite3


class AsyncDataBaseConnector:
    def __init__(self, path_to_db: str = "./", db_prefix: str = "db") -> None:
        self.db_prefix = db_prefix
        self.name = path_to_db
        for path in self.name:
            try:
                mkdir(path)
            except FileExistsError:
                pass
            except PermissionError:
                pass
            except OSError:
                pass
        self.conn = sqlite3.connect(self.name)
        print(f"[SQLite3] получено соединение к базе данных. Путь до неё: {self.name}")

    def __check_subject(self, user_id: Any, subject: str) -> Union[None, int]:
        cursor = self.conn.cursor()
        try:
            subjects: list = [elem for elem in cursor.execute(
                f"""
                SELECT * FROM {self.db_prefix}_{user_id}
                WHERE subjects = {subject.lower()}
                """
            )]
        except sqlite3.OperationalError:
            print("[SQLite3] ой, с базой данных что-то пошло не так")
        else:
            if not subjects:
                return
            elif len(subjects) == 1:
                return True
            elif len(subjects) > 1:
                return 1

    async def add_user(self, user_id: Any) -> Union[None, int]:
        """
        add user to database

        if error with adding: return 1, else return None
        :param user_id:
        :return:
        """
        cursor = self.conn.cursor()
        try:
            cursor.execute(
                f"""
                CREATE TABLE {self.db_prefix}_{user_id}
                (subject text, score text)
                """
            )
        except sqlite3.OperationalError:
            print((
                    f"[SQLite3] таблица {self.db_prefix}_{user_id} "
                    "в базе данных {self.name} уже была создана"
            ))
            return 1
        self.conn.commit()
        print((
                f"[SQLite3] создана новая таблица {self.db_prefix}_{user_id} в "
                "базе данных {self.name}"
        ))

    async def add_subject_to_user(self, user_id: Any, subject: str, scores: str = "") -> Union[None, int]:
        """
        if error with adding or databse: return 1, else None
        :param user_id:
        :param subject:
        :param scores:
        :return:
        """
        cursor = self.conn.cursor()
        try:
            subj_res = self.__check_subject(user_id=user_id, subject=subject)
            if subj_res and type(subj_res) == bool:
                cursor.execute(
                    f"""
                    INSERT INTO {self.db_prefix}_{user_id}
                    VALUES ("{subject.lower()}", "{scores.lower()}")
                    """
                )
            else:
                return 1
        except sqlite3.OperationalError:
            print((
                    "[SQLite3] что-то пошло не так с добавлением пользователю"
                    f" {user_id} предмета"
            ))
            return 1
        self.conn.commit()
        print((
                f"[SQLite3] к пользователю {user_id}"
                f" добавлен предмет {subject} и оценки {scores}"
        ))

    async def add_scores_to_subject(self, user_id: Any, subject: str, scores: str = "") -> Union[None, int]:
        """
        аналог "!дописать"
        """
        cursor = self.conn.cursor()
        try:
            subj_res = self.__check_subject(user_id=user_id, subject=subject)
            if subj_res and type(subj_res) == bool:
                subjects: list = [elem for elem in cursor.execute(
                    f"""
                    SELECT * FROM {self.db_prefix}_{user_id}
                    WHERE subjects = {subject.lower()}
                    """
                )]
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
            print((
                    "[SQLite3] что-то пошло не так с получением пользователя"
                    f" {user_id} предмета {subject}"
            ))
        else:
            if subjects:
                subjects[1] += scores.lower()
            try:
                cursor.execute(
                    f"""
                    UPDATE {self.db_prefix}_{user_id}
                    SET subject = {subjects[0]},
                        score = {subjects[1]}
                    """
                )
            except sqlite3.OperationalError:
                print((
                    "[SQLite3] что-то пошло не так с обновлением пользователю"
                    f" {user_id} предмета {subject}"
                ))
            self.conn.commit()
            print((
                    f"[SQLite3] данные пользователя {user_id} по предмету "
                    f"{subject} обновлены"
            ))

    async def clean_subject(self, user_id: Any, subject: str) -> None:
        """
        "!очистить"
        """
        cursor = self.conn.cursor()
        try:
            subjects: list = [elem for elem in cursor.execute(
                f"""
                SELECT * FROM {self.db_prefix}_{user_id}
                WHERE subjects = {subject.lower()}
                """
            )]
            '''
            subjects = cursor.execute(
                f"""
                SELECT * FROM {self.db_prefix}_{user_id}
                WHERE subjects = {subject.lower()}
                """
            )
            '''
        except sqlite3.OperationalError:
            print((
                    "[SQLite3] что-то пошло не так с получением пользователя"
                    f" {user_id} предмета {subject}"
            ))
        else:
            if subjects:
                subjects[1] = ""
            try:
                cursor.execute(
                    f"""
                    UPDATE {self.db_prefix}_{user_id}
                    SET subject = {subjects[0]},
                        score = {subjects[1]}
                    """
                )
            except sqlite3.OperationalError:
                print((
                    "[SQLite3] что-то пошло не так с обновлением пользователю"
                    f" {user_id} предмета {subject}"
                ))
            self.conn.commit()
            print((
                    f"[SQLite3] данные пользователя {user_id} по предмету "
                    f"{subject} обновлены"
            ))

    async def clean_all_users_subjects(self, user_id: Any) -> None:
        """
        "!стереть_всё"
        """
        cursor = self.conn.cursor()
        try:
            cursor.execute(
                f"""
                DELETE FROM {self.db_prefix}_{user_id}
                """
            )
        except sqlite3.OperationalError:
            print((
                "[SQLite3] что-то пошло не так с удалением данных пользователя"
                f" {user_id}"
            ))
        self.conn.commit()

    async def now_score(self, user_id: Any, subject: str) -> None:
        cursor = self.conn.cursor()
        try:
            subjects = cursor.execute(
                f"""
                SELECT * FROM {self.db_prefix}_{user_id}
                WHERE subjects = {subject.lower()}
                """
            )
        except sqlite3.OperationalError:
            print((
                    "[SQLite3] что-то пошло не так с получением пользователя"
                    f" {user_id} предмета {subject}"
            ))
        else:
            if subjects:
                pass  # тут у меня уже заканчиваются силы над логикой бота Т_Т
