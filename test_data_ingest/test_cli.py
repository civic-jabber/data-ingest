from click.testing import CliRunner

import data_ingest.cli as cli


def test_run_ingest(monkeypatch, capsys):
    monkeypatch.setattr(cli, "load_news", lambda *args: "NEWS")
    monkeypatch.setattr(cli, "load_va_regulations", lambda *args: "VA_REGS")

    runner = CliRunner()
    result = runner.invoke(cli.main, ["run-ingest"])
