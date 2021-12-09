from django.db import models
from phone_field import PhoneField

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
class Nomination(models.Model):
    business_name    = models.CharField(max_length=200)
    website          = models.URLField(blank=True, max_length=500, null=True)
    instagram        = models.URLField(blank=True, null=True, max_length=200)
    twitter          = models.URLField(blank=True, null=True, max_length=200)
    facebook         = models.URLField(blank=True, null=True, max_length=200)
    city             = models.CharField(max_length=100, null=True, blank=True)
    state            = models.CharField(max_length=270, choices=STATE_CHOICES)
    phone            = PhoneField(blank=True, help_text='Business Phone Number')
    category         = models.CharField(max_length=200, choices=CATEGORY_CHOICES, null=True, blank=True)
    subcategory      = models.CharField(max_length=200, blank=True, null=True)
    nominator_name   = models.CharField(max_length=300, blank=True, null=True)
    nominator_email  = models.EmailField(blank=True, null=True)
    nominator_owner  = models.BooleanField(default=False, blank=True, null=True)
    nominator_recommended  = models.BooleanField(default=False, blank=True, null=True)    
    owner_name   = models.CharField(max_length=300, blank=True, null=True)
    created          = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated          = models.DateTimeField(auto_now=True, blank=True, null=True)
    years_in_business   = models.CharField(max_length=270, blank=True, null=True)
    employees        = models.CharField(max_length=270, blank=True, null=True)
    revenue          = models.CharField(max_length=270, blank=True, null=True)
    priority1         = models.CharField(max_length=270, blank=True, null=True)
    other1        = models.CharField(max_length=270, blank=True, null=True)
    priority2         = models.CharField(max_length=270, blank=True, null=True)
    other2         = models.CharField(max_length=270, blank=True, null=True)
    priority3         = models.CharField(max_length=270, blank=True, null=True)
    other3         = models.CharField(max_length=270, blank=True, null=True)
    structure        = models.CharField(max_length=270, blank=True, null=True)

    def __str__(self):
        return str(self.business_name)

    class Meta:
        verbose_name = 'Village Empowerment Network Nomination'
        verbose_name_plural = 'Village Empowerment Network Nominations'

