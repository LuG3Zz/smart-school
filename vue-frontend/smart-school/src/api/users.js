import axios from '~/axios'

export function login(username,password){
    return axios.post("/user/login",{
        username,
        password
    })
}
export function create_user(role_id,data){
    return axios.post("/user/create",{
        username:data.username ,
        password_hash: data.password_hash,
        role:role_id,
        associated_id: data.associated_id
    })
}

export function getinfo(){
    return axios.get("/user/get_cur_user")
}
export function changepsw(data){
    return axios.post("/user/changepassword",{
        password:data.oldpasswd,
        newpassword:data.newpasswd,
    })
}
export function getStatistics1(){
    return axios.post("/user/get_usr_statistics")
}
export function getStatistics2(){
    return axios.post("/user/get_usr_statistics3")
}
export function getStatistics3(Semester){
    return axios.get(`/student_course/student/get_course_statistics?&semester=${Semester}`)
}

export function get_analytics1(){
    return axios.get("/student/get_analytics1")
}