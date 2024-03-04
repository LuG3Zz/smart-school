import axios from '~/axios'
export function get_course_list(skip){
    return axios.get(`/course/courses/?skip=${skip-1}&limit=10`)
}
export function create_course(data){
    return axios.post("/course/courses/",
        data)
}

export function delete_course(course_id){
    return axios.delete(`/course/courses/${course_id}`)
}

export function update_course(course_id,data){
    return axios.put(`/course/courses/${course_id}`,data)
}