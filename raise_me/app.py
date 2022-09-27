from typing import Optional

import typer

from raise_me import RAISE_CONFIG_PATH, RAISE_DEPLOYMENT_PATH
from raise_me.build import OpenwhiskBuilder
from raise_me.parser import ConfigParser, DeploymentParser
from raise_me.wsk import WskClient


app = typer.Typer()


@app.command()
def up(config_path: Optional[str] = None, events_path: Optional[str] = None):
    conf_path = RAISE_CONFIG_PATH if config_path is None else config_path
    events_path = RAISE_DEPLOYMENT_PATH if events_path is None else events_path
    
    typer.echo('Creating RaiseMe OpenWhisk resources...')
    typer.echo(f' Configuration file: {conf_path}')
    typer.echo(f' Deployment file: {events_path}')
    
    OpenwhiskBuilder(
        wsk_client=WskClient.from_config(
            config=ConfigParser.from_yaml(path=conf_path)
    )).create_resources(
        deployment=DeploymentParser.from_yaml(path=events_path))

    typer.echo('OpenWhisk resources created!')


@app.command()
def destroy(config_path: Optional[str] = None):
    conf_path = RAISE_CONFIG_PATH if config_path is None else config_path

    typer.echo('Destroying RaiseMe OpenWhisk resources...')

    OpenwhiskBuilder(
        wsk_client=WskClient.from_config(
            config=ConfigParser.from_yaml(path=conf_path)
    )).destroy_resources()

    typer.echo('OpenWhisk resources destroyed!')