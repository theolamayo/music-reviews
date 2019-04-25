"""
Helpers for exporting a written to different formats review.
"""

import os
import re

import click
from jinja2 import Template

from .creator import fill_template, import_template, write_review


def export_review(data, root=os.getcwd(), extension='md'):
    """Exports review in given format. Formats metadata and content."""
    template = import_template(root, 'template.' + extension)
    content = replace_track_tags(data['content']).format(**data)

    if extension == 'md':
        content = wiki_to_markdown(content)
        # ensure tracks are sorted
        tracks = [data['tracks'][i] for i in sorted(data['tracks'])]
        # use general review template
        formatted_review = fill_template(
            template=template,
            artist=data['artist'],
            album=data['album'],
            year=data['year'],
            rating=data['rating'],
            uri=data['uri'],
            picks=data['picks'],
            tracks=tracks,
            state=data['state'],
            content=content,
            date=data['date']
        )
    else:
        formatted_review = fill_html(template, data)
    write_review(
        content=formatted_review,
        folder=data['artist_tag'],
        filename=data['album_tag'],
        root=root,
        extension=extension,
        overwrite=True
    )


def replace_track_tags(content):
    """Replaces tags like {4} to formatting compatible tags like {tracks[4]}."""
    return re.sub('{(\d+)}', '{tracks[\\1]}', content)


def wiki_to_markdown(string):
    """Translates the string from vimwiki format to markdown."""
    string = re.sub('\*', '**', string)
    string = re.sub('_', '*', string)
    return string


def fill_html(template, data):
    """Fills Jinja template with data to generate a HTML string."""
    template = Template(template)
    return template.render(**data)
