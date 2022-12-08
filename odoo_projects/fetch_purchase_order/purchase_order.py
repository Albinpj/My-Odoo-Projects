import xmlrpc.client

url_db1 = "http://localhost:8015"
db_1 = 'test'
username_db_1 = '1'
password_db_1 = '1'
common_1 = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url_db1))
models_1 = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url_db1))
version_db1 = common_1.version()

url_db2 = "http://localhost:8021"
db_2 = '555'
username_db_2 = '1'
password_db_2 = '1'
common_2 = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url_db2))
models_2 = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url_db2))
version_db2 = common_2.version()

uid_db1 = common_1.authenticate(db_1, username_db_1, password_db_1, {})
uid_db2 = common_2.authenticate(db_2, username_db_2, password_db_2, {})

# vendor

res_partner_id = models_2.execute_kw(db_2, uid_db2, password_db_2, 'ir.model', 'search_read',
                                     [[['model', '=', 'res.partner']]], {'fields': ['id']})

models_2.execute_kw(db_2, uid_db2, password_db_2, 'ir.model.fields', 'create',
                    [{'name': 'x_vid', 'ttype': 'integer', 'model': 'res.partner',
                      'model_id': res_partner_id[0]['id'], 'store': 'true'}])

vendor = models_1.execute_kw(db_1, uid_db1, password_db_1, 'res.partner', 'search_read', [[]],
                             {'fields': ['name', 'email', 'mobile']})
if not vendor:
    for i in vendor:
        models_2.execute_kw(db_2, uid_db2, password_db_2, 'res.partner', 'create',
                            [{'name': i['name'], 'email': i['email'], 'mobile': i['mobile'],
                              'x_vid': i['id']}])
else:
    for i in vendor:
        vendor_id = models_2.execute_kw(db_2, uid_db2, password_db_2, 'res.partner', 'search_read',
                                        [[['x_vid', '=', i['id']]]])
        if not vendor_id:
            models_2.execute_kw(db_2, uid_db2, password_db_2, 'res.partner', 'create',
                                [{'name': i['name'], 'email': i['email'], 'mobile': i['mobile'],
                                  'x_vid': i['id']}])

# product

res_product_id = models_2.execute_kw(db_2, uid_db2, password_db_2, 'ir.model', 'search_read',
                                     [[['model', '=', 'product.template']]], {'fields': ['id']})

models_2.execute_kw(db_2, uid_db2, password_db_2, 'ir.model.fields', 'create',
                    [{'name': 'x_pid', 'ttype': 'integer', 'model': 'product.template',
                      'model_id': res_product_id[0]['id'], 'store': 'true'}])

product = models_1.execute_kw(db_1, uid_db1, password_db_1, 'product.product', 'search_read', [[]],
                              {'fields': ['name', 'list_price']})
product2 = models_1.execute_kw(db_2, uid_db2, password_db_2, 'product.product', 'search_read', [[]],
                               {'fields': ['name', 'list_price']})

if not product2:
    for i in product:
        models_2.execute_kw(db_2, uid_db2, password_db_2, 'product.product', 'create',
                            [{'name': i['name'], 'list_price': i['list_price'],
                              'x_pid': i['id']}])
else:
    for i in product:
        product_id = models_2.execute_kw(db_2, uid_db2, password_db_2, 'product.product', 'search_read',
                                         [[['x_pid', '=', i['id']]]])
        if not product_id:
            models_2.execute_kw(db_2, uid_db2, password_db_2, 'product.product', 'create',
                                [{'name': i['name'], 'list_price': i['list_price'],
                                  'x_pid': i['id']}])

# purchase_order

res_purchase_order_id = models_2.execute_kw(db_2, uid_db2, password_db_2, 'ir.model', 'search_read',
                                            [[['model', '=', 'purchase.order']]], {'fields': ['id']})

models_2.execute_kw(db_2, uid_db2, password_db_2, 'ir.model.fields', 'create',
                    [{'name': 'x_po_id', 'ttype': 'integer', 'model': 'purchase.order',
                      'model_id': res_purchase_order_id[0]['id'], 'store': 'true'}])

purchase_order = models_1.execute_kw(db_1, uid_db1, password_db_1, 'purchase.order', 'search_read', [[]],
                                     {'fields': ['name', 'partner_id', 'state']})

purchase_order2 = models_2.execute_kw(db_2, uid_db2, password_db_2, 'purchase.order', 'search_read', [[]],
                                      {'fields': ['name', 'partner_id', 'state']})

if not purchase_order2:
    for i in purchase_order:
        res_part_id = models_2.execute_kw(db_2, uid_db2, password_db_2, 'res.partner', 'search_read',
                                          [[['x_vid', '=', i['partner_id'][0]]]], {'fields': ['id']})

        p_id = models_2.execute_kw(db_2, uid_db2, password_db_2, 'purchase.order', 'create',
                                   [{'name': i['name'], 'partner_id': res_part_id[0]['id'], 'state': i['state'],
                                     'x_po_id': i['id']}])

        res_purchase_order_line_id = models_1.execute_kw(db_1, uid_db1, password_db_1, 'purchase.order.line','search_read',
                            [[['order_id', '=', p_id]]], {'fields': ['product_id', 'price_subtotal','product_uom_qty']})
        for j in res_purchase_order_line_id:
            res_product_product_id = models_2.execute_kw(db_2, uid_db2, password_db_2, 'product.product', 'search_read',
                                                         [[['x_pid', '=', j['product_id'][0]]]], {'fields': ['id']})
            if res_product_product_id:
                models_2.execute_kw(db_2, uid_db2, password_db_2, 'purchase.order.line', 'create',
                                    [{'order_id': int(p_id), 'product_id': int(res_product_product_id[0]['id']),
                                      'product_uom_qty': j['product_uom_qty'], 'price_subtotal': j['price_subtotal']}])


else:
    for i in purchase_order:
        purchase_order_id = models_2.execute_kw(db_2, uid_db2, password_db_2, 'purchase.order', 'search_read',
                                                [[['x_po_id', '=', i['id']]]])

        if not purchase_order_id:
            res_part_id = models_2.execute_kw(db_2, uid_db2, password_db_2, 'res.partner', 'search_read',
                                              [[['x_vid', '=', i['partner_id'][0]]]], {'fields': ['id']})
            p_id = models_2.execute_kw(db_2, uid_db2, password_db_2, 'purchase.order', 'create',
                                       [{'name': i['name'], 'partner_id': res_part_id[0]['id'], 'state': i['state'],
                                         'x_po_id': i['id']}])

            res_purchase_order_line_id = models_1.execute_kw(db_1, uid_db1, password_db_1, 'purchase.order.line', 'search_read',
                            [[['order_id', '=', p_id]]], {'fields': ['product_id', 'price_subtotal','product_uom_qty']})
            for j in res_purchase_order_line_id:
                res_product_product_id = models_2.execute_kw(db_2, uid_db2, password_db_2, 'product.product',
                                                             'search_read',
                                                             [[['x_pid', '=', j['product_id'][0]]]], {'fields': ['id']})
                if res_product_product_id:
                    models_2.execute_kw(db_2, uid_db2, password_db_2, 'purchase.order.line', 'create',
                                        [{'order_id': int(p_id), 'product_id': int(res_product_product_id[0]['id']),
                                          'product_uom_qty': j['product_uom_qty'],
                                          'price_subtotal': j['price_subtotal']}])
