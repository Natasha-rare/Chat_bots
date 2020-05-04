'''
запрос статистики со стены сообщества с id = 17916162, метод stats_get(group_id, fields=reach)
'''
from flask import Flask, render_template, redirect, abort, request, make_response, jsonify
import vk_api
import datetime
from auth_data import VK_USER, VK_PASS, group_id

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vk_static'
a = 131803965

@app.route('/vk_stat/<int:group_id>')
def index(group_id):
    login, password = VK_USER, VK_PASS
    vk_session = vk_api.VkApi(login, password)
    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return
    vk = vk_session.get_api()

    response = vk.stats.get(group_id=group_id, fields="reach")
    activity = []
    age = []
    cities = []
    countries = []
    sex = []
    if response:
        for item in response[:1]:
            value = datetime.datetime.fromtimestamp(item['period_from'])
            print(value.strftime('%Y-%m-%d'))
            activity.append(item['activity'])
            reach = item['reach']
            age = reach['age']
            cities = reach['cities']
            countries = reach['countries']
            sex = reach['sex']
            print(item['activity'])

        return render_template('main.html', activity=activity, age=age, cities=cities, countries=countries, sex=sex)

def main():
    app.run()


if __name__ == '__main__':
    main()
