
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
    # идентификатор пользователя, первичный ключ. 
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



# функция для установления соединения с базой данных
def connect_db():
	# Устанавливает соединение к базе данных, создает таблицы, если их еще нет и возвращает объект сессии

	# создаем соединение к БД
	engine = sa.create_engine(DB_PATH)
	# создаем описанные таблицы 
	Base.metadata.create_all(engine)
	# создаем фабрику сессий
	session = sessionmaker(engine)
	# возвращаем сессию
	return session()



"""эта функция запрашивает у пользователя данные
и записывает их в User"""
def request_data():
	
	# вывод приветствия:
	print("Привет! Я запишу ваши данные!")
	
	# запрос данных:
	first_name = input("Введите ваше имя: ")
	last_name = input("Введите вашу фамилию: ")
	gender = input("Введите свой пол (варианты ответа - Male или Female): ")
	email = input("Адрес вашей электронной почты: ")
	birthdate = input("Дата вашего рождения (в формате ГГГГ-ММ-ДД): ")
	height = input("Ваш рост в метрах? Для разделения метров и сантиметров используйте точку: ")

	# Создаем нового пользователя (экземпляр класса User):
	user = User(
		first_name=first_name,
        last_name=last_name,
        gender=gender,
        email=email,
        birthdate=birthdate,
        height=height
	)

	# возвращаем созданного пользователя
	return user


# эта функция обрабатывает пользовательский ввод:
# функция использует класс Users 
def main():

	session = connect_db()

	# запрашиваем данные пользователя
	user = request_data()
	# добавляем нового пользователя в сессию:
	session.add(user)

    # сохраняем все изменения, накопленные в сессии
	session.commit()
	print("Спасибо! Данные сохранены")


if __name__ == "__main__":
	main()
