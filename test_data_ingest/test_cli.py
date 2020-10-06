from click.testing import CliRunner
import pandas as pd

import data_ingest.cli as cli


def test_run_ingest(monkeypatch, capsys):
    monkeypatch.setattr(cli, "load_news", lambda *args: "NEWS")
    monkeypatch.setattr(cli, "load_va_regulations", lambda *args: "VA_REGS")

    runner = CliRunner()
    result = runner.invoke(cli.main, ["run-ingest"])


def test_people_to_csv(monkeypatch, tmpdir):
    def mock_get_all_people(state, per_page, links):
        return [
            {
                "name": "Tiki",
                "party": "Republican",
                "current_role": {"title": "Senator", "district": "1"},
                "links": [{"url": "www.tiki.com"}],
            },
            {
                "name": "Jabber",
                "party": "Democrat",
                "current_role": {"title": "Senator", "district": "2"},
                "links": [],
            },
        ]

    monkeypatch.setattr(cli, "get_all_people", mock_get_all_people)

    filename = f"{tmpdir.dirname}/people.csv"
    runner = CliRunner()
    result = runner.invoke(
        cli.main, ["people-to-csv", "--state", "va", "--outfile", filename]
    )

    data = pd.read_csv(filename)
    expected = pd.DataFrame(
        {
            "name": ["Tiki", "Jabber"],
            "party": ["Republican", "Democrat"],
            "role": ["Senator", "Senator"],
            "district": [1, 2],
            "link": ["www.tiki.com", None],
        }
    )
    pd.testing.assert_frame_equal(data, expected)
