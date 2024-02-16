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