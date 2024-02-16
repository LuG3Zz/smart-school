import axios from '~/axios'

export function getState(){
    return axios.post("/user/login",{
        username,
        password
    })
}
