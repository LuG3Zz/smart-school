import axios from "~/axios"

export function getImageList(id,page = 1){
    return axios.get(`/image/images/?skip=${page-1}&name=${id}&limit=10`)
}

export function updateImage(id,name){
    return axios.post(`/admin/image/${id}`,{ name })
}

export function deleteImage(ids){
    axios.delete('/image/delete_image/'+ids)
}

//export const uploadImageAction = import.meta.env.VITE_APP_BASE_API + "/admin/image/upload"
export const uploadImageAction =  "/api/image/upload_file/"