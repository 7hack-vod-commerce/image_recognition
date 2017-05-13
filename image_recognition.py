from flask import Flask, request,jsonify
import http.client, urllib.request, urllib.parse, urllib.error, base64, json


app = Flask(__name__)
colors = ['aliceblue',
          'antiquewhite',
          'aqua',
          'aquamarine',
          'azure',
          'beige',
          'bisque',
          'black',
          'blanchedalmond',
          'blue',
          'blueviolet',
          'brown',
          'burlywood',
          'cadetblue',
          'chartreuse',
          'chocolate',
          'coral',
          'cornflowerblue',
          'cornsilk',
          'crimson',
          'cyan',
          'darkblue',
          'darkcyan',
          'darkgoldenrod',
          'darkgray',
          'darkgreen',
          'darkkhaki',
          'darkmagenta',
          'darkolivegreen',
          'darkorange',
          'darkorchid',
          'darkred',
          'darksalmon',
          'darkseagreen',
          'darkslateblue',
          'darkslategray',
          'darkturquoise',
          'darkviolet',
          'deeppink',
          'deepskyblue',
          'dimgray',
          'dodgerblue',
          'firebrick',
          'floralwhite',
          'forestgreen',
          'fuchsia',
          'gainsboro',
          'ghostwhite',
          'gold',
          'goldenrod',
          'gray',
          'green',
          'greenyellow',
          'honeydew',
          'hotpink',
          'indianred',
          'indigo',
          'ivory',
          'khaki',
          'lavender',
          'lavenderblush',
          'lawngreen',
          'lemonchiffon',
          'lightblue',
          'lightcoral',
          'lightcyan',
          'lightgoldenrodyellow',
          'lightgreen',
          'lightgray',
          'lightpink',
          'lightsalmon',
          'lightseagreen',
          'lightskyblue',
          'lightslategray',
          'lightsteelblue',
          'lightyellow',
          'lime',
          'limegreen',
          'linen',
          'magenta',
          'maroon',
          'mediumaquamarine',
          'mediumblue',
          'mediumorchid',
          'mediumpurple',
          'mediumseagreen',
          'mediumslateblue',
          'mediumspringgreen',
          'mediumturquoise',
          'mediumvioletred',
          'midnightblue',
          'mintcream',
          'mistyrose',
          'moccasin',
          'navajowhite',
          'navy',
          'oldlace',
          'olive',
          'olivedrab',
          'orange',
          'orangered',
          'orchid',
          'palegoldenrod',
          'palegreen',
          'paleturquoise',
          'palevioletred',
          'papayawhip',
          'peachpuff',
          'peru',
          'pink',
          'plum',
          'powderblue',
          'purple',
          'red',
          'rosybrown',
          'royalblue',
          'saddlebrown',
          'salmon',
          'sandybrown',
          'seagreen',
          'seashell',
          'sienna',
          'silver',
          'skyblue',
          'slateblue',
          'slategray',
          'snow',
          'springgreen',
          'steelblue',
          'tan',
          'teal',
          'thistle',
          'tomato',
          'turquoise',
          'violet',
          'wheat',
          'white',
          'whitesmoke',
          'yellow',
          'yellowgreen']
clothes = ['dress','shirt','skirt','cap','hat','high heels','tank top']

@app.route('/', methods=['POST'])
def detect_objects():
    try:
        print(type(request.data), request.data, request)
        in_req = json.loads(request.data.decode('utf-8'))
        print(in_req, type(in_req))
        url = in_req['url']
        print(url)
        trained_tags = trained_detect(url)
        result_tags = trained_tags
        if len(trained_tags) == 0:
            auto_tags = auto_detect(url)
            result_tags = auto_tags
        # result = [i for i in auto_tags if i in colors]
        return jsonify(result_tags)
    except Exception as e:
        print(repr(e))
        return 'error'


def auto_detect(url):
    print(url)
    headers = {
        # Request headers. Replace the key below with your subscription key.
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': 'be3c594836c645838ea2b215c8a66002',
    }

    params = urllib.parse.urlencode({
        # Request parameters. Use "model": "celebrities" to use the Celebrity model.
        'visualFeatures': 'Color,Tags,Categories,Description',
        'details': 'Celebrities,Landmarks',
        'language': 'en',
    })

    # The URL of a JEPG image containing text.
    body_json = {'url': url}
    body = json.dumps(body_json)
    print(body)

    try:
        conn = http.client.HTTPSConnection('westeurope.api.cognitive.microsoft.com')
        conn.request("POST", "/vision/v1.0/analyze?%s" % params, body, headers)
        response = conn.getresponse()
        data = response.read()
        # 'data' contains the JSON data. The following formats the JSON data for display.
        # encoding = response.headers.get_content_charset()
        # parsed = json.loads(data.decode(encoding))
        parsed = json.loads(data.decode('utf-8'))
        tags = parsed['description']['tags']
        auto_result = []
        for item in clothes:
            if item in tags:
                res_item = {}
                res_item['category'] = item
                colors_tags = [i for i in tags if i in colors]
                try:
                    res_item['detail'] = colors_tags[0]
                except IndexError:
                    res_item['detail'] = ''
                auto_result.append(res_item)
        print(auto_result)
        print("REST Response:")
        print(json.dumps(parsed, sort_keys=True, indent=2))
        conn.close()
    except Exception as e:
        print(repr(e))
    return auto_result

def trained_detect(url):
    headers = {
        # Request headers. Replace the key below with your subscription key.
        'Content-Type': 'application/json',
        'Prediction-Key': '484086a53b5e45d3ac361ccaefd811d0',
    }

    # params = urllib.parse.urlencode({
    #     # Request parameters. Use "model": "celebrities" to use the Celebrity model.
    #     'visualFeatures': 'Color,Tags,Categories,Description',
    #     'details': 'Celebrities,Landmarks',
    #     'language': 'en',
    # })

    # The URL of a JEPG image containing text.
    body_json = {'url': url}
    body = json.dumps(body_json)
    body_bin = ' '.join(format(ord(letter), 'b') for letter in body)
    # print(body)
    # params = urllib.parse.urlencode({'iterationId':'e9d32d10-34ee-4a24-a1ba-532b8460211b'})
    params = {'iterationId':'e9d32d10-34ee-4a24-a1ba-532b8460211b'}
    try:
        conn = http.client.HTTPSConnection('southcentralus.api.cognitive.microsoft.com')
        conn.request("POST", "/customvision/v1.0/Prediction/33357994-abdf-4299-948a-119f974836a8/url?%s" , body, headers)
        response = conn.getresponse()
        data = response.read()
        # 'data' contains the JSON data. The following formats the JSON data for display.
        # encoding = response.headers.get_content_charset()
        # parsed = json.loads(data.decode(encoding))
        parsed = json.loads(data.decode('utf-8'))
        # r = requests.post(r'https://southcentralus.api.cognitive.microsoft.com/customvision/v1.0/Prediction/33357994-abdf-4299-948a-119f974836a8/url', params=params, headers=headers, data=body)
        # print(r.text)
        train_results = []
        predictions = parsed['Predictions']
        res_item = {}
        for prediction in predictions:
            if prediction['Probability'] >= 0.7:
                if prediction['Tag'] in clothes:
                    res_item['category'] = prediction['Tag']
                elif prediction['Tag'] in colors:
                    res_item['detail'] = prediction['Tag']
        train_results.append(res_item)
        print(json.dumps(train_results, sort_keys=True, indent=2))
        return train_results
    except Exception as e:
        print(repr(e))

if __name__ == '__main__':
    app.run(debug=True)
