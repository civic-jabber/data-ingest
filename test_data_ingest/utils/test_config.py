import data_ingest.utils.config as config


def test_news_config_is_well_formed():
    newspaper_config = config.read_config("newspaper")
    for value in newspaper_config:
        assert "id" in value
        assert "url" in value
        assert "states" in value
        assert isinstance(value["states"], list)


def test_news_ids_are_unique():
    newspaper_config = config.read_config("newspaper")
    ids = [value["id"] for value in newspaper_config]
    assert len(ids) == len(set(ids))
