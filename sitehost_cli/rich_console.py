from rich.console import Console
from rich.theme import Theme
import rich

sitehost_theme = Theme({
    "sitehost": "bold #F5821F",
    "sitehost_grey": "bold black",
    "sitehost_white": "bold white",
})

console = Console(theme=sitehost_theme)