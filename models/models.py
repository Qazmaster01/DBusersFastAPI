from sqlalchemy import MetaData, Integer, String, TIMESTAMP, ForeignKey, Table, Column, Boolean

metadata = MetaData()

save_user = Table(
    "save_user",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("surname", String, nullable=False),
    Column("fatherland", String, nullable=False),
    Column("gender", String, nullable=False),
    Column("phone_number", String, nullable=False),
    Column("email", String, nullable=False),
    Column("password", String, nullable=False),

)

user = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String, nullable=False),
    Column("email", String, nullable=False),
    Column("hashed_password", String, nullable=False),
    Column("is_active", Boolean, default=True, nullable=False),
    Column("is_superuser", Boolean, default=False, nullable=False),
    Column("us_verifed", Boolean, default=False, nullable=False),


)

# usersauth = Table(
#     "users_auth",
#     metadata,
#     Column("id", Integer, primary_key=True),
#     Column("name", String, nullable=False),
#     Column("email",String, nullable=False),
#     Column("password", String, nullable=False),
#     Column("user_id", Integer, ForeignKey("users.id")),
#
# )