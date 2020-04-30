import pytest
from application import create_app, db as _db
from sqlalchemy import create_engine


@pytest.fixture(scope='session', autouse=True)
def app():
    _app = create_app('test')
    ctx = _app.app_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.fixture(scope='session')
def client(app):
    client = app.test_client()
    yield client


@pytest.fixture(scope='session')
def db(app):
    _db.create_all()

    yield _db

    _db.drop_all()


@pytest.fixture(scope='session')
def connection(app):
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    connection = engine.connect()

    yield connection

    connection.close()


@pytest.fixture(scope='module')
def session(connection, db):
    transaction = connection.begin()
    session = db.scoped_session(db.sessionmaker(bind=connection))
    db.session = session

    yield session
    print("\n*********** ROLLBACK ***********")
    transaction.rollback()
    session.close()
