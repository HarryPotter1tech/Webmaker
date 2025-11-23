from math import e
from sqlite3 import connect
from docx import Document

DATABASE_PATH = "database/database.db"


def get_db_connection(db_path=DATABASE_PATH):
    conn = connect(db_path)
    print("Database connection established.")
    return conn


def close_db_connection(conn):
    conn.close()
    print("Database connection closed.")


def init_db(db_path=DATABASE_PATH):
    connection = get_db_connection(db_path)
    cursor = connection.cursor()
    cursor.execute(
        "CREATE TABLE chat_history(person TEXT, message TEXT, talkcycle INTEGER)"
    )
    connection.commit()
    close_db_connection(connection)


def update_db(role: str, message: str, talkcycle: int, db_path=DATABASE_PATH):
    connection = get_db_connection(db_path)
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO chat_history (person, message, talkcycle) VALUES (?, ?, ?)",
        (role, message, talkcycle),
    )
    connection.commit()
    close_db_connection(connection)


def get_all_chat_history(db_path=DATABASE_PATH):
    connection = get_db_connection(db_path)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM chat_history")
    rows = cursor.fetchall()
    close_db_connection(connection)
    return rows


def transform_db_to_word(db_path=DATABASE_PATH):
    rows = get_all_chat_history(db_path)
    chat_history_doc = Document()
    chat_history_doc.add_heading("与Deepseek的聊天记录", level=1)
    with open("chat_history.docx", "w", encoding="utf-8") as f:
        for row in rows:
            person, message, talkcycle = row
            f.write(f"轮次 {talkcycle} - {person}:\n{message}\n\n")
    chat_history_doc.save("chat_history.docx")
    return {
        "file_path": "chat_history.docx",
        "filename": "chat_history.docx",
    }  # 返回生成的文件路径
