#!/bin/sh
source venv/bin/activate
cd assets
echo "Building frontend..."
npm run build
cd ..
echo "Collecting static files..."
python manage.py collectstatic --noinput
# hack to get around zappa exclude being broken
cp assets/dist/index.html favorite_things/templates
echo "Deploying to AWS Lambda..."
zappa deploy production || zappa update production
rm favorite_things/templates/index.html
echo "Migrating database..."
zappa manage production migrate
echo "Deployment finished."
