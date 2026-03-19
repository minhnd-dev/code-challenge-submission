import typer
from rich import print

app = typer.Typer(help="Data CLI - A data processing tool")


@app.command()
def main(name: str = "World") -> None:
    print(f"Hello, {name}!")


if __name__ == "__main__":
    app()