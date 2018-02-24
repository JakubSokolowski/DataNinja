import database.ads

# database.ads.create_ads_db('ads_2016_11_01.db')
# database.ads.create_ads_db('ads_2016_12_01.db')
# database.ads.create_ads_db('001_anonimized.db')
# database.ads_parser.parse("/home/jakub/DataNinja/data/ads/001_anonimized", 10)
database.ads_parser.parse2("/home/jakub/DataNinja/data/ads/001_anonimized", 1000)
