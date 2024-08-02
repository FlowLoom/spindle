import click

__all__ = ['parse_slide_range']


def parse_slide_range(ctx, param, value):
    if value is None:
        return None
    try:
        if '-' in value:
            start, end = map(int, value.split('-'))
            if start is end:
                return int(start - 1)

            if start < 1 or end < start:
                raise click.BadParameter('Slide range must start at 1 and be in the format "start-end" where start < end or "start" where start is the slide number.')
            return (start - 1, end)  # Convert to 0-based index
        else:
            slide = int(value)
            return slide - 1  # Convert to 0-based index
    except ValueError:
        raise click.BadParameter('Slide range must be a number or a range (e.g., 1-3). Count starts at 1')
