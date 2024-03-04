import axios from '~/axios'
import { queryParams } from '../util/util'


export function read_notification(id){
    return axios.get(`/notification/Notification/${id}`)
}
export function get_uncheck_notification_count(){
    return axios.get(`/notification/notification_count`)
}

export function get_role_notification(skip,query={}){
   
    let r=queryParams(query)
    console.log(r)
    return axios.get(`/notification/notification?${r}&skip=${skip-1}&limit=10`)
}

export function delete_notification(discipline_id){
    return axios.delete(`/notification/${discipline_id}`)
}

export function create_notification(data){
    return axios.post("/notification/notification/",
        data)
}
export function update_notification(record_id,data){
    return axios.put(`/notification/${record_id}`,data)
}