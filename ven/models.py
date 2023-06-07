from django.db import models
from django.db.models.signals import pre_save, post_save
from phone_field import PhoneField
from etv.utils import unique_ven_id_generator
import json

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
COUNSELOR_CHOICES = (
    ('Unassigned', 'Unassigned'),
    ('Andrew Frazier', 'Andrew Frazier'),
    ('Michelle Harlan', 'Michelle Harlan'),
)

class NominationManager(models.Manager):
    def filter_objs(self):
        filtered_qs = Nomination.objects.all()
        return filtered_qs
        
    def dashboard_get_fields(self):
        list_fields = [{'field':'business_name','type':'plain'},{'field':'owner_name','type':'plain'},{'field':'city','type':'plain'},{'field':'state','type':'plain'},{'field':'counselor','type':'plain'},]
        return list_fields
    
    def dashboard_get_view_fields(self):
        fields = [{'field':'business_name','type':'plain'},
        {'field':'counselor','type':'select'},
        {'field':'owner_name','type':'plain'},
        {'field':'nominator_name','type':'plain'},
        {'field':'nominator_email','type':'email'},
        {'field':'phone','type':'phone'},
        
        {'field':'city','type':'plain'},
        {'field':'state','type':'plain'},

        {'field':'instagram','type':'instagram'},
        {'field':'facebook','type':'facebook'},
        {'field':'twitter','type':'twitter'},

        {'field':'category','type':'plain'},
        {'field':'subcategory','type':'plain'},
        {'field':'years_in_business','type':'plain'},
        {'field':'revenue','type':'plain'},
        {'field':'priority1','type':'alt1'},
        {'field':'other1','type':'alt2'},
        {'field':'priority2','type':'alt1'},
        {'field':'other2','type':'alt2'},
        {'field':'priority3','type':'alt1'},
        {'field':'other3','type':'alt2'},
        {'field':'expo_vendor','type':'boolean'},
        {'field':'pitch_comp','type':'boolean'},
        {'field':'created','type':'datetime'},
        {'field':'updated','type':'datetime'},]
        return fields
        
    def dashboard_display_qty(self):
        qty = 20
        return qty
        
    def dashboard_category(self):
        category = 'Village Empowerment Network'
        return category

class Nomination(models.Model):
    ven_id           = models.CharField(max_length=270, null=True, blank=True)
    counselor        = models.CharField(blank=True, null=True, max_length=200, default='Unassigned', choices=COUNSELOR_CHOICES)
    business_name    = models.CharField(max_length=200)
    website          = models.URLField(blank=True, max_length=500, null=True)
    city             = models.CharField(max_length=100, null=True, blank=True)
    state            = models.CharField(max_length=270, choices=STATE_CHOICES)
    phone            = PhoneField(blank=True, help_text='Business Phone Number')
    category         = models.CharField(max_length=200, null=True, blank=True)
    subcategory      = models.CharField(max_length=200, blank=True, null=True)
    nominator_name   = models.CharField(max_length=300, blank=True, null=True)
    nominator_email  = models.EmailField(blank=True, null=True)
    nominator_owner  = models.BooleanField(default=False, blank=True, null=True)
    nominator_recommended  = models.BooleanField(default=False, blank=True, null=True)    
    owner_name   = models.CharField(max_length=300, blank=True, null=True)
    instagram        = models.CharField(blank=True, null=True, max_length=200)
    twitter          = models.CharField(blank=True, null=True, max_length=200)
    facebook         = models.CharField(blank=True, null=True, max_length=200)
    years_in_business   = models.CharField(max_length=270, blank=True, null=True)
    employees        = models.CharField(max_length=270, blank=True, null=True)
    revenue          = models.CharField(max_length=270, blank=True, null=True)
    priority1         = models.CharField(max_length=270, blank=True, null=True, verbose_name="Priority #1")
    other1        = models.CharField(max_length=270, blank=True, null=True, verbose_name="Priority #1")
    priority2         = models.CharField(max_length=270, blank=True, null=True, verbose_name="Priority #2")
    other2         = models.CharField(max_length=270, blank=True, null=True, verbose_name="Priority #2")
    priority3         = models.CharField(max_length=270, blank=True, null=True, verbose_name="Priority #3")
    other3         = models.CharField(max_length=270, blank=True, null=True, verbose_name="Priority #3")
    structure        = models.CharField(max_length=270, blank=True, null=True)
    created          = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated          = models.DateTimeField(auto_now=True, blank=True, null=True)
    expo_vendor      = models.BooleanField(default=False, null=True, blank=True, verbose_name="Interested in being Expo Vendor")
    pitch_comp       = models.BooleanField(default=False, null=True, blank=True, verbose_name="Interested in Pitch Competition")
    
    objects = NominationManager()

    def __str__(self):
        return str(self.business_name)

    class Meta:
        verbose_name = 'VEN Business Nomination'
        verbose_name_plural = 'VEN Business Nominations'
        ordering = ['-created']

