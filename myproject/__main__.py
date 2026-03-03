import click
from .processor import DataProcessor

@click.group()
def cli():
    """Data processing command line interface."""
    pass

@cli.command()
@click.argument('filename')
def process(filename):
    """Process a data file and show results."""
    config_obj = Config(config)
    processor = DataProcessor(config_obj)
    data = processor.read_file(filename)
    stats = processor.get_stats(data)
    click.echo(f"File: {filename}")
    click.echo(f"Records: {stats['count']}")
    click.echo(f"Total value: {stats['sum']}")
    click.echo(f"Average value: {stats['mean']:.2f}")

if __name__ == '__main__':
    cli()
