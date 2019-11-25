from author_details import AuthorDetails
from post_details import PostDetais
import json
import time
from bs4 import BeautifulSoup
from selenium import webdriver
import requests


def page_info(link):
    try:
        CHROME_DRIVER_PATH = '/home/mrx/Downloads/chromedriver'
        driver = webdriver.Chrome(CHROME_DRIVER_PATH)
        url = link
        driver.get(url)
        scrolls = 4
        while scrolls > 0:
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight-1000);")
            time.sleep(2)
            scrolls -= 1
        time.sleep(1)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
        return soup
    except Exception as e:
        error_trace = {}
        error_trace["link"] = link
        error_trace["method"] = "page_info"
        error_trace["message"] = str(e)
        print(json.dumps(error_trace, indent=4))
    return ""


def get_post_info(link):
    try:
        headers = requests.utils.default_headers()
        headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
        })
        request_link = requests.get(link, headers=headers)
        # request_link = urllib.request.urlopen(link, headers=headers)
        request_content = BeautifulSoup(request_link.content, 'html.parser')
        post_details = PostDetais(request_content, link)

        json_basic_script = json.loads(post_details.json_response_basic())
        json_full_script = json.loads(post_details.json_response_whole())
        first_key_element = post_details.find_first_key(json_full_script)

        post_title = post_details.get_title()
        # author_name, author_link = post_details.get_author_name(json_basic_script)
        creation_date, published_date, modified_date = post_details.get_date(json_basic_script)
        post_tags = post_details.get_tags(json_basic_script)
        post_readtime = post_details.get_read(first_key_element, json_full_script)
        post_claps, post_voters = post_details.get_upvote(first_key_element, json_full_script)
        post_contents = post_details.get_post_content()
        post_responses = post_details.get_response(first_key_element, json_full_script)
        return post_title, published_date, post_tags, (str(post_readtime))[:4], post_claps, post_voters, post_contents, post_responses
    except Exception as e:
        error_trace = {}
        error_trace["link"] = link
        error_trace["method"] = "get_post_info"
        error_trace["message"] = str(e)
        print(json.dumps(error_trace, indent=4))
    return ""


def final_data_collection(final_author_links):
    try:
        count = 1
        final_author_data = []
        # test = ["https://medium.com/@preethikasireddy", "https://medium.com/@noamlevenson"]
        # for link in test:
        for link in final_author_links:
            try:
                other_post_data = []
                page_contents = page_info(link)
                print("\n ############################")
                print("Collecting Author {}: {}".format(count, link))
                count += 1
                post_count = 0
                author_details = AuthorDetails(page_contents, link)

                json_script = json.loads(author_details.info_json_response())
                user_data_key = author_details.find_first_key_user(json_script)
                user_social_key = author_details.find_first_key_social(json_script)

                user_name, author_name, author_bio, author_twitter = author_details.get_author_details(user_data_key, json_script)
                following, followers = author_details.get_author_social(user_social_key, json_script)
                other_post_links, other_post_titles = author_details.get_other_post_links_titles()

                print("No of other posts for", author_name, "are: ", len(other_post_links))
                for item in other_post_links:
                    print("Collecting post from", post_count, ": ", item)
                    post_count += 1
                    time.sleep(1)

                    try:
                        title, date, tags, read, claps, voters, contents, responses = get_post_info(item)
                    except Exception as e:
                        error_trace = {}
                        error_trace["link"] = link
                        error_trace["method"] = "tried to get post info"
                        error_trace["message"] = str(e)
                        print(json.dumps(error_trace, indent=4))

                    single_post_info = {
                        "title": title,
                        "publish date": date[:10],
                        "tags": tags,
                        "read time": read,
                        "claps": claps,
                        "voters": voters,
                        # "contents": contents,
                        "responses": responses
                    }
                    other_post_data.append(single_post_info)

                single_author_info = {
                    "username": user_name,
                    "name": author_name,
                    "bio": author_bio,
                    "author_twitter": author_twitter,
                    "following": following,
                    "followers": followers,
                    "other_posts": other_post_data,
                    "other_post_titles": other_post_titles
                }
                final_author_data.append(single_author_info)
            except Exception as e:
                error_trace = {}
                error_trace["link"] = link
                error_trace["method"] = "tried to get author info"
                error_trace["message"] = str(e)
                print(json.dumps(error_trace, indent=4))
        return final_author_data
    except Exception as e:
        error_trace = {}
        error_trace["link"] = link
        error_trace["method"] = "final_data_collection"
        error_trace["message"] = str(e)
        print(json.dumps(error_trace, indent=4))
    return ""


if __name__ == '__main__':
    author_links = []
    with open("related_data_rm_duplicacy.json", "r") as f:
        author_data = json.load(f)
    for key in author_data:
        author_links.append(key['author_link'])

    # Final Author list after removing duplicacy
    author_links_unique = list(set(author_links))
    print(len(author_links_unique))

    final_data = final_data_collection(author_links_unique)
    with open("author_info_final_paper.json", 'w') as fp:
        json.dump(final_data, fp)
