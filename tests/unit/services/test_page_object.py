from src.services.scraping.page_object import Page


def test_Page_id_extract():
    test_urls = [
        {
            "data": "https://classroom.google.com/u/3/c/NjcyOTEyOTk2Nzgx",
            "expected": "NjcyOTEyOTk2Nzgx",
        },
        {
            "data": "https://classroom.google.com/u/3/c/NjcyOTEyOTk2Nzgx/m/NjkwNTE0Njc3NDA3/details",  # noqa: E501
            "expected": "NjkwNTE0Njc3NDA3",
        },
        {
            "data": "https://classroom.google.com/u/3/c/NjcyOTEyOTk2Nzgx/m/NjkwNTE0Njc3NDA3/submissions/by-status/all-students/late",  # noqa: E501
            "expected": "",
        },
    ]

    for param in test_urls:
        data, expected = param.values()
        id = Page.id_extract(data)
        assert id == expected
