import json
final_count = 0
final_json_data = []

file_name_list = ["smart-contract.json", "metamask.json",
                      "solidity.json", "vyper.json",
                      "truffle.json", "web3.json", "erc20.json"]
tag_list = ["smart contracts", "metamask", "solidity", "vyper",
                "truffle", "web3", "erc20"]

for file_name, tag in zip(file_name_list, tag_list):

    count = 0
    json_data = json.load(open("post_data/"+file_name))

    for key in json_data:
        tags = key['tags']
        titles = key['title']

        if tag in key['title']:
            final_json_data.append(key)
            count += 1
        else:
            for item in tags:
                if tag in item.lower():
                    final_json_data.append(key)
                    count += 1
                    final_count += 1
    print("Number of total post for ", tag, "is =", count)

# Output the updated file with pretty JSON
open("post_data/related_all_post_data_without_ethereum.json", "w").write(
        json.dumps(final_json_data, sort_keys=True, indent=4, separators=(',', ': '))
    )

print("The number of total post is: ", final_count)
