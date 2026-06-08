from app.utils.slug import slugify


def test_slugify_normalizes_text_to_url_safe_slug():
    assert slugify("Engineering Workspace!") == "engineering-workspace"


def test_slugify_collapses_symbols_and_trims_separators():
    assert slugify("  Finance & HR / Admin  ") == "finance-hr-admin"


def test_slugify_returns_default_for_empty_input():
    assert slugify("!!!") == "item"
