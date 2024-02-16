import axios from '~/axios'


export function read_own_discipline_record(){
    return axios.get("/student/discipline-records/")
}

