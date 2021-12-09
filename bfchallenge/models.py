from django.db import models
from django.conf import settings
import random
import os

from accounts.models import Team
from django.db.models.fields import CharField, DateField
from django.db.models.fields.files import ImageField

CATEGORY_CHOICES = (
    ('beauty','Beauty & Personal Grooming'),
    ('books', 'Books & Publishing'),
    ('cars', 'Cars & Automotive'),
    ('child', "Childcare | Children's Services & Products"),
    ('cleaning', 'Cleaning'),
    ('clothing', 'Clothing & Fashion'),
    ('construction', 'Construction & Trades'),
    ('education', 'Education'),
    ('eldercare', 'Eldercare'),
    ('electronics', 'Electronics & Technology'),
    ('entertainment', 'Entertainment'),
    ('farming', 'Farming & Agriculture'),
    ('florists', 'Florists'),
    ('grocery', 'Grocery & Food Services'),
    ('health', 'Health & Wellness'),
    ('home', 'Home & Garden'),
    ('hotels', 'Hotels & Hospitality | Travel'),
    ('jewelry', 'Jewelry & Accessories'),
    ('legal', 'Legal & Financial Services'),
    ('lifestyle', 'Lifestyle'),
    ('marketing', 'Marketing & Advertising'),
    ('medical', 'Medical Services'),
    ('packaging', 'Packaging | Delivery | Shipping'),
    ('pets', 'Pets & Animal Care'),
    ('photography', 'Photography & Video'),
    ('professional', 'Professional Services'),
    ('real estate', 'Real Estate'),
    ('recreation', 'Recreation & Sports'),
    ('restaurants', 'Restaurants & Bars | Event Spaces'),
    ('security', 'Security Services'),
    ('transportation', 'Transportation & Trucking'),
    ('visual', 'Visual & Performing Arts | Culture'),
    ('other', 'Other'),
)
STATE_CHOICES = (
    ('AL', 'Alabama'),
    ('AK', 'Alaska'),
    ('AZ', 'Arizona'),
    ('AR', 'Arkansas'),
    ('CA', 'California'),
    ('CO', 'Colorado'),
    ('CT', 'Connecticut'),
    ('DE', 'Delaware'),
    ('DC', 'District of Columbia'),
    ('FL', 'Florida'),
    ('GA', 'Georgia'),
    ('HI', 'Hawaii'),
    ('ID', 'Idaho'),
    ('IL', 'Illinois'),
    ('IN', 'Indiana'),
    ('IA', 'Iowa'),
    ('KS', 'Kansas'),
    ('KY', 'Kentucky'),
    ('LA', 'Louisiana'),
    ('ME', 'Maine'),
    ('MD', 'Maryland'),
    ('MA', 'Massachusetts'),
    ('MI', 'Michigan'),
    ('MN', 'Minnesota'),
    ('MS', 'Mississippi'),
    ('MO', 'Missouri'),
    ('MT', 'Montana'),
    ('NE', 'Nebraska'),
    ('NV', 'Nevada'),
    ('NH', 'New Hampshire'),
    ('NJ', 'New Jersey'),
    ('NM', 'New Mexico'),
    ('NY', 'New York'),
    ('NC', 'North Carolina'),
    ('ND', 'North Dakota'),
    ('OH', 'Ohio'),
    ('OK', 'Oklahoma'),
    ('OR', 'Oregon'),
    ('PA', 'Pennsylvania'),
    ('RI', 'Rhode Island'),
    ('SC', 'South Carolina'),
    ('SD', 'South Dakota'),
    ('TN', 'Tennessee'),
    ('TX', 'Texas'),
    ('UT', 'Utah'),
    ('VT', 'Vermont'),
    ('VA', 'Virginia'),
    ('WA', 'Washington'),
    ('WV', 'West Virginia'),
    ('WI', 'Wisconsin'),
    ('WY', 'Wyoming'),
)
SPOT_CHOICES = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
    ('7', '7'),
    ('8', '8'),
    ('9', '9'),
    ('10', '10'),
    ('11', '11'),
    ('12', '12'),
    ('13', '13'),
    ('14', '14'),
    ('15', '15'),
    ('16', '16'),
    ('17', '17'),
    ('18', '18'),
    ('19', '19'),
    ('20', '20'),
    ('21', '21'),
    ('22', '22'),
    ('23', '23'),
    ('24', '24'),
    ('25', '25'),
)

