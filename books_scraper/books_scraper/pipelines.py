# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


from itemadapter import ItemAdapter


class BooksScraperPipeline:
    """Pipeline for cleaning and normalizing scraped data."""

    RATING_MAP = {
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5,
    }

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # Normalize price to float
        raw_price = adapter.get("price")
        if raw_price:
            cleaned_price = raw_price.replace("£", "").strip()
            adapter["price"] = float(cleaned_price)

        # Normalize amount_in_stock to int or None
        raw_amount = adapter.get("amount_in_stock")
        adapter["amount_in_stock"] = int(raw_amount) if raw_amount else None

        # Normalize rating to int
        raw_rating = adapter.get("rating")
        adapter["rating"] = self.RATING_MAP.get(raw_rating)

        # Strip description
        description = adapter.get("description")
        if description:
            adapter["description"] = description.strip()

        # Ensure UPC exists
        if not adapter.get("upc"):
            raise ValueError("UPC is missing")

        return item
