import json

with open("integrated_all_post_data.json", "r") as f:
    data = json.load(f)
unique_post = {each['title']: each for each in data}
listed_dictionary_items = list(unique_post.values())
with open("related_data_rm_duplicacy.json", "w") as f:
    json.dump(listed_dictionary_items, f)
print("# of post after removing duplicacy = ", len(listed_dictionary_items))
