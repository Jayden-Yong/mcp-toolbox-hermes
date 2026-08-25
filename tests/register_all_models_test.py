from unittest.mock import MagicMock, patch

from tools import register_all


def _capturing_mcp(tools: dict) -> MagicMock:
    mcp = MagicMock()
    mcp.tool.side_effect = lambda: lambda fn: tools.setdefault(fn.__name__, fn)
    return mcp


def test_register_all_discovers_leaf_modules():
    tools = {}

    register_all(_capturing_mcp(tools))

    assert set(tools) == {
        "extract_pdf_text",
        "extract_pdf_via_vision",
        "pdf_page_count",
        "get_daily_usage",
        "get_litellm_model_name",
    }


def test_register_all_skips_pkgs_and_unregistered(capsys):
    mod_with_register = MagicMock(spec=["register"])
    mod_without_register = MagicMock(spec=["other"])
    specs = [
        ("importer", "tools.a_package", True),
        ("importer", "tools.with_register", False),
        ("importer", "tools.no_register", False),
    ]

    def fake_import(name):
        return {
            "tools.with_register": mod_with_register,
            "tools.no_register": mod_without_register,
        }[name]

    with (
        patch("tools.pkgutil.walk_packages", return_value=specs),
        patch("tools.importlib.import_module", side_effect=fake_import),
    ):
        mcp = MagicMock()
        register_all(mcp)

    mod_with_register.register.assert_called_once_with(mcp)
    output = capsys.readouterr().out
    assert "Registered tool module: tools.with_register" in output
    assert "no_register" not in output
