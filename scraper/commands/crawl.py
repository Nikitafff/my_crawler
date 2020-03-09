from scraper import engine
from scraper.spiders import fortnite


def execute(args):
    engine.start(fortnite.BASE_URL,  fortnite.parse_fortnite, args.pages, args.outfile, args.format)

