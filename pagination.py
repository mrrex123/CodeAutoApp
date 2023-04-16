from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect

# this is to tell paginator to paginate user_list in pages of 10
#it has rows of 53 users , each page will have 10 users. So it will be devided into 6 pages.
#the last page will have 3 users.

user_list = User.objects.all()
paginator = Paginator(user_list, 10)

#below are the commands to get details of paginator
paginator.count
paginator.num_pages
paginator.page_range
paginator.page(2)

#example below
users = paginator.page(2)

users
users.has_next()
users.has_previous()
users.has_other_pages()
users.next_page_number()
users.previous_page_number()
users.start_index()
users.end_index()


def index(request):
    user_list = User.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(user_list, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    return render(request, 'core/user_list.html', { 'users': users })


'''
<table class="table table-bordered">
  <thead>
    <tr>
      <th>Username</th>
      <th>First name</th>
      <th>Email</th>
    </tr>
  </thead>
  <tbody>
    {% for user in users %}
      <tr>
        <td>{{ user.username }}</td>
        <td>{{ user.first_name }}</td>
        <td>{{ user.email }}</td>
      </tr>
    {% endfor %}
  </tbody>
</table>

{% if users.has_other_pages %}
  <ul class="pagination">
    {% if users.has_previous %}
      <li><a href="?page={{ users.previous_page_number }}">&laquo;</a></li>
    {% else %}
      <li class="disabled"><span>&laquo;</span></li>
    {% endif %}
    {% for i in users.paginator.page_range %}
      {% if users.number == i %}
        <li class="active"><span>{{ i }} <span class="sr-only">(current)</span></span></li>
      {% else %}
        <li><a href="?page={{ i }}">{{ i }}</a></li>
      {% endif %}
    {% endfor %}
    {% if users.has_next %}
      <li><a href="?page={{ users.next_page_number }}">&raquo;</a></li>
    {% else %}
      <li class="disabled"><span>&raquo;</span></li>
    {% endif %}
  </ul>
{% endif %}

'''