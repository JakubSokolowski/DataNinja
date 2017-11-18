import database.ads_parser
import database.ads

#database.ads.create_ads_db('ads_2016_11_01.db')
#database.ads.create_ads_db('ads_2016_12_01.db')
database.ads_parser.parse("/home/jakub/DataNinja/data/ads/ads_2016_12_01", 1000)
