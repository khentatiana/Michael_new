import sqlite3

connection = sqlite3.connect("db.sqlite")
cursor = connection.cursor()

input_list = list(input('Вашь оотзыв: ').split())

cursor.execute("INSERT INTO reviews (review, author) VALUES (?, ?)", input_list)
cursor.execute("")

reviews = cursor.fetchall()

connection.commit()
print(reviews)
