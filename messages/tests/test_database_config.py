import importlib


def test_database_url_is_loaded_from_environment(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "postgresql+psycopg://user:pass@localhost:5432/example")

    config = importlib.import_module("database.config")
    importlib.reload(config)

    assert config.DATABASE_URL == "postgresql+psycopg://user:pass@localhost:5432/example"
