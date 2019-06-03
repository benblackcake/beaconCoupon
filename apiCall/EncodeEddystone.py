import binascii
class EncodeEddyston:
    
    def __init__(self):
        pass
        
    def strTohex(url):
        prefix = ('http://www.', 'https://www.', 'http://', 'https://')#11  12  7  8
        encode_url=""
        
        encode_search = True
        for http_pattern in prefix:
            if http_pattern in url and encode_search==True:
                print("__DEBUG__",http_pattern)
                encode_prefix=hex(prefix.index(http_pattern))[2:].zfill(2)
                print("http Type: ",encode_prefix)
                # print(format(25, '02x'))
                # print(hex(encode_prefix))
                url_encode=url.split(http_pattern)[1]
                b=bytes(url_encode,'utf-8')
                binascii.b2a_hex(b)
                result=encode_prefix+binascii.b2a_hex(b).decode('utf-8')
                # print(encode_prefix+binascii.b2a_hex(b).decode('utf-8'))
                encode_search=False
                return result
