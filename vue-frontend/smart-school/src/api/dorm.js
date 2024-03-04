import axios from '~/axios'
import { queryParams } from '../util/util'



export function get_role_dormitorys(skip,query={}){
   
    let r=queryParams(query)
    console.log(r)
    return axios.get(`/dormitory/get_dormitories?${r}&skip=${skip-1}&limit=10`)
}

export function delete_dormitory(ids){
    return axios.delete('/dormitory/dormitories/'+ids)
}
export function delete_student_dormitory(ids){
    return axios.delete('/student_dormitory/student_dormitories/'+ids)
}

export function create_dormitory(data){
    return axios.post("/dormitory/dormitories/",
        data)
}
export function create_student_dormitory(data){
    return axios.post("/student_dormitory/student_dormitories/",
        data)
}

export function read_dormitory(id){
    return axios.get(`/dormitory/dormitories/${id}`)
}

export function update_dormitory(dormitory_id,data){
    return axios.put(`/dormitory/dormitories/${dormitory_id}`,data)
}