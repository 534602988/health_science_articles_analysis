import os
import pandas as pd
from process_mongo import get_db, insert_with_check
import jieba


def files2db(folder_path, header, collection):
    folder_name = os.path.basename(folder_path)
    author = folder_name.split("_")[1:]
    author = "_".join(author)
    records = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".txt") and file_name.startswith(header):
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
                title = file_name.replace(".txt", "").replace(f"{header}_", "")
                record = {header: content, "title": title, "author": author}
                insert_with_check(collection, record)
                records.append(record)
    return records


def xlsx2db(folder_path, collection):
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".xlsx"):
            file_path = os.path.join(folder_path, file_name)
            df = pd.read_excel(file_path, na_values=["无"], keep_default_na=True)
            df = df.rename(
                columns={"标题": "title", "作者": "author", "阅读量": "read"}
            )
            columns = df.columns
            start_index = columns.get_loc("打赏人数")
            end_index = columns.get_loc("有我关心的内容")
            columns_to_check = columns[start_index : end_index + 1]
            df["data_availability"] = (df[columns_to_check].sum(axis=1) != 0).astype(
                int
            )
            df.fillna(0, inplace=True)
            data_dict = df.to_dict(orient="records")
            for record in data_dict:
                insert_with_check(collection, "title", record)


def segment():
    database = get_db()
    collection = database["articles"].find()
    count = 0
    for record in collection:
        if "text" in record.keys():
            text_seg = " ".join(jieba.lcut(record["text"]))
            record1 = {"title": record["title"], "text_seg": text_seg}
            insert_with_check(database["articles"], record1)
            count += 1
            if count % 1000 == 0:
                print(f"Processed {count} records")


if __name__ == "__main__":
    database = get_db()
    parent_folder = "/workspace/dataset/health_article/article"
    for folder_name in os.listdir(parent_folder):
        folder_path = os.path.join(parent_folder, folder_name)
        #     contents = files2db(folder_path, 'text')
        #     htmls = files2db(folder_path, 'html')
        xlsx2db(folder_path, database["demand"])
