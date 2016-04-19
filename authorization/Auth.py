#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import time
import json
import hashlib
from authorization.Response import Response
from tacyt.Version import Version
import Error

class Auth(object):

    API_PORT = 443
    API_HTTPS = True
    API_PROXY = None
    API_PROXY_PORT = None

    AUTHORIZATION_METHOD = "11PATHS"
    X_11PATHS_HEADER_PREFIX = "X-11paths-"
    BODY_HASH_HEADER_NAME = X_11PATHS_HEADER_PREFIX + "Body-Hash"
    AUTHORIZATION_HEADER_FIELD_SEPARATOR = " "
    UTC_STRING_FORMAT = "%Y-%m-%d %H:%M:%S"
    CHARSET_ASCII = "US-ASCII"
    CHARSET_ISO_8859_1 = "ISO-8859-1"
    CHARSET_UTF_8 = "UTF-8"
    HTTP_METHOD_GET = "GET"
    HTTP_METHOD_POST = "POST"
    HTTP_METHOD_PUT = "PUT"
    HTTP_METHOD_DELETE = "DELETE"
    HTTP_HEADER_CONTENT_LENGTH = "Content-Length"
    HTTP_HEADER_CONTENT_TYPE = "Content-Type"
    HTTP_HEADER_CONTENT_TYPE_FORM_URLENCODED = "application/x-www-form-urlencoded"
    HTTP_HEADER_CONTENT_TYPE_JSON = "application/json"
    PARAM_SEPARATOR = "&"
    PARAM_VALUE_SEPARATOR = "="
    X_11PATHS_HEADER_SEPARATOR = ":"
    FILE_HASH_HEADER_NAME = X_11PATHS_HEADER_PREFIX + "File-Hash"
    AUTHORIZATION_HEADER_NAME = "Authorization"
    DATE_HEADER_NAME = X_11PATHS_HEADER_PREFIX + "Date"
    MULTIPART_FORM_DATA = "multipart/form-data"
    THREAD_POOL_SIZE = 10

    def __init__(self, appId, secretKey):
        '''
        Create an instance of the class with the Application ID and secret obtained from Tacyt
        @param $appId
        @param $secretKey
        '''
        self.appId = appId
        self.secretKey = secretKey

    @staticmethod
    def set_host(host):
        '''
        @param $host The host to be connected with (http://hostname) or (https://hostname)
        '''
        if host.startswith("http://"):

            Version.API_HOST = host[len("http://"):]
            Auth.API_PORT = 80
            Auth.API_HTTPS = False

        elif host.startswith("https://"):
            Version.API_HOST = host[len("https://"):]
            Auth.API_PORT = 443
            Auth.API_HTTPS = True

    @staticmethod
    def set_proxy(proxy, port):
        '''
        Enable using a Proxy to connect through
        @param $proxy The proxy server
        @param $port The proxy port number
        '''
        Auth.API_PROXY = proxy
        Auth.API_PROXY_PORT = port

    @staticmethod
    def get_part_from_header(part, header):
        '''
        The custom header consists of three parts, the method, the appId and the signature.
        This method returns the specified part if it exists.
        @param $part The zero indexed part to be returned
        @param $header The HTTP header value from which to extract the part
        @return string the specified part from the header or an empty string if not existent
        '''
        if header:
            parts = header.split(Auth.AUTHORIZATION_HEADER_FIELD_SEPARATOR)
            if len(parts) >= part:
                return parts[part]
        return ""

    @staticmethod
    def get_auth_method_from_header(authorization_header):
        '''
        @param $authorization_header authorization HTTP Header
        @return string the authorization method. Typical values are "Basic", "Digest" or "11PATHS"
        '''
        return Auth.get_part_from_header(0, authorization_header)

    @staticmethod
    def parse_query_params(query_params):
        global query, key, value
        if query_params is None or len(query_params) == 0:
            return ""

        if len(query_params) > 0:
            query = "?"
        else:
            query = ""

        for elements in query_params:
            key = query_params['key']
            value = query_params['value']
            if len(value) > 0:
                query += key + Auth.PARAM_VALUE_SEPARATOR + value.encode(Auth.CHARSET_UTF_8) + Auth.PARAM_SEPARATOR

        if len(query) > 0 and query[len(query) - 1] == '&':

            return query[0:(len(query) - 1)]

        else:
            return query


    def get_api_host(self):
        return Version.API_HOST


    def http_get_proxy(self, url, query_params = None):
        try:
            query = Auth.parse_query_params(query_params)
            url += query
            return self.http_get(self.get_api_host() + url,
                                 self.authentication_headers(self.HTTP_METHOD_GET, url, None, None))

        except:
            return None

    def http_get(self, url, headers):
        return self._http(Auth.HTTP_METHOD_GET, url,  headers, None)


    def http_delete_proxy(self, url):
        try:
            return self.http_delete(self.get_api_host() + url, self.authentication_headers(self.HTTP_METHOD_DELETE, url, None), None)

        except:
            return None

    def http_post_proxy(self, url, data=None, body=None):
        try:
            if data is not None:
                return self.http_post(self.get_api_host() + url, self.authentication_headers(self.HTTP_METHOD_POST,url,None,data),data)

            elif body is not None:
                return self.http_post(self.get_api_host() + url, self.authentication_headers_with_body(self.HTTP_METHOD_POST, url, None, body), body)

        except:
            return None


    def http_put_proxy(self,url,data=None,body=None):
        try:
            if data is not None:
                return self.http_put(self.get_api_host() + url, self.authentication_headers(self.HTTP_METHOD_PUT,url,None,data),data)

            elif body is not None:
                return self.http_put(self.get_api_host() + url, self.authentication_headers_with_body(self.HTTP_METHOD_PUT, url, None, body), body)
        except:
            return None

    @staticmethod
    def get_appId_from_header(authorization_header):
        '''
        @param $authorization_header authorization HTTP Header
        @return string the requesting application Id. Identifies the application using the API
        '''
        return Auth.get_part_from_header(1, authorization_header)

    @staticmethod
    def get_signature_from_header(authorization_header):
        '''
        @param $authorization_header authorization HTTP Header
        @return string the signature of the current request. Verifies the identity of the application using the API
        '''
        return Auth.get_part_from_header(2, authorization_header)

    @staticmethod
    def get_current_UTC():
        '''
        @return a string representation of the current time in UTC to be used in a Date HTTP Header
        '''
        return time.strftime(Auth.UTC_STRING_FORMAT, time.gmtime())


    def _http(self, method, url, x_headers=None, body=None, file=None, content_type=None):
        '''
        HTTP Request to the specified API endpoint
        @param method string
        @param x_headers list
        @param body dict json
        @return TacytResponse
        '''

        auth_headers = None
        json_body = None

        try:
            # Try to use the new Python3 HTTP library if available
            import http.client as http
            import urllib.parse as urllib
        except:
            # Must be using Python2 so use the appropriate library
            import httplib as http
            import urllib

        if Auth.API_PROXY != None:
            if Auth.API_HTTPS:
                conn = http.HTTPSConnection(Auth.API_PROXY, Auth.API_PROXY_PORT)
                conn.set_tunnel(Version.API_HOST, Auth.API_PORT)
            else:
                conn = http.HTTPConnection(Auth.API_PROXY, Auth.API_PROXY_PORT)
                url = "http://" + Version.API_HOST + url
        else:
            if Auth.API_HTTPS:
                conn = http.HTTPSConnection(Version.API_HOST, Auth.API_PORT)
            else:
                conn = http.HTTPConnection(Version.API_HOST, Auth.API_PORT)


        if self.HTTP_METHOD_GET == method or self.HTTP_METHOD_DELETE == method:
            auth_headers = self.authentication_headers(method, url, x_headers, None, None)
            conn.request(method, url, headers=auth_headers)

        elif self.HTTP_METHOD_POST == method or self.HTTP_METHOD_PUT == method:

            if body is not None and file is None:
                json_body = json.dumps(body)
                auth_headers = self.authentication_headers_with_body(method, url, x_headers, json_body, None)
                auth_headers[self.HTTP_HEADER_CONTENT_TYPE] = content_type


        try:

            all_headers = auth_headers

            if body is not None:
                conn.request(method=method, url=url, body=json_body, headers=all_headers)

            res = conn.getresponse()
            response_data = res.read().decode('utf8')

            conn.close()
            ret = Response(json_string=response_data)

        except Exception, e:
            print "Exception"
            print e
            print repr(e)
            ret = None

        return ret

    def sign_data(self, data):
        '''
        @param $data the string to sign
        @return string base64 encoding of the HMAC-SHA1 hash of the data parameter using {@code secretKey} as cipher key.
        '''
        from hashlib import sha1
        import hmac
        import binascii

        sha1_hash = hmac.new(self.secretKey.encode(), data.encode(), sha1)
        return binascii.b2a_base64(sha1_hash.digest())[:-1].decode('utf8')

    def authentication_headers(self, http_method, query_string, x_headers=None, utc=None, params=None):
        '''
        Calculate the authentication headers to be sent with a request to the API
        @param $http_method the HTTP Method
        @param $query_string the urlencoded string including the path (from the first forward slash) and the parameters
        @param $x_headers HTTP headers specific to the 11-paths API. null if not needed.
        @param $utc the Universal Coordinated Time for the Date HTTP header
        @return array a map with the authorization and Date headers needed to sign a Tacyt API request
        '''

        if not utc:
            utc = Auth.get_current_UTC()

        utc = utc.strip()

        string_to_sign = (http_method.upper().strip() + "\n" +
                          utc + "\n" +
                          self.get_serialized_headers(x_headers) + "\n" +
                          query_string.strip())


        if params is not None and len(params)>0:
            serialized_params = self.get_serialized_params(params)
            if serialized_params is not None and len(serialized_params)>0:
                string_to_sign = string_to_sign + "\n" + serialized_params


        authorization_header = (Auth.AUTHORIZATION_METHOD + Auth.AUTHORIZATION_HEADER_FIELD_SEPARATOR +
                                self.appId + Auth.AUTHORIZATION_HEADER_FIELD_SEPARATOR +
                                self.sign_data(string_to_sign))

        headers = dict()
        headers[Auth.AUTHORIZATION_HEADER_NAME] = authorization_header
        headers[Auth.DATE_HEADER_NAME] = utc

        return headers


    def authentication_headers_with_body(self, http_method, query_string, x_headers=None, body=None, utc=None):
        """
        Calculates the headers to be sent with a request to the API so the server
            can verify the signature
        @param method The HTTP request method.
        @param queryString The urlencoded string including the path (from the
            first forward slash) and the parameters.
        @param xHeaders The HTTP request headers specific to the API, excluding
            X-11Paths-Date. null if not needed.
        @param body The HTTP request body. Null if not needed.
        @param utc the Universal Coordinated Time for the X-11Paths-Date HTTP header
        @return header with the {@value #AUTHORIZATION_HEADER_NAME}, the {@value
            #DATE_HEADER_NAME} and the {@value #BODY_HASH_HEADER_NAME} headers
            needed to be sent with a request to the API.
        """

        headers = dict()
        body_hash = None

        if body is not None:
            body_hash = hashlib.sha1(str(body)).hexdigest()
            if x_headers is None:
                x_headers = dict()
            else:
                for key,value in x_headers.items():
                    headers[key] = value

            x_headers[Auth.BODY_HASH_HEADER_NAME] = body_hash

        if not utc:
            utc = Auth.get_current_UTC()

        utc = utc.strip()

        string_to_sign = (http_method.upper().strip() + "\n" +
                          utc + "\n" +
                          self.get_serialized_headers(x_headers) + "\n" +
                          query_string.strip())



        authorization_header = (Auth.AUTHORIZATION_METHOD + Auth.AUTHORIZATION_HEADER_FIELD_SEPARATOR +
                                self.appId + Auth.AUTHORIZATION_HEADER_FIELD_SEPARATOR +
                                self.sign_data(string_to_sign))


        headers[Auth.AUTHORIZATION_HEADER_NAME] = authorization_header
        headers[Auth.DATE_HEADER_NAME] = utc
        if body_hash is not None:
            headers[Auth.BODY_HASH_HEADER_NAME] = body_hash

        return headers


    def get_serialized_headers(self, x_headers):
        '''
        Prepares and returns a string ready to be signed from the 11-paths specific HTTP headers received
        @param $x_headers a non neccesarily ordered map (array without duplicates) of the HTTP headers to be ordered.
        @return string The serialized headers, an empty string if no headers are passed, or None if there's a problem such as non 11paths specific headers
        '''
        if x_headers:
            headers = dict((k.lower(), v) for k, v in x_headers.iteritems())

            serialized_headers = ""
            for key, value in sorted(headers.iteritems()):
                if not key.startswith(Auth.X_11PATHS_HEADER_PREFIX.lower()):
                    logging.error("Error serializing headers. Only specific " + Auth.X_11PATHS_HEADER_PREFIX + " headers need to be signed")
                    return None
                serialized_headers += key + Auth.X_11PATHS_HEADER_SEPARATOR + value + " "
            return serialized_headers.strip()
        else:
            return ""

    def get_serialized_params(self, params):
        """
         Prepares and returns a string ready to be signed from the params of an HTTP request
         The params must be only those included in the body of the HTTP request
            when its content type is application/x-www-urlencoded and must beurldecoded.
         @param params The params of an HTTP request.
         @return A serialized representation of the params ready to be signed.
            null if there are no valid params.
        """
        try:
            # Try to use the new Python3 HTTP library if available
            import http.client as http
            import urllib.parse as urllib
        except:
            # Must be using Python2 so use the appropriate library
            import httplib as http
            import urllib
        if params:
            serialized_params = ""
            for key in sorted(params):
                serialized_params += key + Auth.PARAM_VALUE_SEPARATOR + urllib.quote_plus(params[key]) + Auth.PARAM_SEPARATOR
            return serialized_params.strip(Auth.PARAM_SEPARATOR)
        else:
            return ""

    def http_delete(self, url, headers, body):
        return self._http(self.HTTP_METHOD_DELETE, url, headers, body)

    def http_post(self, url, headers, data=None, body=None):
        if data is not None:
            return self._http(self.HTTP_METHOD_POST,url,  headers, data)
        elif body:
            return self._http(self.HTTP_METHOD_POST,url,  headers, body, None, self.HTTP_HEADER_CONTENT_TYPE_JSON)


    def http_post_file(self, url, headers, file_stream, file_name):
        try:
            import requests
        except Exception:
            return Response(error=Error.Error({"code":"-1","message":"The Python \"request\" library was not found. Please, install it before call the upload method."}))


        files = {'file': (file_name, file_stream, 'application/octet-stream')}
        if Auth.API_HTTPS:
            url = "https://" + self.get_api_host() + url
        else:
            url = "http://" + self.get_api_host() + url
        res = requests.post( url, headers=headers, files=files)
        res.raise_for_status()

        response_data = Response(json_string=res.content)

        return response_data

    def http_put(self, url, headers, data=None, body=None):
        if data is not None:
            return self._http(self.HTTP_METHOD_PUT,url,  headers, data)
        elif body is not None:
            return self._http(self.HTTP_METHOD_PUT,url,  headers, body, None, self.HTTP_HEADER_CONTENT_TYPE_JSON)





