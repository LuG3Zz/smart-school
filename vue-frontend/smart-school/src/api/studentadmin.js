import axios from '~/axios'

export function get_student_list(skip){
    return axios.get(`/student/students/?skip=${skip-1}&limit=10`)
}
export function get_departments(){
    return axios.get("department/departments/?skip=0&limit=100")

}
export function delete_student(student_id){
    return axios.delete(`/student/students/${student_id}`)
}

export function create_student(data){
    return axios.post("/student/students/",{
        student_id: data.student_id,
        name: data.name,
        gender: data.gender,
        date_of_birth: data.date_of_birth,
        department_id: data.department_id,
        major: data.major,
        class_: data.class_,
        enrollment_date: data.enrollment_date,
        contact_info: data.contact_info,
        status: data.status
    })
}
export function update_student(student_id,data){
    return axios.put(`/student/students/${student_id}`,{
        name: data.name,
        gender: data.gender,
        date_of_birth: data.date_of_birth,
        department_id: data.department_id,
        major: data.major,
        class_: data.class_,
        enrollment_date: data.enrollment_date,
        contact_info: data.contact_info,
        status: data.status
    })
}
