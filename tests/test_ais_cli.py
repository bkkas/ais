import pytest
from src.ais_analyzer.handlers import cli_handler


#@pytest.fixture()
#def cli(tmp_path_factory):
#    yield [cli_handler.AISCLI({"output": tmp_path_factory.mktemp("temp")} + "/out.csv")]


class TestCase:

    @pytest.mark.skip(reason="Currently gives an error as one cannot give args to AISCLI")
    def test_cli_retain_args(self):
        args = {
            "output": "./tmp/out.csv",
            "path": "./data/dk_test_data_10k_rows.csv",
            "command": "statistics",
        }
        ais_cli = cli_handler.AISCLI(args)
        assert args == ais_cli.get_args(asdict=True)


