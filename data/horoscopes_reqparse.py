from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('sign', required=True)
parser.add_argument('image', required=True)
parser.add_argument('day_horoscope', required=True)
parser.add_argument('data', required=True)