class FamilyNominationManager(models.Manager):
    def filter_objs(self):
        filtered_qs = FamilyNomination.objects.all()
        return filtered_qs
        
    def dashboard_get_fields(self):
        list_fields = [{'field':'ven_id','type':'plain'},{'field':'name','type':'plain'},{'field':'city','type':'plain'},{'field':'state','type':'plain'},{'field':'counselor','type':'plain'},]
        return list_fields
    
    def dashboard_get_view_fields(self):
        fields = [{'field':'name','type':'plain'},
        {'field':'counselor','type':'plain'},
        {'field':'email','type':'email'},
        {'field':'city','type':'plain'},
        {'field':'state','type':'plain'},
        {'field':'phone','type':'phone'},
        {'field':'employment_status','type':'plain'},
        {'field':'age_range','type':'plain'},
        {'field':'household_size','type':'plain'},
        {'field':'income','type':'plain'},
        {'field':'priority1','type':'alt1'},
        {'field':'other1','type':'alt2'},
        {'field':'priority2','type':'alt1'},
        {'field':'other2','type':'alt2'},
        {'field':'priority3','type':'alt1'},
        {'field':'other3','type':'alt2'},
        {'field':'updated','type':'datetime'},]
        return fields
        
    def dashboard_display_qty(self):
        qty = 20
        return qty
        
    def dashboard_category(self):
        category = 'Village Empowerment Network'
        return category

class FamilyNomination(models.Model):
    ven_id              = models.CharField(max_length=270, null=True, blank=True)
    name                = models.CharField(max_length=200)
    email               = models.EmailField(blank=True, null=True)
    city                = models.CharField(max_length=100, null=True, blank=True)
    state               = models.CharField(max_length=270, choices=STATE_CHOICES)
    phone               = PhoneField(blank=True, help_text='Business Phone Number')
    created             = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated             = models.DateTimeField(auto_now=True, blank=True, null=True)
    employment_status   = models.CharField(max_length=270, blank=True, null=True)
    age_range           = models.CharField(max_length=270, blank=True, null=True)
    household_size      = models.CharField(max_length=270, blank=True, null=True)
    income              = models.CharField(max_length=270, blank=True, null=True)
    priority1           = models.CharField(max_length=270, blank=True, null=True)
    other1              = models.CharField(max_length=270, blank=True, null=True)
    priority2           = models.CharField(max_length=270, blank=True, null=True)
    other2              = models.CharField(max_length=270, blank=True, null=True)
    priority3           = models.CharField(max_length=270, blank=True, null=True)
    other3              = models.CharField(max_length=270, blank=True, null=True)
    counselor        = models.CharField(blank=True, null=True, max_length=200, default='Unassigned', choices=COUNSELOR_CHOICES)
    
    objects = FamilyNominationManager()

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'VEN Family Nomination'
        verbose_name_plural = 'VEN Family Nominations'
        ordering = ['-created']

def nomination_create_id(sender, instance, *args, **kwargs):
    if not instance.ven_id:
        instance.ven_id = unique_ven_id_generator(instance)

pre_save.connect(nomination_create_id, sender=Nomination)
pre_save.connect(nomination_create_id, sender=FamilyNomination)

class sponsor_img(models.Model):
    image = models.ImageField()
    name = models.TextField(max_length=270)
    
    def __str__(self):
        return str(self.name)