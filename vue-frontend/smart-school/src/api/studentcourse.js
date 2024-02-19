import axios from '~/axios'
import { queryParams } from '../util/util'

export function get_student_course_by_studentid(skip,student_id){
    return axios.get(`student_course/student_courses/?${student_id}&${skip}&limit=10`)
}
export function create_student_courses(courseData){
    return axios.post("/student/courses", courseData)
}
export function update_student_courses(courseId, courseData){
    return axios.put(`/student/courses/${courseId}`, courseData)
}
export function delete_student_courses(courseId){
    return axios.delete(`/student/courses/${courseId}`)
}

export function get_student_statistics(){
    return axios.post("student_course/student/statistics")
}

export function get_student_courses(skip,query={}){
    let r=queryParams(query)
    console.log(r)
    return axios.get(`/student_course/student/get_course${r}&skip=${skip-1}&limit=10`)
}