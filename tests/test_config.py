from app.config import load_settings


def test_defaults(monkeypatch):
    monkeypatch.delenv("APP_NAME", raising=False)
    monkeypatch.delenv("APP_DEBUG", raising=False)
    settings = load_settings()
    assert settings.app_name == "My Python App"
    assert settings.debug is False


def test_reads_environment(monkeypatch):
    monkeypatch.setenv("APP_NAME", "Inventory")
    monkeypatch.setenv("APP_DEBUG", " TRUE ")
    settings = load_settings()
    assert settings.app_name == "Inventory"
    assert settings.debug is True
