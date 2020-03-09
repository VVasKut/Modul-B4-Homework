import datetime
from datetime import datetime

# импортируем библиотеку sqlalchemy и ее функции
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# константа, указывающая способ соеденения с базой данных
DB_PATH = "sqlite:///sochi_athletes.sqlite3"

# создаем базовый класс моделей таблиц
Base = declarative_base()


class User(Base):
# Данный класс описывает структуру таблицы user для хранения регистрационных данных пользователей

	# задаем название таблицы
    __tablename__ = "user"
    # идентификатор пользователя, первичный ключ. String(36) - ограничение поля текстового типа 36 символами
    id = sa.Column(sa.Integer, primary_key=True)
    # имя пользователя
    first_name = sa.Column(sa.Text)
    # фамилия пользователя
    last_name = sa.Column(sa.Text)
    # пол пользователя
    gender = sa.Column(sa.Text)
    # адрес электронной почты пользователя
    email = sa.Column(sa.Text)
    # дата рождения
    birthdate = sa.Column(sa.Text)
    height = sa.Column(sa.Float)



class Athelete(Base):
	# Класс описывает структуру таблицы athelete для хранения данных спортсменов

	# задаем название таблицы
    __tablename__ = "athelete"
    # идентификатор пользователя, первичный ключ
    id = sa.Column(sa.Integer, primary_key=True)
    age = sa.Column(sa.Integer)
    birthdate = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    height = sa.Column(sa.Float)
    name = sa.Column(sa.Text)
    weight = sa.Column(sa.Integer)
    gold_medals = sa.Column(sa.Integer)
    silver_medals = sa.Column(sa.Integer)
    bronze_medals = sa.Column(sa.Integer)
    total_medals = sa.Column(sa.Integer)
    sport = sa.Column(sa.Text)
    country = sa.Column(sa.Text)


# функция для установления соединения с базой данных
def connect_db():
	# Устанавливает соединение к базе данных и возвращает объект сессии

	engine = sa.create_engine(DB_PATH)
	Base.metadata.create_all(engine)
	session = sessionmaker(engine)
	return session()


"""эта функция запрашивает у пользователя идентификатор пользователя
и возвращает его в виде числа"""
def request_data():
	
	# вывод приветствия:
	print("Привет! Я найду участников Олимпийских игр, близких по параметрам пользователю")
	
	# запрос данных:
	user_id = input("Введите идентификтор пользователя (число): ")
	
	# возвращаем числовое значение идентификатора
	return int(user_id)


# Функция, которая производит поиск пользователя в таблице user по заданному имени name
def find_athlete_with_birthday(user, session):

	# находим все записи в таблице Athelete
	athletes_all = session.query(Athelete).all()

	# из записей строим словарь с парами ключ-значение, где ключ - id атлета, значение - его день рождения в формате date
	athletes_dict = {}
	for athlete in athletes_all:
		athlete_birthdate = datetime.strptime(athlete.birthdate, "%Y-%m-%d").date()
		athletes_dict[athlete.id] = athlete_birthdate
	
	# конвертируем текстовый формат даты рождения пользователя в формат date
	user_birthdate = datetime.strptime(user.birthdate, "%Y-%m-%d").date()

	minimum_distance_by_bdate = None
	athlete_id = None
	athlete_bdate = None

	for id_, bd_ in athletes_dict.items():
		dist = abs(bd_ - user_birthdate)
		if not minimum_distance_by_bdate or dist < minimum_distance_by_bdate:
			minimum_distance_by_bdate = dist
			athlete_id = id_
			athlete_bdate = bd_
	return athlete_id, athlete_bdate


def find_athlete_with_height(user, session):

	athletes_all = session.query(Athelete).filter(Athelete.height != None).all()

	# из записей строим словарь со значениями роста спортсменов
	athletes_height_dict = {athlete.id: athlete.height for athlete in athletes_all}

	# находим значение роста пользователя с указанным идентификатором
	user_height = user.height
	minimum_distance_by_height = None
	athlete_id = None
	athlete_height = None

	for id_, height_ in athletes_height_dict.items():
		dist_height = abs(height_ - user_height)
		if not minimum_distance_by_height or dist_height < minimum_distance_by_height:
			minimum_distance_by_height = dist_height
			athlete_id = id_
			athlete_height = height_
	return athlete_id, athlete_height

# эта функция взаимодействует с пользователем и обрабатывает пользовательский ввод:
# функция использует класс Users и Athelete
def main():

	session = connect_db()

	# запрашиваем данные пользователя
	user_id = request_data()
	# находим пользователя по введенному идентификтору
	user = session.query(User).filter(User.id == user_id).first()
	# выводим, если пользователя с введенным id нет в таблице user
	if not user:
		print("Пользователь с таким идентификатором отсутствует в таблице")
	else:
		ath_id, birthdate = find_athlete_with_birthday(user, session)
		print("Ближайший по дате рождения атлет с идентификатором {} имеет дату рождения {}".format(ath_id, birthdate))
		athl_id, athl_height = find_athlete_with_height(user, session)
		print("Ближайший по росту атлет с идентификатором {} имеет рост {}.".format(athl_id, athl_height))


if __name__ == "__main__":
	main()
