"""Implement CLI for deps2repos"""

import argparse

from npm import js_package_dot_json_analysis
from pypi import python_requirements_dot_text_analysis


def parse_command_line_arguments():
    """Parse command line arguments with argparse."""
    parser = argparse.ArgumentParser(
        description="Convert dependency files into list of GitHub links.",
        epilog="For help with this program, contact John Speed at jmeyers@iqt.org.",
    )
    parser.add_argument(
        "--python",
        default=False,  # default value is False
        help="Convert requirements.txt file into GitHub links.",
    )
    parser.add_argument(
        "--javascript",
        default=False,  # default value is False
        help="Convert package.json file into GitHub links.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_command_line_arguments()

    # parse specified Python requirements.txt file and generate GitHub links
    # for all top-level AND transitive dependencies.
    if args.python:
        python_requirements_dot_text_analysis(args.python)

    # parse specified Python requirements.txt file and generate GitHub links
    # for all top-level dependencies
    # TODO: Analyze transitive dependencies too.
    if args.javascript:
        js_package_dot_json_analysis(args.javascript)