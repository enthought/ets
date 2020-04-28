# (C) Copyright 2005-2020 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

from pathlib import Path

import click

from ets.click_helpers import (
    docs_option, editable_option, environment_manager_option,
    environment_option, runtime_option, tests_option, verbose_option
)

ets_repo_path = Path(__file__).parent

dependencies = [
    {
        'pip': "bandit",
    },
    {
        'pip': "click",
        'edm': "click",
    },
    {
        'pip': "coverage",
        'edm': "coverage",
    },
    {
        'pip': "flake8",
        'edm': "flake8",
    },
    {
        'pip': "mypy",
    },
    {
        'pip': "pydocstyle",
        'edm': "pydocstyle",
    },
]
test_dependencies = []
doc_dependencies = [
    {
        'pip': "sphinx",
        'edm': "sphinx",
    },
    {
        'pip': "enthought_sphinx_theme",
        'edm': "enthought_sphinx_theme",
    },
]


@click.group()
def cli():
    """
    Developer and CI support commands for ETS.
    """
    pass


@cli.command()
@runtime_option
@environment_option
@environment_manager_option
@editable_option
@tests_option
@docs_option
def install(runtime, environment, environment_manager, editable, tests, docs):
    """ Install the project in a new environemnt.

    Creates a clean environment using the specified environment management
    system and installs all required packages for the project. Optionally
    installs further dependencies required for testing and building
    documentation.
    """
    message = "Creating environment '{}' with {}"
    click.echo(
        click.style(
            message.format(
                environment_manager.environment,
                environment_manager.manager,
            ),
            bold=True,
        )
    )

    packages = dependencies[:]
    if tests:
        packages += test_dependencies
    if docs:
        packages += doc_dependencies

    environment_manager.create()
    environment_manager.install(packages)
    environment_manager.install_source(ets_repo_path, editable=editable)


@cli.command()
@runtime_option
@environment_option
@environment_manager_option
@verbose_option
def test(runtime, environment, environment_manager, verbose):
    module = 'ets.tests'
    message = "Running tests for '{}' in '{}'"
    click.echo(
        click.style(
            message.format(module, environment_manager.environment),
            bold=True,
        )
    )
    environment_manager.run_tests(
        module,
        coveragerc=ets_repo_path / "setup.cfg"
    )


@cli.command()
@runtime_option
@environment_option
@environment_manager_option
@verbose_option
def flake8(runtime, environment, environment_manager, verbose):
    dir = 'ets'
    message = "Running flake8 for '{}' in '{}'"
    click.echo(
        click.style(
            message.format(dir, environment_manager.environment),
            bold=True,
        )
    )
    environment_manager.flake8(ets_repo_path / dir)


@cli.command()
@runtime_option
@environment_option
@environment_manager_option
@verbose_option
def bandit(runtime, environment, environment_manager, verbose):
    dir = 'ets'
    message = "Security checks for '{}' in '{}'"
    click.echo(
        click.style(
            message.format(dir, environment_manager.environment),
            bold=True,
        )
    )
    environment_manager.bandit(ets_repo_path / dir)


@cli.command()
@runtime_option
@environment_option
@environment_manager_option
@verbose_option
def pydocstyle(runtime, environment, environment_manager, verbose):
    dir = 'ets'
    message = "Checking docstrings for '{}' in '{}'"
    click.echo(
        click.style(
            message.format(dir, environment_manager.environment),
            bold=True,
        )
    )
    environment_manager.pydocstyle(ets_repo_path / dir)


@cli.command()
@runtime_option
@environment_option
@environment_manager_option
@verbose_option
def mypy(runtime, environment, environment_manager, verbose):
    dir = 'ets'
    message = "Running mypy for '{}' in '{}'"
    click.echo(
        click.style(
            message.format(dir, environment_manager.environment),
            bold=True,
        )
    )
    environment_manager.mypy(ets_repo_path / dir)


@cli.command()
@runtime_option
@environment_option
@environment_manager_option
@verbose_option
def apidoc(runtime, environment, environment_manager, verbose):
    package = "ets"
    click.echo("Generating API documentation for '{}' in '{}'".format(
        package,
        environment_manager.environment))
    environment_manager.apidoc(
        ets_repo_path / package,
        ets_repo_path / "docs" / "source" / "api",
        exclude=[str(ets_repo_path / package / "scripts")],
    )


@cli.command()
@runtime_option
@environment_option
@environment_manager_option
@verbose_option
def build_docs(runtime, environment, environment_manager, verbose):
    click.echo("Building documentation for '{}'".format(
        environment_manager.environment))
    environment_manager.build_docs(docs_dir=ets_repo_path / "docs")


@cli.command()
@runtime_option
@environment_option
@environment_manager_option
@click.argument('command', nargs=-1, required=True)
def run(runtime, environment, environment_manager, command):
    print(command)
    environment_manager.invoke_script(*command)


@cli.command()
@runtime_option
@environment_option
@environment_manager_option
def clean(runtime, environment, environment_manager):
    click.echo("Cleaning environment '{}'".format(
        environment_manager.environment))
    environment_manager.clean()


@cli.command()
@runtime_option
@click.option(
    "--environment-manager",
    default='venv',
    help="Environment management tool to use",
)
@docs_option
def test_clean(runtime, environment_manager, docs):
    """ Run tests and build documentation in a clean environment.

    A clean environment is created for the test run, and removed
    again afterwards.
    """
    args = [
        "--runtime={}".format(runtime),
        "--environment-manager={}".format(environment_manager),
    ]
    if docs:
        install_args = args + ['--docs']
    else:
        install_args = args + ['--no-docs']

    try:
        install(args=install_args, standalone_mode=False)
        flake8(args=args, standalone_mode=False)
        mypy(args=args, standalone_mode=False)
        bandit(args=args, standalone_mode=False)
        pydocstyle(args=args, standalone_mode=False)
        test(args=args, standalone_mode=False)
        if docs:
            apidoc(args=args, standalone_mode=False)
            build_docs(args=args, standalone_mode=False)
    finally:
        clean(args=args, standalone_mode=False)


if __name__ == "__main__":
    cli(prog_name="python etstool.py")
