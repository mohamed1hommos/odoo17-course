from os.path import join
from urllib.parse import parse_qs

from OpenSSL.rand import status

from odoo import http
from odoo.http import request
import json
from odoo.exceptions import ValidationError ,UserError


def valid_response(data,status) :
    response_body = {
        'data': data,
        
    }
    return request.make_json_response(response_body,status=status)

class property_api(http.Controller):

    @http.route('/v1/property/<int:property_id>', methods=["PUT"], type="http", auth="none", csrf=False)
    def update_property(self,property_id):
        try :
            property_id = request.env['property'].sudo().search([('id','=',property_id)])
            if not property_id.exists():
                return request.make_json_response({
                    "message": "Property not found"
                }, status=404)
            args = request.httprequest.data.decode()  # call data
            vals = json.loads(args)  # transfer from json
            if 'name' in vals:
                existing = request.env['property'].sudo().search([
                    ('name', '=', vals['name']),
                    ('id', '!=', property_id.id)
                ])
                if existing:
                    return request.make_json_response({
                        "message": "Name already exists!"
                    }, status=400)
            property_id.write(vals)
            # print(property_id.expected_price)
            return request.make_json_response({
                "message": "ok! success!",
                "record_id": property_id.id,  # ID الريكورد في الداتا بيز
                "record_ref": property_id.ref,  # رقم الريكورد (ref field)
                "created_by": property_id.create_uid.id,  # ID اليوزر اللي كريت
                "created_by_name": property_id.create_uid.name,  # اسم اليوزر
            }, status=200)
        except Exception as error:
            return request.make_json_response({
                "message" : error
            },status=400)


    # @http.route('/v1/property',methods=["GET","POST"],type="http",auth="none",csrf=False)
    # def post_property(self):
    #     args = request.httprequest.data.decode() #call data
    #     vals = json.loads(args) #transfer from json
    #
    #     def validation_property_name(self, vals):
    #         if not vals.get("name"):
    #             return "name is required"
    #         return None
    #     # error_message= self.validation_property_name(vals)
    #     if validation_property_name:
    #         return request.make_json_response({
    #             "ddMessage name is required"
    #         },status=500)
    #     # if not vals.get("name") :
    #     #     return request.make_json_response({
    #     #         "Message name is required"
    #     #     },status=500)
    #     try:
    #         res = request.env['property'].sudo().create(vals)
    #         if res:
    #             return request.make_json_response({
    #                 "message":"ok! success!",
    #                 "record_id": res.id,  # ID الريكورد في الداتا بيز
    #                 "record_ref": res.ref,  # رقم الريكورد (ref field)
    #                 "created_by": res.create_uid.id,  # ID اليوزر اللي كريت
    #                 "created_by_name": res.create_uid.name,  # اسم اليوزر
    #             },status=200)
    #     except Exception as error:
    #         return request.make_json_response({
    #             "message":str(error),
    #         }, status=500)
    @http.route('/v1/property', methods=["GET", "POST"], type="http", auth="none", csrf=False)
    def post_property(self):
        try:
            args = request.httprequest.data.decode()
            vals = json.loads(args)
            cr = request.env.cr
            column =','.join(vals.keys())
            values=','.join(['%s']*len(vals))
            query = f"""INSERT INTO property ({column}) VALUES ({values})RETURNING id,name,postcode"""
            cr.execute(query,tuple(vals.values()))
            res = cr.fetchone()
            print(res)
            if res:
                    return request.make_json_response({
                        "message": "ok! success!",
                        "record_id": res[0],
                        "name": res[1],
                        "postcode": res[2],
                        # "living_room": res[3],
                    })
        except Exception as error:
            return request.make_json_response({
                "message": str(error),
            }, status=500)
    @http.route('/v1/property/json',methods=["GET","POST"],type="json",auth="none",csrf=False)
    def post_property_json(self):
        args = request.httprequest.data.decode()
        vals = json.loads(args)
        res = request.env['property'].sudo().create(vals)
        if res:
            return ({
                "message":"ok! success!",
                "name":res.name,
                "id" : res.id,
                "status": 200
            })
        return None

    @http.route('/v1/property/<int:property_id>', methods=["GET", "POST"], type="http", auth="none", csrf=False)
    def get_property_json(self,property_id):
        try:
            property_id = request.env['property'].sudo().search([('id', '=',property_id)])
            if  property_id:
                pass
            else:
                return request.make_json_response({
                    "message": "Property not found"
                },status=400)
            return valid_response({
                "id": property_id.id,
                "name": property_id.name,
                "ref": property_id.ref,
                "description": property_id.description,
                "bedrooms": property_id.bedrooms,
            },status=200)
        except Exception as error:
            return request.make_json_response({
                "Error404":str(error),
            },status=400)

    @http.route('/v1/property/<int:property_id>', methods=["DELETE"], type="http", auth="none", csrf=False)
    def delete_property(self,property_id):
        try:
            property_id = request.env['property'].sudo().search([('id', '=',property_id)])
            if not property_id:
                return request.make_json_response({
                    "message": "Property not found"
                },status=400)
            property_id.unlink()
            return request.make_json_response({
                "message":"ok! Deleted successfully!",
            },status=200)
        except Exception as error:
            return request.make_json_response({
                "Error404":str(error),
            },status=400)

    @http.route('/v1/propertiess', methods=["GET", "POST"], type="http", auth="none", csrf=False)
    def get_property_list(self):
        try:
            params = parse_qs(request.httprequest.query_string.decode('utf-8')) #reserve parmas from api
            property_domain = []
            if params.get("state"):
                property_domain += [('state','=',params.get("state")[0])]
            property_ids = request.env['property'].sudo().search(property_domain)
            if  property_ids:
                pass
            else:
                return request.make_json_response({
                    "there are not records"
                }, status=400)
            return valid_response([{
                "id": property_id.id,
                "name": property_id.name,
                "ref": property_id.ref,
                "description": property_id.description,
                "bedrooms": property_id.bedrooms,
            }for property_id in property_ids ],status=200)
        except Exception as error:
            return request.make_json_response({
                "Error404": str(error),
            }, status=400)
    # @http.route('/v1/properties', methods=["GET", "POST"], type="http", auth="none", csrf=False)
    # def get_property_list(self):
    #     try:
    #         property_ids = request.env['property'].sudo().search([])
    #         if not property_ids:
    #             return request.make_json_response({
    #                 "message": "there are no records"
    #             }, status=400)
    #
    #         return request.make_json_response([{
    #             "id": property_id.id,
    #             "name": property_id.name,
    #             "ref": property_id.ref,
    #             "description": property_id.description,
    #             "bedrooms": property_id.bedrooms,
    #         } for property_id in property_ids], status=200)
    #
    #     except Exception as error:
    #         return request.make_json_response({
    #             "error": str(error),
    #         }, status=400)




    # def validation_property_name(self,vals):
    #     if not vals.get("name"):
    #         return "name is required"
    #     return None

