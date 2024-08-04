import pandas as pd
from pymongo import MongoClient
import count_topic
import global_var
from read_data import write_txt_html_xlsx2db, xlsx2db
import process_mongo
import calculate_index
import sentiment






def main():
        # Establish a connection to MongoDB
    client = MongoClient(global_var.client_url)
    database = client[global_var.database_name]
    articles = database['articles']
    indexs = database['indexs_backend']
    indexs.insert_one({'title':'test'})
    # print('starting write topic count')
    # count_topic.count_topic_all(articles,indexs)
    # print('topic are successfully wrote')
    calculate_index.calculate_all(articles,indexs,None)
    # process_mongo.segment(database,'articles')
    # process_mongo.delete_incomplete_documents(database,'indexs_backend',['text'])
    # process_mongo.map_fields(database,'indexs_backend',global_var.get_field_map())
    # process_mongo.merge(database,'demand','indexs_backend_copy','title','title','indexs_backend_merge2')



if __name__ == "__main__":
    main()
