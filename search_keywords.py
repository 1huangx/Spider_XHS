import json
import re
import requests
from one import OneNote
from xhs_utils.xhs_util import get_headers, get_search_data, get_params, js, check_cookies

cookies = check_cookies()

search_api = '/api/sns/web/v1/search/notes'

class SearchXHS:
    """the class defined the functions to search xiaohongshu by keyword"""
    def __init__(self):
        self.search_url = "https://edith.xiaohongshu.com/api/sns/web/v1/search/notes"
        self.headers = get_headers()
        self.params = get_params()
        self.oneNote = OneNote(cookies)
    
    async def search(self, query: str):
        """search xiaohongshu by keyword"""
        params = get_search_data()
        params['keyword'] = query
        params['page'] = 1

        note_ids = []
        while True :
            params = json.dumps(params)
            ret = js.call('get_xs', search_api, params, cookies['a1'])
            self.headers['x-s'], self.headers['x-t'] = ret['X-s'], str(ret['X-t'])

            try:
                response = requests.post(self.search_url, headers=self.headers, cookies=cookies, data=params.encode('utf-8'))
                response.raise_for_status()
                res = response.json()

                params['page'] += 1
                
                if items:= res.get('data' ):
                    for item in items:
                        note_id = item.get('id')
                        if note_id not in note_ids:
                            note_ids.append(note_id)

                if not res['data']['has_more']:
                    print('no more notes')
                    break
            except Exception as e:
                print(e)
                raise e
        return note_ids
    

    async def search_notes(self, query: str):
        """search xiaohongshu by keyword and save the notes to onenote
        
        Args:
            query: the keyword to search
            """
        params = get_search_data()
        params['sort'] = 'general'
        params['keyword'] = query
        params['page'] = 1

        while True:
            params = json.dumps(params)
            ret = js.call('get_xs', search_api, params, cookies['a1'])
            self.headers['x-s'], self.headers['x-t'] = ret['X-s'], str(ret['X-t'])

            try:
                response = requests.post(self.search_url, headers=self.headers, cookies=cookies, data=params.encode('utf-8'))
                response.raise_for_status()
                res = response.json()

                items = res['data']
                params['page'] += 1
                
                for note in items['items']:
                    self.oneNote.save_one_note_info(self.oneNote.detail_url + note['id'], True, '', 'datas_search')
                    
                if not res['data']['has_more']:
                    print('no more notes')
                    break
            except Exception as e:
                print(e)
                raise e
        
        