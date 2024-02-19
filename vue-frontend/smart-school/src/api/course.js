import axios from '~/axios'
export function get_course_list(skip){
    return axios.get(`/course/courses/?skip=${skip-1}&limit=10`)
}