#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ExternalApiFilterRequest import ExternalApiFilterRequest
from ExternalApiTagRequest import ExternalApiTagRequest
from Filter import Filter
from ExternalApiCompareRequest import ExternalApiCompareRequest
from ExternalApiSearchRequest import ExternalApiSearchRequest
from Version import Version
from authorization.Auth import Auth

import hashlib
from os import path

try:
    import simplejson as json
except ImportError:
    import json

json_encode = lambda x: json.dumps(x)
json_decode = lambda x: json.loads(x)


class TacytApp(Auth):

    API_SEARCH_URL = "/api/"+Version.API_VERSION+"/search"
    API_DETAILS_URL = "/api/"+Version.API_VERSION+"/details"
    API_FILTERS_URL = "/api/"+Version.API_VERSION+"/filters"
    API_TAGS_URL = "/api/"+Version.API_VERSION+"/tags"
    API_COMPARER_URL = "/api/"+Version.API_VERSION+"/compare"
    API_UPLOAD_URL = "/api/" +Version.API_VERSION+ "/upload"

    def __init__(self, app_id, secret_key):
        '''
        Create an instance of the class with the Application ID and secret obtained from Tacyt
        @param $app_id
        @param $secret_key
        '''
        super(TacytApp, self).__init__(app_id, secret_key)


    def search_apps(self, query, numberPage=None, maxResults=None, outfields = None, grouped=None):
        '''
        @param $query The query string will filter the search results.
        @param $numberPage A number greater or equal to 1 indicating the page of results which have to be retrieved.
        @param $maxResults A number between 1 and 100 indicating the max number of apps which have to be retrieved.
        @return Json structure with the keys to the Applications found.
        '''
        result = ExternalApiSearchRequest(query, numberPage, maxResults, outfields, grouped)
        return self.http_post(self.API_SEARCH_URL, None, body=result.get_json_encode_for_search())

    def get_app_details(self, key):
        '''
        @param $key The key of an application.
        @return Json structure with the details of an application.
        '''
        return self.http_get(self.API_DETAILS_URL + "/" + key, None)

    def list_tags(self):
        '''
        @return A list of tags that have been created.
        '''
        result = ExternalApiTagRequest(ExternalApiTagRequest.LIST_REQUEST, None, None)
        return self.http_post(self.API_TAGS_URL, None, body=result.get_json_encode_dict_for_tag_based_requests())

    def assign_tag(self, tag, app_keys):
        '''
		This method associates a tag created with applications.
        @param $tag the name of the tag to create
        @param $app_keys Key applications that want to associate with the tag
        @return A list of applications associates with a tag.
        '''
        result = ExternalApiTagRequest(ExternalApiTagRequest.CREATE_REQUEST, tag, app_keys)
        return self.http_post(self.API_TAGS_URL, None, body=result.get_json_encode_dict_for_tag_based_requests())

    def remove_tag_for_apps(self, tag, app_keys):
        '''
		This method remove a tag associate with applications.
        @param $tag the name of the tag to create
        @param $app_keys Key applications that want to remove with the tag
        '''
        result = ExternalApiTagRequest(ExternalApiTagRequest.REMOVE_REQUEST, tag, app_keys)
        return self.http_post(self.API_TAGS_URL, None, body=result.get_json_encode_dict_for_tag_based_requests())

    def delete_tag(self, tag):
        '''
        This method delete a tag.
        @param $tag the name of the tag you want to delete.
        '''
        result = ExternalApiTagRequest(ExternalApiTagRequest.REMOVE_ALL_REQUEST, tag, None)
        return self.http_post(self.API_TAGS_URL, None, body=result.get_json_encode_dict_for_tag_based_requests())

    def create_filter(self, filter):
        '''
        This method create a filter.
        @param $filter Filter structure.
        '''
        result = ExternalApiFilterRequest(ExternalApiFilterRequest.CREATE_REQUEST, filter, 0, None)
        return self.http_post(self.API_FILTERS_URL, None, body=result.get_json_encode_for_filter_based_requests())

    def update_filter(self, filter):
        '''
        This method update changes associates with a filter.
        @param $filter Filter structure.
        '''
        result = ExternalApiFilterRequest(ExternalApiFilterRequest.UPDATE_REQUEST, filter, 0, None)
        return self.http_post(self.API_FILTERS_URL, None, body=result.get_json_encode_for_filter_based_requests())

    def read_group_filters(self):
        '''
        @return all group filters created
        '''
        result = ExternalApiFilterRequest(ExternalApiFilterRequest.READ_GROUPS, None, 0, None)
        return self.http_post(self.API_FILTERS_URL, None, body=result.get_json_encode_for_filter_based_requests())

    def read_all_filters(self):
        '''
        @return a list of filters creates.
        '''
        result = ExternalApiFilterRequest(ExternalApiFilterRequest.READ_REQUEST, None, 0, None)
        return self.http_post(self.API_FILTERS_URL, None, body=result.get_json_encode_for_filter_based_requests())

    def read_one_filter(self, filter_id):
        '''
        @param $filter_id id of the filter you want to read.
        @return This method returns the details of filter associate with this filter_id.
        '''
        filter = Filter(filter_id)
        result = ExternalApiFilterRequest(ExternalApiFilterRequest.READ_REQUEST, filter, 0, None)
        return self.http_post(self.API_FILTERS_URL, None, body=result.get_json_encode_for_filter_based_requests())

    def delete_filter(self, filter_id):
        '''
     	This method delete a filter create.
        @param $filter_id id of the filter you want to delete.
        '''
        filter = Filter(filter_id)
        result = ExternalApiFilterRequest(ExternalApiFilterRequest.DELETE_REQUEST, filter, 0, None)
        return self.http_post(self.API_FILTERS_URL, None, body=result.get_json_encode_for_filter_based_requests())

    def search_public_filter(self, query, page):
        '''
        @param $query any word or phrase within the description or title Filter
        @param $page A number greater or equal to 1 indicating the page of results which have to be retrieved.
        @return A list of public filters(Visibility = Public)
        '''
        result = ExternalApiFilterRequest(ExternalApiFilterRequest.SEARCH_PUBLIC_FILTER_REQUEST, None, page, query)
        return self.http_post(self.API_FILTERS_URL, None, body=result.get_json_encode_dict_filter_for_content_based_requests())

    def list_detected_apps(self, page,filter_id):
        '''
        @param $filter_id id to the filter.
        @return Json structure with the details of applications detected by the filter.
        '''
        result = ExternalApiFilterRequest(ExternalApiFilterRequest.LIST_DETECTIONS_REQUEST, None, page, filter_id)
        return self.http_post(self.API_FILTERS_URL, None, body=result.get_json_encode_dict_filter_for_content_based_requests())

    def list_group_detected_apps(self, page, groupName):
        '''
        @param $groupName name of the group.
        @param $page A number greater or equal to 1 indicating the page of results which have to be retrieved.
        @return Json structure with the details of applications detected by the filters group.
        '''
        result = ExternalApiFilterRequest(ExternalApiFilterRequest.LIST_GROUP_DETECTIONS, None, page, groupName)
        return self.http_post(self.API_FILTERS_URL, None, body=result.get_json_encode_dict_filter_for_content_based_requests())

    def unsubscribe_public_filter(self, filter_id):
        '''
        With this method you can subscribe to filter.
        @param $filter_id id to filter you want subscribe.
        '''
        result = ExternalApiFilterRequest(ExternalApiFilterRequest.UNSUBSCRIBE_REQUEST, None, 0, filter_id)
        return self.http_post(self.API_FILTERS_URL, None, body=result.get_json_encode_dict_filter_for_content_based_requests())

    def subscribe_public_filter(self, filter_id):
        '''
        With this method you can unsubscribe to filter.
        @param $filter_id id to filter you want unsubscribe.
        '''
        result = ExternalApiFilterRequest(ExternalApiFilterRequest.SUBSCRIBE_REQUEST, None, 0, filter_id)
        return self.http_post(self.API_FILTERS_URL, None, body=result.get_json_encode_dict_filter_for_content_based_requests())

    def get_RSS_info(self, filter_id):
        '''
        This method get the RSS information of a filter.
        @param $filter_id id to filter you want get RSS information.
        '''
        result = ExternalApiFilterRequest( ExternalApiFilterRequest.GET_RSS_REQUEST, None, None, filter_id)
        return self.http_post(self.API_FILTERS_URL, None, body=result.get_json_encode_dict_filter_for_content_based_requests())

    def get_group_RSS_info(self, groupName):
        '''
        This method get the RSS information of a filters group.
        @param $groupName name of the filters group you want get RSS information.
        '''
        result = ExternalApiFilterRequest(ExternalApiFilterRequest.GET_GROUP_RSS, None, None, groupName)
        return self.http_post(self.API_FILTERS_URL, None, body=result.get_json_encode_dict_filter_for_content_based_requests())

    def compare_apps(self, apps, include_details):
        '''
        @param $apps the key of the app you want to compare. The array of apps is limited to 10 apps.
        @param $include_details with a value of true in includeDetails you will get not only the matching fields and their values, but all the values defined for the applications.
        '''
        result = ExternalApiCompareRequest(apps, include_details)
        return self.http_post(self.API_COMPARER_URL, None, body=result.get_json_encode_for_compare_apps())

    def upload_app(self, apk_file):
        """
        Upload app to Tacyt
        :param apk_file: path to file apk
        :return: Response
        """
        try:
            f = open(apk_file, 'rb')
            file_name = path.basename(f.name)
            file_stream = f.read()
            f.close()
            headers = dict()
            headers[Auth.FILE_HASH_HEADER_NAME] = hashlib.sha1(file_stream).hexdigest()

            return self.http_post_file(self.API_UPLOAD_URL, self.authentication_headers_with_body(self.HTTP_METHOD_POST, self.API_UPLOAD_URL, headers, ""), file_stream, file_name)

        except Exception, e:
            print repr(e)
            return None
        