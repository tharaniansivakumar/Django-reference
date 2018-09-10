import jwt
from django.http import HttpResponse, HttpResponseForbidden

from myapp.models import Member
from myapp.token_set import token_set


class AuthenticationMiddleware(object):
    pass
#     def process_request(self,request):
#         try:
#             api = request.get_full_path().split('/')
#
#             if (api[2] != "login"):
#                 auth = request.META.get('HTTP_AUTHORIZATION')
#                 token = []
#                 token = auth.split()
#                 payload = dict(jwt.decode(token[1], "SECRET_KEY"))
#                 id = payload["id"]
#                 ob = token_set()
#                 ob.set(id)
#                 val=ob.get()
#                 print (val)
#                 if (Member.objects.filter(m_username=val).values()):
#                     pass
#                 else:
#                     return HttpResponseForbidden("Invalid Access")
#             else:
#                 pass
#         except Exception as e:
#             return HttpResponseForbidden(str(e))
#
#
#
