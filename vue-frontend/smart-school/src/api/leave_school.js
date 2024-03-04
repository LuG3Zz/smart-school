import axios from '~/axios'
import { queryParams } from '../util/util'



export function get_role_LeaveSchools(skip,query={}){
   
    let r=queryParams(query)
    console.log(r)
    return axios.get(`/LeaveSchool/LeaveSchool?${r}&skip=${skip-1}&limit=10`)
}

export function delete_LeaveSchool(id){
    return axios.delete(`/LeaveSchool/${id}`)
}

export function create_LeaveSchool(data){
    return axios.post("/LeaveSchool/LeaveSchool/",
        data)
}

export function read_LeaveSchool(id){
    return axios.get(`/LeaveSchool/LeaveSchool/${id}`)
}

export function update_LeaveSchool(LeaveSchool_id,data){
    return axios.put(`/LeaveSchool/${LeaveSchool_id}`,data)
}