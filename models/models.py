from sqlalchemy import MetaData, Integer, String, TIMESTAMP, ForeignKey

metadata = MetaData()

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", Integer, nullable=False),
    Column("surname", Integer, nullable=False),
    Column("fatherland", Integer, nullable=False),
    Column("gender", Integer, nullable=False),
    Column("phone_number", Integer, nullable=False),
    Column("email", Integer, nullable=False),
    Column("password", Integer, nullable=False),

)