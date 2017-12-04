import requests
import base64
import json

headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
}


def get_access_token(client_id, sec_key):
    request_url = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={}&client_secret={}'.format(
        client_id, sec_key)
    res_text = requests.get(request_url).text
    res_data = json.loads(res_text)
    return res_data['access_token']


def face_match(image_path_1, image_path_2, token):
    request_url = "https://aip.baidubce.com/rest/2.0/face/v2/match?access_token=" + token
    img1 = base64.b64encode(open(image_path_1, 'rb').read()).decode()
    img2 = base64.b64encode(open(image_path_2, 'rb').read()).decode()
    data = {
        'images': img1 + ',' + img2
    }
    res_text = requests.post(request_url, data=data).text
    res_data = json.loads(res_text)
    return res_data


if __name__ == '__main__':
    img1 = './2017.jpg'
    img2 = './image.jpg'
    client_id = ''
    sec_key = ''
    access_token = get_access_token(client_id, sec_key)
    face_match(img1, img2, 'access_token')
