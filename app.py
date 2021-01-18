from flask import Flask, render_template, jsonify, request
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

app = Flask(__name__)

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta  # 'dbsparta'라는 이름의 db를 만들거나 사용합니다.


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/diet', methods=['POST'])
def post_articles():
    # 1. 클라이언트로부터 데이터를 받기
    category_receive = request.form['category_give']
    image_url_receive = request.form['image_url_give']
    name_receive = request.form['name_give']
    company_receive = request.form['company_give']
    comment_receive = request.form['comment_give']
    ref_receive = request.form['ref_url_give']
    agree_receive = request.form['agree_give']
    disagree_receive = request.form['disagree_give']
    # 2. db에 삽입할 리뷰만들기
    review = {
        'category': category_receive,
        'image': image_url_receive,
        'name': name_receive,
        'company': company_receive,
        'comment': comment_receive,
        'ref': ref_receive,
        'agree': agree_receive,
        'disagree': disagree_receive
    }

    # 3. mongoDB에 데이터 넣기 (리뷰스에 리뷰넣기)
    db.dietinfo.insert_one(review)

    return jsonify({'result': 'success', 'msg': '리뷰가 성공적으로 작성되었습니다. 허위광고 없는 세상을 향하여..! '})


@app.route('/list', methods=['GET'])
def read_articles():
    # 1. mongoDB에서 _id 값을 제외한 모든 데이터 조회해오기(Read)
    reviews = list(db.dietinfo.find({}, {'_id': False}).sort('agree', -1))
    # 2. 성공여부, 리뷰목록 반환
    return jsonify({'result': 'success', 'reviews': reviews})


@app.route('/agree', methods=['POST'])
def agree():
    # 1. 클라이언트가 전달한 name_give를 name_receive 변수에 넣습니다.
    name_receive = request.form['name_give']

    # 2. mystar 목록에서 find_one으로 name이 name_receive와 일치하는 star를 찾습니다.
    reviews = db.dietinfo.find_one({'name': name_receive})
    # # 3. star의 like 에 1을 더해준 new_like 변수를 만듭니다.
    new_agree = reviews['agree'] + 1

    # 4. mystar 목록에서 name이 name_receive인 문서의 like 를 new_like로 변경합니다.
    db.dietinfo.update_one({'name': name_receive}, {'$set': {'agree': new_agree}})
    # 참고: '$set' 활용하기!
    # 5. 성공하면 success 메시지를 반환합니다.
    return jsonify({'result': 'success'})


@app.route('/disagree', methods=['POST'])
def disagree():
    # 1. 클라이언트가 전달한 name_give를 name_receive 변수에 넣습니다.
    name_receive = request.form['name_give']
    # 2. mystar 목록에서 find_one으로 name이 name_receive와 일치하는 star를 찾습니다.
    diet = db.dietinfo.find_one({'name': name_receive})
    # 3. star의 like 에 1을 더해준 new_like 변수를 만듭니다.
    new_disagree = diet['disagree'] + 1
    # 4. mystar 목록에서 name이 name_receive인 문서의 like 를 new_like로 변경합니다.
    db.dietinfo.update_one({'name': name_receive}, {'$set': {'disagree': new_disagree}})
    # 참고: '$set' 활용하기!
    # 5. 성공하면 success 메시지를 반환합니다.
    return jsonify({'result': 'success'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
