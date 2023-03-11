# HEXOCEAN
## Recruitment task for Backend (Python + Django) Engineer position
### Cezary Suwiński - 11 March 2023

 &nbsp; 

**How to run the project**
1. Go to your terminal window, go to the desired directory and run ```git clone https://github.com/Ma-xwell/DRF-API-images.git``` in your terminal
2. After successful cloning, run ```docker compose up``` in your terminal while being in the root directory (top *hexocean* directory). This might take a while.
3. You can click CTRL+C and run ```python manage.py createsuperuser``` in your terminal and follow the instructions
4. Again, run ```docker compose up``` and navigate to */admin/* route on the website
5. Log In using credentials you have provided in step **3.**
6. Now you can create new Users. After creating any, click on them and assign them to any tier (there are three built-in tiers: Basic, Premium, Enterprise)
7. Each tier can be modified, as well as new ones can be created. As an admin, you can specify if newly created tier should have expirable links available, presence of the link to the originally uploaded file but also you can set arbitrary thumbnail sizes. When setting arbitrary thumbnail sizes, height should be always provided. Width is optional - if you will set width to 0 *(zero)*, it will be automatically calculated based on height without losing image's ratio. However, you can set width to any positive integer you want.
*remember: newly created user has not tier allocated by default. Do it, otherwise user will not be able to upload any images to the page!*
8. As a logged user, navigate to */images_api/images/* and upload your first image.
9. After successful upload, click on **Images** at the top of the DRF UI, this will show you GET request, listing all the images that currently logged user has uploaded along with their attributes such as height, width, information if image is expirable and if it is, the date and time of expiration.