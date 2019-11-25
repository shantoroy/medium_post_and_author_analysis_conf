from bs4 import BeautifulSoup
from selenium import webdriver
import re
import json


class AuthorDetails(object):

    def __init__(self, soup, link=None):
        self.page_soup = soup
        self.link = link

    def info_json_response(self):
        try:
            for tag in self.page_soup.find_all('script'):
                if 'window.__APOLLO_STATE__' in tag.text:
                    j_data = tag.text
            return j_data[26:]
        except Exception as e:
            error_trace = {}
            error_trace["link"] = self.link
            error_trace["method"] = "info_json_response"
            error_trace["message"] = str(e)
            print(json.dumps(error_trace, indent=4))
        return ""

    def find_first_key_user(self, json_data):
        try:
            find_key_string = [re.compile("^User:*").match]
            required_key = [k for k, v in json_data.items()
                            if any(item(k) for item in find_key_string)]
            return required_key[0]
        except Exception as e:
            error_trace = {}
            error_trace["link"] = self.link
            error_trace["method"] = "find_first_key_user"
            error_trace["message"] = str(e)
            print(json.dumps(error_trace, indent=4))
        return ""

    def find_first_key_social(self, json_data):
        try:
            find_key_string = [re.compile("^\$User:.*socialStats$").match]
            required_key = [k for k, v in json_data.items()
                            if any(item(k) for item in find_key_string)]
            return required_key[0]
        except Exception as e:
            error_trace = {}
            error_trace["link"] = self.link
            error_trace["method"] = "find_first_key_social"
            error_trace["message"] = str(e)
            print(json.dumps(error_trace, indent=4))
        return ""

    def get_author_details(self, key, json_data):
        try:
            user_name = json_data[key]['username']
            author_name = json_data[key]['name']
            author_bio = json_data[key]['bio']
            author_twitter = json_data[key]['twitterScreenName']
            return user_name, author_name, author_bio, author_twitter
        except Exception as e:
            error_trace = {}
            error_trace["link"] = self.link
            error_trace["method"] = "get_author_details"
            error_trace["message"] = str(e)
            print(json.dumps(error_trace, indent=4))
        return ""

    def get_author_social(self, key, json_data):
        try:
            user_following = json_data[key]['followingCount']
            author_follower = json_data[key]['followerCount']
            return user_following, author_follower
        except Exception as e:
            error_trace = {}
            error_trace["link"] = self.link
            error_trace["method"] = "get_author_social"
            error_trace["message"] = str(e)
            print(json.dumps(error_trace, indent=4))
        return ""

    def get_other_post_links_titles(self):
        try:
            other_post_links = []
            other_post_titles = []
            # my_tag = "a"
            for i in self.page_soup.find_all('a', {"rel": "noopener"}):
                if i.find('h1'):
                    new_link = i.get('href').split("?")[0]
                    if new_link.startswith("http"):
                        other_post_links.append(new_link)
                    else:
                        other_post_links.append("https://medium.com" + new_link)

                    other_post_titles.append(i.text)
            return other_post_links, other_post_titles
        except Exception as e:
            error_trace = {}
            error_trace["link"] = self.link
            error_trace["method"] = "get_other_post_links_titles"
            error_trace["message"] = str(e)
            print(json.dumps(error_trace, indent=4))
        return ""
