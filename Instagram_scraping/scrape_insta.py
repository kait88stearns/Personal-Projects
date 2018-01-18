import requests
from bs4 import BeautifulSoup
import re
import json.decoder as decoder
import pandas as pd
import time

class make_insta_dataframe:


    def __init__(self, sleep):
        self.sleep = sleep

    def scrape(self, urls, shortcode=False):
        """ Scrapes post information for all urls given, or shortcodes given if shortcode = True.
            Input:
                  urls : list of urls, or list of shortcodes if shortcode= True
                  shortcode : boolean. default = False. set to True if urls is a list of shortcodes
            Output:
                   df: pandas DataFrame with relevant information from scraped posts
        """
        dic=[]
        if shortcode == False:
            for i in range(len(urls)):
                print("{} of {}".format(i,len(urls)))
                info = self.scrape_info(urls[i])
                dic.append(info)
                time.sleep(self.sleep)
        else:
            i=1
            for code in urls:
                print("{} of {}".format(i,len(urls)))
                i += 1
                url ='http://www.instagram.com/p/{}/?taken-by=thedriftcollective'.format(code)
                info = self.scrape_info(url)
                dic.append(info)
                time.sleep(self.sleep)
        df = pd.DataFrame(dic)
        return df

    def scrape_info(self, url):
        """ Scrapes post information for the given url
            Input:
                  url : url of relevant post
            Output:
                   df: dictionary containing relevant post information
        """
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        decode = decoder.JSONDecoder()
        for i in soup.find_all("script", {"type":"text/javascript"}):
            if (re.findall('sharedData', str(i))):
                raw = re.sub('<.+?>', '', str(i))
        without_header =raw[21:-1]
        content = decode.decode(without_header)
        post_content = content['entry_data']['PostPage'][0]['graphql']['shortcode_media']
        taken_at = post_content['taken_at_timestamp']
        number_of_likes = post_content['edge_media_preview_like']['count']
        caption = post_content['edge_media_to_caption']['edges'][0]['node']['text']
        number_of_comments = len(post_content['edge_media_to_comment']['edges'])
        people_tagged = [tagged['node']['user']['username'] for tagged in post_content['edge_media_to_tagged_user']['edges']]
        hashtags =[]
        comments = []
        commenters=[]
        if post_content['edge_media_to_comment']['edges']:
            if post_content['edge_media_to_comment']['edges'][0]['node']['owner']['username'] == 'thedriftcollective':
                caption += (' ' + post_content['edge_media_to_comment']['edges'][0]['node']['text'])
                number_of_comments -= 1
                for i in range(1, number_of_comments + 1):
                    comments.append(post_content['edge_media_to_comment']['edges'][i]['node']['text'])
                    commenters.append(post_content['edge_media_to_comment']['edges'][i]['node']['owner']['username'])
            else:
                comments = [item['node']['text'] for item in post_content['edge_media_to_comment']['edges']]
                commenters = [item['node']['owner']['username'] for item in post_content['edge_media_to_comment']['edges']]
                hashtags += [tag.strip() for tag in re.findall('\#.+?\s', post_content['edge_media_to_comment']['edges'][0]['node']['text'])]
        caption_hashtags = [tag.strip() for tag in re.findall('\#.+?\s', caption)]
        hashtags += caption_hashtags
        people_tagged += [re.sub('\@', '', tag) for tag in re.findall('\@.\w+', caption)]


        return {'taken_at':taken_at, 'url':url, 'number_of_likes' : number_of_likes, 'caption':caption, 'hashtags':hashtags, 'comments': comments, 'commenters' :commenters, 'people_tagged ':people_tagged , 'number_of_comments':number_of_comments }


    def scrape_shortcodes(self, initial_url, ):
        """ Scrapes shortcodes contained in initial_url (ie. the redirect information for urls of the page's posts)
            Input:
                  initial_url : url to initial page
            Output: 
                   df: pandas DataFrame with relevant information from scraped posts
        """
        is_more = True
        shortcodes = []
        next_url = initial_url
        while is_more:
            response = requests.get(next_url)
            print(response.status_code)
            soup = BeautifulSoup(response.text, "html.parser")
            decode = decoder.JSONDecoder()
            home_page = decode.decode(str(soup))
            for i in range(len(home_page['data']['user']['edge_owner_to_timeline_media']['edges'])):
                sc = home_page['data']['user']['edge_owner_to_timeline_media']['edges'][i]['node']['shortcode']
                shortcodes.append(sc)
                time.sleep(self.sleep)
            if home_page['data']['user']['edge_owner_to_timeline_media']['page_info']['has_next_page'] == True:
                nextpage = home_page['data']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']
                next_url = 'https://www.instagram.com/graphql/query/?query_id=17888483320059182&variables=%7B%22id%22%3A%222183125078%22%2C%22first%22%3A12%2C%22after%22%3A%22{}%22%7D'.format(nextpage)
            else:
                is_more = False
        self.shortcodes = shortcodes



    def save_shortcodes(self):
        file_handler = open('shortcode.txt', 'w')
        for code in self.short_codes:
            file_handler.write("{}\n".format(code))
