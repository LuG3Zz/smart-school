
import axios from '~/axios'

export function get_department_list(skip){
    return axios.get(`department/departments?skip=${skip-1}&limit=10`)
}