/* @odoo-module */

import { Component ,useState} from "@odoo/owl" ;
import { registry } from "@web/core/registry" ;
import { useService } from "@web/core/utils/hooks"

export class SaleOwl extends Component{
    static template = 'app_one.SaleOwl' ;
    setup(){
        this.state =useState({
            'records' : []
        });
        this.orm = useService('orm');
        this.loadRecords();
    }
    async loadRecords(){
        const result = await this.orm.searchRead('sale.order',[],['name', 'partner_id', 'amount_total', 'state'])
        console.log(result)
        this.state.records=result

    }

}
registry.category("actions").add('app_one.action_saleOrdr_owl',SaleOwl)