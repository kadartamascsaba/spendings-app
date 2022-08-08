from datetime import datetime, timedelta
from time import sleep
from dateutil import parser

from app import app
from models import Spending


def around_now(spent_at):
    now = datetime.now()
    return (
        (now - timedelta(seconds=1))
        < parser.parse(spent_at) <
        (now + timedelta(seconds=1))
    )


def test_empty_spendings():
    app.spendings = []
    with app.test_client() as cli:
        resp = cli.get('/spendings')
        assert resp.status_code == 200
        assert len(resp.json) == 0


def test_get_one_spendings():
    app.spendings = [
        Spending({'description': 'Banana', 'amount': 300.0, 'currency': 'HUF'})]

    with app.test_client() as cli:
        resp = cli.get('/spendings')
        assert resp.status_code == 200
        assert len(resp.json) == 1


def test_get_multiple_spendings():
    app.spendings = [
        Spending({'description': 'Banana', 'amount': 300.0, 'currency': 'HUF'}),
        Spending({'description': 'Raspberry',
                 'amount': 2.0, 'currency': 'USD'}),
    ]

    with app.test_client() as cli:
        resp = cli.get('/spendings')
        assert resp.status_code == 200
        assert len(resp.json) == 2


def test_create_spending():
    with app.test_client() as cli:
        resp = cli.post(
            '/spendings',
            json={'description': 'Banana', 'amount': 300.0, 'currency': 'HUF'}
        )
        assert resp.status_code == 201
        assert resp.json['description'] == 'Banana'
        assert resp.json['amount'] == 300.0
        assert resp.json['currency'] == 'HUF'
        assert around_now(resp.json['spent_at']) == True


def test_order_spendings_by_spent_at():
    app.spendings = [
        Spending({'description': 'Banana', 'amount': 300.0, 'currency': 'HUF'})]
    sleep(0.001)
    app.spendings += [
        Spending({'description': 'Raspberry', 'amount': 2.0, 'currency': 'USD'})
    ]

    with app.test_client() as cli:
        resp = cli.get('/spendings?order=spent_at')
        assert resp.status_code == 200
        assert len(resp.json) == 2
        assert resp.json[0]['description'] == 'Banana'
        assert resp.json[1]['description'] == 'Raspberry'

        resp = cli.get('/spendings?order=-spent_at')
        assert resp.status_code == 200
        assert len(resp.json) == 2
        assert resp.json[0]['description'] == 'Raspberry'
        assert resp.json[1]['description'] == 'Banana'


def test_order_spendings_by_amount():
    app.spendings = [
        Spending({'description': 'Banana', 'amount': 300.0, 'currency': 'HUF'}),
        Spending({'description': 'Apple', 'amount': 1500.0, 'currency': 'HUF'}),
        Spending({'description': 'Raspberry', 'amount': 2.0, 'currency': 'USD'})
    ]

    with app.test_client() as cli:
        resp = cli.get('/spendings?order=amount')
        assert resp.status_code == 200
        assert len(resp.json) == 3
        assert resp.json[0]['description'] == 'Banana'
        assert resp.json[1]['description'] == 'Raspberry'
        assert resp.json[2]['description'] == 'Apple'

        resp = cli.get('/spendings?order=-amount')
        assert resp.status_code == 200
        assert len(resp.json) == 3
        assert resp.json[0]['description'] == 'Apple'
        assert resp.json[1]['description'] == 'Raspberry'
        assert resp.json[2]['description'] == 'Banana'


def test_filter_spendings_by_HUF():
    app.spendings = [
        Spending({'description': 'Banana', 'amount': 300.0, 'currency': 'HUF'}),
        Spending({'description': 'Apple', 'amount': 1500.0, 'currency': 'HUF'}),
        Spending({'description': 'Raspberry', 'amount': 2.0, 'currency': 'USD'})
    ]

    with app.test_client() as cli:
        resp = cli.get('/spendings?currency=HUF')
        assert resp.status_code == 200
        assert len(resp.json) == 2
        assert resp.json[0]['description'] == 'Banana'
        assert resp.json[1]['description'] == 'Apple'


