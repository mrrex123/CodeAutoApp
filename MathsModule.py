import math
import random
import datetime
import json

#print(math.cos(3))
#print(random.randrange(50))
#print(datetime.date.today())
now = datetime.date.today()

other = datetime.datetime(1999,10,10,12,59)

#print(now - other)

print(now)

employee_data='''

{
    "people" : [
    {
    "name":"Rex",
    "email":["taipan@yahoo.com","jame@gmail.com"],
    "married":"false"
    },
    {
    "name":"John",
    "email":["john@yahoo.com","jaoj@gmail.com"],
    "married":"true"
    }
    ]
}

'''

print(employee_data)

data=json.loads(employee_data)
print(data)


