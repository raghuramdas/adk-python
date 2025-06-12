from scripts import generate_portfolio as gp


def test_generate_html_contains_project():
    sites = [{"name": "Example", "url": "https://example.com", "apps": False}]
    html = gp.generate_html(sites)
    assert "Example" in html
    assert "https://example.com" in html
    assert gp.THUMB_URL.split('{')[0] in html