def test_filter_spendings_by_USD():
    app.spendings = [
        Spending({'description': 'Banana', 'amount': 300.0, 'currency': 'HUF'}),
        Spending({'description': 'Apple', 'amount': 1500.0, 'currency': 'HUF'}),
        Spending({'description': 'Raspberry', 'amount': 2.0, 'currency': 'USD'})
    ]

    with app.test_client() as cli:
        resp = cli.get('/spendings?currency=USD')
        assert resp.status_code == 200
        assert len(resp.json) == 1
        assert resp.json[0]['description'] == 'Raspberry'


def test_filter_spendings_by_invalid():
    app.spendings = [
        Spending({'description': 'Banana', 'amount': 300.0, 'currency': 'HUF'}),
        Spending({'description': 'Apple', 'amount': 1500.0, 'currency': 'HUF'}),
        Spending({'description': 'Raspberry', 'amount': 2.0, 'currency': 'USD'})
    ]

    with app.test_client() as cli:
        resp = cli.get('/spendings?currency=invalid')
        assert resp.status_code == 200
        assert len(resp.json) == 0


def test_filter_spendings_by_invalid():
    app.spendings = [
        Spending({'description': 'Banana', 'amount': 300.0, 'currency': 'HUF'}),
        Spending({'description': 'Apple', 'amount': 1500.0, 'currency': 'HUF'}),
        Spending({'description': 'Raspberry', 'amount': 2.0, 'currency': 'USD'})
    ]

    with app.test_client() as cli:
        resp = cli.get('/spendings?currency=ALL')
        assert resp.status_code == 200
        assert len(resp.json) == 3
        assert resp.json[0]['description'] == 'Banana'
        assert resp.json[1]['description'] == 'Apple'
        assert resp.json[2]['description'] == 'Raspberry'


def test_filtering_and_ordering_spendings():
    app.spendings = [
        Spending({'description': 'Banana', 'amount': 300.0, 'currency': 'HUF'}),
        Spending({'description': 'Apple', 'amount': 1500.0, 'currency': 'HUF'}),
        Spending({'description': 'Raspberry', 'amount': 2.0, 'currency': 'USD'})
    ]

    with app.test_client() as cli:
        resp = cli.get('/spendings?currency=HUF&order=-amount')
        assert resp.status_code == 200
        assert len(resp.json) == 2
        assert resp.json[0]['description'] == 'Apple'
        assert resp.json[1]['description'] == 'Banana'


def test_missing_description():
    with app.test_client() as cli:
        resp = cli.post(
            '/spendings',
            json={'description': '', 'amount': 300.0, 'currency': 'HUF'}
        )
        assert resp.status_code == 400
        assert resp.json['description'] == ['This field is required.']

        resp = cli.post(
            '/spendings',
            json={'amount': 300.0, 'currency': 'HUF'}
        )
        assert resp.status_code == 400
        assert resp.json['description'] == ['This field is required.']


def test_missing_amount():
    with app.test_client() as cli:
        resp = cli.post(
            '/spendings',
            json={'description': 'Banana', 'currency': 'HUF'}
        )
        assert resp.status_code == 400
        assert resp.json['amount'] == ['This field is required.']


def test_not_positive_amount():
    with app.test_client() as cli:
        resp = cli.post(
            '/spendings',
            json={'description': 'Banana', 'amount': -1, 'currency': 'HUF'}
        )
        assert resp.status_code == 400
        assert resp.json['amount'] == ['Should be a positive number.']


def test_not_supported_currency():
    with app.test_client() as cli:
        resp = cli.post(
            '/spendings',
            json={'description': 'Banana', 'amount': 10, 'currency': 'EUR'}
        )
        assert resp.status_code == 400
        assert resp.json['currency'] == ['Not supported currency.']


def test_multiple_validation_error():
    with app.test_client() as cli:
        resp = cli.post(
            '/spendings',
            json={'description': '', 'amount': -1, 'currency': 'EUR'}
        )
        assert resp.status_code == 400
        assert resp.json['description'] == ['This field is required.']
        assert resp.json['amount'] == ['Should be a positive number.']
        assert resp.json['currency'] == ['Not supported currency.']
