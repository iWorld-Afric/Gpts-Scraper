import click
from scraper.main_scraper import scrape_website_from_db

@click.group()
def cli():
    pass

@click.command()
@click.option('--db_path', default='visited_urls.db', help='Path to the visited URLs database.')
@click.option('--filter_path', default='/gpt-store/', help='Path to filter the URLs for scraping.')
@click.option('--max_workers', default=10, help='Maximum number of concurrent workers.')
def start(db_path, filter_path, max_workers):
    """ Start the scraping process with specified URL, path, and depth. """
    scrape_website_from_db(db_path, filter_path, max_workers)

cli.add_command(start)

if __name__ == '__main__':
    cli()
