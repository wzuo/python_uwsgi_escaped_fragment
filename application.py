import selenium.webdriver


WEBSITE_URL = 'http://localhost/#!'
PHANTOMJS_PORT = 64750
DELETE_FRAGMENT_FROM_RENDERED = True

DELETE_FRAGMENT_SCRIPT = '''
var i, refAttr;
var metaTags = document.getElementsByTagName('meta');
for(i = metaTags.length-1; i >= 0; i--){
    if((nameAttr = metaTags[i].getAttribute("name")) && (nameAttr == 'fragment')){
        metaTags[i].parentNode.removeChild(metaTags[i]);
    }
}

var scriptTags = document.getElementsByTagName('script');
for(i = scriptTags.length-1; i >= 0; i--){
    scriptTags[i].parentNode.removeChild(scriptTags[i]);
}
'''


def get_driver_data(url):
    driver = selenium.webdriver.PhantomJS(port=PHANTOMJS_PORT)
    driver.get(url)
    if DELETE_FRAGMENT_FROM_RENDERED is True:
        driver.execute_script(DELETE_FRAGMENT_SCRIPT)

    content = driver.page_source
    driver.quit()

    return content


def application(env, start_response):
    query_string = env['QUERY_STRING']
    keyparam = query_string.split('&')

    escaped_fragment_value = None
    for kp in keyparam:
        try:
            key, value = kp.split('=', 1)
            if key == '_escaped_fragment_':
                escaped_fragment_value = value
        except ValueError:
            pass

    # If there is no _escaped_fragment_ then return error 404 (It should be handled by nginx anyway)
    if escaped_fragment_value is None:
        start_response('404 Not Found', [('Content-Type', 'text/html')])
        return []

    start_response('200 OK', [('Content-Type', 'text/html')])

    url = "%s%s" % (WEBSITE_URL, escaped_fragment_value)
    response = get_driver_data(url)
    return [response.encode('utf-8')]