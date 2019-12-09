# Pip install the client:
# pip install clarifai

import config
from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage

# Create your API key in your account's Application details page:
# https://clarifai.com/apps

# You can also create an environment variable called `CLARIFAI_API_KEY`
# and set its value to your API key.

app = ClarifaiApp(api_key=config.clarifai_api_key)

model = app.models.get('demographics')

