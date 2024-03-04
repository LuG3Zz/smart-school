import axios from "~/axios"

export function getImageClassList(page){
    return axios.get("/image/get_image_class/?size=10&page=" + page)
}

export function createImageClass(data){
    return axios.post("image/create_image_class/",data)
}

export function updateImageClass(id,data){
    return axios.post("/image_class/"+id,data)
}

export function deleteImageClass(id){
    return axios.post(`/image_class/${id}/delete`)
}