User = settings.AUTH_USER_MODEL

def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext

def upload_image_path(instance, filename):
    new_filename = random.randint(1, 3000)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "bfchallenge/{new_filename}/{final_filename}".format(new_filename=new_filename, final_filename=final_filename)

class bingo_card(models.Model):
    card_title       = models.CharField(max_length=300)
    spot1            = models.CharField(max_length=500)
    spot1_img        = models.ImageField(null=True, blank=True)
    spot2            = models.CharField(max_length=500)
    spot2_img        = models.ImageField(null=True, blank=True)
    spot3            = models.CharField(max_length=500)
    spot3_img        = models.ImageField(null=True, blank=True)
    spot4            = models.CharField(max_length=500)
    spot4_img        = models.ImageField(null=True, blank=True)
    spot5            = models.CharField(max_length=500)
    spot5_img        = models.ImageField(null=True, blank=True)
    spot6            = models.CharField(max_length=500)
    spot6_img        = models.ImageField(null=True, blank=True)
    spot7            = models.CharField(max_length=500)
    spot7_img        = models.ImageField(null=True, blank=True)
    spot8            = models.CharField(max_length=500)
    spot8_img        = models.ImageField(null=True, blank=True)
    spot9            = models.CharField(max_length=500)
    spot9_img        = models.ImageField(null=True, blank=True)
    spot10           = models.CharField(max_length=500)
    spot10_img       = models.ImageField(null=True, blank=True)
    spot11           = models.CharField(max_length=500)
    spot11_img       = models.ImageField(null=True, blank=True)
    spot12           = models.CharField(max_length=500)
    spot12_img       = models.ImageField(null=True, blank=True)
    spot13           = models.CharField(max_length=500, null=True, blank=True)
    spot13_img       = models.ImageField(null=True, blank=True)
    spot14           = models.CharField(max_length=500)
    spot14_img       = models.ImageField(null=True, blank=True)
    spot15           = models.CharField(max_length=500)
    spot15_img       = models.ImageField(null=True, blank=True)
    spot16           = models.CharField(max_length=500)
    spot16_img       = models.ImageField(null=True, blank=True)
    spot17           = models.CharField(max_length=500)
    spot17_img       = models.ImageField(null=True, blank=True)
    spot18           = models.CharField(max_length=500)
    spot18_img       = models.ImageField(null=True, blank=True)
    spot19           = models.CharField(max_length=500)
    spot19_img       = models.ImageField(null=True, blank=True)
    spot20           = models.CharField(max_length=500)
    spot20_img       = models.ImageField(null=True, blank=True)
    spot21           = models.CharField(max_length=500)
    spot21_img       = models.ImageField(null=True, blank=True)
    spot22           = models.CharField(max_length=500)
    spot22_img       = models.ImageField(null=True, blank=True)
    spot23           = models.CharField(max_length=500)
    spot23_img       = models.ImageField(null=True, blank=True)
    spot24           = models.CharField(max_length=500)
    spot24_img       = models.ImageField(null=True, blank=True)
    spot25           = models.CharField(max_length=500)
    spot25_img       = models.ImageField(null=True, blank=True)

    def __str__(self):
        return str(self.card_title)
    
    class Meta:
        verbose_name = 'Bingo Card'
        verbose_name_plural = 'Bingo Cards'

class user_bingo_card(models.Model):
    user             = models.ForeignKey(User, models.SET_NULL, null=True, blank=True)
    spot1            = models.BooleanField(default=False)
    spot2            = models.BooleanField(default=False)
    spot3            = models.BooleanField(default=False)
    spot4            = models.BooleanField(default=False)
    spot5            = models.BooleanField(default=False)
    spot6            = models.BooleanField(default=False)
    spot7            = models.BooleanField(default=False)
    spot8            = models.BooleanField(default=False)
    spot9            = models.BooleanField(default=False)
    spot10           = models.BooleanField(default=False)
    spot11           = models.BooleanField(default=False)
    spot12           = models.BooleanField(default=False)
    spot14           = models.BooleanField(default=False)
    spot15           = models.BooleanField(default=False)
    spot16           = models.BooleanField(default=False)
    spot17           = models.BooleanField(default=False)
    spot18           = models.BooleanField(default=False)
    spot19           = models.BooleanField(default=False)
    spot20           = models.BooleanField(default=False)
    spot21           = models.BooleanField(default=False)
    spot22           = models.BooleanField(default=False)
    spot23           = models.BooleanField(default=False)
    spot24           = models.BooleanField(default=False)
    spot25           = models.BooleanField(default=False)
    complete         = models.BooleanField(default=False)
    created        = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return str(self.id)
    
    class Meta:
        verbose_name = 'User Bingo Card'
        verbose_name_plural = 'User Bingo Cards'

