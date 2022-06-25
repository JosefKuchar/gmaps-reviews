#!/usr/bin/python3
""" Get reviews from arbitrary user on Google maps """

import re
import json
import argparse
import requests


def parse_args():
    """
    Setup argument parser and return parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="Get reviews from arbitrary user on Google maps")
    parser.add_argument('user_id')
    return parser.parse_args()


def download_page(user_id):
    """
    Download page from Google maps
    """
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ' + \
        '(KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'

    headers = {
        'User-Agent': user_agent}

    return requests.get(
        "https://www.google.com/maps/contrib/{}/reviews/data".format(user_id), headers=headers).text


def get_review_data(page):
    """
    Extract review data from raw page content
    """
    matches = re.findall(
        r"window\.APP_INITIALIZATION_STATE=(.+);window\.APP_FLAGS=", page)

    if not matches:
        raise Exception("APP INITIALIZATION STATE not found")

    initialization_state = json.loads(matches[0])
    reviews_json_string = initialization_state[3][-1]
    # Starts with some junk, so we need to remove it
    return json.loads(reviews_json_string[5:])


def get_review_count(review_data):
    """
    Get number of reviews for user
    """
    return review_data[16][8][0][0][7]


def get_reviews(review_data):
    """
    Get reviews from review data
    """
    reviews = review_data[24][0]

    return map(lambda review: {
        'when': review[0][1],
        'text': review[0][3],
        'rating': review[0][4],
        'name': review[1][2],
        'address': review[1][3]
    }, reviews)


def print_reviews(reviews):
    """
    Print reviews
    """
    for review in reviews:
        print(review['name'])
        print(review['address'])
        print(review['when'])
        print("{}/5".format(review['rating']))
        print(review['text'])
        print("\n\n-----------------\n\n")


if __name__ == "__main__":
    ARGS = parse_args()
    PAGE = download_page(ARGS.user_id)
    REVIEW_DATA = get_review_data(PAGE)
    REVIEW_COUNT = get_review_count(REVIEW_DATA)
    REVIEWS = get_reviews(REVIEW_DATA)

    print(REVIEW_COUNT)
    print_reviews(REVIEWS)
