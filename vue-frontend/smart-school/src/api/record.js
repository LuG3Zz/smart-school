import axios from '~/axios'
import { queryParams } from '../util/util'



export function get_role_records(skip,query={}){
   
    let r=queryParams(query)
    console.log(r)
    return axios.get(`/record/get_records?${r}&skip=${skip-1}&limit=10`)
}

export function delete_record(ids){
    return axios.delete('/record/record/',ids)
}

export function create_record(data){
    return axios.post("/record/record/",
        data)
}

export function read_record(id){
    return axios.get(`/record/record/${id}`)
}

export function update_record(record_id,data){
    return axios.put(`/record/record/${record_id}`,data)
}