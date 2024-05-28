import os
import requests


class LinkedinProfileScrapper:
    def __init__(self):
        self.gist_url = ("https://gist.githubusercontent.com/mohamed-2112/44bff0285827d41d53cf16356c945450/raw"
                         "/a7fab86f801de43c8011d5f93a863da41e80b682/john-marty.json")

    def scrape_linkedin_profile(self, linkedin_profile_url: str, mock: bool = False):
        """scrape information from LinkedIn profiles,
        Manually scrape the information from the LinkedIn profile"""

        if mock:
            response = self.__request_gist()
        else:
            response = self.__request_scrape(linkedin_profile_url)

        data = self.__clean_response(response)
        print(data)
        return data

    def __request_gist(self):
        response = requests.get(
            self.gist_url,
            timeout=10
        )
        return response

    def __request_scrape(self, linkedin_profile_url: str):
        headers = {'Authorization': f'Bearer {os.environ.get("PROXYCURL_API_KEY")}'}
        api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'

        params = {
            'linkedin_profile_url': linkedin_profile_url,
        }
        response = requests.get(api_endpoint,
                                params=params,
                                headers=headers,
                                timeout=10)
        return response

    def __clean_response(self, response):
        data = response.json()
        data = {
            k: v
            for k, v in data.items()
            if v not in ([], "", "", None)
            and k not in ["people_also_viewed", "certifications"]
        }
        if data.get("groups"):
            for group_dict in data.get("groups"):
                group_dict.pop("profile_pic_url")
        return data
