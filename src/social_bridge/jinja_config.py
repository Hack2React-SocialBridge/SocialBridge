from pathlib import Path

from jinja2 import Environment, FileSystemLoader


env = Environment(loader=FileSystemLoader(Path('social_bridge/static/templates/emails')))