class user_bingo_form(models.Model):
    card            = models.ForeignKey(user_bingo_card, models.CASCADE)
    spot            = models.CharField(max_length=20)
    field1          = models.CharField(max_length=300)
    field2          = models.CharField(max_length=300, blank=True, null=True)
    field3          = models.CharField(max_length=300, blank=True, null=True)
    field4          = models.CharField(max_length=300, blank=True, null=True)
    field5          = models.CharField(max_length=300, blank=True, null=True)
    field6          = models.CharField(max_length=300, blank=True, null=True)
    field7          = models.CharField(max_length=300, blank=True, null=True)
    field8          = models.CharField(max_length=300, blank=True, null=True)
    field9          = models.CharField(max_length=300, blank=True, null=True)
    field10         = models.CharField(max_length=300, blank=True, null=True)
    field11         = models.CharField(max_length=300, blank=True, null=True)
    field12         = models.CharField(max_length=300, blank=True, null=True)
    field13         = models.CharField(max_length=300, blank=True, null=True)
    field14         = models.CharField(max_length=300, blank=True, null=True)
    field15         = models.CharField(max_length=300, blank=True, null=True)
    field16         = models.CharField(max_length=300, blank=True, null=True)
    receipt         = models.FileField(blank=True, null=True)
    submitted       = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'User Bingo Form'
        verbose_name_plural = 'User Bingo Forms'

class readysetshop_transaction(models.Model):
    user             = models.ForeignKey(User, models.SET_NULL, null=True, blank=True)
    first_name       = models.CharField(max_length=200, null=True, blank=True)
    last_name        = models.CharField(max_length=200, null=True, blank=True)
    email            = models.EmailField(null=True, blank=True)
    team             = models.ForeignKey(Team, models.SET_NULL, null=True, blank=True)
    amount           = models.CharField(max_length=200)
    date             = models.CharField(max_length=50)
    business_name    = models.CharField(max_length=200)
    industry         = models.CharField(max_length=200, choices=CATEGORY_CHOICES)
    receipt_aws      = models.FileField(blank=True, null=True)
    submitted          = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return str(self.user)
    
    class Meta:
        verbose_name = 'Ready, Set, Shop! Transaction'
        verbose_name_plural = 'Ready, Set, Shop! Transactions'

class everyfriday_transaction(models.Model):
    user             = models.ForeignKey(User, models.SET_NULL, null=True, blank=True)
    amount           = models.DecimalField(decimal_places=2, max_digits=7)
    date             = models.CharField(max_length=50)
    business_name    = models.CharField(max_length=200)
    industry         = models.CharField(max_length=200, choices=CATEGORY_CHOICES)
    receipt_aws      = models.FileField(blank=True, null=True)
    submitted          = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    
    def __str__(self):
        return str(self.id)
    
    class Meta:
        verbose_name = 'Every Friday! Transaction'
        verbose_name_plural = 'Every Friday! Transactions'
        
class nomination(models.Model):
    user             = models.ForeignKey(User, models.SET_NULL, null=True, blank=True)
    name             = models.CharField(max_length=200, null=True, blank=True)
    email            = models.EmailField(null=True, blank=True)
    business_name    = models.CharField(max_length=200)
    submitted        = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    team             = models.ForeignKey(Team, models.SET_NULL, null=True, blank=True)
    state            = models.CharField(choices=STATE_CHOICES, max_length=50, null=True, blank=True)
    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Nomination'
        verbose_name_plural = 'Nominations'

class spread_the_love_submission(models.Model):
    user             = models.ForeignKey(User, models.SET_NULL, null=True, blank=True)
    link             = models.URLField(max_length=200)
    submitted        = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Spread the Love Submission'
        verbose_name_plural = 'Spread the Love Submissions'