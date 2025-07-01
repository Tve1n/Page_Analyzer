from datetime import date

from psycopg2 import extras


def get_all_urls(conn):
    with conn.cursor(cursor_factory=extras.NamedTupleCursor) as cursor:
        cursor.execute("""
            SELECT
                id,
                name,
                created_at
            FROM
                urls
            ORDER BY
                id DESC;
            """)
        return cursor.fetchall()


def create_url(conn, name):
    date_create = date.today()
    with conn.cursor(cursor_factory=extras.NamedTupleCursor) as cursor:
        cursor.execute("""
            INSERT INTO urls(name, created_at)
            VALUES
                (%s, %s) RETURNING id;
            """, (name, date_create))
        return cursor.fetchone()[0]


def get_url_by_id(conn, id):
    with conn.cursor(cursor_factory=extras.NamedTupleCursor) as cursor:
        cursor.execute("""
            SELECT
                id,
                name,
                created_at
            FROM
                urls
            WHERE
                id = (%s);
            """, (id,))
        return cursor.fetchone()


def get_url_by_name(conn, name):
    with conn.cursor(cursor_factory=extras.NamedTupleCursor) as cursor:
        cursor.execute("""
                SELECT
                    id,
                    name,
                    created_at
                FROM    
                    urls
                WHERE
                    name = %s;
                """, (name, ))
        return cursor.fetchone()


def create_check(conn, url_id):
    with conn.cursor(cursor_factory=extras.NamedTupleCursor) as cursor:
        creation_date = date.today()
        cursor.execute("""  
                INSERT INTO url_checks(
                    url_id, created_at
                )
                VALUES
                    (%s, %s);
        """, (url_id, creation_date))


def get_checks_by_url_id(conn, id):
    with conn.cursor(cursor_factory=extras.NamedTupleCursor) as cursor:
        cursor.execute("""  
            SELECT
                id,
                url_id,
                created_at
            FROM
                url_checks
            WHERE
                url_id = (%s)
            ORDER BY
                id DESC;
        """, (id, ))
        return cursor.fetchall()
