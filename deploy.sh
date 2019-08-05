#!/bin/sh
source venv/bin/activate
cd assets
echo "Building frontend..."
npm run build
cd ..
echo "Collecting static files..."
python manage.py collectstatic --noinput
echo "Deploying to AWS Lambda..."
zappa deploy production || zappa update production
echo "Deployment finished."
