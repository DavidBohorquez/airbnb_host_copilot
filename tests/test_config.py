"""M0 checkpoint: settings load and paths resolve. This test should pass on the bare skeleton."""

from host_copilot.config import get_settings


def test_settings_load():
    s = get_settings()
    assert s.llm_provider in {"ollama", "anthropic", "openai"}
    assert s.top_k > 0


def test_paths_resolve():
    s = get_settings()
    # data_airbnb_bordeaux sits next to host_copilot at the repo root
    assert s.data_path.name == "data_airbnb_bordeaux"
    assert s.chroma_path.is_absolute()
