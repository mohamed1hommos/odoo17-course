
from odoo import http

class TestApi(http.Controller):
    @http.route("/api/test",methods=["GET"],type="http",auth="none",csrf=False)
    def test_endpoint(self):
        print("test_endpoint")


# from odoo import http
#
#
# class TestApi(http.Controller):
#
#     @http.route("/api/test", methods=['POST'], type="json", auth="none", csrf=False)
#     def test_endpoint(self):
#         return {"message": "test_endpoint works!", "statu
# s": "ok"}

# from odoo import http
# from odoo.http import Response
# import
# class TestApi(http.Controller):
#     @http.route("/api/test", methods=['GET'], type="http", auth="none", csrf=False)
#     def test_endpoint(self):
#         return Response(
#             json.dumps({"message": "ok"}),
#             content_type='application/json',
#             status=200
#         )