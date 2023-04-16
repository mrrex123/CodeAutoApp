from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
   # path('', views.hi, name='home-page'),
    path('', views.home, name ='home'), # get and post request for insert operation. localhost:/p/employee/list
    path('run/', views.runScript_php, name ='runphp'),
    path('<int:id>', views.home, name ='home'), # get and post request for insert operation.
    path('<int:id>', views.home, name='run_code'),
    path('<int:id>', views.home,name='employee_update'), # get and post request for update operation
    path('visuals', views.data_visuals, name ='data_visualizations'),

    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),

    path('sms', views.smsJob, name='sms_job'),
    path('python', views.pythonJob, name='python_job'),
    path('php', views.phpJobs, name='php_job'),
    path('buycredit', views.buyRunCredit, name='buy_run_credit'),
    path('buysms', views.buySMSCredit, name='buy_sms_credit'),
                  # footer urls
    path('home', views.home, name='contact'),
    path('automations', views.automations, name='automations'),
    path('centers', views.centers, name='centers'),
    path('branches', views.branches, name='branches'),
    path('about', views.about, name='about'),

    path('contact', views.contact, name='contact'),
    path('howItWorks', views.howItWorks, name='howItWorks'),
    path('terms', views.terms, name='terms'),
    path('policy', views.policy, name='policy'),
    path('moneyback', views.moneyback, name='moneyback'),

    path('list', views.employee_list, name='employee_list') #get request to retrieve and display all records


]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
