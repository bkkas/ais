import pytest
from src.ais_analyzer.handlers import cli_handler


@pytest.fixture
def arguments_passed(tmp_path_factory):
    yield {
        'input_file': "tests/data/no_test_data_vestland_10k_rows.csv",
        'command': "statistics",
        'output_file': (tmp_path_factory.mktemp('temp')/"output.csv").__str__()
    }


@pytest.fixture
def args_(arguments_passed):
    yield [
        '--input-file=' + arguments_passed.get('input_file'),
        arguments_passed.get('command'),
        '--output=' + arguments_passed.get('output_file')
        ]


class TestCase:

    def test_cli_initiates(self, args_):
        try:
            cli_handler.CommandLineInterfaceHandler(args=args_)
        except Exception as e:
            assert False, f"Exception raised: {e}"

    def test_cli_retain_args(self, args_, arguments_passed):
        ais_cli = cli_handler.CommandLineInterfaceHandler(args=args_)
        arg_dict = ais_cli.get_args(asdict=True)
        for key, item in arguments_passed.items():
            assert arg_dict.get(key) == item

    def test_cli_error_on_wrong_arg(self, args_):
        args_.append('--unused=5')
        # Argparse handles errors in a way that makes them
        # near impossible to access with normal error handling,
        # as it exits out of the program on a wrong argument
        with pytest.raises(SystemExit):
            cli_handler.CommandLineInterfaceHandler(args=args_)

    def test_cli_default_full(self, args_):
        # Full should not be True by default, unless
        # named to reflect the chane in state.
        ais_cli = cli_handler.CommandLineInterfaceHandler(args=args_)
        arg_dict = ais_cli.get_args(asdict=True)
        assert not arg_dict.get('full')

    def test_cli_full_arg_should_make_full(self, args_):
        args_.append('--full')
        ais_cli = cli_handler.CommandLineInterfaceHandler(args=args_)
        arg_dict = ais_cli.get_args(asdict=True)
        assert arg_dict.get('full')



