import typer


app = typer.Typer()


@app.command()
def up():
    # RaiseBuilder.create_whisk_resources()
    typer.echo('"up" command non-implemented command.')

@app.command()
def destroy():
    # RaiseBuilder.destroy_whisk_resources()
    typer.echo('"destroy" command non-implemented command.')