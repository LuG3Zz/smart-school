import axios from '~/axios'
import { queryParams } from '../util/util'


export function create_course(data){
    return axios.post("/course/courses/",
        data)
}

export function get_role_disciplines(skip,query={}){
   
    let r=queryParams(query)
    console.log(r)
    return axios.get(`/discipline/discipline?${r}&skip=${skip-1}&limit=10`)
}

export function delete_discipline(discipline_id){
    return axios.delete(`/discipline/${discipline_id}`)
}

export function create_discipline(data){
    return axios.post("/discipline/Discipline/",
        data)
}