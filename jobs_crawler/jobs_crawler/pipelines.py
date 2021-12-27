# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter
import psycopg2


class JobsCrawlerPipeline:

    def __init__(self):
        self.connection = None
        self.cur = None

    def open_spider(self, spider):
        hostname = 'localhost'
        username = 'donor'
        password = 'jaimelachatteetlepate'
        database = 'job_market'
        self.connection = psycopg2.connect(
            host=hostname, user=username, password=password,
            dbname=database)
        self.cur = self.connection.cursor()

    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()

    def process_item(self, item, spider):
        for field in item.fields:
            item.setdefault(field, 'NULL')
        try:
            self.cur.execute(
                "INSERT INTO jobs(url, title, company, location, type, industry, text, remote, created_at) "
                "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (item['url'][0], item['title'][0], item['company'][0], item['location'][0], item['type'][0],
                 item['industry'][0], item['text'][0], item['remote'][0], item['created_at'][0]))
            self.connection.commit()
        except:
            self.connection.rollback()
            raise
        return item
