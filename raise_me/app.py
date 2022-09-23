from typing import Optional

import typer

from raise_me import RAISE_CONFIG_PATH, RAISE_DEPLOYMENT_PATH
from raise_me.build import OpenwhiskBuilder
from raise_me.parser import ConfigParser, DeploymentParser
from raise_me.wsk import WskClient


app = typer.Typer()


@app.command()
def up(config_path: Optional[str] = None, deploy_path: Optional[str] = None):
    conf_path = RAISE_CONFIG_PATH if config_path is None else config_path
    deploy_path = RAISE_DEPLOYMENT_PATH if deploy_path is None else deploy_path
    
    typer.echo('Creating OpenWhisk resources...')
    
    OpenwhiskBuilder(
        wsk_client=WskClient.from_config(
            config=ConfigParser.from_yaml(path=conf_path)
    )).create_resources(
        deployment=DeploymentParser.from_yaml(path=deploy_path))

    typer.echo('OpenWhisk resources created!')


@app.command()
def destroy(config_path: Optional[str] = None):
    conf_path = RAISE_CONFIG_PATH if config_path is None else config_path

    typer.echo('Destroying OpenWhisk resources...')

    OpenwhiskBuilder(
        wsk_client=WskClient.from_config(
            config=ConfigParser.from_yaml(path=conf_path)
    )).destroy_resources()

    typer.echo('OpenWhisk resources destroyed!')