from contextvars import ContextVar

# Current logged-in user
current_user = ContextVar(
    "current_user",
    default=None
)

# Current SQLAlchemy session
current_db = ContextVar(
    "current_db",
    default=None
)


def set_current_user(user):

    current_user.set(user)


def get_current_user():

    return current_user.get()


def set_db(db):

    current_db.set(db)


def get_db():

    return current_db.get()


def clear_context():

    current_user.set(None)

    current_db.set(None)
