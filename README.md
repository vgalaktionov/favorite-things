# Favorite Things

> An app to keep track of your favorite things.

The application is deployed at [this URL](https://bzksv2i2ae.execute-api.eu-central-1.amazonaws.com/production)

Built with:

- Python 3
- Django
- Vue
- PostgreSQL
- Zappa
- AWS Lambda + RDS + S3

## Install requirements

```bash
$ source venv/bin/activate
$ pip install -r requirements.txt
$ cd assets
$ npm install
```

## Development

To setup pre-commit linting:

```bash
cp pre-commit .git/hooks
chmod +x .git/hooks/pre-commit
```

Run the application locally:

```bash
# in one terminal
$ source venv/bin/activate
$ python manage.py runserver
# in a second terminal
$ cd assets
$ npm run dev
```

## Deployment

####1-command deploy:

```bash
$ bash deploy.sh
```

####When deploying for the first time, the following commands must be ran afterwards:

```bash
$ zappa manage production create_pg_db
$ zappa manage production create_admin_user
```

Note: the environment variables `DB_PASSWORD` and `DB_HOST` need to be set in the AWS Lambda console.
Once DNS has been setup in Route53, a custom domain may be used with `zappa certify`.

## License

GPLv3 © Vadim Galaktionov
