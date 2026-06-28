/* @odoo-module */

import { Component ,useState, onWillUnmount } from "@odoo/owl" ;
import { registry } from "@web/core/registry" ;
import { useService } from "@web/core/utils/hooks"

export class ListViewAction extends Component {
    static template= "app_one.ListView";
    setup(){
        this.state =useState({
            'records' : []
        });
        this.orm =useService("orm");
        this.rpc =useService("rpc");
        this.loadRecords();
        this.intervalID = setInterval(() => {this.loadRecords()},3000);
        onWillUnmount(()=>{clearInterval(this.intervalID)});
    }
    async loadRecords(){
        const result = await this.orm.searchRead("property",[],['id','name','postcode','date_availability'],{limit: false})
        console.log(result)
        this.state.records = result ;
    }
    async createRecord(){
        const record = await this.rpc("/web/dataset/call_kw/",{
            model: "property",
            method: "create",
            args:[{
                name: "property name",
                description: "Description",
                living_rooms: "4",
                postcode: "33",
            }],
            kwargs:{},
        })
        this.loadRecords()
    };
    async deleteRecord(recordId){
        const record = await this.rpc("/web/dataset/call_kw/",{
            model: "property",
            method: "unlink",
            args:[recordId],
            kwargs:{}
        })
        this.loadRecords()
    }

    // async loadRecords(){
    //     const result = await this.rpc("/web/dataset/call_kw",{
    //         model: "property",
    //         method : "search_read",
    //         args: [[]],
    //         kwargs: {fields:['id','name','postcode','date_availability','living_rooms','is_late']}
    //         }
    //     );
    //     console.log(result)
    //     this.state.records = result
    // }

}
registry.category("actions").add("app_one.action_list_view",ListViewAction);
