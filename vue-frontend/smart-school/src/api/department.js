import { queryParams } from '../util/util'
import axios from '~/axios'

export function get_department_list(skip){
    return axios.get(`department/departments?skip=${skip-1}&limit=10`)
}

export function get_department_statistics(){
    return axios.post("department/department/statistics")
}

export function get_departments_info(skip){
    return axios.get(`department/department/get_department?&skip=${skip-1}&limit=10`)
}


export function delete_department_info(department_id){
    return axios.delete(`/department/departments/${department_id}`)
}

export function update_department_info(departmentId, Data){
    return axios.put(`/department/departments/${departmentId}`, Data)
}

export function create_department_info(data){
    return axios.post("/department/departments/",{
            name: data.name,
            head_id: data.head_id,
            contact_info: data.contact_info
    })
}