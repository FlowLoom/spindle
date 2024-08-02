import click

__all__ = ['parse_slide_index']


def parse_slide_index(ctx, param, value):
    if value is None:
        return None
    try:
        return int(value) - 1  # Convert to 0-based index
    except ValueError:
        raise click.BadParameter('Slide index must be a number')
