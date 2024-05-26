import os
import requests


class LinkedinProfileScrapper:
    def __init__(self):
        self.gist_url = ("https://gist.githubusercontent.com/mohamed-2112/44bff0285827d41d53cf16356c945450/raw"
                         "/7a128d36caa99e79f5476016e5915fb1dae5ada4/john-marty.json")

    def scrape_linkedin_profile(self, linkedin_profile_url: str, mock: bool = False):
        """scrape information from LinkedIn profiles,
        Manually scrape the information from the LinkedIn profile"""

        if mock:
            response = requests.get(
                self.gist_url,
                timeout=10
            )
        else:
            headers = {'Authorization': f'Bearer {os.environ.get("PROXYCURL_API_KEY")}'}
            api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'

            params = {
                'linkedin_profile_url': linkedin_profile_url,
            }
            response = requests.get(api_endpoint,
                                    params=params,
                                    headers=headers,
                                    timeout=10)

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
        print(data)
        return data
