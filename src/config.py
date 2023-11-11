from dotenv import load_dotenv
import os

load_dotenv()

base_url = os.getenv('BASE_URL')
username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')
workspace = os.getenv('WORKSPACE')
defaultReviewers = os.getenv('DEFAULT_REVIEWERS').split(',')
min_date = os.getenv('MIN_DATE')

headers = {
  'Authorization': f'Basic {password}'
}