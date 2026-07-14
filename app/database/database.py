import aiosqlite


DATABASE_PATH = "data/library.db"


async def create_database():
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER UNIQUE NOT NULL,
                username TEXT,
                full_name TEXT
            )
            """
        )

        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS bookings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                date TEXT NOT NULL,
                time TEXT NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(id),
                UNIQUE(date, time)
            )
            """
        )

        await db.commit()


async def create_booking(
        user_id: int,
        date: str,
        time: str
) -> bool:
    try:
        async with aiosqlite.connect(DATABASE_PATH) as db:
            await db.execute(
                """
                INSERT INTO bookings
                (user_id, date, time)
                VALUES (?, ?, ?)
                """,
                (
                    user_id,
                    date,
                    time
                )
            )

            await db.commit()

        return True

    except aiosqlite.IntegrityError:
        return False


async def get_user_bookings(
        user_id: int
):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        cursor = await db.execute(
            """
            SELECT id, date, time
            FROM bookings
            WHERE user_id = ?
            ORDER BY date, time
            """,
            (user_id,)
        )

        return await cursor.fetchall()


async def cancel_booking(
        booking_id: int,
        user_id: int
):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            """
            DELETE FROM bookings
            WHERE id = ?
            AND user_id = ?
            """,
            (
                booking_id,
                user_id
            )
        )

        await db.commit()

async def get_all_bookings():
    async with aiosqlite.connect(DATABASE_PATH) as db:
        cursor = await db.execute(
            """
            SELECT bookings.id, users.full_name, bookings.date, bookings.time
            FROM bookings
            JOIN users ON bookings.user_id = users.id
            ORDER BY bookings.date, bookings.time
            """
        )
        return await cursor.fetchall()


async def get_today_bookings(today: str):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        cursor = await db.execute(
            """
            SELECT bookings.id, users.full_name, bookings.date, bookings.time
            FROM bookings
            JOIN users ON bookings.user_id = users.id
            WHERE bookings.date = ?
            ORDER BY bookings.time
            """,
            (today,)
        )
        return await cursor.fetchall()
    
async def count_bookings(date: str, time: str) -> int:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        cursor = await db.execute(
            """
            SELECT COUNT(*)
            FROM bookings
            WHERE date = ? AND time = ?
            """,
            (date, time)
        )

        result = await cursor.fetchone()
        return result[0] if result else 0